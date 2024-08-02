from flask import Blueprint, jsonify, render_template
import random

particles_bp = Blueprint('particles', __name__, template_folder='templates')

@particles_bp.route('/particles')
def learn_particles():
    return render_template('learn_particles.html')

@particles_bp.route('/get_particle_question')
def get_particle_question():
    particle_exercises = [
        {
            "sentence": "わたし__がっこう__いきます。",
            "particles": ["は", "に", "が", "を", "で"],
            "correct": ["は", "に"],
            "translation": "Ich gehe zur Schule.",
        },
        {
            "sentence": "ともだち__えいが__みます。",
            "particles": ["は", "を", "が", "に", "で"],
            "correct": ["は", "を"],
            "translation": "Mein Freund sieht einen Film.",
        },
        {
            "sentence": "こうえん__あそびます。",
            "particles": ["で", "に", "を", "は", "が"],
            "correct": ["で"],
            "translation": "Ich spiele im Park.",
        },
        {
            "sentence": "にほんご__べんきょう__します。",
            "particles": ["が", "を", "は", "に", "で"],
            "correct": ["を"],
            "translation": "Ich lerne Japanisch.",
        },
        {
            "sentence": "せんせい__しつもん__します。",
            "particles": ["に", "を", "は", "が", "で"],
            "correct": ["に", "を"],
            "translation": "Ich stelle dem Lehrer eine Frage.",
        },
    ]
    return jsonify(random.choice(particle_exercises))

@particles_bp.route('/get_particle_explanations')
def get_particle_explanations():
    particle_explanations = {
        "は": "は (wa): Das ist wie ein Zeigefinger, der sagt: 'Schau mal, darüber reden wir jetzt!'",
        "が": "が (ga): Das ist wie ein Superhelden-Umhang. Es zeigt, wer die Hauptperson ist, die etwas tut.",
        "を": "を (wo): Das ist wie eine Geschenkbox. Es zeigt, was jemand bekommt oder womit jemand etwas macht.",
        "に": "に (ni): Das ist wie ein Pfeil auf einer Schatzkarte. Es zeigt, wohin jemand geht oder wem etwas gegeben wird.",
        "で": "で (de): Das ist wie ein Spielplatz. Es zeigt, wo oder womit etwas passiert.",
    }
    return jsonify(particle_explanations)