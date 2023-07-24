import hashlib
import re
from unidecode import unidecode


def normalize(text):
    # Transliterate to Latin script
    text = unidecode(text)

    # Normalize to lowercase
    text = text.lower()

    # Remove non-alphanumeric characters and standardize whitespace
    text = re.sub(r"\W+", " ", text)
    return text


def shorten(text, max_words=5, max_length=10):
    # Split the description into words
    words = text.split()
    # Take only the first few words
    words = words[:max_words]
    # Truncate each word after a certain number of characters
    words = [word[:max_length] for word in words]
    return words


def encode(words):
    # Join words with underscores to form a Python identifier
    identifier = "_".join(words)
    return identifier


def generate_unique_function_name(description: str) -> str:
    normalized = normalize(description)
    shortened = shorten(normalized)
    name = encode(shortened)
    # Append a hash of the original description
    hash_object = hashlib.md5(description.encode())
    hex_dig = hash_object.hexdigest()
    short_hash = hex_dig[:6]  # Take only first 6 characters
    unique_name = f"{name}_{short_hash}"
    return unique_name
