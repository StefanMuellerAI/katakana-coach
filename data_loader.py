import json

def load_json_data():
    with open('static/japanese_dict.json', 'r', encoding='utf-8') as f:
        japanese_dict = json.load(f)

    with open('static/japanese_words.json', 'r', encoding='utf-8') as f:
        japanese_words = json.load(f)

    with open('static/kanji_dict.json', 'r', encoding='utf-8') as f:
        kanji_list = json.load(f)

    with open('static/hiragana_dict.json', 'r', encoding='utf-8') as f:
        hiragana_dict = json.load(f)

    with open('static/japanese_vocabulary_conjugations.json', 'r', encoding='utf-8') as f:
        japanese_vocabulary_conjugations = json.load(f)

    with open('static/kanji_sentences.json', 'r', encoding='utf-8') as file:
        kanji_sentences = json.load(file)

    return japanese_dict, japanese_words, kanji_list, hiragana_dict, japanese_vocabulary_conjugations, kanji_sentences