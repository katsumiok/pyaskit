from pyaskit import define
import pyaskit.types as t


nli = define(
    t.literal("entailment", "neutral", "contradiction"),
    "What is the relationship between {{s1}} and {{s2}}?",
)

pairs = [
    ("The dog is playing with the ball", "There is a dog playing with a ball."),
    ("The dog is playing with the ball", "The cat is playing with the ball."),
    ("The dog is playing with the ball", "The dog is not playing with the ball.")
]

for s1, s2 in pairs:
    result = nli(s1, s2)
    print("---")
    print(s1)
    print(s2)
    print(result)
    print(nli.reason)
