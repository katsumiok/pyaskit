from pyaskit import function
from typing import TypedDict, List


class Person(TypedDict):
    name: str
    job_title: str
    address: str


@function(codable=False)
def extract_information(text: str) -> List[Person]:
    """
    Extract names, job titles, and addresses of people mentioned in the {{text}}.
    """


text = """
John Doe, a software engineer at Tech Innovations Inc., recently moved to 123 Main Street, Anytown, USA. He works closely with his colleague, Jane Smith, the lead data scientist, who resides at 456 Oak Avenue, Somewhere City, Canada. Their manager, Robert Johnson, a senior project manager, is based out of the company's headquarters at 789 Elm Road, Big City, United Kingdom.

In the marketing department, Sarah Williams, a creative director, collaborates with Mark Davis, the content strategist. Sarah lives at 321 Pine Lane, Small Town, Australia, while Mark's address is 654 Cedar Boulevard, Another City, New Zealand.

The company's HR manager, Emily Brown, who has her office at 987 Maple Drive, Somewhere Else, USA, recently hired a new recruitment specialist named Michael Wilson. Michael's current address is 741 Birch Street, Yet Another Town, Canada.

This diverse team, spread across multiple countries, works together to create innovative software solutions for clients worldwide.

Feel free to use this text to verify if your tool correctly identifies and extracts the names, job titles, and addresses mentioned. Let me know if you need any further assistance!
"""

people = extract_information(text)
for person in people:
    print("-" * 40)
    print(person)
