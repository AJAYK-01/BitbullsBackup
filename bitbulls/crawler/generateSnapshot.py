import json


def GenerateSnap(html):
    html = html.replace(r'\n', '').replace(r'\r', '')
    return html


def main():
  filename = "wikikijoy3lk2anu.onion.json"
  with open(filename,'r') as f:
      data = f.read()
      Json = json.loads(data)
      print(GenerateSnap(Json[0]['html']))


if __name__ == "__main__":
    main()
