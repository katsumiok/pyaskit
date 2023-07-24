import pyaskit as ai
import pyaskit.types as t

paraphrase = ai.define(t.str, 'Paraphrase {{text}}')
s = paraphrase(text='Hello World!')
# s = paraphrase('Hello World!') # This is also valid
print(s)
