from flask import Blueprint, jsonify, render_template
import random
from data_loader import load_json_data

katakana_bp = Blueprint('katakana', __name__, template_folder='templates')

japanese_dict, japanese_words, _, _, _, _ = load_json_data()

@katakana_bp.route('/katakana')
def learn_katakana():
    return render_template('learn_katakana.html')

@katakana_bp.route('/get_question')
def get_question():
    modes = ['katakana_to_romanji', 'romanji_to_katakana', 'katakana_to_hiragana', 'hiragana_to_katakana', 'word_to_romanji']
    weights = [1, 1, 1, 1, 2]
    mode = random.choices(modes, weights=weights, k=1)[0]

    if mode == 'word_to_romanji':
        katakana_word, (romanji_word, german_translation) = random.choice(list(japanese_words.items()))
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

        question, correct_answer, options = generate_katakana_question(mode, katakana, hiragana, romanji)

        return jsonify({
            'mode': mode,
            'question': question,
            'options': options,
            'correct_answer': correct_answer,
            'example': example
        })

def generate_katakana_question(mode, katakana, hiragana, romanji):
    if mode == 'katakana_to_romanji':
        return katakana, romanji, generate_options(romanji, 'romanji')
    elif mode == 'romanji_to_katakana':
        return romanji, katakana, generate_options(katakana, 'katakana')
    elif mode == 'katakana_to_hiragana':
        return katakana, hiragana, generate_options(hiragana, 'hiragana')
    else:  # hiragana_to_katakana
        return hiragana, katakana, generate_options(katakana, 'katakana')

def generate_options(correct_answer, option_type):
    options = [correct_answer]
    while len(options) < 3:
        if option_type == 'romanji':
            option = random.choice([info['romanji'] for info in japanese_dict.values()])
        elif option_type == 'katakana':
            option = random.choice(list(japanese_dict.keys()))
        else:  # hiragana
            option = random.choice([info['hiragana'] for info in japanese_dict.values()])
        if option not in options:
            options.append(option)
    random.shuffle(options)
    return options