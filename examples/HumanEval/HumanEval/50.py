from pyaskit import function

@function(codable=True)
def encode_shift(s: str):
    """
    returns encoded string by shifting every character in {{s}} by 5 in the alphabet.
    """
    return "".join([chr(((ord(ch) + 5 - ord("a")) % 26) + ord("a")) for ch in s])

@function(codable=True)
def decode_shift(s: str):
    """
    takes as input string {{s}} encoded with encode_shift function. Returns decoded string.
    """
