from services.ChatService import ChatService

if __name__ == "__main__":
    ai = ChatService()

    reply1 = ai.chat("wechat", 123, 1, 1, 1, "Hello, I am Sam.Can you tell me who you are?")
    print("AI:", reply1)

    reply2 = ai.chat("wechat", 123, 1, 1, 1, "Thank you very much.")
    print("AI:", reply2)
    