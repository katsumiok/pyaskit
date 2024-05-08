import os
import ast
import random
import time
import openai
import numpy as np
import anthropic
import asyncio


from datasets import load_dataset
from .code_generator import extract_python_code, validate_python_code, make_messages as make_code_messages
from timeout_decorator import timeout, TimeoutError

NUM_PROGRAMS = 20
NUM_TESTS = 20
MODELS = ['openai', 'anthropic']
DATASET = load_dataset("openai_humaneval")


def chat_with_regenerate_openai(messages, max_retries=10, num_generations=5):
    """
    Interacts with OpenAI's API to generate completions for given chat messages.
    
    Args:
        messages (list): List of messages to send to the API.
        max_retries (int): Maximum number of retry attempts in case of failure.
        num_generations (int): Number of responses to generate.

    Returns:
        response: Response from the OpenAI API.
    """
    model = "gpt-3.5-turbo-16k"
    base_wait_time = 1  # wait time in seconds
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"), max_retries=0)
    for i in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                n=num_generations
            )
            return response
        except (
            openai.APIError,
            openai.APITimeoutError,
            openai.APIConnectionError,
            openai.RateLimitError,
            openai.InternalServerError,
        ) as e:
            # https://platform.openai.com/docs/guides/error-codes/python-library-error-types
            # print(e)
            wait_time = base_wait_time * 2**i
            wait_time = min(wait_time, 30)
            jitter = wait_time / 2
            time.sleep(wait_time + random.uniform(-jitter, jitter))
    raise Exception(f"Failed to get response after {max_retries} attempts")


async def chat_with_regenerate_anthropic(messages, max_retries=10, num_generations=5):
    """
    Asynchronously interacts with Anthropic's API to generate completions for given chat messages.

    Args:
        messages (list): List of messages to send to the API.
        max_retries (int): Maximum number of retry attempts in case of failure.
        num_generations (int): Number of responses to generate.

    Returns:
        list: List of responses from the Anthropic API.
    """
    system_prompt = None
    if messages[0]["role"] == "system":
        system_prompt = messages[0]["content"]
        messages = messages[1:]

    model = "claude-3-haiku-20240307"
    base_wait_time = 1  # wait time in seconds

    client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    async def make_request():
        return await client.messages.create(
            model=model,
            system=system_prompt,
            messages=messages,
            max_tokens=4096
        )

    for i in range(max_retries):
        try:
            responses = await asyncio.gather(
                *(make_request() for _ in range(num_generations))
            )
            return responses
        except Exception as e:
            print(e)
            wait_time = base_wait_time * 2**i
            wait_time = min(wait_time, 30)
            jitter = wait_time / 2
            time.sleep(wait_time + random.uniform(-jitter, jitter))

    raise Exception(f"Failed to get response after {max_retries} attempts")


def make_test_messages(skeleton: str):
    """
    Creates a list of messages prompting the model to generate test cases.

    Args:
        skeleton (str): The function skeleton to generate test cases for.

    Returns:
        list: A list of messages to be sent to the model.
    """
    return [
        {
            "role": "system",
            "content": (
                f"You are a Python programmer. Your task is to generate some test cases for the given function description. Be sure the test cases are accurate and that they test the edge cases of the given function. Do not generate anything other than the test cases. "
                "The test cases should be a Python list of dictionaries, each representing a test case with 'input' and 'output' keys. The inputs should match the input types of the function and the output should match the return type. "
                "For example: [{'input': {'name': 'hello'}, 'output': 5}, {'input': {'name': 'five'}, 'output': 4}]"
            ),
        },
        {
            "role": "user",
            "content": skeleton,
        },
    ]


async def generate_completions(messages, num_generations, models):
    """
    Asynchronously generates completions using multiple models (OpenAI and Anthropic).

    Args:
        messages (list): The prompt messages to generate completions for.
        num_generations (int): The number of completions to generate.
        models (list): The models to use for generation.

    Returns:
        list: The generated completions.
    """
    completions = []
    if 'openai' in models:
        response_openai = chat_with_regenerate_openai(messages, num_generations=num_generations // len(models))
        completions += [choice.message.content for choice in response_openai.choices]
    if 'anthropic' in models:
        response_anthropic = await chat_with_regenerate_anthropic(messages, num_generations=num_generations // len(models))
        completions += [choice.content[0].text for choice in response_anthropic]
    
    return completions


async def generate_code(function_name: str, skeleton: str):
    """
    Asynchronously generates function code completions and test cases using provided models.

    Args:
        function_name (str): Name of the function to generate code for.
        skeleton (str): The function skeleton.
        n_programs (int): Number of programs to generate.
        models (list): List of models to use for generation.

    Returns:
        tuple: A tuple containing a list of valid functions and a list of valid test cases.
    """
    # Generate function completions
    code_completions = await generate_completions(make_code_messages(skeleton), NUM_PROGRAMS, MODELS)

    # Validate them and collect all that are syntactically correct
    valid_functions = []
    for code_completion in code_completions:
        code = extract_python_code(code_completion)
        try:
            namespace = {}
            exec(code, namespace)
            func = namespace[function_name]
            if func is not None:
                valid_functions.append({'function': func, 'content': code, 'namespace': namespace})
        except:
            continue
        # func = validate_python_code(code, function_name)
        # if func is not None:
        #     valid_functions.append({'function': func, 'content': code})

    # Generate test cases and validate them
    test_completions = await generate_completions(make_test_messages(skeleton), NUM_TESTS, MODELS)

    valid_test_cases = []
    for test_completion in test_completions:
        try:
            valid_tests = eval(test_completion)
            valid_test_cases += valid_tests
        except:
            continue

    return valid_functions, valid_test_cases

@timeout(0.1)
def run_test(func, test):
    """
    Runs a test case on a given function.

    Args:
        func (function): The function to test.
        test (dict): A dictionary representing the test case, with 'input' and 'output' keys.

    Returns:
        bool: True if the function's output matches the expected output, False otherwise.
    """
    try:
        output = func(**test['input'])
        return output == test['output']
    except:
        return False


def test_code(functions, test_cases):
    """
    Tests each function against each test case.

    Args:
        functions (list): List of functions to test.
        test_cases (list): List of test cases to run on the functions.

    Returns:
        list: A matrix of booleans indicating the success or failure of each function-test combination.
    """
    test_matrix = [[False for _ in test_cases] for _ in functions]
    for i, elem in enumerate(functions):
        func = elem['function']
        for j, test in enumerate(test_cases):
            try:
                test_matrix[i][j] = run_test(func, test)
            except TimeoutError:
                print(f'Timeout for function {i}')
                test_matrix[i][j] = False
    
    return test_matrix


def get_best_function_old(test_matrix, n_iterations=100):
    """
    Identifies the best function based on the test results using a weighted scoring system.
    
    Args:
        test_matrix (list): A matrix of booleans representing function-test success.
        n_iterations (int): Number of iterations for scoring.
    
    Returns:
        int: Index of the function with the highest score.
    """
    function_scores = [0.5] * len(test_matrix)
    test_scores = [0.5] * len(test_matrix[0])

    for _ in range(n_iterations):
        new_function_scores = [0] * len(function_scores)
        for f in range(len(function_scores)):
            for t in range(len(test_scores)):
                if test_matrix[f][t]:
                    new_function_scores[f] += test_scores[t]
        
        new_test_scores = [0] * len(test_scores)
        for t in range(len(test_scores)):
            for f in range(len(function_scores)):
                if test_matrix[f][t]:
                    new_test_scores[t] += function_scores[f]
                else:
                    new_test_scores[t] += 1 - function_scores[f]
        
        for f in range(len(function_scores)):
            if max(new_function_scores) == 0:
                function_scores[f] = 1
            else:
                function_scores[f] = new_function_scores[f] / max(new_function_scores)
        for t in range(len(test_scores)):
            if max(new_test_scores) == 0:
                test_scores[f] = 1
            else:
                test_scores[t] = new_test_scores[t] / max(new_test_scores)
    
    print('Function Scores:', function_scores)
    print('Test Scores:', test_scores)
    return np.argmax(function_scores)

def get_best_function(test_matrix, n_iterations=100):
    """
    Identifies the best function based on the test results by counting the number of successful tests.
    
    Args:
        test_matrix (list): A matrix of booleans representing function-test success.
        n_iterations (int): Number of iterations for scoring.

    Returns:
        int: Index of the function with the highest score.
    """
    function_scores = [0] * len(test_matrix)
    for i in range(len(test_matrix)):
        for j in range(len(test_matrix[i])):
            if test_matrix[i][j]:
                function_scores[i] += 1

    print('Function Scores:', function_scores)
    return np.argmax(function_scores)

def extract_functions_details(code):
    """
    Extracts details of functions defined in a Python code string.
    
    Args:
        code (str): The Python code string.

    Returns:
        list: A list of dictionaries, each containing a function's name and its skeleton.
    """
    # Parse the code into an AST
    tree = ast.parse(code)
    
    # Create a visitor that will collect function details
    class FunctionDetailsVisitor(ast.NodeVisitor):
        def __init__(self):
            self.functions_details = []

        def visit_FunctionDef(self, node):
            # Extract the function signature
            args = ast.unparse(node.args)
            function_signature = f"def {node.name}({args})"
            
            if node.returns:
                returns = ast.unparse(node.returns)
                function_signature += f" -> {returns}"
            
            function_signature += ":\n"

            # Extract the docstring if it exists
            docstring = ast.get_docstring(node)
            if docstring:
                docstring = '    """' + docstring.replace('"""', '\\"""') + '"""\n'
            else:
                docstring = ''

            # Combine signature and docstring
            skeleton = function_signature + docstring

            # Append the function name and skeleton to the list as a dictionary
            self.functions_details.append({
                'function_name': node.name,
                'skeleton': skeleton
            })
            
            # To continue the search inside the function definition
            self.generic_visit(node)

    # Instantiate the visitor and use it on the AST
    visitor = FunctionDetailsVisitor()
    visitor.visit(tree)

    return visitor.functions_details


def form_matrix(s: str):
    """
    Converts a string representation of a matrix to a boolean matrix.

    Args:
        s (str): A string representation of a matrix.

    Returns:
        list: A boolean matrix derived from the string.
    """
    arr = s.split('\n')
    return [[x == '1' for x in line] for line in arr]


async def test_example(ind):
    """
    Tests a specific example function based on its index.

    Args:
        ind (int): Index of the example function.

    Returns:
        bool: True if the function passes the test, False otherwise.
    """
    start = time.time()
    print(f'Example {ind}')
    with open(f'examples/HumanEval/HumanEval/{ind}.py', 'r') as file:
        code = file.read()
    
    function_details = extract_functions_details(code)[0]
    function_name = function_details['function_name']
    skeleton = f"```python\n{function_details['skeleton']}\n```"

    functions, test_cases = await generate_code(function_name, skeleton)
    func = functions[0]['function']
    print(functions[0]['content'])

    namespace = {}
    exec(DATASET['test'][ind]['test'], namespace)
    try:
        namespace['check'](func)
        print(f'Passed | {time.time() - start:.3f} s')
        return True
    except:
        print(f'Failed | {time.time() - start:.3f} s')
        return False


async def test_example_regenerate(ind):
    """
    Regenerates and tests a specific example function based on its index.

    Args:
        ind (int): Index of the example function.

    Returns:
        bool: True if the function passes the test, False otherwise.
    """
    start = time.time()
    print(f'Example {ind}')
    with open(f'examples/HumanEval/HumanEval/{ind}.py', 'r') as file:
        code = file.read()
    
    function_details = extract_functions_details(code)[0]
    function_name = function_details['function_name']
    skeleton = f"```python\n{function_details['skeleton']}\n```"

    print('---------SKELETON---------')
    print(function_details['skeleton'])
    print('--------------------------')

    functions, test_cases = await generate_code(function_name, skeleton)
    test_matrix = test_code(functions, test_cases)
    
    for f in range(len(test_matrix)):
        for t in range(len(test_matrix[f])):
            if test_matrix[f][t]:
                print('1', end='')
            else:
                print('0', end='')
        print()

    best_function_ind = get_best_function(test_matrix)

    print('---------ANSWER---------')
    print(functions[best_function_ind]['content'])

    print('---------TESTS---------')
    for t in range(len(test_matrix[best_function_ind])):
        if test_matrix[best_function_ind][t]:
            print(test_cases[t])
    print('------------------------')

    namespace = functions[best_function_ind]['namespace']
    exec(DATASET['test'][ind]['test'], namespace)
    try:
        namespace['check'](functions[best_function_ind]['function'])
        print(f'Passed | {time.time() - start:.3f} s')
        return True
    except:
        print(f'Failed | {time.time() - start:.3f} s')
        return False


async def main(regenerate=True):
    """
    Tests code generation on HumanEval dataset
    """
    results = []
    count = 0
    for i in range(0, len(DATASET['test'])):
        try:
            if regenerate:
                result = await test_example_regenerate(i)
            else:
                result = await test_example(i)
        except:
            result = False
        
        if result:
            count += 1
        results.append(result)
        print(f"Accuracy: {count / len(results)}")
    
    print(results)


if __name__ == "__main__":
    # asyncio.run(test_example_regenerate(41))
    asyncio.run(main())
