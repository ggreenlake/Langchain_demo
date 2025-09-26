from services.ChatService import ChatService
from acfilter.acfilter import ACDetector
from acfilter.ACAutomaton import ACAutomaton

if __name__ == "__main__":
    ai = ChatService()
    Input = "你好，你是谁？"
    Ac = ACDetector()
    if Ac.has_sensitive_words(Input):
        print("Not suitable!")
    else:
        reply1 = ai.chat("wechat", 1223, 2, 0, 1 , Input)
        print("AI:", reply1)