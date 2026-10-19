"""当前练习：打开同目录的 sample.md，用 UTF-8 读取全部内容并打印。
只做读取与打印，暂不统计、不定义函数。
请在下方写你自己的代码。
"""

# TODO: 打开 sample.md，读取全部内容，然后 print。

# Q4：怎样打开、读取、打印并关闭文件？
# A4：open → read → print → close。print(f) 只会打印文件对象信息。
f = open("sample.md", encoding="utf-8")
content = f.read()
f.close()
print("Q4（文件内容）:")
print(content)


# Q5：为什么连续调用两次 f.read()，第二次通常读不到内容？
# A5：第一次读完后，读取位置已到文件末尾；应只读一次并保存到 content。
# 错误示例（不要执行）：
# print(f.read())
# content = f.read()


# Q6：怎样统计文件行数？为什么不能写 f.splitlines()？
# A6：splitlines() 是字符串的方法，要对读取后的 content 调用。
lines = content.splitlines()
print("Q6（行数）:", len(lines))  # 示例 sample.md 应为 4 行


# 待学：Markdown 标题数量、字符数量、inspect_document(path) 函数。