import json

f = open("books.json")
data = json.load(f)


for i in range(10):
    print(data[i])