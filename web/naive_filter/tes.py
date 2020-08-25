import json

with open('../static/conproba.json') as data:
    data = json.loads(data.read())

for label in data:
    print(label)
    for kata in data[label]:
        nilai = data[label][kata]
        print(kata)
        print(nilai)