from wordfreq import zipf_frequency,iter_wordlist
from collections import Counter
from tabulate import tabulate
import regex
import os
from pathlib import Path

def build_rank_dict(lang="en", wordlist="best", max_rank=600_000):
    """
    wordfreq の頻度リストから
    word -> rank の辞書を作る
    """
    rank_dict = {}
    for rank, w in enumerate(iter_wordlist(lang, wordlist), start=1):
        rank_dict[w] = rank
        if rank >= max_rank:
            break
    return rank_dict

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

def print_progress(current, total, bar_len=30):
    ratio = current / total
    filled = int(bar_len * ratio)
    bar = "█" * filled + "░" * (bar_len - filled)
    print(f"\r🔄 Progress: |{bar}| {ratio*100:5.1f}% ({current}/{total})", end="")

def export_feature_words_with_proper_nouns(
    text,
    out_path="rare_words.md",
    top_n=None,
    score_threshold=1.0,
    min_occurrences=2,
    word_rank=None,   # ← 追加
):
    words = regex.findall(r"\p{L}+", text.lower())
    counts = Counter(words)
    rows = []
    one_time_words = []
    proper_nouns = []
    total_words = len(counts)

    for i, (w, c) in enumerate(counts.items(), 1):
        if i % 200 == 0 or i == total_words:
            print_progress(i, total_words)
    print()

    for w, c in counts.items():
        z = zipf_frequency(w, "en")
        rank = word_rank.get(w) if word_rank else None
        if z == 0 and (not word_rank or w not in word_rank):
            proper_nouns.append((w, c))
            continue
        per_words = 10 ** (6 - z)
        score = per_words * c / 100
        if score < score_threshold:
            continue
        if c < min_occurrences:
            one_time_words.append((w, c, z, rank, per_words, score))
            continue
        rows.append((w, c, z, rank, per_words, score))

    # 並べ替え
    rows_by_score = sorted(rows, key=lambda x: x[4], reverse=True)
    rows_by_count = sorted(rows, key=lambda x: x[1], reverse=True)
    one_time_words.sort(key=lambda x: x[3], reverse=True)
    proper_nouns.sort(key=lambda x: x[1], reverse=True)

    if top_n:
        rows_by_score = rows_by_score[:top_n]
        rows_by_count = rows_by_count[:top_n]
        one_time_words = one_time_words[:top_n]

    headers = [
        "No.",
        "word",
        "occurrences",
        "Zipf",
        "Rank",
        "Appearance rate (in how many words)",
        "Feature Score",
    ]

    def make_table(rows):
        return tabulate(
            [
                [
                    i,
                    w,
                    c,
                    f"{z:.2f}",
                    rank if rank else "—",
                    f"{per_words:,.0f}",
                    f"{score:.1f}",
                ]
                for i, (w, c, z, rank, per_words, score) in enumerate(rows, 1)
            ],
            headers=headers,
            tablefmt="github"
    )


    # Markdown 組み立て
    md = []
    md.append(f"# Top feature word score (occurrence {min_occurrences} times or more)\n")
    md.append(make_table(rows_by_score))
    md.append(f"\n# Occurrence of upper bound (more than {min_occurrences} occurrences)\n")
    md.append(make_table(rows_by_count))
    md.append("\n# One-time rare award (one appearance only)\n")
    if one_time_words:
        md.append(make_table(one_time_words))
    else:
        md.append("N/A")
    md.append("\n# Proper nouns (dictionary unrecorded)Candidates\n")
    if proper_nouns:
        for i, (w, c) in enumerate(proper_nouns, 1):
            md.append(f"{i:>3}. `{w}` （出現: {c}回）")
    else:
        md.append("_Not found._")

    # 書き出し
    os.makedirs(Path(out_path).parent, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"✅ Written out. → {out_path}")

if __name__ == "__main__":
    print("📊 Building word rank dictionary...")
    WORD_RANK = build_rank_dict(max_rank=600_000)

    text = load_all_texts_from_folder("txtdata")
    export_feature_words_with_proper_nouns(text, word_rank=WORD_RANK)