import re


def remove_duplicates(my_list):
    return list(dict.fromkeys(my_list))


def extract_variables(template_string):
    variables = re.findall(r"\{\{\s*(.*?)\s*\}\}", template_string)
    pattern = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
    all_valid = all(pattern.match(variable) for variable in variables)
    if not all_valid:
        raise ValueError("Invalid variable name")
    return remove_duplicates(variables)


def convert_template(template_string):
    return re.sub(r"\{\{\s*(.*?)\s*\}\}", r"'\1'", template_string)
