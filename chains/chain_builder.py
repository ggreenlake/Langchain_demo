from prompts.prompt_builder import build_prompt
from langchain_ollama.llms import OllamaLLM
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

    # 初始化模型
    model_conf = cfg.model
    model = OllamaLLM(
        model=model_conf["name"],
        base_url=model_conf["base_url"]
    )

    # 返回 chain
    chain = prompt | model
    return chain
