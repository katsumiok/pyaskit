import pyaskit as ai
import pyaskit.types as t

s = ai.ask(t.str, 'Paraphrase "Hello World!"')
print(s)