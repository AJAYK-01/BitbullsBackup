import json

categories = [
        "Child Abuse",
        "Identity Forgery",
        "Rent a Hacker",
        "Drug Sale",
        "Gore and Torture",
        "Terrorism",
        "Slave Trade",
        "Hitman Hiring",
        "Hacktivism",
        "Social Networking",
        "Wikis",
        "Forums"
]

def outputter(Json):
    Json = json.loads(Json)
    for category in categories:
        print(Json[category]['url'])
