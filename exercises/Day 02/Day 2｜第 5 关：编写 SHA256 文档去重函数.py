'''功能要求
1. 使用之前学过的 clean_text() 清洗两段文本。
2. 使用 SHA256 分别计算哈希值。
3. 比较两个哈希值。
4. 使用 return 返回布尔值 True 或 False。
注意：不能只使用 print()，必须使用 return。
三、测试数据
测试 1：
text1 = "Hello\r\nPython "text2 = "Hello\nPython"print(is_duplicate(text1, text2))


预期输出：
True

测试 2：
text1 = "Hello Python"text2 = "Hello Java"print(is_duplicate(text1, text2))


预期输出：
False'''
import hashlib
def clean_text(text):
    text = text.replace("\r\n", "\n")
    text = text.replace("\t", "")
    text = text.replace(" ", "")
    return text
def is_duplicate(text1, text2):
    text1 = clean_text(text1)
    text2 = clean_text(text2)
    hash1 = hashlib.sha256(text1.encode("utf-8")).hexdigest()
    hash2 = hashlib.sha256(text2.encode("utf-8")).hexdigest()
    return hash1 == hash2
print(is_duplicate("Hello\r\nPython", "Hello\nPython"))
print(is_duplicate("Hello Python", "Hello Java"))