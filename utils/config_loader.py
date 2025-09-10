import yaml

def load_yaml(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise RuntimeError(f"❌ Config file not found: {path}")
    except yaml.YAMLError as e:
        raise RuntimeError(f"❌ YAML parsing error in {path}: {e}")
