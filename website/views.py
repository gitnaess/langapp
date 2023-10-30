from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for,current_app
from flask_login import login_required, current_user
from .models import Question, Note, QuizResult, Answered, Answeredagg  # Import QuizResult along with Note
from . import db
import json
import random
from flask import session
from sqlalchemy import func
import stripe

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # Fetch data from Answeredagg for the current user
    user_answer_data = Answeredagg.query.filter_by(user_id=current_user.id).all()

    it_imp_sco = 0
    it_fut_sco = 0
    it_con_sco = 0
    it_imt_sco = 0
    it_sub_sco = 0
    it_pas_sco = 0

    de_imp_sco = 0
    de_fut_sco = 0
    de_con_sco = 0
    de_imt_sco = 0
    de_sub_sco = 0
    de_pas_sco = 0

    fr_imp_sco = 0
    fr_fut_sco = 0
    fr_con_sco = 0
    fr_imt_sco = 0
    fr_sub_sco = 0
    fr_pas_sco = 0

    en_imp_sco = 0
    en_fut_sco = 0
    en_con_sco = 0
    en_imt_sco = 0
    en_sub_sco = 0
    en_pas_sco = 0

    es_imp_sco = 0
    es_fut_sco = 0
    es_con_sco = 0
    es_imt_sco = 0
    es_sub_sco = 0
    es_pas_sco = 0

# italian

    it_imp_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="it", qtype="imperfect").scalar()
    it_imp_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="it", qtype="imperfect").scalar()
    if it_imp_tot != None:
       it_imp_sco = it_imp_tot / 5 + it_imp_cor
    if it_imp_cor < 10:
        it_imp_abc = "Just getting started"
    elif it_imp_cor < 20:
        it_imp_abc = "Hey, this is not bad"
    elif it_imp_cor < 50:
        it_imp_abc = "Still some way to go"
    elif it_imp_cor < 90:
        it_imp_abc = "Closer to the goal every day"

    it_con_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="it", qtype="conditional").scalar()
    it_con_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="it", qtype="conditional").scalar()
    if it_con_tot != None:
       it_con_sco = it_con_tot / 5 + it_con_cor
    if it_con_cor < 10:
        it_con_abc = "Just getting started"
    elif it_con_cor < 20:
        it_con_abc = "Hey, this is not bad"
    elif it_con_cor < 50:
        it_con_abc = "Still some way to go"
    elif it_con_cor < 90:
        it_con_abc = "Closer to the goal every day"       

    it_fut_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="it", qtype="future").scalar()
    it_fut_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="it", qtype="future").scalar()
    if it_fut_tot != None:
       it_fut_sco = it_fut_tot / 5 + it_fut_cor


    it_pas_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="it", qtype="passato prossimo").scalar()
    it_pas_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="it", qtype="passato prossimo").scalar()
    if it_pas_tot != None:
       it_pas_sco = it_pas_tot / 5 + it_pas_cor


    it_imt_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="it", qtype="imperativo").scalar()
    it_imt_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="it", qtype="imperativo").scalar()
    if it_imt_tot != None:
       it_imt_sco = it_imt_tot / 5 + it_imt_cor


    it_sub_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="it", qtype="subjunctive").scalar()
    it_sub_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="it", qtype="subjunctive").scalar()
    if it_sub_tot != None:
       it_sub_sco = it_sub_tot / 5 + it_sub_cor


# german

    de_imp_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="de", qtype="imperfect").scalar()
    de_imp_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="de", qtype="imperfect").scalar()
    if de_imp_tot != None:
       de_imp_sco = de_imp_tot / 5 + de_imp_cor

    de_con_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="de", qtype="conditional").scalar()
    de_con_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="de", qtype="conditional").scalar()
    if de_con_tot != None:
       de_con_sco = de_con_tot / 5 + de_con_cor

    de_fut_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="de", qtype="future").scalar()
    de_fut_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="de", qtype="future").scalar()
    if de_fut_tot != None:
       de_fut_sco = de_fut_tot / 5 + de_fut_cor


    de_pas_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="de", qtype="passato prossimo").scalar()
    de_pas_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="de", qtype="passato prossimo").scalar()
    if de_pas_tot != None:
       de_pas_sco = de_pas_tot / 5 + de_pas_cor


    de_imt_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="de", qtype="imperativo").scalar()
    de_imt_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="de", qtype="imperativo").scalar()
    if de_imt_tot != None:
       de_imt_sco = de_imt_tot / 5 + de_imt_cor


    de_sub_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="de", qtype="subjunctive").scalar()
    de_sub_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="de", qtype="subjunctive").scalar()
    if de_sub_tot != None:
       de_sub_sco = de_sub_tot / 5 + de_sub_cor


# french

    fr_imp_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="fr", qtype="imperfect").scalar()
    fr_imp_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="fr", qtype="imperfect").scalar()
    if fr_imp_tot != None:
       fr_imp_sco = fr_imp_tot / 5 + fr_imp_cor

    fr_con_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="fr", qtype="conditional").scalar()
    fr_con_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="fr", qtype="conditional").scalar()
    if fr_con_tot != None:
       fr_con_sco = fr_con_tot / 5 + fr_con_cor

    fr_fut_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="fr", qtype="future").scalar()
    fr_fut_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="fr", qtype="future").scalar()
    if fr_fut_tot != None:
       fr_fut_sco = fr_fut_tot / 5 + fr_fut_cor


    fr_pas_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="fr", qtype="passato prossimo").scalar()
    fr_pas_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="fr", qtype="passato prossimo").scalar()
    if fr_pas_tot != None:
       fr_pas_sco = fr_pas_tot / 5 + fr_pas_cor


    fr_imt_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="fr", qtype="imperativo").scalar()
    fr_imt_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="fr", qtype="imperativo").scalar()
    if fr_imt_tot != None:
       fr_imt_sco = fr_imt_tot / 5 + fr_imt_cor


    fr_sub_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="fr", qtype="subjunctive").scalar()
    fr_sub_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="fr", qtype="subjunctive").scalar()
    if fr_sub_tot != None:
       fr_sub_sco = fr_sub_tot / 5 + fr_sub_cor


# english

    en_imp_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="en", qtype="imperfect").scalar()
    en_imp_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="en", qtype="imperfect").scalar()
    if en_imp_tot != None:
       en_imp_sco = en_imp_tot / 5 + en_imp_cor

    en_con_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="en", qtype="conditional").scalar()
    en_con_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="en", qtype="conditional").scalar()
    if en_con_tot != None:
       en_con_sco = en_con_tot / 5 + en_con_cor

    en_fut_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="en", qtype="future").scalar()
    en_fut_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="en", qtype="future").scalar()
    if en_fut_tot != None:
       en_fut_sco = en_fut_tot / 5 + en_fut_cor


    en_pas_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="en", qtype="passato prossimo").scalar()
    en_pas_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="en", qtype="passato prossimo").scalar()
    if en_pas_tot != None:
       en_pas_sco = en_pas_tot / 5 + en_pas_cor


    en_imt_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="en", qtype="imperativo").scalar()
    en_imt_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="en", qtype="imperativo").scalar()
    if en_imt_tot != None:
       en_imt_sco = en_imt_tot / 5 + en_imt_cor


    en_sub_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="en", qtype="subjunctive").scalar()
    en_sub_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="en", qtype="subjunctive").scalar()
    if en_sub_tot != None:
       en_sub_sco = en_sub_tot / 5 + en_sub_cor


# spanish

    es_imp_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="es", qtype="imperfect").scalar()
    es_imp_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="es", qtype="imperfect").scalar()
    if es_imp_tot != None:
       es_imp_sco = es_imp_tot / 5 + es_imp_cor

    es_con_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="es", qtype="conditional").scalar()
    es_con_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="es", qtype="conditional").scalar()
    if es_con_tot != None:
       es_con_sco = es_con_tot / 5 + es_con_cor

    es_fut_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="es", qtype="future").scalar()
    es_fut_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="es", qtype="future").scalar()
    if es_fut_tot != None:
       es_fut_sco = es_fut_tot / 5 + es_fut_cor


    es_pas_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="es", qtype="passato prossimo").scalar()
    es_pas_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="es", qtype="passato prossimo").scalar()
    if es_pas_tot != None:
       es_pas_sco = es_pas_tot / 5 + es_pas_cor


    es_imt_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="es", qtype="imperativo").scalar()
    es_imt_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="es", qtype="imperativo").scalar()
    if es_imt_tot != None:
       es_imt_sco = es_imt_tot / 5 + es_imt_cor


    es_sub_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="es", qtype="subjunctive").scalar()
    es_sub_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="es", qtype="subjunctive").scalar()
    if es_sub_tot != None:
       es_sub_sco = es_sub_tot / 5 + es_sub_cor

       
    return render_template("home.html", user=current_user, user_answer_data=user_answer_data, 
                           it_imp_tot=it_imp_tot, it_imp_cor=it_imp_cor, it_imp_sco=it_imp_sco,
                           it_fut_tot=it_fut_tot, it_fut_cor=it_fut_cor, it_fut_sco=it_fut_sco,
                           it_sub_tot=it_sub_tot, it_sub_cor=it_sub_cor, it_sub_sco=it_sub_sco,
                           it_imt_tot=it_imt_tot, it_imt_cor=it_imt_cor, it_imt_sco=it_imt_sco,
                           it_pas_tot=it_pas_tot, it_pas_cor=it_pas_cor, it_pas_sco=it_pas_sco,
                           it_con_tot=it_con_tot, it_con_cor=it_con_cor, it_con_sco=it_con_sco,
                           de_imp_tot=de_imp_tot, de_imp_cor=de_imp_cor, de_imp_sco=de_imp_sco,
                           de_fut_tot=de_fut_tot, de_fut_cor=de_fut_cor, de_fut_sco=de_fut_sco,
                           de_sub_tot=de_sub_tot, de_sub_cor=de_sub_cor, de_sub_sco=de_sub_sco,
                           de_imt_tot=de_imt_tot, de_imt_cor=de_imt_cor, de_imt_sco=de_imt_sco,
                           de_pas_tot=de_pas_tot, de_pas_cor=de_pas_cor, de_pas_sco=de_pas_sco,
                           de_con_tot=de_con_tot, de_con_cor=de_con_cor, de_con_sco=de_con_sco,
                           fr_imp_tot=fr_imp_tot, fr_imp_cor=fr_imp_cor, fr_imp_sco=fr_imp_sco,
                           fr_fut_tot=fr_fut_tot, fr_fut_cor=fr_fut_cor, fr_fut_sco=fr_fut_sco,
                           fr_sub_tot=fr_sub_tot, fr_sub_cor=fr_sub_cor, fr_sub_sco=fr_sub_sco,
                           fr_imt_tot=fr_imt_tot, fr_imt_cor=fr_imt_cor, fr_imt_sco=fr_imt_sco,
                           fr_pas_tot=fr_pas_tot, fr_pas_cor=fr_pas_cor, fr_pas_sco=fr_pas_sco,
                           fr_con_tot=fr_con_tot, fr_con_cor=fr_con_cor, fr_con_sco=fr_con_sco,
                           en_imp_tot=en_imp_tot, en_imp_cor=en_imp_cor, en_imp_sco=en_imp_sco,
                           en_fut_tot=en_fut_tot, en_fut_cor=en_fut_cor, en_fut_sco=en_fut_sco,
                           en_sub_tot=en_sub_tot, en_sub_cor=en_sub_cor, en_sub_sco=en_sub_sco,
                           en_imt_tot=en_imt_tot, en_imt_cor=en_imt_cor, en_imt_sco=en_imt_sco,
                           en_pas_tot=en_pas_tot, en_pas_cor=en_pas_cor, en_pas_sco=en_pas_sco,
                           en_con_tot=en_con_tot, en_con_cor=en_con_cor, en_con_sco=en_con_sco,
                           es_imp_tot=es_imp_tot, es_imp_cor=es_imp_cor, es_imp_sco=es_imp_sco,
                           es_fut_tot=es_fut_tot, es_fut_cor=es_fut_cor, es_fut_sco=es_fut_sco,
                           es_sub_tot=es_sub_tot, es_sub_cor=es_sub_cor, es_sub_sco=es_sub_sco,
                           es_imt_tot=es_imt_tot, es_imt_cor=es_imt_cor, es_imt_sco=es_imt_sco,
                           es_pas_tot=es_pas_tot, es_pas_cor=es_pas_cor, es_pas_sco=es_pas_sco,
                           es_con_tot=es_con_tot, es_con_cor=es_con_cor, es_con_sco=es_con_sco,
                           it_imp_abc=it_imp_abc, it_con_abc=it_con_abc
                           )
    




@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})




@views.route('/set-language', methods=['POST'])
@login_required
def set_language():
    language = request.form.get('language')
    session['language'] = language
    return redirect(url_for('views.quiz'))



@views.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    language_map = {
        'it': 'Italian',
        'de': 'German',
        'fr': 'French',
        'en': 'English',
        'es': 'Spanish'
    }

    # Retrieve language from session
    language = session.get('language', 'it')  # Default to 'it' if not set
    language_name = language_map.get(language, 'Italian')  # Default to 'Italian' if language code is not recognized
    
    question_ids = [q.id for q in Question.query.filter_by(language=language).all()]

    if len(question_ids) > 10:
        question_ids = random.sample(question_ids, 10)
        print(question_ids)


    questions = Question.query.filter(Question.id.in_(question_ids)).all()
    print(questions)

    # Shuffle answer options
    for q in questions:
        options = [
            {'label': 'a', 'text': q.option_a},
            {'label': 'b', 'text': q.option_b},
            {'label': 'c', 'text': q.option_c}
        ]
        random.shuffle(options)
        q.shuffled_options = options

    
    # If POST method is used (form submission), handle score
    if request.method == 'POST':
        score = request.form.get('score')  # Get the score from form data
        if score:
            if language == 'it':
                current_user.total_score_it += int(score)
            elif language == 'de':
                current_user.total_score_de += int(score)
            elif language == 'fr':
                current_user.total_score_fr += int(score)
            elif language == 'en':
                current_user.total_score_en += int(score)
            elif language == 'es':
                current_user.total_score_es += int(score)
            
            db.session.commit()
            flash('Quiz result saved!', category='success')
    
    return render_template('quiz.html', user=current_user, questions=questions, language_name=language_name)



@views.route('/submit-answer', methods=['POST'])
@login_required
def submit_answer():
    data = request.get_json()
    question_id = data.get('question_id')
    user_answer = data.get('user_answer')
    qlang = data.get('qlang')
    
    # Find the correct answer from your database
    question = Question.query.get(question_id)
    is_correct = 1 if question.correct_option == user_answer else 0
    
    # Log the answer in your database
    answer = Answered(
        user_id=current_user.id,
        question_id=question_id,
        correct=user_answer,
        qlang=qlang
    )
    db.session.add(answer)
    db.session.commit()
    
    return jsonify(success=True)



@views.route('/submit-answer-agg', methods=['POST'])
@login_required
def submit_answer_agg():
    data = request.get_json()
    question_id = data.get('question_id')
    user_answer = data.get('user_answer')
    qlang = data.get('qlang')
    qtype = data.get('qtype')
    difficulty = data.get('difficulty')
    
    # Find the correct answer from your database
    question = Question.query.get(question_id)
    is_correct = 1 if question.correct_option == user_answer else 0
    
    # Check if a record with the specified parameters already exists
    existing_answer = Answeredagg.query.filter_by(
        user_id=current_user.id,
        qlang=qlang,
        qtype=qtype,
        difficulty=difficulty
    ).first()

    # If it exists, update the existing record
    if existing_answer:
        existing_answer.icount += 1
        existing_answer.icountcorrect += user_answer
        a = existing_answer.icountcorrect / existing_answer.icount
        existing_answer.correctpct = a
    # If it does not exist, create a new record
    else:
        answer = Answeredagg(
            user_id=current_user.id,
            icount=1,
            icountcorrect=user_answer,
            correctpct=user_answer,
            qlang=qlang,
            qtype=qtype,
            difficulty=difficulty
        )
        db.session.add(answer)
    
    db.session.commit()
    
    return jsonify(success=True)


@views.route('/start_quiz/<language>')
@login_required
def start_quiz(language):
    # Set the language in the session
    session['language'] = language
    # Redirect to the quiz page for the selected language
    return redirect(url_for('views.quiz'))





@views.route('/start-payment', methods=['POST'])
def start_payment():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Premium Subscription',
                },
                'unit_amount': 999,  # This represents $9.99
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('payment_success', _external=True),
        cancel_url=url_for('payment_cancel', _external=True),
    )
    return jsonify(id=session.id)

@views.route('/create-charge', methods=['POST'])
@login_required
def create_charge():
    try:
        # Amount in cents
        amount = 500  # This is an example, set the actual amount based on your need

        customer = stripe.Customer.create(
            email=current_user.email,
            source=request.form['stripeToken']
        )

        charge = stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description='Your Product or Service Description'
        )

        # TODO: Save the payment status, etc. in your database if needed

        return redirect(url_for('success_page'))  # Or wherever you'd like to redirect after a successful payment

    except stripe.error.StripeError:
        flash('Payment failed. Please try again later.', 'danger')
        return redirect(url_for('payment_page'))  # Redirect to your payment page

@views.route('/payment-success')
def payment_success():
    # Handle post-payment logic here
    return "Payment was successful!"

@views.route('/payment-cancel')
def payment_cancel():
    # Handle payment cancellation logic here
    return "Payment was cancelled."



@views.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    stripe_public_key = current_app.config['STRIPE_PUBLIC_KEY']
    return render_template('payment.html', user=current_user, STRIPE_PUBLIC_KEY=stripe_public_key)


@views.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)



