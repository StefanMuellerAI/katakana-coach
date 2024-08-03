from flask import Blueprint, jsonify, render_template
import random
from data_loader import load_json_data

hiragana_bp = Blueprint('hiragana', __name__, template_folder='templates')

_, _, _, hiragana_dict, _, _ = load_json_data()

@hiragana_bp.route('/hiragana')
def learn_hiragana():
    return render_template('learn_hiragana.html')

@hiragana_bp.route('/get_hiragana_data')
def get_hiragana_data():
    selected_hiragana = random.sample(list(hiragana_dict.items()), 40)
    return jsonify(dict(selected_hiragana))