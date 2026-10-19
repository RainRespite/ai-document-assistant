'''编写一个 Python 函数：
inspect_document(path)
功能：输入一个文件路径，自动分析文件，返回统计结果。
例如，文件 sample.md 的内容为：
# 标题
正文
## 小节
内容

程序需要完成以下功能：
功能	具体要求	预期结果
1. 读取文件	使用 UTF-8 编码	获取完整正文
2. 获取文件名	只保留文件名，不包含路径	sample.md
3. 统计行数	使用 splitlines()	4
4. 统计标题	统计以 # 开头的行	2
5. 统计字符	包括空格和换行符	17
6. 返回结果	使用字典 return	包含以上四项统计数据


字符数 17 的前提是文件最后也有一个换行符。'''
def inspect_document(path):
    # 1. 读取文件：以 UTF-8 编码打开并一次性读入全部正文，with 语句会自动关闭文件
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # 2. 获取文件名：按 '/' 切分路径，取最后一段，去掉目录部分（如 sample.md）
    filename = path.split('/')[-1]
    # 3. 统计行数：splitlines() 按换行符把正文拆成行列表，len() 得到总行数
    linenum = len(content.splitlines())
    # 4. 统计标题数：筛出以 '#' 开头的行（Markdown 标题），列表推导式只保留这些行再计数
    #一句话记忆：[要保留的东西 for 每一项 in 列表 if 筛选条件]
    titlenum = len([line for line in content.splitlines() if line.startswith('#')])
    # 5. 统计字符数：直接取字符串长度，包含空格和换行符
    charnum = len(content)
    # 6. 返回结果：用字典一次性打包四项统计数据，便于调用者按key取值
    return {'name': filename, 'lines': linenum, 'headings': titlenum, 'characters': charnum}
print(inspect_document("empty.md"))
