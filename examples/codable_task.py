from pyaskit import define
import pyaskit.types as t

get_html = define(t.str, "Get the webpage from {{url}}.").compile()
html = get_html(url="https://csail.mit.edu/")
print(html)
