import random
import json
import os

def load_items():
    path = os.path.join(os.path.dirname(__file__), "items.json")
    with open(path) as f:
        return json.load(f)

def generate_pool(seed: int, n: int = 15) -> list:
    items = load_items()
    rng = random.Random(seed)
    n = min(n, len(items))
    return rng.sample(items, n)
