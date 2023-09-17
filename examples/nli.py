from pyaskit import define
import pyaskit.types as t


nli = define(
    t.literal("entailment", "neutral", "contradiction"),
    'What is the relationship between {{s1}} and {{s2}}?')

result = nli("The dog is playing with the ball", "There is a dog playing with a ball.")
print(result)
print(nli.reason)


