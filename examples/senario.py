
from pyaskit import ask, define
import pyaskit.types as t


ask(t.str, "Translate the number 10 into a month.")
ask(t.int, "Convert October into its numerical representation.")
month = t.dict({"month": t.str, "number": t.int})
ask(month, "What is the first month of the year?")
ask(t.list(t.int), "List all the month numbers of the year.")


translate = define(t.str, 'Translate {{text}} int {{lang}}')
translate(text="Hello World!", lang="Spanish")

sort = define(t.list(t.int), 'Sort {{numbers}} in ascending order')
sort([1, -2, 3, -4, 5])

get_title = define(t.str, 'Get the web page in {{url}}').compile()

sort = define(t.list(t.int), 'Sort {{numbers}} in ascending order.')
