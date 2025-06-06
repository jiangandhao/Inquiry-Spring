from openai import OpenAI
from langchain_community.llms import QianfanLLMEndpoint
import os

def getAIChatMsg(userMsg):
    # client = OpenAI(
    #     # 替换下列示例中参数，将your_APIKey替换为真实值，如何获取API Key请查看https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Um2wxbaps#步骤二-获取api-key
    #     api_key="bce-v3/ALTAK-aFDSKHhZxlMhgzYk0tDAG/22d02964efd407d620ec17bfec23521ddae88b35",
    #     # 千帆ModelBuilder平台地址
    #     base_url="https://qianfan.baidubce.com/v2",
    # )
    #userMsg=userMsg+"用markdown格式输出"
    messages = [{"role": "user", "content": userMsg}]  # 对话messages信息
    # response = client.chat.completions.create(
    #     model="ERNIE-4.0-8K",
    #     # 模型对应的model值，请查看支持的模型列表：https://cloud.baidu.com/doc/WENXINWORKSHOP/s/wm7ltcvgc
    #     messages=messages  # messages信息
    # )
    #print(response.choices[0].message.content)
    os.environ["QIANFAN_AK"] = "2XxiOBeXECBe3vXDJCCGTUkz"
    os.environ["QIANFAN_SK"] = "lPMgYn8fAjhKzfBRDSNqTcHXIrvWSG5R"

    llm_wenxin = QianfanLLMEndpoint()

    res = llm_wenxin(userMsg)
    print(res)
    return res



    return response.choices[0].message.content