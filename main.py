from services.ChatService import ChatService
from acfilter.acfilter import ACDetector
from acfilter.build import ACAutomation

if __name__ == "__main__":
    ai = ChatService()
    Input = "Hello, I am Sam.Can you tell me who you are?"
    Ac = ACDetector()
    print(Ac(Input))
    # reply1 = ai.chat("wechat", 123, 1, 2, 1 , Input)
    # print("AI:", reply1)