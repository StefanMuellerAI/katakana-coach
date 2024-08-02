from flask import Blueprint, jsonify, render_template, request
import random
from data_loader import load_json_data

kanji_bp = Blueprint('kanji', __name__, template_folder='templates')

_, _, kanji_list, _, _ = load_json_data()

@kanji_bp.route('/kanji')
def learn_kanji():
    return render_template('learn_kanji.html')

@kanji_bp.route('/get_kanji_question')
def get_kanji_question():
    modes = ['kanji_to_hiragana', 'deutsch_to_kanji', 'hiragana_to_kanji', 'hiragana_to_deutsch', 'deutsch_to_hiragana']
    mode = random.choice(modes)

    kanji_entry = random.choice(kanji_list)
    word = list(kanji_entry.keys())[0]
    info = kanji_entry[word]

    question, correct_answer, options = generate_kanji_question(mode, word, info)

    return jsonify({
        'mode': mode,
        'question': question,
        'options': options,
        'correct_answer': correct_answer,
        'kanji': word,
        'hiragana': info['hiragana'],
        'meaning': info['bedeutung'],
        'hint': info['hint'],
        'example': f"{word} - {info['hiragana']} - {info['bedeutung']}"
    })

@kanji_bp.route('/check_kanji_answer', methods=['POST'])
def check_kanji_answer():
    data = request.json
    user_answer = data['user_answer']
    correct_answer = data['correct_answer']
    mode = data['mode']

    is_correct = False
    if mode in ['hiragana_to_deutsch', 'deutsch_to_hiragana']:
        is_correct = user_answer.lower().strip() == correct_answer.lower().strip()
    else:
        is_correct = user_answer == correct_answer

    return jsonify({
        'is_correct': is_correct,
        'correct_answer': correct_answer
    })

def generate_kanji_question(mode, word, info):
    if mode == 'kanji_to_hiragana':
        return word, info['hiragana'], generate_kanji_options(info['hiragana'], 'hiragana')
    elif mode == 'deutsch_to_kanji':
        return info['bedeutung'], word, generate_kanji_options(word, 'kanji')
    elif mode == 'hiragana_to_kanji':
        return info['hiragana'], word, generate_kanji_options(word, 'kanji')
    elif mode == 'hiragana_to_deutsch':
        return info['hiragana'], info['bedeutung'], []
    else:  # deutsch_to_hiragana
        return info['bedeutung'], info['hiragana'], []

def generate_kanji_options(correct_answer, option_type):
    options = [correct_answer]
    while len(options) < 3:
        random_entry = random.choice(kanji_list)
        random_word = list(random_entry.keys())[0]
        random_info = random_entry[random_word]

        if option_type == 'kanji':
            option = random_word
        elif option_type == 'hiragana':
            option = random_info['hiragana']
        else:  # bedeutung
            option = random_info['bedeutung']

        if option not in options:
            options.append(option)

    random.shuffle(options)
    return options