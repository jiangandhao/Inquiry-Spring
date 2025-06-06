from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from myApp.aichatService.getAIChatMsg import getAIChatMsg
import json
import os

aiMessage = ""

def chat(request):
    if request.method == 'POST':
        data=json.loads(request.body)
        ###############在此处处理用户指令###############
        userMessage=data['message']
        global aiMessage
        aiMessage=getAIChatMsg(userMessage)
        print(userMessage)  #检验是否正确接收用户指令
        return JsonResponse({'message':'successfully sent message'})
    elif request.method == 'GET':
        #global aiMessage
        responseDict={'AIMessage':''}
        #############在此处装入AI的回复信息##############
        print(aiMessage)
        responseDict['AIMessage']=aiMessage
#         responseDict['AIMessage']="""
# ### **创新点**
#
# 本项目在**混合RAG架构、多模式交互、微服务架构、知识库管理和应用创新**五个方面提出了一系列创新技术方案，经检索分析，核心查新点如下：
#
# #### **1. 混合RAG架构的创新设计**
# - **多维度动态检索机制**：结合**关键词检索、语义检索和知识图谱检索**，采用**动态权重调整算法**（基于查询类型和上下文自动优化权重比例），实现多源检索结果的融合与冲突消解（检索准确率提升20%以上）。
# - **知识图谱增强的语义检索**：在传统向量检索基础上，引入**知识图谱关联推理**，解决语义关联不足问题，支持**基于上下文的检索扩展**（多轮对话检索召回率提升15%）。
# - **生成-检索闭环优化**：采用**多层次提示词模板系统**（支持10+场景动态构建）、**答案验证与溯源机制**（溯源准确率≥95%），确保生成内容与原始知识的一致性。
#
# #### **2. 多模式交互的智能优化**
# - **智能问答模式**：支持**文档问答与通用问答无缝切换**，结合**问题意图识别**（准确率≥88%）和**多轮对话管理**（20轮以上上下文保持率93%），提供精准交互体验。
# - **结构化知识总结**：融合**文本摘要与知识图谱技术**，生成**层级化、关联化的知识总结**（关键概念关联覆盖率≥85%），支持粒度自定义。
# - **自适应智能测验**：基于文档内容**自动生成多样化题目**（5+题型，知识点匹配度＞90%），并采用**难度动态调整算法**（响应时间＜0.5秒）。
#
# #### **3. 微服务架构的高效实现**
# - **AI模型服务化封装**：支持**模型动态加载与版本管理**（切换时间＜1秒，回滚成功率100%），实现业务逻辑与模型解耦。
# - **高性能数据流优化**：采用**增量更新机制**（处理效率提升60%）和**实时缓存技术**（延迟＜100ms），保障系统高吞吐（10,000+请求/秒）。
#
# #### **4. 知识库管理的智能化升级**
# - **分层存储架构**（文档层、向量层、关系层）：支持**跨层关联查询**（检索效率提升35%），并实现**知识冲突检测与解决**（成功率95%）。
# - **智能文档处理**：保留文档语义结构（逻辑结构保持率＞90%），支持**10+文件格式解析**（PDF/Word/Markdown等），并自动提取元数据。
# - **动态知识图谱构建**：实现**知识点自动关联与隐含推理**（关联推理准确率85%），支持知识库的实时更新（时效性＜5分钟）。
#
# #### **5. 应用场景的创新拓展**
# - **个性化学习支持**：基于用户学习进度**智能推荐内容**（路径匹配度＞90%），并提供**实时反馈**（延迟＜200ms）。
# - **智能教学辅助**：实现**教学资源智能管理**（知识点覆盖率≥98%）和**教学策略动态调整**（响应时间＜1秒）。
# - **沉浸式学习体验**：结合**交互式界面与激励机制**，用户学习效率提升40%，满意度达4.8/5。
#
# ### **查新结论**
# 经检索分析，本项目在**混合RAG架构的动态权重调整、知识图谱增强检索、生成-溯源闭环优化、多模式交互的自适应测验、微服务化的AI模型管理、分层知识库存储及动态关联推理**等方面具有显著创新性，国内外未见相同技术组合的公开报道，具备**技术新颖性和应用先进性**。
#         """
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
        #data = json.loads(request.body)
        data=request.GET
        print(data)
        responseDict_1 = {'AIMessage':''}
        responseDict_2 = {'AIMessage': ''}
        ############# 在此处装入AI的回复信息 ###############
        responseDict_1['AIMessage'] = """
### **论文详细总结：Big Data Quality: A Survey**  
#### **1. 研究背景与动机**    
- 大数据时代下，数据量激增（如每日生成2.5 EB数据，Page 2），传统数据质量管理方法无法应对其动态性、多样性和规模（Page 1-2）。  
- 质量管理的必要性：低质量数据会导致分析结果偏差（Page 1）。  

> "Quality has been recognized by the Big Data community as an essential facet of its maturity... should be implemented at the earlier stages of its lifecycle"  
> **原文位置**：Abstract（Page 1）
---

#### **2. 大数据与数据质量基础**  
##### **2.1 大数据定义与特征**  
- **3V特性**（Volume, Velocity, Variety）：  
  - **Volume**：数据规模（如2020年达35 ZB，Page 2）。  
  - **Velocity**：实时或批处理生成（Figure 2, Page 3）。  
  - **Variety**：结构化与非结构化数据混合（Page 2）。  
- **扩展特性**：真实性（Veracity）、价值（Value）等（Page 3）。  

> "Big Data is high-volume, high-velocity and high-variety information assets"  
> **原文位置**：II.A.1 Definition（Page 2）  

##### **2.2 大数据生命周期**  
- **关键阶段**（Figure 3, Page 4）：  
  1. **数据生成**：传感器、社交媒体等（Page 3）。  
  2. **预处理**：清洗、去重、格式转换（Page 4）。  
  3. **分析**：机器学习、深度学习（Page 4）。  

> "Big Data lifecycle includes: data generation, collection, transportation, storage, preprocessing, analytics, and visualization"  
> **原文位置**：II.C（Page 3-4）  

##### **2.3 数据质量（DQ）核心概念**  
- **质量维度（DQDs）**（Figure 4, Page 5）：  
  - **内在维度**：准确性（Accuracy）、一致性（Consistency）。  
  - **上下文维度**：时效性（Timeliness）。  
- **评估方法**：通过指标（如缺失值比率）量化（Page 5）。  

> "Data quality is 'fitness for use'"  
> **原文位置**：II.D.1 Definition（Page 4） 

---

#### **3. 大数据质量管理框架**  
- **全生命周期管理**（Figure 5, Page 6）：  
  1. **数据采集**：过程驱动策略（Page 6）。  
  2. **传输与存储**：QoS保障（如带宽、容错，Page 7）。  
  3. **预处理**：清洗、集成（Page 7）。  
  4. **可视化**：工具质量评估（Page 7）。  
- **持续改进**：通过质量报告反馈（Page 7）。  

> "We propose a holistic quality management model... across the Big Data value chain"  
> **原文位置**：III（Page 5-7）

---

#### **4. 研究分类与挑战**  
- **研究分类**（Figure 6, Page 7）：  
  - **生命周期管理**（I-III）：聚焦预处理、存储（Page 8）。  
  - **质量维度**（VII-IX）：如准确性、一致性（Page 8）。  
- **关键挑战**：  
  - 缺乏实时监控工具（Page 9）。  
  - 非结构化数据质量评估困难（Page 9）。  

> "Most existing works address quality in an ad hoc manner... no comprehensive model"  
> **原文位置**：IV（Page 7-8）

---

#### **5. 未来方向**  
- **研究方向**：  
  - 动态质量指标（Page 9）。  
  - 自动化实时仪表盘（Page 9）。  
  - 标准化框架（Page 9）。  

> "Future research should develop... end-to-end quality integration"  
> **原文位置**：V（Page 9）  

---

#### **6. 结论**  
- 质量管理需贯穿全生命周期，需跨学科合作（Page 9）。  

> "Big Data quality is the key for its acceptance... conventional techniques are no longer suitable"  
> **原文位置**：VI（Page 9）  

---

**标注说明**：  
- 引用格式：`> "原文"` + **原文位置**。  
- 图表（如Figure 3）和章节（如II.C）直接对应PDF页码。  
- 关键术语（如“3V”）可在原文中快速定位。  

**论文来源**：  
- 标题：*Big Data Quality: A Survey*  
- 作者：Ikbal Taleb et al.  
- 会议：2018 IEEE International Congress on Big Data  
- DOI：10.1109/BigDataCongress.2018.00029
        """

        responseDict_2['AIMessage'] = """
### **论文详细总结：大数据科学与工程的挑战与思考**

#### **1. 研究背景与意义**  
- **数据科学的兴起**：数据分析成为继理论、实验和计算之后的**第四种科学范式**，推动经济价值和社会应用。  
  > "计算模式每隔15年发生一次变革...2010年前后催生出云计算、物联网等新兴产业平台"（Page 1）  
- **大数据时代特征**：数据量爆炸性增长，数据成为**战略资源**，美国启动“大数据研究与发展计划”。  
  > "数据量爆炸性增长（如Facebook用户超8亿）、数据成为**战略资源**，美国启动‘大数据研究与发展计划’"（Page 1-2）  

---

#### **2. 大数据的关键问题**  
##### **2.1 可表示问题**  
- **挑战**：非结构化数据（如文本、图像）缺乏统一模型，传统关系模型难以处理。  
  > "非结构化数据在互联网大数据中占比超过70%~80%...增长速度是结构化数据的10~50倍"（Page 2）  
- **解决方案**：需开发**统一数据模型**（如面向对象模型、E-R模型扩展）。  
  > "非结构化数据增长速度是结构化数据的10~50倍"（Page 3）  

##### **2.2 可处理问题**  
- **数据规模与处理需求**：传统技术无法应对大规模数据处理需求（如MapReduce优化前Facebook分析需2天）。  
  > "淘宝网每日新增交易数据达10TB...沃尔玛每小时处理100万件交易，数据量达2.5PB"（Page 2）  
- **技术方向**：采用分布式计算（如Hadoop）和实时处理（如谷歌Percolator）来处理大数据。  
  > "数据规模与处理需求：传统技术无法应对...分布式计算（如Hadoop）、实时处理（如谷歌Percolator）"（Page 4-5）  

##### **2.3 可靠性问题**  
- **数据质量**：错误、冗余、过时数据影响决策。  
  > "全球财富1000强公司中超过25%的关键数据不正确...CSDN泄露600万用户密码"（Page 3）  
- **隐私保护**：需平衡数据价值与隐私安全，采用差分隐私技术等手段保障数据安全。  
  > "错误、冗余、过时数据影响决策（如医疗数据错误率13.6%~81%）。隐私保护：需平衡数据价值与安全（如差分隐私技术）"（Page 6-7）  

---

#### **3. 核心研究方向**  
##### **3.1 海量异构数据模型与存储**  
- **模型局限**：传统关系模型、面向对象模型在表达非结构化数据时存在缺陷。  
  > "如何构建模型规范表达异构数据...现有模型无法描述复杂关系"（Page 3）  
- **存储技术**：采用分布式文件系统（如GFS、HDFS），以适应动态数据增长。  
  > "分布式文件系统（如GFS、HDFS）需适应动态数据增长"（Page 3-4）  

##### **3.2 复杂数据智能分析**  
- **图数据匹配**：子图同构、图模拟查询等算法用于社会网络分析。  
  > "图匹配是社会网络分析的核心...推荐系统需融合社交网络隐性关系"（Page 4）  
- **社交网络分析**：应用于舆情预测和社区发现（如Facebook的PUMA平台）。  
  > "舆情预测、社区发现（如Facebook的PUMA平台）"（Page 4）  

##### **3.3 大数据处理技术**  
- **批处理 vs 实时处理**：  
  - **批处理**：采用Hadoop和Hive处理批量数据。  
  > "MapReduce不擅长迭代计算...Prege和Giraph专为图数据处理设计"（Page 4-5）  
  - **实时处理**：采用NoSQL（如BigTable）、增量处理（如Percolator）进行实时数据处理。  
  > "实时处理：NoSQL（如BigTable）、增量处理（如Percolator）"（Page 5）  

##### **3.4 数据质量管理**  
- **核心问题**：处理数据的正确性、完整性、时效性和冗余问题。  
  > "数据质量研究管理数据的‘质’...需统一逻辑框架处理多类错误"（Page 5-6）  
- **挑战**：对于半结构化数据（如XML）和分布式清洗存在困难。  
  > "挑战：半结构化数据（如XML）、分布式清洗（NPC问题）"（Page 6）  

##### **3.5 安全与隐私保护**  
- **动态监控**：确保数据处理过程中的内存、进程安全（如IBM IMA框架）。  
  > "动态监控：内存、进程安全（如IBM IMA框架）"（Page 6）  
- **隐私技术**：应用差分隐私和k-匿名技术进行数据隐私保护。  
  > "差分隐私与k-匿名技术结合...社会网络隐私保护更复杂"（Page 6-7）  

---

#### **4. 未来挑战与结论**  
- **跨学科融合**：需要结合数学、计算科学等领域的知识解决数据的不确定性问题。  
  > "需结合数学、计算科学解决数据不确定性"（Page 2）  
- **标准化与实时性**：缺乏统一的框架和实时处理能力是当前的挑战。  
  > "缺乏统一框架和实时处理能力"（Page 5,7）  

---

**标注说明**：  
- 引用格式：`> "原文"` + **原文位置**（如Page 2）。  
- 图表未直接引用，但关键术语（如“3V”）可定位至对应章节。  

**论文来源**：  
- 标题：*大数据科学与工程的挑战与思考*  
- 作者：马帅、李建欣、胡春明  
- 期刊：*中国计算机学会通讯* 2012年第9期  
- 关键词：互联网、大数据
        """
        if data['fileName']=="Big_Data_Quality_A_Survey.pdf":
            return JsonResponse(responseDict_1)
        else:
            return JsonResponse(responseDict_2)


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
        q_4="""
在机器学习中，过拟合指的是模型在训练集上表现得很好，但在测试集上表现差。
        """
        q_5="""
以下哪些方法可以用于解决机器学习中的过拟合问题？（可多选）

A) 增加训练数据量

B) 使用更复杂的模型

C) 正则化

D) 提前停止（Early Stopping）
        """


        t_1=t_2="单选题"
        t_3="填空题"
        t_4="判断题"
        t_5="多选题"

        ans_1='C'
        ans_2='B'
        ans_3="卷积层；全连接层"
        ans_4="正确"
        ans_5=['A','C','D']

        ana_1="""
监督学习是机器学习中的一种方法，其中训练数据由一对一的输入数据和其对应的输出标签组成。模型通过输入数据（特征）学习到映射规则，然后可以用来预测新的数据的标签。所以，正确答案是C，训练数据包含了输入数据和输出标签。
        """
        ana_2="""
支持向量机（SVM）是一种监督学习方法，广泛用于分类任务。它通过找到最佳的超平面来区分不同类别的数据。SVM可以用于线性和非线性分类任务，常见于文本分类、图像识别等任务中。
- **线性回归** 是一种回归算法，适用于预测连续数值。
- **K均值聚类** 是一种无监督学习算法，主要用于数据聚类，而不是分类。
- **主成分分析（PCA）** 主要用于数据降维，是无监督学习方法，用于特征提取和数据压缩。
        """
        ana_3="""
- **卷积层**（Convolutional Layer）是深度学习中，尤其是在卷积神经网络（CNN）中常见的层，它通过卷积操作提取输入数据（通常是图像）的局部特征。这些特征有助于捕捉图像中的边缘、纹理、形状等低级信息。卷积层通常用于数据的初步处理和特征提取。
- **全连接层**（Fully Connected Layer, FC）位于神经网络的最后阶段，它将通过卷积层提取到的特征映射展平并通过神经元进行处理，最终生成网络的输出。在分类任务中，全连接层的输出通常会经过激活函数（如softmax）来产生最终的类别标签。
        """
        ana_4="""
过拟合是指模型在训练数据上学得过于精细，甚至包括数据中的噪声和不规则性，因此能够很好地预测训练集中的数据。然而，由于模型在训练过程中过于依赖训练数据的具体特征，它可能在新的、未见过的数据（如测试集）上表现得很差，无法泛化到新的情境。这是机器学习中常见的一个问题，通常通过正则化、交叉验证等方法来缓解。
        """
        ana_5="""
- **A) 增加训练数据量**：增加训练数据量可以帮助模型学习到更加普遍的特征，从而减少对训练集的过度拟合。更多的数据有助于模型获得更多的模式，从而提升其泛化能力。
- **B) 使用更复杂的模型**：使用更复杂的模型可能会加剧过拟合，而不是减少过拟合。复杂的模型往往会记住数据中的噪声而不是提取出通用的模式，因此不建议用复杂模型来解决过拟合问题。
- **C) 正则化**：正则化是减少过拟合的常用技术之一，它通过在损失函数中增加额外的约束（例如L1或L2正则化）来减少模型的复杂度，迫使模型找到更加简洁的解。
- **D) 提前停止（Early Stopping）**：提前停止是一种防止过拟合的方法。在训练过程中，当模型的性能在验证集上开始下降时，就停止训练。这样可以避免模型在训练集上学得过于精细，导致过拟合。
        """

        q_dict_1={"type":t_1,"question":q_1,"answer":ans_1,"analysis":ana_1}
        q_dict_2={"type":t_2,"question":q_2,"answer":ans_2,"analysis":ana_2}
        q_dict_3={"type":t_3,"question":q_3,"answer":ans_3,"analysis":ana_3}
        q_dict_4={"type":t_4,"question":q_4,"answer":ans_4,"analysis":ana_4}
        q_dict_5={"type":t_5,"question":q_5,"answer":ans_5,"analysis":ana_5}

        questions=[q_dict_1,q_dict_2,q_dict_5,q_dict_3,q_dict_4]
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