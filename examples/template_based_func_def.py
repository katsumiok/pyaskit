from pyaskit import ask, define
import pyaskit.types as t

translate = define(t.str, "Translate {{text}} int {{lang}}")
spanish = translate(text="Hello World!", lang="Spanish")
french = translate("Hello World!", lang="French")
chinese = translate("Hello World!", "Chinese")
print(spanish, french, chinese)

double = define(t.int, "Add {{x}} + {{x}} mathematically")
y = double(10)
print(y)

f = define(t.int, "Add {{x}}, {{x}} and {{y}} mathematically")
z = f(10, 20)
print(z)
