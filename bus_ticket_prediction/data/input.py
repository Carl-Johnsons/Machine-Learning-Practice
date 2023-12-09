import json
from fuzzywuzzy import fuzz
import os
import random

from vietnam_provinces.enums import ProvinceDEnum, DistrictDEnum

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


def remove_location_prefix(input_string):
    prefixes = ["thành phố", "tỉnh"]
    for prefix in prefixes:
        if input_string.startswith(prefix):
            input_string = input_string.replace(prefix, "", 1).strip()
    return input_string


def update_progress_bar(
    progress_percent: int,
    progress_bar: str,
    step: int,
    current: int,
    max: int,
    complete_symbol="=",
):
    if progress_percent % step != 0:
        return
    os.system("cls")
    index = int(progress_percent / step)
    progress_bar = (
        progress_bar[:1] + (complete_symbol * index) + progress_bar[index + 1 :]
    )
    formatted_progress_bar = progress_bar.format(current=current, max=max)
    print(formatted_progress_bar)


def writeToJson(new_data_list):
    max_progress = len(new_data_list)
    current_progress = 0
    last_progress_percent = 0
    current_percent = 0
    step = 5
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

        new_data["sentence"] = sentence
        new_data["label"] = PROVINCES_DICT[closest_member]
        data.append(new_data)
        # for display progress bar
        current_progress += 1
        current_percent = int(current_progress / max_progress * 100)
        if current_percent > last_progress_percent:
            last_progress_percent = current_percent
            update_progress_bar(
                current_percent,
                "[....................] {current}/{max} write to json file",
                step,
                current_progress,
                max_progress,
            )

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def preprocessing_data(
    provinces_dict, name_array: list[str], sentence_array: list[str], output: list[str]
):
    max_progress = len(provinces_dict) * len(name_array) * len(sentence_array)
    current_progress = 0
    last_progress_percent = 0
    current_percent = 0
    step = 5

    temp_city = ""
    for sentence in sentence_array:
        for name_item in name_array:
            for city_item, index in PROVINCES_DICT.items():
                temp_city = city_item
                if random.random() < 0.4:
                    temp_city = remove_location_prefix(temp_city)
                title_str = temp_city.title()
                new_data_template = {
                    "sentence": sentence.format(name=name_item, city=title_str),
                    "label": title_str,
                }
                # for displaying progress
                current_progress += 1
                current_percent = int(current_progress / max_progress * 100)
                output.append(new_data_template)
                if current_percent > last_progress_percent:
                    last_progress_percent = current_percent
                    update_progress_bar(
                        current_percent,
                        "[....................] {current}/{max} preprocessing data",
                        step,
                        current_progress,
                        max_progress,
                    )


name_template = [
    "mình",
    "bạn",
    "tôi",
    "tui",
    "ông",
    "bà",
    "chị",
    "anh",
    "mẹ",
    "ba",
    "ông nội",
    "ông ngoại",
    "bà nội",
    "bà ngoài",
    "dì",
    "chú",
    "bác",
    "chồng",
    "vợ",
    "anh",
    "em",
]

sentence_template = [
    "Muốn đi {city} quá à",
    "{name} ở {city}, nơi này có nhiều điểm du lịch lịch sử hay.",
    "Cuối tháng, {name} lên {city} thăm người thân.",
    "{name} đang ở {city}, có gì vui ở đây không?",
    "Buổi tối ở {city} thì nên đi đâu chơi?",
    "{city} dễ thương quá, {name} thích thăm lại lần nữa.",
    "{name} sắp đến {city}, nơi này có đồ ăn ngon không?",
    "{name} ở {city}, có điểm du lịch gì độc đáo không?",
    "{city} có nhiều địa điểm mua sắm, {name} muốn ghé không?",
    "{name} thích đi chơi ở {city}, có gì hot không nhỉ?",
    "{city} có nhiều điểm ẩm thực ngon, {name} biết chưa?",
    "Buổi tối ở {city} thì nên ghé quán nào để cảm nhận không khí?",
    "Phong cảnh ở {city} thơ mộng, {name} muốn đến đây ngắm cảnh.",
    "{name} thấy {city} có thời tiết se lạnh, có đúng không?",
    "Ở {city} có nhiều cửa hàng độc đáo, {name} đã mua đồ ở đó chưa?",
    "{name} ở {city}, có nơi nào là địa điểm check-in nổi tiếng không?",
    "Tại {city}, có nhiều sự kiện văn hóa độc đáo, {name} muốn tham gia không?",
    "{name} thích hải sản ở {city}, có quán nào ngon mà giới thiệu không?",
    "Mùa lễ hội ở {city}, {name} thích tham gia lễ hội nào nhất?",
]

output_data = []
preprocessing_data(PROVINCES_DICT, name_template, sentence_template, output_data)
random.shuffle(output_data)
writeToJson(output_data)
