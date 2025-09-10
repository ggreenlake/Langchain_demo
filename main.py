from chains.chain_builder import build_chain

def main():
    user_id = "user_001"
    profile = "yuki"
    scene = "cafe"

    # 后端告知 affection level
    affection_level = 1

    chain = build_chain(user_id, profile, scene, affection_level)

    question = "Hello, what is the sun and moon?"
    response = chain.invoke({"question": question})
    print("Q:", question)
    print("A:", response)

if __name__ == "__main__":
    main()
