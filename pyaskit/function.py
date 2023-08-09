import os
import importlib
from . import types as t
from .types.schema import generate_schema
from .template import convert_template, extract_variables
from .gpt import chat
from .function_name import generate_unique_function_name
from .code_generator import implement_body
from .prompt import make_coding_prompt
from .path import add_to_sys_path
from .example import ExampleType, check_examples
from .logging_config import setup_logger
import logging

logger = setup_logger(__name__)

# Default path
module_path = os.path.join(os.getcwd(), "askit")


class Function:
    def __init__(
        self, return_type, template: str, training_examples: ExampleType = []
    ) -> None:
        if not isinstance(return_type, t.Type):
            raise ValueError("return_type must be a Type defined in py_askit.type")
        self.return_type = return_type
        self.template = template
        self.variables = extract_variables(self.template)
        check_examples(return_type, self.variables, training_examples)
        self.training_examples = training_examples
        self._reason = ""
        self._errors = []
        self._completion = None
        self._recompilation_count = 0

    def __call__(self, *args, **kwargs):
        converted_template = convert_template(self.template)
        variableMap = {}
        self.check_args(args, kwargs, self.variables, variableMap)

        result, self._reason, self._errors, self._completion = chat(
            converted_template,
            variableMap,
            self.return_type,
            self.training_examples,
        )
        return result
    
    @property
    def reason(self):
        return self._reason
    
    @property
    def errors(self):
        return self._errors
    
    @property
    def completion(self):
        return self._completion
    
    @property
    def recompilation_count(self):
        return self._recompilation_count

    def check_args(self, args, kwargs, variables, variableMap):
        for var, arg in zip(variables, args):
            if var in kwargs:
                raise ValueError(f"got multiple values for argument '{var}'")
            variableMap[var] = arg
        for variable in variables:
            if variable in variableMap:
                continue
            if variable in kwargs:
                variableMap[variable] = kwargs[variable]
            else:
                raise ValueError("Variable not found: " + variable)

    def compile(self, test_examples: ExampleType = []):
        check_examples(self.return_type, self.variables, test_examples)
        task = convert_template(self.template)
        function_name = generate_unique_function_name(task)
        # check if function_name.py exists
        module_file_path = os.path.join(module_path, function_name + ".py")
        if not os.path.exists(module_file_path):
            print(f"Creating file {module_file_path}")
            prompt = make_coding_prompt(
                self.return_type,
                task,
                function_name,
                self.variables,
                self.training_examples,
            )
            # print("Prompt:", prompt)
            code, self._recompilation_count = implement_body(function_name, prompt, test_examples)
            os.makedirs(module_path, exist_ok=True)
            with open(module_file_path, "w") as f:
                f.write("# Recompilation count: " + str(self._recompilation_count) + "\n")
                f.write(code)
        else:
            # logger.setLevel(logging.DEBUG)
            logger.debug(f"File {module_file_path} already exists")
        with add_to_sys_path(module_path):
            module = importlib.import_module(function_name)
            importlib.reload(module)
        return getattr(module, function_name)
