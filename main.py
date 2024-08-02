from flask import Flask, render_template, send_from_directory
import os
from data_loader import load_json_data
from blueprints.katakana import katakana_bp
from blueprints.kanji import kanji_bp
from blueprints.hiragana import hiragana_bp
from blueprints.particles import particles_bp
from blueprints.vocabulary import vocabulary_bp

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load JSON data
japanese_dict, japanese_words, kanji_list, hiragana_dict, japanese_vocabulary_conjugations = load_json_data()

app.register_blueprint(katakana_bp)
app.register_blueprint(kanji_bp)
app.register_blueprint(hiragana_bp)
app.register_blueprint(particles_bp)
app.register_blueprint(vocabulary_bp)

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
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)