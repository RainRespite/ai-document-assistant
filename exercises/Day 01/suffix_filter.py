"""后缀筛选练习：按用户要求重建，非昨日原代码存档。"""


def get_txt_names(docs, suffix):
    names = []
    for doc in docs:
        name = doc["name"]
        if name.endswith(suffix):
            names.append(name)
    return names


if __name__ == "__main__":
    docs = [
        {"name": "lesson.md"},
        {"name": "notes.txt"},
        {"name": "guide.md"},
    ]
    print(get_txt_names(docs, ".md"))
    print(get_txt_names(docs, ".txt"))
    print(get_txt_names([], ".md"))
