from prompts.prompt_builder import build_prompt
from langchain_ollama.llms import OllamaLLM
from langchain_openai import ChatOpenAI  
from config.config import Config

# 全局加载配置
cfg = Config()

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

    try:
        # 尝试使用 cfg.model 初始化

        model_conf = cfg.model
        model = OllamaLLM(
            model=model_conf["name"],
            base_url=model_conf["base_url"]
        )
    except Exception as e:
        print(f"[Warning] Ollama init failed: {e}")
        print("[Info] Falling back to Siliconflow API ...")

        # 使用 Siliconflow API
        api_conf = cfg.api
        model = ChatOpenAI(
            openai_api_key=api_conf["Siliconflow"],
            model_name=api_conf["name"],
            base_url= "https://api.siliconflow.cn/v1"
        )

    # 返回 chain
    chain = prompt | model
    return chain