"""
RAG引擎模块 - 负责文档处理、向量化、检索和生成
"""
import logging
import json
import re
import time
from typing import List, Dict, Any, Optional

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings # 也可以选择 OpenAIEmbeddings
from langchain.chains import RetrievalQA

from apps.documents.models import Document, DocumentChunk
from .llm_client import LLMClientFactory
from .prompt_manager import PromptManager
from apps.quiz.models import Quiz, Question

logger = logging.getLogger(__name__)

class RAGEngine:
    # RAG引擎，用于处理文档和生成答案
    
    def __init__(self, document_id: int = None, llm_client = None):
        self.document = None
        self.document_chunks = []
        self.vector_store = None
        
        if document_id:
            try:
                self.document = Document.objects.get(id=document_id)
                self.document_chunks = list(self.document.chunks.all())
            except Document.DoesNotExist:
                logger.error(f"文档ID {document_id} 不存在.")
                # 可以选择抛出异常或允许在没有文档的情况下初始化

        # 初始化LLM客户端
        self.llm_client = llm_client if llm_client else LLMClientFactory.create_client()
        
        # 初始化嵌入模型 (这里使用OpenAI，也可以替换为本地模型如sentence-transformers)
        # 需要确保OPENAI_API_KEY已设置
        self.embeddings = SentenceTransformerEmbeddings()
        
        # 如果文档已处理，则加载向量存储
        if self.document and self.document.is_processed and self.document_chunks:
            self._load_vector_store()

    def _split_document(self, content: str, chunk_size: int = 1000, chunk_overlap: int = 100) -> List[str]:
        """将文档内容分割成文本块"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
        chunks = text_splitter.split_text(content)
        return chunks

    def process_and_embed_document(self, force_reprocess: bool = False) -> bool:
        """处理并嵌入文档"""
        if not self.document:
            logger.error("未加载文档，无法处理。")
            return False

        if self.document.is_processed and not force_reprocess:
            logger.info(f"文档 {self.document.title} 已处理，跳过。")
            if not self.vector_store:
                self._load_vector_store()
            return True

        try:
            logger.info(f"开始处理文档: {self.document.title}")
            
            # 1. 获取文档内容 (优先使用文件内容，其次是文本内容字段)
            doc_content = ""
            if self.document.file:
                try:
                    doc_content = self.document.file.read().decode('utf-8')
                except Exception as e:
                    logger.error(f"读取文件内容失败: {e}")
                    doc_content = self.document.content # 后备方案
            else:
                doc_content = self.document.content
            
            if not doc_content:
                logger.error(f"文档 {self.document.title} 内容为空，无法处理。")
                return False

            # 2. 分割文档
            text_chunks = self._split_document(doc_content)
            if not text_chunks:
                logger.error(f"文档 {self.document.title} 分块失败。")
                return False

            # 3. 清理旧的文档分块 (如果存在)
            self.document.chunks.all().delete()
            self.document_chunks = []

            # 4. 创建并存储DocumentChunk对象
            chunk_objects = []
            current_char_offset = 0
            for i, chunk_text in enumerate(text_chunks):
                chunk_obj = DocumentChunk(
                    document=self.document,
                    content=chunk_text,
                    chunk_index=i,
                    start_char=current_char_offset,
                    end_char=current_char_offset + len(chunk_text) -1
                )
                chunk_objects.append(chunk_obj)
                current_char_offset += len(chunk_text)
            
            DocumentChunk.objects.bulk_create(chunk_objects)
            self.document_chunks = list(self.document.chunks.all())
            logger.info(f"文档 {self.document.title} 分块完成，共 {len(self.document_chunks)} 块。")

            # 5. 创建或更新向量存储
            # 使用Chroma作为示例，可以替换为其他向量数据库
            # 注意：Chroma的持久化需要指定路径
            # persist_directory = f"./vector_store/{self.document.id}"
            # os.makedirs(persist_directory, exist_ok=True)
            # self.vector_store = Chroma.from_documents(
            #     documents=[chunk.content for chunk in self.document_chunks],
            #     embedding=self.embeddings,
            #     ids=[str(chunk.id) for chunk in self.document_chunks], # 使用DocumentChunk的ID
            #     persist_directory=persist_directory
            # )
            # self.vector_store.persist()
            
            # 对于Chroma的内存版本（无持久化，适合简单场景或测试）：
            self.vector_store = Chroma.from_texts(
                texts=[chunk.content for chunk in self.document_chunks],
                embedding=self.embeddings,
                ids=[str(chunk.id) for chunk in self.document_chunks] # 使用DocumentChunk的ID作为向量ID
            )
            logger.info(f"文档 {self.document.title} 向量化完成。")

            # 6. 更新文档状态
            self.document.is_processed = True
            self.document.save()
            
            return True

        except Exception as e:
            logger.exception(f"处理文档 {self.document.title} 失败: {e}")
            self.document.is_processed = False # 出错时标记为未处理
            self.document.save()
            return False

    def _load_vector_store(self):
        """从已处理的文档分块加载向量存储"""
        if not self.document or not self.document.is_processed or not self.document_chunks:
            logger.warning("无法加载向量存储：文档未处理或分块为空。")
            return

        try:
            logger.info(f"加载文档 {self.document.title} 的向量存储...")
            # persist_directory = f"./vector_store/{self.document.id}"
            # if os.path.exists(persist_directory):
            #     self.vector_store = Chroma(persist_directory=persist_directory, embedding_function=self.embeddings)
            # else:
            #     logger.warning(f"持久化向量存储目录 {persist_directory} 不存在，重新创建内存向量库")
            #     # 如果持久化目录不存在，可能需要重新嵌入，或者这里抛出错误
            #     self.process_and_embed_document(force_reprocess=True)
            #     return
            
            # 内存版本加载
            if self.document_chunks:
                 self.vector_store = Chroma.from_texts(
                    texts=[chunk.content for chunk in self.document_chunks],
                    embedding=self.embeddings,
                    ids=[str(chunk.id) for chunk in self.document_chunks]
                )
                 logger.info(f"文档 {self.document.title} 内存向量存储加载完成。")
            else:
                logger.warning(f"文档 {self.document.title} 没有分块，无法加载向量存储。")

        except Exception as e:
            logger.exception(f"加载向量存储失败: {e}")
            self.vector_store = None # 加载失败则清空

    def retrieve_relevant_chunks(self, query: str, top_k: int = 3) -> List[DocumentChunk]:
        """根据查询检索相关的文档分块"""
        if not self.vector_store:
            logger.warning("向量存储未初始化，无法检索。")
            # 尝试加载或处理文档
            if self.document and not self.document.is_processed:
                success = self.process_and_embed_document()
                if not success or not self.vector_store:
                    return []
            elif self.document and self.document.is_processed and not self.vector_store:
                 self._load_vector_store()
                 if not self.vector_store:
                     return []
            else:
                return []

        try:
            # Langchain Chroma 返回的是 Langchain Document 对象
            retrieved_langchain_docs = self.vector_store.similarity_search_with_score(query, k=top_k)
            
            relevant_chunk_ids = []
            # Langchain Document 对象的 metadata 中默认没有我们存储的 chunk.id
            # Chroma.from_texts(ids=...) 会将id存储在Chroma内部，但similarity_search返回的Document对象page_content是文本，metadata是空的
            # 需要调整向量存储创建或检索方式以获取原始DocumentChunk ID

            # 简单的解决方法：如果ids参数在Chroma.from_texts时被正确用作唯一标识符，
            # 并且返回的Document的page_content与我们的chunk.content一致，可以反向查找
            # 但这不是最高效的。更优的做法是确保检索时能拿到ID。
            # LangChain的Chroma包装器可能不直接暴露原始ID，这取决于其实现细节。

            # 假设 self.vector_store.similarity_search 返回包含原始ID的元数据，或能通过其他方式获取ID
            # 修正：Chroma的 `similarity_search` 返回的 `Document` 对象列表，其 `metadata` 字段可以包含额外信息。
            # 如果在 `Chroma.from_texts` 或 `Chroma.from_documents` 时，`metadatas` 参数被正确提供，
            # 我们可以从中提取原始 `DocumentChunk` 的ID。
            # 我们在创建时用的是 ids 参数，这个参数是用来给向量数据库内部使用的，不一定会直接出现在返回的 metadata 里。

            # 让我们在创建Chroma实例时，将chunk_id也加入到metadata中：
            # process_and_embed_document 和 _load_vector_store 中的 Chroma.from_texts 需要修改：
            # metadatas = [{'chunk_id': str(chunk.id), 'document_id': str(self.document.id)} for chunk in self.document_chunks]
            # self.vector_store = Chroma.from_texts(..., metadatas=metadatas)
            # 这样，retrieved_langchain_docs[i].metadata['chunk_id'] 就可以用了。
            # 当前代码没有传递 metadatas，所以这里先基于内容匹配来查找，或者后续修改 Chroma 创建部分。

            # 临时的基于内容查找（效率较低，仅作演示，后续应优化 Chroma 创建方式）
            retrieved_chunks = []
            for lc_doc, score in retrieved_langchain_docs:
                # lc_doc 是 Langchain 的 Document 对象, lc_doc.page_content 是文本
                # 尝试从数据库中通过内容匹配找回 DocumentChunk (效率不高)
                # 注意：这假设了文本块内容是唯一的，实际中可能需要更可靠的ID映射
                try:
                    # 我们在Chroma创建时传入了 ids=[str(chunk.id) ...]
                    # 如果 Chroma 按照 LangChain 的标准实现，其内部应该是用这些ID的。
                    # 但 similarity_search 返回的 Document 对象的元数据可能不包含它。
                    # 我们需要确认 LangChain Chroma 如何处理ids参数和返回。
                    
                    # 优先：如果检索结果的元数据中能找到原始ID (需要修改Chroma创建部分)
                    # chunk_id = lc_doc.metadata.get('chunk_id') 
                    # if chunk_id:
                    #    chunk = DocumentChunk.objects.get(id=chunk_id)
                    #    retrieved_chunks.append(chunk)
                    #    continue

                    # 后备：基于内容的慢速查找 (如果上面ID方案未实现)
                    # 这是一个简化的例子，实际中内容可能不完全精确匹配，且效率低
                    matched_chunk = next((c for c in self.document_chunks if c.content == lc_doc.page_content), None)
                    if matched_chunk:
                        retrieved_chunks.append(matched_chunk)
                    else:
                        logger.warning(f"无法从检索结果中匹配回原始DocumentChunk: {lc_doc.page_content[:100]}...")
                except DocumentChunk.DoesNotExist:
                    logger.warning(f"检索到的chunk ID在数据库中不存在 (这不应该发生如果ID正确传递和使用)")
                except Exception as e:
                    logger.error(f"从检索结果映射回DocumentChunk时出错: {e}")
            
            logger.info(f"为查询 '{query}' 检索到 {len(retrieved_chunks)} 个相关分块。")
            return retrieved_chunks
        
        except Exception as e:
            logger.exception(f"检索相关分块失败: {e}")
            return []

    def generate_answer(self, query: str, relevant_chunks: List[DocumentChunk]) -> Dict[str, Any]:
        """根据查询和相关文档块生成答案"""
        if not relevant_chunks:
            # 如果没有相关文档，可以直接调用LLM进行通用回答，或返回特定提示
            logger.info("没有检索到相关文档，尝试通用回答。")
            # 可以选择使用一个特定的"无上下文"提示词模板
            prompt = PromptManager.render_by_type(
                template_type='chat_response', 
                variables={'query': query, 'reference_text': '没有可用的特定上下文信息。'}
            )
        else:
            context_text = "\n\n---\n\n".join([chunk.content for chunk in relevant_chunks])
            prompt_variables = {
                'query': query,
                'reference_text': context_text
            }
            prompt = PromptManager.render_by_type(
                template_type='chat_response', 
                variables=prompt_variables
            )

        # 使用LLM客户端生成答案
        # TODO: 传递system_prompt (如果需要，可以从PromptManager获取)
        response = self.llm_client.generate_text(prompt=prompt, task_type='chat')
        
        # 可以在这里添加答案的后处理逻辑，比如提取引用等
        response['retrieved_chunks'] = [
            {'id': chunk.id, 'content': chunk.content[:200] + "..."} for chunk in relevant_chunks
        ]
        
        return response

    def answer_query(self, query: str, top_k_retrieval: int = 3) -> Dict[str, Any]:
        """处理用户查询，包括检索和生成"""
        if not self.document and not self.vector_store:
             # 非文档模式，直接调用LLM
            logger.info(f"非文档模式回答查询: {query}")
            prompt = PromptManager.render_by_type(
                template_type='chat_response', 
                variables={'query': query, 'reference_text': '通用知识库'}
            )
            response = self.llm_client.generate_text(prompt=prompt, task_type='chat')
            response['retrieved_chunks'] = []
            return response

        # 1. 确保文档已处理和向量库已加载
        if self.document and not self.document.is_processed:
            success = self.process_and_embed_document()
            if not success:
                return {"error": "文档处理失败", "text": "抱歉，处理您的文档时遇到问题。"}
        elif self.document and self.document.is_processed and not self.vector_store:
            self._load_vector_store()
            if not self.vector_store:
                 return {"error": "向量库加载失败", "text": "抱歉，加载文档知识库时遇到问题。"}

        # 2. 检索相关文档块
        relevant_chunks = self.retrieve_relevant_chunks(query, top_k=top_k_retrieval)
        
        # 3. 生成答案
        answer_response = self.generate_answer(query, relevant_chunks)
        
        return answer_response

    def generate_quiz(self, question_count: int = 5, question_types: List[str] = None, difficulty: str = 'medium') -> Dict[str, Any]:
        """为当前文档生成测验
        
        Args:
            question_count: 生成题目的数量
            question_types: 题目类型列表，可包含 'MC'(单选), 'MCM'(多选), 'TF'(判断), 'FB'(填空), 'SA'(简答)
            difficulty: 难度级别，'easy'=简单，'medium'=中等，'hard'=困难, 'master'=极难
            
        Returns:
            包含生成测验结果的字典
        """
        if not self.document:
            return {"error": "未加载文档，无法生成测验。"}
        
        if not self.document.is_processed:
            success = self.process_and_embed_document()
            if not success:
                return {"error": "文档处理失败，无法生成测验。"}

        # 获取文档完整内容
        doc_content = self.document.content
        if self.document.file:
            try:
                doc_content = self.document.file.read().decode('utf-8')
            except Exception:
                pass # 使用数据库中的content作为后备
        
        if not question_types:
            question_types = ['MC', 'TF'] # 默认单选题和判断题
        
        # 确保所有题型有效
        valid_types = ['MC', 'MCM', 'TF', 'FB', 'SA']
        question_types = [t for t in question_types if t in valid_types]
        
        if not question_types:
            question_types = ['MC'] # 如果没有有效题型，默认使用单选题
        
        prompt_variables = {
            'content': doc_content,
            'question_count': question_count,
            'question_types': ", ".join(question_types), # LLM可能更喜欢字符串形式
            'difficulty': difficulty
        }
        
        prompt = PromptManager.render_by_type(
            template_type='quiz_generation', 
            variables=prompt_variables
        )
        
        # 调用LLM生成测验题目
        response = self.llm_client.generate_text(prompt=prompt, task_type='quiz_generation')
        
        # 解析LLM返回的JSON格式题目，并存入数据库 (Question模型)
        # 这里需要健壮的JSON解析和错误处理
        try:
            # 尝试从LLM响应中提取JSON部分
            text_response = response.get("text", "")
            json_str = text_response
            
            # 如果响应包含```json和```标记，提取其中的内容
            json_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
            json_match = re.search(json_pattern, text_response)
            if json_match:
                json_str = json_match.group(1)
            
            quiz_data = json.loads(json_str)
            
            # 验证和规范化每个题目的格式
            processed_quiz_data = []
            for i, question in enumerate(quiz_data):
                # 确保必要字段存在
                if 'content' not in question or 'type' not in question or 'correct_answer' not in question:
                    logger.warning(f"题目 #{i+1} 缺少必要字段，将被跳过")
                    continue
                    
                # 规范化题目类型
                q_type = question['type'].upper()
                if q_type not in valid_types:
                    logger.warning(f"题目 #{i+1} 类型无效: {q_type}，将被设为MC")
                    q_type = 'MC'
                
                # 验证选项（选择题）
                if q_type in ['MC', 'MCM'] and ('options' not in question or not isinstance(question['options'], list)):
                    logger.warning(f"题目 #{i+1} 选项格式无效，将被跳过")
                    continue
                
                # 验证答案格式
                correct_answer = question['correct_answer']
                if q_type == 'MC' and not isinstance(correct_answer, str):
                    logger.warning(f"题目 #{i+1} 单选题答案格式无效，将被跳过")
                    continue
                elif q_type == 'MCM' and not isinstance(correct_answer, list):
                    # 尝试将可能的字符串答案转换为列表
                    if isinstance(correct_answer, str):
                        try:
                            correct_answer = json.loads(correct_answer)
                        except:
                            # 如果是逗号分隔的字符串，也尝试转换
                            if ',' in correct_answer:
                                correct_answer = [a.strip() for a in correct_answer.split(',')]
                            else:
                                logger.warning(f"题目 #{i+1} 多选题答案格式无效，将被跳过")
                                continue
                    else:
                        logger.warning(f"题目 #{i+1} 多选题答案格式无效，将被跳过")
                        continue
                
                # 更新题目并添加到处理后的列表
                question['type'] = q_type
                if q_type == 'MCM':
                    question['correct_answer'] = correct_answer  # 已处理为列表
                
                processed_quiz_data.append(question)
            
            # 更新响应中的quiz_data
            response['quiz_data'] = processed_quiz_data
            
            quiz_obj = Quiz.objects.create(
                document=self.document,
                title=f"{self.document.title} 测验",
                description=f"基于文档《{self.document.title}》自动生成的测验",
                difficulty_level=difficulty,
                total_questions=len(processed_quiz_data),
                config={
                    'question_types': question_types,
                    'question_count': question_count,
                    'generated_time': time.time()
                }
            )
            
            for q_data in processed_quiz_data:
                Question.objects.create(
                    quiz=quiz_obj,
                    content=q_data['content'],
                    question_type=q_data['type'],
                    options=q_data.get('options', None),
                    correct_answer=q_data['correct_answer'],
                    explanation=q_data.get('explanation', ''),
                    source_passage=q_data.get('source_passage', ''),
                    difficulty=q_data.get('difficulty', difficulty),
                    order=i + 1
                )
            
            response['quiz_id'] = quiz_obj.id
            
        except json.JSONDecodeError as e:
            logger.error(f"解析测验题目JSON失败: {e}. LLM原始输出: {response.get('text')}")
            response['error'] = f"解析测验题目失败: {str(e)}"
            response['quiz_data'] = []
        except Exception as e:
            logger.exception(f"处理测验数据时出错: {e}")
            response['error'] = f"处理测验数据时出错: {str(e)}"
            response['quiz_data'] = []
            
        return response

    def generate_summary(self) -> Dict[str, Any]:
        """为当前文档生成摘要"""
        if not self.document:
            return {"error": "未加载文档，无法生成摘要。"}

        doc_content = self.document.content
        if self.document.file:
            try:
                doc_content = self.document.file.read().decode('utf-8')
            except Exception:
                pass
                
        prompt = PromptManager.render_by_type(
            template_type='summary',
            variables={'content': doc_content}
        )
        
        response = self.llm_client.generate_text(prompt=prompt, task_type='summary')
        return response

    def generate_explanation(self, question_content: str, user_wrong_answer: str, correct_answer: str) -> Dict[str, Any]:
        """为错误答案生成解释"""
        if not self.document:
            # 也可以允许在没有文档上下文的情况下生成通用解释
            # 或者要求必须有文档上下文
            logger.warning("未加载文档，生成的解释可能不包含特定上下文。")
            doc_content_for_explanation = "通用知识。"
        else:
            doc_content_for_explanation = self.document.content
            if self.document.file:
                try:
                    doc_content_for_explanation = self.document.file.read().decode('utf-8')
                except Exception:
                    pass # 使用数据库中的content

        prompt_variables = {
            'content': doc_content_for_explanation, # 学习材料原文
            'question': question_content,
            'wrong_answer': user_wrong_answer,
            'correct_answer': correct_answer
        }
        
        prompt = PromptManager.render_by_type(
            template_type='explanation',
            variables=prompt_variables
        )
        
        response = self.llm_client.generate_text(prompt=prompt, task_type='explanation')
        return response

# 可以在这里添加一些辅助函数，例如初始化默认模板等
def initialize_ai_services():
    """初始化AI服务，例如创建默认的提示词模板"""
    try:
        from django.db import connection
        from .prompt_manager import PromptManager
        
        # 检查表是否存在
        table_names = connection.introspection.table_names()
        if 'ai_services_prompttemplate' not in table_names:
            logger.warning("提示词模板表不存在，跳过创建默认模板")
            return
            
        # 创建默认提示词模板
        PromptManager.create_default_templates()
        logger.info("AI服务初始化完成，默认提示词模板已检查/创建。")
    except Exception as e:
        if 'no such table' in str(e).lower():
            logger.warning("AI服务相关表不存在，跳过初始化")
        else:
            logger.exception(f"初始化AI服务时出错: {str(e)}") 