from services.ChatService import ChatService

if __name__ == "__main__":
    ai = ChatService()

    reply1 = ai.chat("wechat", "u123", "yuki", "cafe", 1, "Hi, who are you?")
    print("AI:", reply1)

    reply2 = ai.chat("wechat", "u123", "yuki", "cafe", 1, "Do you like tea?")
    print("AI:", reply2)
