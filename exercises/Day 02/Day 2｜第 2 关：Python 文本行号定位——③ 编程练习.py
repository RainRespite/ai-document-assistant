'''任务：打印非空行及其原始行号
给定：
text = "\n\n# 标题\n正文"


要求使用三个知识点：
1. splitlines()：把文本拆成多行。
2. enumerate(..., start=1)：给每一行编号。
3. if line.strip()：跳过空行。
目标输出：
3 # 标题
4 正文'''
# 1. 准备文本：开头两个 \n 是空行，真正的内容排在第 3、4 行，用来验证「原始行号」是否正确
text = "\n\n# 标题\n正文"
# 2. 逐行遍历并编号：splitlines() 按换行符拆成行列表；enumerate(..., start=1) 从 1 开始计数，让编号对齐编辑器里的真实行号
#    拆开看：i 是行号(1、2、3、4...)，line 是对应那一行的内容
for i, line in enumerate(text.splitlines(), start=1):
    # 3. 跳过空行：line.strip() 去掉首尾空白，空行会变成 ""（假值），if 条件不成立就跳过；非空行为真值继续执行
    if line.strip():
        # 4. 打印行号和内容，print 默认用空格分隔，所以输出形如 "3 # 标题"
        print(i, line)
