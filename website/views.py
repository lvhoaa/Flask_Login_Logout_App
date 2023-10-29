### CONTAIN API ENDPOINTS -- ROUTES 

# this file is the Blueprint for the app -- have bunch of ROUTES inside 
from flask import Blueprint, render_template, request, flash
import json
from .models import Note
from . import db 
from flask_login import login_required, current_user

views = Blueprint('views',__name__)

@views.route('/',methods = ['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        data=request.form 
        note = data.get('note')
        if len(note)<1:
            flash('Note is too short',category='error')
        else:
            new_note=Note(data=note,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added successfully',category='success')
    return render_template("home.html",user=current_user)

@views.route('/delete-note/',methods = ['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    