import json


def load_Pet_info(filename):
    with open(filename, "r") as f:
        infos = json.load(f)
    return infos


def save_Pet_info(filename, info):
    with open(filename, "w") as f:
        json.dump(info, f, indent=4)


if __name__ == "__main__":
    print(f'this is dataset.py')

