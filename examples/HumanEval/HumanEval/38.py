from pyaskit import function

@function(codable=True)
def decode_cyclic(s: str):
    """
    takes as input string {{s}} encoded with encode_cyclic function. Returns decoded string.

    def encode_cyclic(s: str):
        # split string to groups. Each of length 3.
        groups = [s[(3 * i):min((3 * i + 3), len(s))] for i in range((len(s) + 2) // 3)]
        # cycle elements in each group. Unless group has fewer elements than 3.
        groups = [(group[1:] + group[0]) if len(group) == 3 else group for group in groups]
        return "".join(groups)
    """