from utils.short_term_memory import ShortConversationMemoryManager
from chains.chain_builder import build_chain
from utils.long_term_memory import LongConversationMemoryManager


class ChatService:
    def __init__(self):
        self.Smemory = ShortConversationMemoryManager()
        self.Lmemory = LongConversationMemoryManager()

    def chat(self, platform: str, user_id: int, profile_name: int, scene_name: int, affection_level: int, user_input: str):
        # 1. 保存用户消息
        self.Smemory.add_message(user_id, profile_name, "user", user_input)
        self.Lmemory.save_message(platform, user_id, profile_name, "user", user_input)

        # 2. 取出短期对话历史
        history = self.Smemory.get_history(user_id, profile_name)

        # 3. 构建 chain
        chain = build_chain(user_id,profile_name, scene_name, affection_level)

        # 4. 拼 context（这里你可以后续改成 LangChain 的 memory wrapper）
        context_text = "\n".join([f"{m['role']}: {m['content']}" for m in history])
        result = chain.invoke({"question": f"{context_text}\nUser: {user_input}"})

        # 5. 保存 AI 回复
        self.Lmemory.save_message(platform, user_id, profile_name, "ai", result)
        self.Smemory.add_message(user_id, profile_name, "ai", result)

        return result
