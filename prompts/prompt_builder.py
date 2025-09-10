from langchain_core.prompts import ChatPromptTemplate
from utils.config_loader import load_yaml

def map_affection_to_prompt(affection_level, rules_path):
    # 直接使用 load_yaml 加载文件，不要自己打开
    rules = load_yaml(rules_path)
    
    # 直接返回对应阶段的文本描述
    stage_key = f"Stage{affection_level}"
    if stage_key in rules['levels']:
        return rules['levels'][stage_key]  # 直接返回描述文本
    else:
        return "Default description"  # 或者抛出异常

def build_prompt(profile_name: str, scene_name: str, affection_level: int):
    profile = load_yaml(f"profiles/{profile_name}/profile.yaml")
    scene = load_yaml(f"profiles/{profile_name}/scenes/{scene_name}.yaml")
    affection_prompt = map_affection_to_prompt(affection_level, f"profiles/{profile_name}/affection/affection_rules.yaml")

    template = f"""{profile['base_prompt']}
Scene: {scene['scene_prompt']}
Affection State: {affection_prompt}
Question: {{question}}
Answer:"""

    return ChatPromptTemplate.from_template(template)
