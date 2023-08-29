<!-- {% raw %} -->
# *AskIt* (pyaskit)



## Introduction

*AskIt* serves as a dedicated library or domain-specific language designed to streamline the utilization of Large Language Models (LLMs) such as GPT-4. It simplifies the complexities of prompt engineering and eradicates the requirement for parsing responses from LLMs, making programming tasks smoother.

Using *AskIt*, you can deploy LLMs for a multitude of tasks, such as:

- Natural Language Processing: including translation, paraphrasing, and sentiment analysis.
- Problem Solving: resolving mathematical problems.
- Code Generation: creating new codes, and more.

*AskIt* operates through the [OpenAI API](https://beta.openai.com/) for backend LLM functions. Besides Python, *AskIt* has also been implemented in TypeScript. You can access the TypeScript version, [ts-askit](https://katsumiok.github.io/ts-askit/).

## Key Features

- [x] Type-Guided Output Control: Enhance LLM precision with types.
    ![Type-guided output control demonstration](https://katsumiok.github.io/pyaskit/images/type_guided_output_control.gif)

- [x] Template-Based Function Definition: Define functions using a prompt template.
    ![Template-based function definition demonstration](https://katsumiok.github.io/pyaskit/images/template_based_func_def.gif)

- [x] Natural Language Programming: Employ code synthesis for task execution.
    ![Natural Language Programming demonstration](https://katsumiok.github.io/pyaskit/images/codable_task.gif)

- [x] Programming by Example (PBE): Define functions using examples.
    Refer to the [Programming by Example (PBE)](#programming-by-example-pbe) section for further details.
 
## Installation

To install *AskIt*, run this command in your terminal:

```bash
# XXX: The package is not published yet.
pip install pyaskit
```
or
```bash
pip install git+https://github.com/katsumiok/pyaskit.git
```

Before using *AskIt*, you need to set your OpenAI API key as an environment variable `OPENAI_API_KEY` and `ASKIT_MODEL`:
```bash
export OPENAI_API_KEY=<your OpenAI API key>
```
`<you OpenAI API key>` is a string that looks like this: `sk-<your key>`.
 You can find your API key in the [OpenAI dashboard](https://platform.openai.com/account/api-keys).

You can also specify the model name as an environment variable `ASKIT_MODEL`:
```bash
export ASKIT_MODEL=<model name>
```
`<model name>` is the name of the model you want to use. 
The latest AskIt is tested with `gpt-4` and `gpt-3.5-turbo-16k`. You can find the list of available models in the [OpenAI API documentation](https://platform.openai.com/docs/models).
## Getting Started

Here are some basic examples to help you familiarize yourself with *AskIt*:

### Hello World

```python
import pyaskit as ai
import pyaskit.types as t

s = ai.ask(t.str, 'Paraphrase "Hello World!"')
print(s)
```

To utilize *AskIt*, start by importing the `pyaskit` and `pyaskit.types` modules. The `ask` API, which takes two arguments - the output type and the prompt - produces the LLM's output in the designated format. In this case, the output type is `str` and the prompt is `Paraphrase "Hello World!"`. A comprehensive explanation of types in *AskIt* is provided in the [Types](#types) section. Executing this code will yield a paraphrase of the prompt, such as:
```
Greetings, Planet!
```

### Defining a Function from a Template Prompt

The `define` API allows for prompt parameterization using template syntax:

```python
import pyaskit as ai
import pyaskit.types as t

paraphrase = ai.define(t.str, 'Paraphrase {{text}}')
s = paraphrase(text='Hello World!')
# s = paraphrase('Hello World!') # This is also valid
print(s)
```
In this instance, the `define` API creates a templated function that instructs the LLM to paraphrase specified text. Invoking the `paraphrase` function with 'Hello World!' will return a paraphrased version of this text. Running this code might output something like "Greetings, Planet!".

The `define` API allows for straightforward creation of custom functions to harness the capabilities of large language models for diverse tasks. Further examples can be found in the [examples](examples) directory.

### Translating a Codable Task

Certain tasks, such as those requiring real-time data, external resources like network access, file access, or database access, are unsuitable for LLM execution. However, *AskIt* can handle these tasks by converting the prompt into a Python program in the background.

The subsequent example demonstrates using *AskIt* to tackle a task necessitating network access:

```python
import pyaskit as ai
import pyaskit.types as t

get_html = ai.define(t.str, 'Get the webpage from {{url}}').compile()
html = get_html(url='https://csail.mit.edu')
print(html)
```
In this scenario, you only need to call `compile()` on the function returned by the `define` API. The `compile` function transforms the prompt into a Python program and returns a function that executes this code, behaving just like a regular Python function.

## Programming by Example (PBE)

### Function Definition Using Examples
Language Learning Models (LLMs) offer the advantage of few-shot learning, a capability that *AskIt* utilizes in programming tasks. *AskIt* enables you to solve tasks using the Programming by Example (PBE) technique, where you provide examples of the desired input and output.

Let's consider creating a function to add two binary numbers (represented as strings). This function accepts two binary numbers and returns their sum, also in binary form. The following code demonstrates defining such a function using illustrative examples.

```python
from pyaskit import define
import pyaskit.types as t

training_examples = [
    {"input": {"x": "1", "y": "0"}, "output": "1"},
    {"input": {"x": "1", "y": "1"}, "output": "10"},
    {"input": {"x": "101", "y": "11"}, "output": "1000"},
    {"input": {"x": "1001", "y": "110"}, "output": "1111"},
    {"input": {"x": "1111", "y": "1"}, "output": "10000"},
]

add_binary_numbers = define(t.str, "Add {{x}} and {{y}}", training_examples=training_examples)
sum_binary = add_binary_numbers(x="101", y="11")
print(sum_binary)  # Output: "1000"
```
In this example, the `define` API takes three arguments: the output type, the prompt, and the training examples. Each entry in the training examples list is a dictionary containing an 'input' dictionary (with variable names and values) and an 'output' representing the expected function output given the input. The `define` API then returns a function that accepts input variables as keyword arguments and outputs the LLM's output in the specified type.

The `add_binary_numbers` function, which adds two binary numbers, behaves like any regular Python function.

### Testing the Translated Function

You can use the `compile` function to test the translated function using an optional list of test examples.

The following code demonstrates how to test the function defined above with new test examples:

```python
test_examples = [
    {"input": {"x": "0", "y": "1"}, "output": "1"},
    {"input": {"x": "10", "y": "0"}, "output": "10"},
    {"input": {"x": "110", "y": "10"}, "output": "1000"},
]
f = add_binary_numbers.compile(test_examples=test_examples)
sum_binary = f(x="101", y="11")
print(sum_binary)  # Output: "1000"
```
Here, `f` is the translated function that operates similarly to `add_binary_numbers`. By comparing the output of the translated function with the expected output for each test example, *AskIt* ensures the translated function behaves as expected. If any discrepancy arises, *AskIt* re-attempts the translation. After multiple unsuccessful translation attempts, *AskIt* raises an exception.
## Specifying Types in *AskIt*

*AskIt* offers APIs to designate the output types for Language Learning Models (LLMs). By supplying these types as the first argument to the `ask` and `define` APIs, you can manage the LLM's output format.

The following table describes the various types supported by *AskIt*:

| Type | Description | Type Example | Value Example |
| --- | --- | --- | --- |
| `int` | Integer | `t.int` |  123 |
| `float` | Floating Point Number | `t.float` | 1.23 |
| `bool` | Boolean | `t.bool` | True |
| `str` | String | `t.str` | "Hello World!" |
| `literal` | Literal | `t.literal(123)` | 123 |
| `list` | List |  `t.list(t.int)` | [1, 2, 3] |
| `dict` | Dictionary |  `t.dict({` <br>&nbsp;`'a': t.int, `<br>&nbsp;`'b': t.int` <br>`})` |{'a': 1, 'b': 2} |
| `union` | Union (Multiple Possible Values) | `t.union(t.literal('yes'), t.literal('no'))` | "yes" or "no" |

Note that each type declaration aids *AskIt* in parsing and understanding the desired output, ensuring your LLM returns data in the precise format you require.

## Prompt Template Usage

The prompt template is a string composed of placeholders for the parameters of the function being defined. Placeholders are denoted by double curly braces `{{` and `}}` and can only contain a variable name. This variable name is then used as a parameter in the defined function.

Function parameters can be defined in two ways: either by keyword arguments or by positional arguments. For keyword arguments, the variable name within the placeholder serves as the keyword argument's name. For positional arguments, the sequence in which placeholders appear defines the order of the positional arguments.

Consider the following example which demonstrates how to define a function, `add`, that accepts two arguments `x` and `y` and returns their sum:
```python
from pyaskit import define
import pyaskit.types as t

add = define(t.int, '{{x}} + {{y}}')
print(add(x=1, y=2))  # keyword arguments
print(add(1, 2))  # positional arguments
```
In this case, the `add` function can be invoked using either keyword or positional arguments, with the sum of `x` and `y` returned as the output.

Notably, if the same variable name is used multiple times in the prompt template, subsequent uses are mapped to the initial occurrence. Observe this behavior in the following example:
```python
from pyaskit import define
import pyaskit.types as t

add = define(t.int, '{{x}} + {{y}} + {{x}} + {{z}}')
print(add(x=1, y=2, z=3))
print(add(1, 2, 3))
```
Here, `{{x}}` appears twice in the prompt template. The second occurrence of `{{x}}` maps back to the first. Hence, even though `{{z}}` is the fourth placeholder in the template, it aligns with the third argument of the function.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

<!-- {% endraw %} -->
