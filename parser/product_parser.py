import re
import json
from typing import Dict, List, Tuple


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    text = text.replace("O", "0").replace("S0", "50")
    text = re.sub(r"[^a-zA-Z0-9.,\- ]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_product_name(name: str) -> Tuple[str, bool]:
   
    name = name.upper()

    normalization_rules = [
        (["BANANA", "BREAD"], "BANANA BREAD"),
        (["BLACK", "BEANS"], "BLACK BEANS"),
        (["RICE", "CAKE"], "RICE CAKE BARS"),
        (["VANILLA", "CUSTARD"], "VANILLA CUSTARD"),
        (["PASSATA"], "ORGANIC PASSATA"),
        (["CLEAN", "WIPES"], "CLEANING WIPES"),
        (["BATH", "CLEAN"], "BATHROOM CLEANER"),
        (["TUCCANESE", "BANANA"], "TUCCANESE BANANA BREAD"),
    ]

    for keywords, canonical in normalization_rules:
        if all(k in name for k in keywords):
            return canonical, True

    alpha_chars = sum(c.isalpha() for c in name)
    total_chars = len(name.replace(" ", ""))

    if alpha_chars < 4 or total_chars < 6:
        return "", False

    uppercase_ratio = len(re.findall(r"[A-Z]", name)) / max(total_chars, 1)
    if uppercase_ratio < 0.4:
        return "", False

    return name.title(), True


def normalize_price(price: str) -> float:
    try:
        return float(price.replace(",", ""))
    except ValueError:
        return 0.0


def parse_single_text(text: str) -> List[Dict]:
    text = clean_text(text)
    text = " ".join(text.splitlines())

    price_pattern = re.compile(r"\d+[.,]?\d*")
    matches = list(price_pattern.finditer(text))

    products = []
    last_idx = 0
    buffer_name = ""

    for match in matches:
        raw_price = match.group()
        price = normalize_price(raw_price)

        if price <= 0 or price > 5000:
            last_idx = match.end()
            continue

        fragment = text[last_idx:match.start()].strip()
        if fragment:
            buffer_name = f"{buffer_name} {fragment}".strip()

        cleaned_name = re.sub(
            r"\b(per|pk|g|kg|litre|c|pack|packs)\b$",
            "",
            buffer_name,
            flags=re.IGNORECASE,
        ).strip()

        normalized_name, readable = normalize_product_name(cleaned_name)

        if normalized_name:
            products.append({
                "name": normalized_name,
                "price": round(price, 2),
                "readable": readable
            })

        buffer_name = ""
        last_idx = match.end()

    return products


def parse_products(raw_texts: Dict[str, str]) -> Dict[str, List[Dict]]:
    all_products = {}

    for filename, text in raw_texts.items():
        seen = {}

        for item in parse_single_text(text):
            name = item["name"]
            price = item["price"]

            if name not in seen or price > seen[name]["price"]:
                seen[name] = item

        all_products[filename] = list(seen.values())

    return all_products


def save_to_json(parsed_data, output_file="data.json"):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, indent=4, ensure_ascii=False)
