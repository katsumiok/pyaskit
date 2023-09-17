from pyaskit import define
import pyaskit.types as t


analyze_sentiment = define(
    t.literal("positive", "negative"), "What is the sentiment of {{s}}?"
)

reviews = [
    "The product is fantastic.",
    "The product is terrible.",
]

for review in reviews:
    sentiment = analyze_sentiment(review)
    print("---")
    print(review)
    print(sentiment)
    print(analyze_sentiment.reason)
