import pyaskit as ai

get_html = ai.define(str, 'Get the webpage from {{url}}').compile()
html = get_html(url='https://csail.mit.edu')
print(html)