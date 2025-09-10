from prompts.prompt_builder import build_prompt
from langchain_ollama.llms import OllamaLLM

def main():
    # -----------------------------
    # 1. 构建 prompt
    # -----------------------------
    profile_name = "Yuki"
    scene_name = "cafe"
    affection_level = 1  # 对应你的 levels 配置
    prompt = build_prompt(profile_name, scene_name, affection_level)

    # -----------------------------
    # 2. 初始化模型
    # -----------------------------
    model = OllamaLLM(model="mistral", base_url="http://localhost:11434")

    # -----------------------------
    # 3. 构建 chain
    # -----------------------------
    chain = prompt | model

    # -----------------------------
    # 4. 测试用户问题
    # -----------------------------
    question = "Hello, what is the sun and moon?"
    result = chain.invoke({"question": question})

    print("===== Response =====")
    print(result)

if __name__ == "__main__":
    main()
