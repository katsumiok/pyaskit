from typing import List
import os
import importlib
from . import types as t
from .template import convert_template, extract_variables
from .dialog import query
from .function_name import generate_unique_function_name
from .code_generator import implement_body
from .prompt import make_coding_prompt
from .path import add_to_sys_path
from .example import ExampleType, check_examples
from .logging_config import setup_logger
from .llm import get_history, clear_history
from .types.converter import convert_type


logger = setup_logger(__name__)

# Default path
module_path = os.path.join(os.getcwd(), "askit")


class Function:
    def __init__(
        self,
        return_type,
        param_types,
        template: str,
        training_examples: ExampleType = [],
        order: List[str] = None,
    ) -> None:
        return_type = convert_type(return_type)
        if not isinstance(return_type, t.Type):
            raise ValueError(
                "return_type must be a type hint or Type defined in pyaskit.types"
            )
        if param_types is not None:
            for k, v in param_types.items():
                param_types[k] = convert_type(v)
        self.return_type = return_type
        self.param_types = param_types
        self.template = template
        self.variables = extract_variables(self.template, order=order)

        check_examples(return_type, self.variables, training_examples)
        self.training_examples = training_examples
        self._reason = ""
        self._errors: List[str] = []
        self._completion = None
        self._recompilation_count = 0
        self._validator = None
        self._history = []

    def set_validator(self, validator):
        self._validator = validator

    def __call__(self, *args, **kwargs):
        converted_template = convert_template(self.template)
        variableMap = {}
        self.check_args(args, kwargs, self.variables, variableMap)
        clear_history()
        result, self._reason, self._errors, self._completion = query(
            converted_template,
            variableMap,
            self.return_type,
            self.training_examples,
            self._validator,
        )
        self._history = get_history()
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

    @property
    def history(self):
        return self._history

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
                self.param_types,
                task,
                function_name,
                self.variables,
                self.training_examples,
            )
            # print("Prompt:", prompt)
            code, self._recompilation_count, retry_count = implement_body(
                function_name, prompt, test_examples
            )
            os.makedirs(module_path, exist_ok=True)
            with open(module_file_path, "w") as f:
                f.write(
                    "# Recompilation count: " + str(self._recompilation_count) + "\n"
                    "# Retry count: " + str(retry_count) + "\n"
                )
                f.write(code)
        else:
            # logger.setLevel(logging.DEBUG)
            logger.debug(f"File {module_file_path} already exists")
        with add_to_sys_path(module_path):
            module = importlib.import_module(function_name)
            importlib.reload(module)
        return getattr(module, function_name)
