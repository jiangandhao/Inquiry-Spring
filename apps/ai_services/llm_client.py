"""
LLM客户端模块 - 用于与不同的LLM服务提供商进行通信
"""
import os
import json
import time
import logging
from typing import Dict, Any, Optional

import openai
import google.generativeai as genai
from .models import AIModel, AITaskLog

logger = logging.getLogger(__name__)

class LLMClientFactory:
    
    @staticmethod
    def create_client(model_id=None, provider=None):
        """
        创建LLM客户端
        
        Args:
            model_id: 模型ID，如果提供则直接使用该ID查找模型
            provider: 提供商名称，如果model_id未提供，则使用provider查找默认模型
            
        Returns:
            LLMClient子类的实例
        """
        try:
            # 获取模型配置
            if model_id:
                model_config = AIModel.objects.get(id=model_id, is_active=True)
            elif provider:
                model_config = AIModel.objects.get(provider=provider, is_active=True, is_default=True)
            else:
                # 获取默认模型
                try:
                    model_config = AIModel.objects.get(is_active=True, is_default=True)
                except AIModel.DoesNotExist:
                    logger.warning("找不到默认AI模型配置，使用内置Gemini客户端")
                    return GeminiClient(None)
                except Exception as e:
                    if 'no such table' in str(e).lower():
                        logger.warning("AI模型表不存在，使用内置Gemini客户端")
                        return GeminiClient(None)
                
            # 根据提供商创建对应的客户端
            if model_config.provider == 'gemini':
                return GeminiClient(model_config)
            elif model_config.provider == 'qwen':
                return QwenClient(model_config)
            elif model_config.provider == 'deepseek':
                return DeepSeekClient(model_config)
            else:
                logger.warning(f"不支持的LLM提供商: {model_config.provider}，使用内置Gemini客户端")
                return GeminiClient(None)
                
        except AIModel.DoesNotExist:
            logger.warning(f"找不到可用的模型配置. model_id={model_id}, provider={provider}，使用内置Gemini客户端")
            # 创建一个默认的Gemini客户端作为后备方案
            return GeminiClient(None)
        except Exception as e:
            if 'no such table' in str(e).lower():
                logger.warning("AI模型表不存在，使用内置Gemini客户端")
                return GeminiClient(None)
            logger.exception(f"创建LLM客户端失败: {str(e)}")
            # 出错时也返回默认客户端，而不是抛出异常
            return GeminiClient(None)


class BaseLLMClient:
    """LLM客户端基类"""
    
    def __init__(self, model_config: Optional[AIModel]):
        self.model_config = model_config
        self.model_id = model_config.model_id if model_config else "gpt-3.5-turbo"
        self.max_tokens = model_config.max_tokens if model_config else 1000
        self.temperature = model_config.temperature if model_config else 0.7
        
        # 设置API密钥和基础URL
        if model_config and model_config.api_key:
            self.api_key = model_config.api_key
        else:
            # 从环境变量获取
            self.api_key = os.environ.get("OPENAI_API_KEY", "")
            
        if model_config and model_config.api_base:
            self.api_base = model_config.api_base
        else:
            self.api_base = None
    
    def _create_task_log(self, task_type: str, input_data: Dict) -> AITaskLog:
        """创建任务日志"""
        return AITaskLog.objects.create(
            task_type=task_type,
            model=self.model_config,
            input_data=input_data,
            status='processing'
        )
    
    def _update_task_log(self, task_log: AITaskLog, output_data: Dict, 
                        status: str, tokens_used: int, 
                        processing_time: float, error_msg: str = "") -> None:
        """更新任务日志"""
        task_log.output_data = output_data
        task_log.status = status
        task_log.tokens_used = tokens_used
        task_log.processing_time = processing_time
        task_log.error_message = error_msg
        task_log.completed_at = time.time()
        task_log.save()
    
    def generate_text(self, prompt: str, system_prompt: str = None, 
                    max_tokens: int = None, temperature: float = None,
                    task_type: str = "chat") -> Dict[str, Any]:
        """
        生成文本（由子类实现）
        
        Args:
            prompt: 主提示词
            system_prompt: 系统提示词
            max_tokens: 最大生成令牌数
            temperature: 温度参数
            task_type: 任务类型
            
        Returns:
            包含生成结果的字典
        """
        raise NotImplementedError("子类必须实现此方法")


class GeminiClient(BaseLLMClient):
    """Google Gemini API客户端"""
    
    def __init__(self, model_config: Optional[AIModel]):
        super().__init__(model_config)
        
        api_key = self.api_key
        if not api_key:
            api_key = os.environ.get("GOOGLE_API_KEY", "")
            
        if not api_key:
            logger.warning("未提供Gemini API密钥，将使用模拟响应")
            self.genai = None
            return
            
        genai.configure(api_key=api_key)
        self.genai = genai
        
        # 设置默认模型ID
        if not self.model_id or self.model_id == "gemini-2.5-pro":
            self.model_id = "gemini-2.5-pro"
    
    def generate_text(self, prompt: str, system_prompt: str = None, 
                    max_tokens: int = None, temperature: float = None,
                    task_type: str = "chat") -> Dict[str, Any]:
        """使用Gemini API生成文本"""
        if not max_tokens:
            max_tokens = self.max_tokens
            
        if not temperature:
            temperature = self.temperature
            
        if not system_prompt:
            system_prompt = "你是一名资深教学问答专家。请根据用户的问题提供准确、有用的回答。"
            
        # 创建任务日志
        input_data = {
            "prompt": prompt,
            "system_prompt": system_prompt,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        task_log = self._create_task_log(task_type, input_data)
        
        start_time = time.time()
        
        try:
            if not self.genai:
                # 模拟响应，用于无API密钥的情况
                response_text = f"[Gemini模拟响应] 对于问题: {prompt}"
                tokens_used = 50
            else:
                # 配置生成参数
                generation_config = {
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                    "top_p": 0.95,
                    "top_k": 40,
                }
                
                # 合并system_prompt和prompt
                full_prompt = prompt
                if system_prompt:
                    full_prompt = f"{system_prompt}\n\n{prompt}"
                
                # 调用Gemini API
                model = self.genai.GenerativeModel(self.model_id)
                response = model.generate_content(
                    full_prompt,
                    generation_config=generation_config
                )
                
                response_text = response.text
                tokens_used = 0  # Gemini API可能不直接提供token计数
            
            # 构建结果
            result = {
                "text": response_text,
                "tokens_used": tokens_used,
                "model": self.model_id,
                "finish_reason": "stop"
            }
            
            # 更新任务日志
            processing_time = time.time() - start_time
            self._update_task_log(
                task_log, 
                {"result": result}, 
                "completed", 
                tokens_used, 
                processing_time
            )
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = str(e)
            logger.exception(f"Gemini API调用失败: {error_msg}")
            
            # 更新任务日志
            self._update_task_log(
                task_log,
                {},
                "failed",
                0,
                processing_time,
                error_msg
            )
            
            # 返回错误信息
            return {
                "error": error_msg,
                "text": "很抱歉，Gemini服务暂时不可用，请稍后再试。",
                "model": self.model_id
            }


class QwenClient(BaseLLMClient):
    """阿里云通义千问API客户端"""
    
    def __init__(self, model_config: Optional[AIModel]):
        super().__init__(model_config)
        # 设置默认模型ID
        if not self.model_id or self.model_id == "qwen-max":
            self.model_id = "qwen-max"
            
        # 通义千问使用的是OpenAI兼容接口，可直接使用openai库
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.api_base or "https://dashscope.aliyuncs.com/v1"
        )
    
    def generate_text(self, prompt: str, system_prompt: str = None, 
                    max_tokens: int = None, temperature: float = None,
                    task_type: str = "chat") -> Dict[str, Any]:
        """使用通义千问API生成文本"""
        if not max_tokens:
            max_tokens = self.max_tokens
            
        if not temperature:
            temperature = self.temperature
            
        if not system_prompt:
            system_prompt = "你是一名资深教学问答专家。请根据用户的问题提供准确、有用的回答。"
        
        # 创建任务日志
        input_data = {
            "prompt": prompt,
            "system_prompt": system_prompt,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        task_log = self._create_task_log(task_type, input_data)
        
        start_time = time.time()
        try:
            # 构建消息
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            # 调用API
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            output_text = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            # 构建结果
            result = {
                "text": output_text,
                "tokens_used": tokens_used,
                "model": self.model_id,
                "finish_reason": response.choices[0].finish_reason
            }
            
            # 更新任务日志
            processing_time = time.time() - start_time
            self._update_task_log(
                task_log, 
                {"result": result}, 
                "completed", 
                tokens_used, 
                processing_time
            )
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = str(e)
            logger.exception(f"通义千问API调用失败: {error_msg}")
            
            # 更新任务日志
            self._update_task_log(
                task_log,
                {},
                "failed",
                0,
                processing_time,
                error_msg
            )
            
            # 返回错误信息
            return {
                "error": error_msg,
                "text": "很抱歉，通义千问服务暂时不可用，请稍后再试。",
                "model": self.model_id
            }


class DeepSeekClient(BaseLLMClient):
    """DeepSeek API客户端"""
    
    def __init__(self, model_config: Optional[AIModel]):
        super().__init__(model_config)
        # 设置默认模型ID
        if not self.model_id or self.model_id == "deepseek-v3":
            self.model_id = "deepseek-v3"
            
        # DeepSeek也使用OpenAI兼容接口
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.api_base or "https://api.deepseek.com/v1"
        )
    
    def generate_text(self, prompt: str, system_prompt: str = None, 
                    max_tokens: int = None, temperature: float = None,
                    task_type: str = "chat") -> Dict[str, Any]:
        """使用DeepSeek API生成文本"""
        if not max_tokens:
            max_tokens = self.max_tokens
            
        if not temperature:
            temperature = self.temperature
            
        if not system_prompt:
            system_prompt = "你是一名资深教学问答专家。请根据用户的问题提供准确、有用的回答。"
        
        # 创建任务日志
        input_data = {
            "prompt": prompt,
            "system_prompt": system_prompt,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        task_log = self._create_task_log(task_type, input_data)
        
        start_time = time.time()
        try:
            # 构建消息
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            # 调用API
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            output_text = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            # 构建结果
            result = {
                "text": output_text,
                "tokens_used": tokens_used,
                "model": self.model_id,
                "finish_reason": response.choices[0].finish_reason
            }
            
            # 更新任务日志
            processing_time = time.time() - start_time
            self._update_task_log(
                task_log, 
                {"result": result}, 
                "completed", 
                tokens_used, 
                processing_time
            )
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = str(e)
            logger.exception(f"DeepSeek API调用失败: {error_msg}")
            
            # 更新任务日志
            self._update_task_log(
                task_log,
                {},
                "failed",
                0,
                processing_time,
                error_msg
            )
            
            # 返回错误信息
            return {
                "error": error_msg,
                "text": "很抱歉，DeepSeek服务暂时不可用，请稍后再试。",
                "model": self.model_id
            } 