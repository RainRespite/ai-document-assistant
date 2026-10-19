'''任务要求
编写：
def get_content_lines(text):    # 自己实现


函数需要跳过空白行，保留原始行号，并返回由字典组成的列表。
测试输入：
text = "\n\n# 标题\n正文"


预期输出：
[    {"line": 3, "text": "# 标题"},    {"line": 4, "text": "正文"}]


你可以使用刚才学过的 splitlines()、enumerate()、strip()、append() 和 return。'''
def get_content_lines(text):
    lines = text.splitlines()
    content_lines = []
    for i, line in enumerate(lines, start=1):
        if line.strip():
            content_lines.append({"line": i, "text": line})
    return content_lines
text = "\n\n# 标题\n正文"
print(get_content_lines(text))
[{"line": 3, "text": "# 标题"}, {"line": 4, "text": "正文"}]

