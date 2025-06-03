## 后端接口测试

### 1 解决跨域问题
+ **重要！**
+ [按这篇文章操作，完成基本配置即可](https://cloud.tencent.com/developer/article/2178334)

### 2 接口相关文件
+ ./djangoTest/urls.py **定义了相关路由**
+ ./myApp/views.py **定义了相关接口**


### 3 静态文件存放
+ ./myApp/static/uploadfiles **存放上传的用户文件**

### 4 接口文档
| 接口路径         | 方法   | 请求参数/体                      | 响应内容                                   | 说明                   |
|------------------|--------|----------------------------------|--------------------------------------------|------------------------|
| `/fileUpload/`    | POST   | 文件上传（字段名：`file`）        | 文本：`ok`                                 | 创建学习项目：上传用户文件作为项目知识库               |
| `/chat/`          | POST   | JSON：`{"message": "用户问题"}`      | JSON：`{"message": "successfully sent message"}` | 聊天模式：发送用户消息到后端           |
| `/chat/`          | GET    | 无                               | JSON：`{"AIMessage": "这是来自后端的AI回复"}`     | 聊天模式：获取AI回复             |
| `/summarize/`     | POST   | 文件上传（字段名：`file`）        | 文本：`ok`                                 | 总结模式：上传用户文件并处理         |
| `/summarize/`     | GET    | 无                               | JSON：`{"AIMessage": "这是来自后端的AI总结"}`     | 总结模式：获取AI总结             |
|   `/test/`          |  POST |  JSON:`{"num":"","type":"","level":"","desc":""}` | JSON:`{"AIQuestion":[{"type":"","question":""},{},{},...]}` | 小测模式：生成测试 |
| `/test/` | POST | 文件上传（字段名：`file`） | 文本：`ok` | 小测模式：上传文件 |·