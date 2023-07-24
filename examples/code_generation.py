from pyaskit import define
import pyaskit.types as t

sort = define(t.list(t.int), "Sort {{numbers}} in ascending order")
compiled_sort = sort.compile()

for _ in range(3):
    numbers = sort([1, -2, 3, -4, 5])
    print("sort: ", numbers)

for _ in range(3):
    numbers = compiled_sort([1, -2, 3, -4, 5])
    print("Compiled sort: ", numbers)
