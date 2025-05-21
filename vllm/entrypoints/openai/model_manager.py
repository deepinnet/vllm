import asyncio
from typing import Dict, Optional

from vllm.engine.protocol import EngineClient

class ModelManager:
    """全局模型管理器，用于管理所有已加载的模型实例"""
    _instance = None
    _models: Dict[str, EngineClient] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def get_instance(cls) -> 'ModelManager':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def add_model(self, model_name: str, model: EngineClient):
        """添加一个模型实例到管理器"""
        self._models[model_name] = model
    
    async def get_model(self, model_name: str, wait: bool = True, retry_interval: int = 2) -> Optional[EngineClient]:
        """获取指定名称的模型实例
        
        Args:
            model_name: 模型名称
            wait: 是否等待模型加载完成
            retry_interval: 重试间隔时间(秒)
            
        Returns:
            Optional[EngineClient]: 模型实例，如果未找到则返回 None
        """
        if not wait:
            return self._models.get(model_name)
            
        print("开始等待模型加载...")
        attempt = 1
        while True:
            try:
                print(f"尝试获取模型实例 (尝试 {attempt})...")
                llm = self._models.get(model_name)
                if llm is not None:
                    print(f"模型已成功加载，尝试次数: {attempt}")
                    return llm
            except Exception as e:
                print(f"获取模型实例失败: {str(e)}")
            print(f"等待模型加载中... (尝试 {attempt})")
            await asyncio.sleep(retry_interval)
            attempt += 1
    
    def list_models(self) -> list[str]:
        """列出所有已加载的模型名称"""
        return list(self._models.keys())
    
    def remove_model(self, model_name: str):
        """移除指定名称的模型实例"""
        if model_name in self._models:
            del self._models[model_name] 