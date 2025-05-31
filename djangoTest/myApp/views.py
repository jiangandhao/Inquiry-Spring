from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.conf import settings
import json
import os

def chat(request):
    if request.method == 'POST':
        data=json.loads(request.body)

        #在此处处理用户指令
        userMessage=data['message']
        print(userMessage)  #检验是否正确接收用户指令

        return JsonResponse({'message':'successfully sent message'})
    elif request.method == 'GET':
        responseDict={'AIMessage':''}
        #在此处装入AI的回复信息
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
        # 在下面添加处理文件的逻辑

        return HttpResponse('ok')
    elif request.method == 'GET':
        responseDict={'AIMessage':''}
        # 在此处装入AI的回复信息
        responseDict['AIMessage'] = """这是来自后端的AI总结"""

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
        #在下面添加处理文件的逻辑

    return HttpResponse('ok')