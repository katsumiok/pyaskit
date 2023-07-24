from pyaskit import ask
import pyaskit.types as t

october = ask(t.str, "Translate the number 10 into a month.")
print(october)
ten = ask(t.int, "Convert October into its numerical representation.")
print(ten)

month_type = t.dict({"month": t.str, "number": t.int})
first_month = ask(month_type, "What is the first month of the year?")
print(first_month)
months = ask(t.list(month_type), "List all the month numbers of the year.")
print(months)
