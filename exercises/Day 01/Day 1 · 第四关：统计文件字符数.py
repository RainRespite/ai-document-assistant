'''✏️ 你的任务
请写出一行代码，计算 content 的字符数量，并打印出来。
要求输出格式：
字符数量：17
注意：示例文件末尾包含一个换行符。
只需要写一行 Python 代码。
完成后，我们就进入 Day 1 最后的综合练习：将文件统计功能封装成 inspect_document() 函数。'''

f = open("sample.md", encoding="utf-8")
content = f.read()
f.close()

print("字符数量：", len(content))
