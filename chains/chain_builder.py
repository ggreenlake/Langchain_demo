from prompts.prompt_builder import build_prompt
from langchain_ollama.llms import OllamaLLM
from langchain_openai import ChatOpenAI  
from config.config import Config
import socket

# 全局加载配置
cfg = Config()


def is_port_open(host: str, port: int) -> bool:
    """检查 Ollama 服务是否在运行"""
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except OSError:
        return False

def build_chain(user_id, profile_name, scene_name, affection_level):
    """
    构建 LangChain Chain：
    - profile_name: 角色
    - scene_name: 场景
    - affection_level: 后端传来的亲密度等级
    """
    # 生成 prompt
    prompt = build_prompt(profile_name, scene_name, affection_level)
    model = None
    model_conf = cfg.model
    # 如果 Ollama 可用 → 优先用 Ollama
    if is_port_open(model_conf["base_url"].replace("http://", "").split(":")[0],
                    int(model_conf["base_url"].split(":")[-1])):
        print("[Info] Using Ollama backend")
        model = OllamaLLM(
            model=model_conf["name"],
            base_url=model_conf["base_url"]
        )
    else:
        print("[Warning] Ollama not available, falling back to SiliconFlow")
        api_conf = cfg.api
        model = ChatOpenAI(
            api_key=api_conf["Siliconflow"],
            model=api_conf["name"],
            base_url="https://api.siliconflow.cn/v1"
        )
    # 返回 chain
    chain = prompt | model
    return chain