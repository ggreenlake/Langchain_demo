from services.ChatService import ChatService
from acfilter.acfilter import ACDetector
from acfilter.ACAutomaton import ACAutomaton

if __name__ == "__main__":
    ai = ChatService()
    Input = "你好，你会使用网购吗？"
    Ac = ACDetector()
    if Ac.has_sensitive_words(Input):
        print("Not suitable!")
    else:
        reply1 = ai.chat("wechat", 123, 1, 2, 1 , Input)
        print("AI:", reply1)