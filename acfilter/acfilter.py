from .ACAutomaton import ACAutomaton  # 从统一位置导入
import os

class ACDetector:
    def __init__(self, word_file: str = "./persistence/sensitive words.txt"):
        self.word_file = word_file
        self.automaton = ACAutomaton(normalize=True, case_insensitive=True)
        self._build()

    def _build(self):
        if not os.path.exists(self.word_file):
            raise FileNotFoundError(f"敏感词表文件不存在: {self.word_file}")
        # 加载并构建
        self.automaton.load_words_from_file(self.word_file, encoding="utf-8")
        self.automaton.build()
        print("✅ AC 自动机构建完成")

    def has_sensitive_words(self, text: str) -> bool:
        """检测文本是否包含敏感词"""
        matches = self.automaton.find_all(text)
        return len(matches) > 0

    def find_sensitive_words(self, text: str):
        """返回所有匹配到的敏感词"""
        return [w for _, _, w in self.automaton.find_all(text)]