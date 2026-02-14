from wordfreq import iter_wordlist

def get_word_rank(word, lang='en', wordlist='best'):
    for rank, w in enumerate(iter_wordlist(lang, wordlist), start=1):
        if w == word:
            return rank
    return "リストにありませんでした。"  # リストにないとき

# 例
while True:
    search_word = input("順位を知りたい単語を入力してください：").lower
    print(get_word_rank(search_word, "en"))