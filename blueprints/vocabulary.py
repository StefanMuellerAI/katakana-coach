from flask import Blueprint, jsonify, render_template, request
import random
from data_loader import load_json_data

vocabulary_bp = Blueprint('vocabulary', __name__, template_folder='templates')

_, _, _, _, japanese_vocabulary_conjugations = load_json_data()

@vocabulary_bp.route('/get_vocabulary_data')
def get_vocabulary_data():
    return jsonify(japanese_vocabulary_conjugations)

@vocabulary_bp.route('/vocabulary_conjugation')
def vocabulary_conjugation():
    return render_template('learn_vocabulary_conjugation.html')

@vocabulary_bp.route('/get_vocabulary_question')
def get_vocabulary_question():
    word, info = random.choice(list(japanese_vocabulary_conjugations.items()))

    if info['type'] == 'noun':
        modes = ['meaning_to_hiragana', 'hiragana_to_meaning']
    else:  # verb or adjective
        modes = ['meaning_to_hiragana', 'hiragana_to_meaning', 'present', 'past', 'negative', 'negative_past']

    mode = random.choice(modes)

    question, correct_answer = generate_vocabulary_question(mode, info)

    return jsonify({
        'question': question,
        'word': info['meaning'],
        'correct_answer': correct_answer,
        'word_type': info['type']
    })

@vocabulary_bp.route('/check_vocabulary_answer', methods=['POST'])
def check_vocabulary_answer():
    data = request.json
    user_answer = data['user_answer']
    correct_answer = data['correct_answer']

    is_correct = user_answer.strip().lower() == correct_answer.strip().lower()

    return jsonify({
        'is_correct': is_correct,
        'correct_answer': correct_answer
    })

def generate_vocabulary_question(mode, info):
    if mode == 'meaning_to_hiragana':
        question = f'Wie lautet das japanische Wort (in Hiragana) für "{info["meaning"]}" in Hiragana?'
        correct_answer = info['hiragana']
    elif mode == 'hiragana_to_meaning':
        question = f'Was bedeutet das japanische Wort "{info["hiragana"]}" auf Deutsch?'
        correct_answer = info['meaning']
    elif mode == 'present':
        question = f'Wie lautet die Gegenwartsform von "{info["meaning"]}" in Hiragana?'
        correct_answer = info['conjugations']['present']
    elif mode == 'past':
        question = f'Wie lautet die Vergangenheitsform von "{info["meaning"]}" in Hiragana?'
        correct_answer = info['conjugations']['past']
    elif mode == 'negative':
        question = f'Wie lautet die Verneinung von "{info["meaning"]}" in Hiragana?'
        correct_answer = info['conjugations']['negative']
    else:  # negative_past
        question = f'Wie lautet die verneinte Vergangenheitsform von "{info["meaning"]}" in Hiragana?'
        correct_answer = info['conjugations']['negative_past']

    return question, correct_answer

def generate_vocabulary_options(correct_answer, option_type):
    options = [correct_answer]
    while len(options) < 4:
        if option_type == 'meaning':
            option = random.choice([info['meaning'] for info in japanese_vocabulary_conjugations.values()])
        elif option_type == 'hiragana':
            option = random.choice([info['hiragana'] for info in japanese_vocabulary_conjugations.values()])
        else:  # conjugation
            random_word = random.choice(list(japanese_vocabulary_conjugations.values()))
            random_conjugation = random.choice(list(random_word['conjugations'].values()))
            option = random_conjugation

        if option not in options:
            options.append(option)

    random.shuffle(options)
    return options