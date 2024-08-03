from flask import Blueprint, jsonify, render_template, request
import random
from data_loader import load_json_data

kanji_bp = Blueprint('kanji', __name__, template_folder='templates')

_, _, kanji_list, _, _, sentence_list = load_json_data()


@kanji_bp.route('/kanji')
def learn_kanji():
    return render_template('learn_kanji.html')


@kanji_bp.route('/get_kanji_question')
def get_kanji_question():
    modes = ['kanji_to_hiragana', 'deutsch_to_kanji', 'hiragana_to_kanji', 'hiragana_to_deutsch', 'deutsch_to_hiragana', 'sentence_completion']
    weights = [1, 1, 1, 1, 1, 2]  # Höhere Gewichtung für sentence_completion
    mode = random.choices(modes, weights=weights, k=1)[0]

    if mode == 'sentence_completion':
        sentence = random.choice(sentence_list)
        return jsonify({
            'mode': mode,
            'question': sentence['japanese'],
            'correct_answer': sentence['kanji'],
            'german': sentence['german'],
            'level': sentence['level'],
            'tooltip': sentence['tooltip'],
            'hint': "Ziehen Sie die Kanji in die Lücken",
            'kanji': sentence['kanji']  # Fügen Sie dies hinzu
        })
    else:
        return generate_standard_question(mode)


def generate_standard_question(mode):
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


def generate_sentence_completion_question():
    sentence = random.choice(sentence_list)

    return jsonify({
        'mode': 'sentence_completion',
        'question': sentence['japanese'],
        'correct_answer': sentence['kanji'],
        'german': sentence['german'],
        'level': sentence['level'],
        'hint': "Ziehen Sie die Kanji in die Lücken"
    })


@kanji_bp.route('/check_kanji_answer', methods=['POST'])
def check_kanji_answer():
    data = request.json
    user_answer = data['user_answer']
    correct_answer = data['correct_answer']
    mode = data['mode']

    if mode == 'sentence_completion':
        is_correct = set(user_answer) == set(correct_answer)
    elif mode in ['hiragana_to_deutsch', 'deutsch_to_hiragana']:
        is_correct = user_answer.lower().strip() == correct_answer.lower().strip()
    else:
        is_correct = user_answer == correct_answer

    feedback = get_feedback(is_correct, user_answer, correct_answer, mode)

    return jsonify({
        'is_correct': is_correct,
        'correct_answer': correct_answer,
        'feedback': feedback
    })


def get_feedback(is_correct, user_answer, correct_answer, mode):
    if is_correct:
        return "Richtig! Gut gemacht!"
    elif mode == 'sentence_completion':
        correct_kanji = set(correct_answer)
        user_kanji = set(user_answer)
        missing = correct_kanji - user_kanji
        extra = user_kanji - correct_kanji
        feedback = "Fast richtig! "
        if missing:
            feedback += f"Du hast diese Kanji vergessen: {', '.join(missing)}. "
        if extra:
            feedback += f"Diese Kanji gehören nicht in den Satz: {', '.join(extra)}."
        return feedback.strip()
    else:
        return f"Leider falsch. Die richtige Antwort ist: {correct_answer}"


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
    attempts = 0
    max_attempts = 50  # Vermeidet endlose Schleifen

    while len(options) < 3 and attempts < max_attempts:
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

        attempts += 1

    random.shuffle(options)
    return options
