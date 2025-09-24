import pickle
from acfilter.ACAutomaton import ACAutomaton  # 从统一位置导入

class ACDetector:
    def __init__(self, model_path = "./persistence/ac_model.pkl"):
        try:
            with open(model_path, 'rb') as f:
                self.automaton = pickle.load(f)
            print("AC自动机模型加载成功")
        except Exception as e:
            print(f"模型加载失败: {e}")
            self.automaton = None
    
    def has_sensitive_words(self, text):
        if self.automaton is None:
            return False
        matches = self.automaton.find_all(text)
        return len(matches) > 0