'''创建 exercises/day4/main.py。

使用 FastAPI 创建 GET /status 接口，函数名为 get_status。

返回包含 day 和 status 的 JSON 数据。'''
from fastapi import FastAPI
app = FastAPI()
@app.get("/status")
def get_status():
    return {"day": 4, "status": "learning"}

'''任务需求 1：创建路由

新增一个 GET 接口，路径为 /greet，函数名称为 greet。

任务需求 2：接收参数

使用查询参数接收用户传入的 name，类型为字符串 str。

任务需求 3：返回数据

返回一个字典，键为 message，值为 你好， 加上用户传入的名字。

目标输出
请求地址
GET http://127.0.0.1:8002/greet?name=Rain



期望响应
{
  "message": "你好，Rain"
}



如果参数改成 name=Tom，那么应该返回：
{
  "message": "你好，Tom"
}'''
@app.get("/greet")

def greet(name: str):
    return {"message": "你好，" + name}

'''任务 1：定义请求模型

创建 MessageRequest，继承 BaseModel，其中包含一个字符串字段 content。

任务 2：创建 POST 接口

在现有 exercises/Day4/day4_main.py 中新增一个接口，路径为 /message，函数名为 receive_message。

任务 3：返回接收到的数据

从请求体对象中取出 content，返回一个字典，字段名为 received。'''
from pydantic import BaseModel
class MessageRequest(BaseModel):
    content: str

@app.post("/message")
def receive_message(request: MessageRequest):
    return {"received": request.content}
