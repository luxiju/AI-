from openai import OpenAI
from config import config

class LLMClient:
    _instance = None
    
    def __init__(self):
        self.client = OpenAI(
            base_url=config.LLM_BASE_URL,
            api_key=config.LLM_API_KEY
        )
        self.model = config.LLM_MODEL
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = LLMClient()
        return cls._instance
    
    def generate(self, prompt, stream=True):
        messages = [
            {
                'role': 'system',
                'content': '你是一个智能客服助手，根据提供的知识库内容回答用户问题。'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
            extra_body={
                "enable_thinking": True
            }
        )
        
        full_response = ""
        for chunk in response:
            if chunk.choices:
                content = chunk.choices[0].delta.content
                if content:
                    full_response += content
        
        if not full_response:
            raise ValueError("LLM 返回内容为空")
        
        return full_response