from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Question, Note, QuizResult, Answered, Answeredagg  # Import QuizResult along with Note
from . import db
import json
import random
from flask import session
from sqlalchemy import func


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # Fetch data from Answeredagg for the current user
    user_answer_data = Answeredagg.query.filter_by(user_id=current_user.id).all()

    it_imp_sco = 0
    it_fut_sco = 0
    it_cond_sco = 0
    it_imt_sco = 0
    it_sub_sco = 0
    it_pas_sco = 0

    it_imp_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="it", qtype="imperfect").scalar()
    it_imp_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="it", qtype="imperfect").scalar()
    if it_imp_tot != None:
       it_imp_sco = it_imp_tot / 5 + it_imp_cor

    it_cond_tot = db.session.query(func.sum(Answeredagg.icount)).filter_by(user_id=current_user.id, qlang="it", qtype="conditional").scalar()
    it_cond_cor = db.session.query(func.sum(Answeredagg.icountcorrect)).filter_by(user_id=current_user.id, qlang="it", qtype="conditional").scalar()
    if it_cond_tot != None:
       it_cond_sco = it_cond_tot / 5 + it_cond_cor

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

    return render_template("home.html", user=current_user, user_answer_data=user_answer_data, 
                           it_imp_tot=it_imp_tot, it_imp_cor=it_imp_cor, it_imp_sco=it_imp_sco,
                           it_fut_tot=it_fut_tot, it_fut_cor=it_fut_cor, it_fut_sco=it_fut_sco,
                           it_sub_tot=it_sub_tot, it_sub_cor=it_sub_cor, it_sub_sco=it_sub_sco,
                           it_imt_tot=it_imt_tot, it_imt_cor=it_imt_cor, it_imt_sco=it_imt_sco,
                           it_pas_tot=it_pas_tot, it_pas_cor=it_pas_cor, it_pas_sco=it_pas_sco,
                           it_cond_tot=it_cond_tot, it_cond_cor=it_cond_cor, it_cond_sco=it_cond_sco
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