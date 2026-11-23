import json

with open("evaluation/deepeval_dataset.json", "r", encoding="utf-8") as file:
    dataset = json.load(file)

for record in dataset[:10]:
    print(f"{record['id']} | {record['input']}")