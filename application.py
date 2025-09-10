from utils.config_loader import load_yaml
from constants import CONFIG_PATH

def main():
    # 选择 dev 或 prod 配置
    config = load_yaml(CONFIG_PATH)

    print("=== Application Start ===")
    print("Loaded configuration:")
    print(config)

    # 举个例子：获取角色信息
    if "character" in config:
        print(f"Character: {config['character']['name']}")

if __name__ == "__main__":
    main()
