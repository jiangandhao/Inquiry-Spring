from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.conf import settings
import json
import os

def chat(request):
    if request.method == 'POST':
        data=json.loads(request.body)

        ###############在此处处理用户指令###############
        userMessage=data['message']
        print(userMessage)  #检验是否正确接收用户指令

        return JsonResponse({'message':'successfully sent message'})
    elif request.method == 'GET':
        responseDict={'AIMessage':''}
        #############在此处装入AI的回复信息##############
        responseDict['AIMessage']='这是来自后端的AI回复'

        return JsonResponse(responseDict)


def summarize(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get('file')
        print(uploaded_file)

        # 设置保存路径
        upload_path = os.path.join(settings.BASE_DIR, 'myApp', 'static', 'uploadfiles', uploaded_file.name)
        # 将文件保存到指定路径
        with open(upload_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
        ############# 在下面添加处理文件的逻辑 #############

        return HttpResponse('ok')
    elif request.method == 'GET':
        responseDict={'AIMessage':''}
        ############# 在此处装入AI的回复信息 ###############
        responseDict['AIMessage'] = """
        这是来自后端的AI总结
        1) ...
        2) ...
        """

        return JsonResponse(responseDict)


def test(request):
    if request.method == "POST" and request.FILES.get('file'):
        uploaded_file = request.FILES.get('file')
        print(uploaded_file)

        # 设置保存路径
        upload_path = os.path.join(settings.BASE_DIR, 'myApp', 'static', 'uploadfiles', uploaded_file.name)
        # 将文件保存到指定路径
        with open(upload_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
        ############# 在下面添加处理文件的逻辑 #############

        return HttpResponse('ok')

    elif request.method == 'POST':
        data=json.loads(request.body)
        ############### 在下面处理用户的信息 #############
        testNum=data['num']
        testType=data['type']
        testLevel=data['level']
        testDescription=data['desc']
        print(testNum,testType,testLevel,testDescription)

        #############在此处装入AI生成的测试题目##############
        responseDict={'AIQuestion':[]}

        q_1="""
        在监督学习中，训练数据包含了哪些信息？
A) 仅包含输入数据
B) 仅包含输出标签
C) 输入数据和对应的输出标签
D) 仅包含输入数据的特征
            """
        q_2="""
        哪个机器学习算法主要用于分类任务？
A) 线性回归
B) 支持向量机（SVM）
C) K均值聚类
D) 主成分分析（PCA）
        """
        q_3="""
        在深度学习中，______层用于提取数据的特征，而______层用于生成最终的输出。
        """
        t_1=t_2="选择题"
        t_3="填空题"

        q_dict_1={"type":t_1,"question":q_1}
        q_dict_2={"type":t_2,"question":q_2}
        q_dict_3={"type":t_3,"question":q_3}

        questions=[q_dict_1,q_dict_2,q_dict_3]
        responseDict['AIQuestion'] = questions

        return JsonResponse(responseDict)



def fileUpload(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get('file')
        print(uploaded_file)

        # 设置保存路径
        upload_path = os.path.join(settings.BASE_DIR, 'myApp', 'static', 'uploadfiles', uploaded_file.name)
        # 将文件保存到指定路径
        with open(upload_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
        ################ 在下面添加处理文件的逻辑 #############

    return HttpResponse('ok')