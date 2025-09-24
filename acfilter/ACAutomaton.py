from collections import deque, defaultdict
import unicodedata
import typing as t
import io
import pickle

class ACAutomaton:
    def __init__(self, normalize: bool = True, case_insensitive: bool = True):
        """
        normalize: 是否对输入和敏感词做 unicode 归一化（NFKC）
        case_insensitive: 是否对大小写不敏感（使用 .casefold()）
        """
        self.trie = []  # nodes: list of dict(char->next_index)
        self.out = []   # out[i] = list of words ending at node i
        self.fail = []  # fail links
        self._make_node()  # root = 0
        self.normalize = normalize
        self.case_insensitive = case_insensitive

    def _make_node(self):
        self.trie.append({})    # transitions
        self.out.append([])     # output words at this node
        self.fail.append(0)
        return len(self.trie) - 1

    def _norm(self, s: str) -> str:
        if self.normalize:
            s = unicodedata.normalize('NFKC', s)
        if self.case_insensitive:
            s = s.casefold()
        return s

    def add_word(self, word: str, original_word: t.Optional[str] = None):
        """Add a single word to the trie. original_word is stored for reporting (keeps original case)."""
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
        """Build failure links (BFS)."""
        q = deque()
        # init depth 1 nodes: fail -> root(0)
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
                # merge outputs
                self.out[s].extend(self.out[self.fail[s]])

    def load_words_from_file(self, path: str, encoding: str = 'utf-8', strip: bool = True):
        """
        Load words from a text file. Each line is one word/phrase.
        Empty lines and lines starting with # (comments) are ignored.
        """
        with io.open(path, 'r', encoding=encoding) as f:
            for line in f:
                if strip:
                    line = line.strip()
                if not line:
                    continue
                if line.startswith('#'):
                    continue
                # Keep original word as stored version for reporting
                self.add_word(line, original_word=line)

    def iter_matches(self, text: str):
        """
        Iterate matches as tuples: (start_index, end_index_exclusive, matched_original_word)
        Indexes correspond to the positions in the normalized & casefolded text.
        """
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
        """Return list of matches (start, end, word)."""
        return list(self.iter_matches(text))

    def replace_with_mask(self, text: str, mask_char: str = '*', whole_word: bool = False) -> str:
        """
        Replace detected sensitive substrings with mask_char repeated to keep length.
        whole_word: if True, only replace matches that are whole words (non-word neighbors).
        Note: whole_word detection is done on the normalized/casefolded string and checks unicode "word" via isalnum.
        """
        tnorm = self._norm(text)
        mask_flags = [False] * len(tnorm)

        for start, end, word in self.iter_matches(text):
            if whole_word:
                left_ok = (start == 0) or (tnorm[start-1].isalnum() == False)
                right_ok = (end == len(tnorm)) or (tnorm[end].isalnum() == False)
                if not (left_ok and right_ok):
                    continue
            for i in range(start, end):
                mask_flags[i] = True

        # Reconstruct result but preserve original string lengths and combining characters:
        # We will map mask_flags over the normalized string; to preserve user-visible characters
        # we will mask based on grapheme-like units by iterating original string and normalized through simple index alignment.
        # Simpler approach: operate on normalized string and return masked normalized text (sufficient in many cases).
        # If preserving exact original visual form is needed, a more complex mapping is required.
        res_chars = []
        for i, ch in enumerate(tnorm):
            if mask_flags[i]:
                res_chars.append(mask_char)
            else:
                res_chars.append(ch)
        return ''.join(res_chars)
