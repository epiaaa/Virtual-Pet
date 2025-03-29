import json
import os


def load_from_json(json_path):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"JSON 文件路径不存在: {json_path}")
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def save_Pet_info(filename, info):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=4)


if __name__ == "__main__":
    print(f'this is dataset.py')
