# text = "Hello\r\nPy\x00thon\r\n"
# text = text.replace("\r\n", "\n")
# text = text.replace("\x00", "")
# text = text.rstrip()
# print(repr(text))

'''Day 2｜第 1 关：Python 文本清洗函数——③ 独立编程任务
当前阶段：正式任务（尚未验收）
现在将刚才学到的知识封装成一个函数。
任务要求
在 day02.py 中编写：
def clean_text(text):    # 由你独立实现


函数需要完成：
1. 将 \r\n 替换为 \n。
2. 将单独的 \r 替换为 \n。
3. 删除 \x00。
4. 使用 rstrip() 清理末尾空白。
5. 使用 return 返回处理结果，不能只用 print()。
注意：必须保留文本开头的空行。
测试代码
sample = "\n\n# 标题\r\n正\x00文\r结束\r\n"result = clean_text(sample)print(repr(result))


预期输出：
'\n\n# 标题\n正文\n结束'

验收标准
你需要独立写出函数，并能通过测试。
现在请你尝试完成 clean_text() 函数，把完整代码和运行结果发给我。
这次我先不提供完整答案。如果遇到困难，我会根据你写出的代码进行针对性指导。'''
def clean_text(text):
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    text = text.replace("\x00", "")
    text = text.rstrip()
    return text
sample = "\n\n# 标题\r\n正\x00文\r结束\r\n"
result = clean_text(sample)
print(repr(result))
sample2 = "\n\n\nHello\rWorld\x00   \n\n"

result2 = clean_text(sample2)

print(repr(result2))