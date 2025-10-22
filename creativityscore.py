from wordfreq import zipf_frequency
from collections import Counter
from tabulate import tabulate
import regex
import os
from pathlib import Path

def load_all_texts_from_folder(folder_path="txtdata"):
    texts = []
    folder = Path(__file__).parent / folder_path
    if not folder.exists():
        raise FileNotFoundError(f"📁 Folder not found:{folder}")
    
    for file in folder.glob("*.txt"):
        with file.open("r", encoding="utf-8") as f:
            texts.append(f.read())
    print(f"📄 {len(texts)} files read.")
    return "\n".join(texts)

def export_feature_words_with_proper_nouns(text, out_path="rare_words.md", top_n=None, score_threshold=1.0):
    words = regex.findall(r"\p{L}+", text.lower())
    counts = Counter(words)
    rows = []
    proper_nouns = []

    for w, c in counts.items():
        z = zipf_frequency(w, "en")
        if z == 0:
            proper_nouns.append((w, c))
            continue
        per_words = 10 ** (6 - z)
        score = per_words * c / 100
        if score < score_threshold:
            continue
        rows.append((w, c, z, per_words, score))

    # --- 特徴スコア順 ---
    rows_by_score = sorted(rows, key=lambda x: x[4], reverse=True)
    if top_n:
        rows_by_score = rows_by_score[:top_n]

    # --- 出現回数順 ---
    rows_by_count = sorted(rows, key=lambda x: x[1], reverse=True)
    if top_n:
        rows_by_count = rows_by_count[:top_n]

    # Markdown出力
    from tabulate import tabulate
    markdown = []

    markdown.append("# Top feature word scores\n")
    headers = ["No.", "word", "occurrences", "Zipf", "Appearance rate (in how many words)", "Feature Score"]
    table1 = [
        [i, w, c, f"{z:.2f}", f"{per_words:,.0f}", f"{score:.1f}"]
        for i, (w, c, z, per_words, score) in enumerate(rows_by_score, 1)
    ]
    markdown.append(tabulate(table1, headers=headers, tablefmt="github"))

    markdown.append("\n# In order of number of occurrences (ranking of frequently appearing words)\n")
    table2 = [
        [i, w, c, f"{z:.2f}", f"{per_words:,.0f}", f"{score:.1f}"]
        for i, (w, c, z, per_words, score) in enumerate(rows_by_count, 1)
    ]
    markdown.append(tabulate(table2, headers=headers, tablefmt="github"))

    markdown.append("\n# Candidates for proper nouns (not in dictionary)\n")
    if not proper_nouns:
        markdown.append("_Not found._")
    else:
        proper_nouns.sort(key=lambda x: x[1], reverse=True)
        for i, (w, c) in enumerate(proper_nouns, 1):
            markdown.append(f"{i:>3}. `{w}` （出現: {c}回）")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(markdown))
    print(f"✅ written out → {out_path}")


if __name__ == "__main__":
    text = load_all_texts_from_folder("txtdata")
    export_feature_words_with_proper_nouns(text)