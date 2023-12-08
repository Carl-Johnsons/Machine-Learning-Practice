import json
from fuzzywuzzy import fuzz
import os

from vietnam_provinces.enums import ProvinceEnum, ProvinceDEnum, DistrictDEnum

PROVINCES_DICT = {}
i = 0
for member in ProvinceDEnum:
    lowercase = member.value.name.lower()
    PROVINCES_DICT[lowercase] = i
    i += 1
for member in DistrictDEnum:
    lowercase = member.value.name.lower()
    if lowercase.startswith("thành phố"):
        PROVINCES_DICT[lowercase] = i
        i += 1

file_path = "./data/dataset.json"
data = []

if not os.path.exists(file_path):
    # If the file doesn't exist, create it
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    print(f"File '{file_path}' created.")
else:
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    print(f"File '{file_path}' already exists. Load existed data")


new_data_list = [

]

for item in new_data_list:
    new_data = {"sentence": "sentence", "label": "label"}
    sentence = item["sentence"]
    label = item["label"]

    # Find the member with the highest similarity score
    max = -1
    closest_member = ""
    label = label.lower()
    for name, code in PROVINCES_DICT.items():
        lowercase_member = name
        ratio = fuzz.ratio(label, lowercase_member)
        if max < ratio:
            max = ratio
            closest_member = lowercase_member
            print(ratio)
            print(closest_member)
            print(PROVINCES_DICT[closest_member])

    new_data["sentence"] = sentence
    new_data["label"] = PROVINCES_DICT[closest_member]
    data.append(new_data)

with open(file_path, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)
