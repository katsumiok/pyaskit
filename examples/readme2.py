import pyaskit as ai

paraphrase = ai.define(str, 'Paraphrase {{text}}')
s = paraphrase(text='Hello World!')
# s = paraphrase('Hello World!') # This is also valid
print(s)
