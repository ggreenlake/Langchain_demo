from utils.short_term_memory import ConversationMemoryManager
from chains.chain_builder import build_chain

class ChatService:
    def __init__(self):
        self.memory = ConversationMemoryManager()

    def chat(self, platform: str, user_id: int, profile_name: str, scene_name: str, affection_level: int, user_input: str):
        # 1. 保存用户消息
        self.memory.add_message(platform, user_id, "user", user_input)

        # 2. 取出短期对话历史
        history = self.memory.get_history(platform, user_id)

        # 3. 构建 chain
        chain = build_chain(user_id,profile_name, scene_name, affection_level)

        # 4. 拼 context（这里你可以后续改成 LangChain 的 memory wrapper）
        context_text = "\n".join([f"{m['role']}: {m['content']}" for m in history])
        result = chain.invoke({"question": f"{context_text}\nUser: {user_input}"})

        # 5. 保存 AI 回复
        self.memory.add_message(platform, user_id, "ai", result)

        return result
