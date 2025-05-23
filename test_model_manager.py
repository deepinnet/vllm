import asyncio
import uvloop
from vllm.entrypoints.openai.api_server import run_server
from vllm.entrypoints.openai.cli_args import make_arg_parser, validate_parsed_serve_args
from vllm.utils import FlexibleArgumentParser
from vllm.sampling_params import SamplingParams
from vllm.entrypoints.openai.model_manager import ModelManager

# 获取全局模型管理器实例
model_manager = ModelManager.get_instance()

class TestModelManager:
    def __init__(self):
        self.model_name = "/root/yunteng_dev/llms/modelscope/Qwen/Qwen2.5-VL-7B-Instruct"
        self.port = 8102
        
    async def start_server(self):
        """启动 vLLM 服务器"""
        print("开始启动服务器...")
        parser = FlexibleArgumentParser()
        parser = make_arg_parser(parser)
        
        args = parser.parse_args([
            "--model", self.model_name,
            "--tensor-parallel-size", "1",
            "--gpu-memory-utilization", "0.9",
            "--port", str(self.port),
            "--trust-remote-code"
        ])
        
        print("参数解析完成，开始验证参数...")
        validate_parsed_serve_args(args)
        print("参数验证完成，开始创建服务器任务...")
        # 在后台运行服务器
        self.server_task = asyncio.create_task(run_server(args))
        print("服务器任务已创建")
        
    async def test_model_operations(self):
        """测试模型管理器的各种操作"""
        # 1. 获取模型实例（等待加载完成）
        llm = await model_manager.get_model(self.model_name)
        if llm is None:
            print(f"模型 {self.model_name} 未加载")
            return
            
        print(f"成功获取模型: {self.model_name}")
        
        # 2. 列出所有已加载的模型
        loaded_models = model_manager.list_models()
        print(f"已加载的模型: {loaded_models}")
        
        # 3. 使用模型进行推理
        sampling_params = SamplingParams(
            temperature=0.7,
            top_p=0.95,
            max_tokens=100
        )
        
        try:
            async for output in llm.generate(
                prompt="你好，请介绍一下你自己",
                sampling_params=sampling_params,
                request_id="test_request_1"
            ):
                if output.finished:
                    print(f"模型输出: {output.outputs[0].text}")
        except Exception as e:
            print(f"推理过程出错: {e}")
            
    async def wait_for_model_ready(self, retry_interval=2):
        """等待模型加载完成"""
        print("开始等待模型加载...")
        attempt = 1
        while True:
            try:
                print(f"尝试获取模型实例 (尝试 {attempt})...")
                llm = model_manager.get_model(self.model_name)
                if llm is not None:
                    print(f"模型已成功加载，尝试次数: {attempt}")
                    return True
            except Exception as e:
                print(f"获取模型实例失败: {str(e)}")
            print(f"等待模型加载中... (尝试 {attempt})")
            await asyncio.sleep(retry_interval)
            attempt += 1

    async def run_tests(self):
        """运行所有测试"""
        try:
            # 启动服务器
            print("正在启动服务器...")
            await self.start_server()
            
            # 运行模型操作测试
            print("\n开始测试模型操作...")
            await self.test_model_operations()
            
        except Exception as e:
            print(f"测试过程出错: {e}")
        finally:
            # 清理资源
            print("\n清理资源...")
            if hasattr(self, 'server_task'):
                self.server_task.cancel()
                try:
                    await self.server_task
                except asyncio.CancelledError:
                    pass
            if self.model_name in model_manager._models:
                model_manager.remove_model(self.model_name)
                print(f"已移除模型: {self.model_name}")

def main():
    test = TestModelManager()
    # uvloop.run(test.run_tests())
    asyncio.run(test.run_tests())

if __name__ == "__main__":
    main() 