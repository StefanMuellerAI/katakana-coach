from flask import Flask, render_template, jsonify, send_from_directory
import os
import json
import random

app = Flask(__name__, static_folder='static')

# Load JSON files
with open('static/japanese_dict.json', 'r', encoding='utf-8') as f:
    japanese_dict = json.load(f)

with open('static/japanese_words.json', 'r', encoding='utf-8') as f:
    japanese_words = json.load(f)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/impressum')
def impressum():
    return render_template('impressum.html')

@app.route('/datenschutz')
def datenschutz():
    return render_template('datenschutz.html')

@app.route('/')
def index():
    return render_template('learn_katakana.html')

@app.route('/get_question')
def get_question():
    # Define modes and their weights
    modes = ['katakana_to_romanji', 'romanji_to_katakana', 'katakana_to_hiragana', 'hiragana_to_katakana', 'word_to_romanji']
    weights = [1, 1, 1, 1, 2]  # 'word_to_romanji' has weight 2, others have weight 1

    # Choose a mode based on the weights
    mode = random.choices(modes, weights=weights, k=1)[0]

    if mode == 'word_to_romanji':
        katakana_word, (romanji_word, german_translation) = random.choice(list(japanese_words.items()))
        print(katakana_word, romanji_word, german_translation)
        return jsonify({
            'mode': mode,
            'question': katakana_word,
            'correct_answer': romanji_word,
            'german_translation': german_translation
        })
    else:
        katakana, info = random.choice(list(japanese_dict.items()))
        hiragana = info['hiragana']
        romanji = info['romanji']
        example = info['example']

        if mode == 'katakana_to_romanji':
            question = katakana
            correct_answer = romanji
            options = [romanji]
            while len(options) < 3:
                option = random.choice([info['romanji'] for info in japanese_dict.values()])
                if option not in options:
                    options.append(option)
        elif mode == 'romanji_to_katakana':
            question = romanji
            correct_answer = katakana
            options = [katakana]
            while len(options) < 3:
                option = random.choice(list(japanese_dict.keys()))
                if option not in options:
                    options.append(option)
        elif mode == 'katakana_to_hiragana':
            question = katakana
            correct_answer = hiragana
            options = [hiragana]
            while len(options) < 3:
                option = random.choice([info['hiragana'] for info in japanese_dict.values()])
                if option not in options:
                    options.append(option)
        else:  # hiragana_to_katakana
            question = hiragana
            correct_answer = katakana
            options = [katakana]
            while len(options) < 3:
                option = random.choice(list(japanese_dict.keys()))
                if option not in options:
                    options.append(option)

        random.shuffle(options)

        return jsonify({
            'mode': mode,
            'question': question,
            'options': options,
            'correct_answer': correct_answer,
            'example': example
        })


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)