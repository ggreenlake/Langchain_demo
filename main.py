from services.ChatService import ChatService

if __name__ == "__main__":
    ai = ChatService()

    reply1 = ai.chat("wechat", 123, "yuki", "cafe", 1, "Well,to be honest,I have no idea to drink tea.Can you offer me a choice")
    print("AI:", reply1)

    reply2 = ai.chat("wechat", 123, "yuki", "cafe", 1, "Who am I?")
    print("AI:", reply2)
