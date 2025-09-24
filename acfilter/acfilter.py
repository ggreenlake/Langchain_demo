import pickle
from collections import deque, defaultdict
import unicodedata
import typing as t
import io

class ACDetector:
    def __init__(self, model_path = ".\\persistence\\ac_model.pkl"):
        """
        加载AC自动机模型
        Args:
            model_path: 模型文件路径
        """
        try:
            with open(model_path, 'rb') as f:
                self.automaton = pickle.load(f)
            print("AC自动机模型加载成功")
        except Exception as e:
            print(f"模型加载失败: {e}")
            self.automaton = None
    
    def has_sensitive_words(self, text):
        """
        检测文本是否包含敏感词
        Returns:
            bool: True表示包含敏感词，False表示安全
        """
        if self.automaton is None:
            print("模型未正确加载")
            return False
        
        try:
            matches = self.automaton.find_all(text)
            return len(matches) > 0
        except Exception as e:
            print(f"检测过程中出错: {e}")
            return False
    
    def get_sensitive_words(self, text):
        """
        获取文本中所有的敏感词
        Returns:
            list: 敏感词列表
        """
        if self.automaton is None:
            return []
        
        try:
            matches = self.automaton.find_all(text)
            # 提取敏感词（每个match的第三个元素是敏感词）
            sensitive_words = list(set([match[2] for match in matches]))
            return sensitive_words
        except Exception as e:
            print(f"获取敏感词列表出错: {e}")
            return []

# 为了确保pickle能正确加载，需要在这里定义ACAutomaton类
class ACAutomaton:
    def __init__(self, normalize: bool = True, case_insensitive: bool = True):
        self.trie = []
        self.out = []
        self.fail = []
        self.normalize = normalize
        self.case_insensitive = case_insensitive
        self._make_node()

    def _make_node(self):
        self.trie.append({})
        self.out.append([])
        self.fail.append(0)
        return len(self.trie) - 1

    def _norm(self, s: str) -> str:
        if self.normalize:
            s = unicodedata.normalize('NFKC', s)
        if self.case_insensitive:
            s = s.casefold()
        return s

    def add_word(self, word: str, original_word: t.Optional[str] = None):
        if not word:
            return
        w = self._norm(word)
        node = 0
        for ch in w:
            if ch not in self.trie[node]:
                nxt = self._make_node()
                self.trie[node][ch] = nxt
            node = self.trie[node][ch]
        self.out[node].append(original_word if original_word is not None else word)

    def build(self):
        q = deque()
        for ch, nxt in self.trie[0].items():
            self.fail[nxt] = 0
            q.append(nxt)
        while q:
            r = q.popleft()
            for ch, s in self.trie[r].items():
                q.append(s)
                f = self.fail[r]
                while f != 0 and ch not in self.trie[f]:
                    f = self.fail[f]
                self.fail[s] = self.trie[f].get(ch, 0)
                self.out[s].extend(self.out[self.fail[s]])

    def load_words_from_file(self, path: str, encoding: str = 'utf-8', strip: bool = True):
        with io.open(path, 'r', encoding=encoding) as f:
            for line in f:
                if strip:
                    line = line.strip()
                if not line:
                    continue
                if line.startswith('#'):
                    continue
                self.add_word(line, original_word=line)

    def iter_matches(self, text: str):
        tnorm = self._norm(text)
        node = 0
        for i, ch in enumerate(tnorm):
            while node != 0 and ch not in self.trie[node]:
                node = self.fail[node]
            node = self.trie[node].get(ch, 0)
            if self.out[node]:
                for w in self.out[node]:
                    L = len(self._norm(w))
                    yield (i - L + 1, i + 1, w)

    def find_all(self, text: str) -> t.List[t.Tuple[int,int,str]]:
        return list(self.iter_matches(text))

    def replace_with_mask(self, text: str, mask_char: str = '*', whole_word: bool = False) -> str:
        tnorm = self._norm(text)
        mask_flags = [False] * len(tnorm)
        for start, end, word in self.iter_matches(text):
            if whole_word:
                left_ok = (start == 0) or (not tnorm[start-1].isalnum())
                right_ok = (end == len(tnorm)) or (not tnorm[end].isalnum())
                if not (left_ok and right_ok):
                    continue
            for i in range(start, end):
                mask_flags[i] = True
        res_chars = []
        for i, ch in enumerate(tnorm):
            if mask_flags[i]:
                res_chars.append(mask_char)
            else:
                res_chars.append(ch)
        return ''.join(res_chars)