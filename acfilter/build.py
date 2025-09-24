import pickle
from acfilter.ACAutomaton import ACAutomaton  # 从统一位置导入

if __name__ == "__main__":
    ac = ACAutomaton(normalize=True, case_insensitive=True)
    ac.load_words_from_file("C:\\Users\\Sherl\\Desktop\\sensitive words.txt", encoding="utf-8")
    ac.build()
    
    with open("ac_model.pkl", "wb") as f:
        pickle.dump(ac, f)