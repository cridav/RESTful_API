#!/usr/bin/env python3
# from sqlalchemy import MetaData,create_engine

from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
# from flask_restful import reqparse, abort, Api, Resource
from datetime import datetime

app = Flask(__name__)
# api = Api(app)

# now define a DATABASE


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_BINDS']={'record':'sqlite:///record.db'}

#in-memory
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
# app.config['SQLALCHEMY_BINDS']={'record':'sqlite:///:memory:'}

#in-memory
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
# app.config['SQLALCHEMY_ENGINE_OPTIONS']= create_engine('sqlite://')

# db = SQLAlchemy(app).create_engine('sqlite://','SQLALCHEMY_ENGINE_OPTIONS')
db = SQLAlchemy(app)
db.create_engine('sqlite://',{})

# db = SQLAlchemy(app=app, engine_options=create_engine('sqlite://'))
# db.create_all()

class Notes(db.Model):
    # unique keys
    id = db.Column(db.Integer, primary_key =True)
    # nullabla = False means that it requires something to be there
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text, nullable = False)
    created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())
    modified = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())
    # def __repr__(self):
    #     return 'Note Nr. ' + str(self.id)

class History(db.Model):
    __bind_key__ = 'record'
    # unique keys
    id = db.Column(db.Integer, primary_key =True)
    # nullabla = False means that it requires something to be there
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text, nullable = False)
    created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())
    modified = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())
    ref_id = db.Column(db.Integer,nullable = False)
    version = db.Column(db.Integer,nullable = False, default = 0)

@app.route('/notes', methods = ['GET','POST'])
def notes():

    if request.method == 'POST':
        # If it is 'POST', read data from the form and send it
        # to the database
        in_note = request.get_json(force=True)
        # title = request.json['title']
        # content = request.json['content']

        new_note = Notes(  title=in_note['title'],\
                            content=in_note['content'],
                            created = datetime.utcnow(),
                            modified = datetime.utcnow(),
                            # version = 1
                        )
        db.session.add(new_note)
        db.session.commit()
        # return None
        # return in_note
        # return str(type(in_note))
        return jsonify({"MESSAGE":"OK"},str(200))
    else:
        all_notes = Notes.query.all() #this is a list
        output = []
        for note in all_notes:
            notes = {}
            notes['id'] = note.id
            notes['title'] = note.title
            notes['content'] = note.content
            notes['created'] = note.created
            notes['modified']= note.modified

            output.append(notes)
        return (jsonify({'notes':output}),str(200))


@app.route('/record', methods = ['GET'])
def record():
    all_notes = History.query.all() #this is a list
    output = []
    for note in all_notes:
        notes = {}
        notes['id'] = note.id
        notes['title'] = note.title
        notes['content'] = note.content
        notes['created'] = note.created
        notes['modified']= note.modified
        notes['ref_id'] =  note.ref_id
        notes['version'] = note.version

        output.append(notes)
    return jsonify({'notes':output},str(200))

@app.route('/record/<int:note_id>', methods = ['GET'])
def record_by_id(note_id):
    all_notes = History.query.filter(History.ref_id == note_id).all() #this is a list
    output = []
    for note in all_notes:
        notes = {}
        notes['id'] = note.id
        notes['title'] = note.title
        notes['content'] = note.content
        notes['created'] = note.created
        notes['modified']= note.modified
        notes['ref_id'] =  note.ref_id
        notes['version'] = note.version

        output.append(notes)
    return jsonify({'notes':output},str(200))

@app.route('/notes/<int:note_id>', methods = ['GET'])
def get_note(note_id):
    note = Notes.query.get(note_id)
    if note:
        out = { 'id':note.id,
                'title':note.title,
                'content':note.content,
                'created':note.created,
                'modified':note.modified,
        }
        return (out,200)
    return ({"MESSAGE":"entry not found"},str(404))

@app.route('/notes/<int:note_id>', methods = ['PUT'])
def modify(note_id):
    try:
        in_note = request.get_json(force=True)
    except:
        return ({"MESSAGE":"Bad Request"},str(400))

    h_notes = History.query.filter(History.ref_id == note_id).order_by(History.version.desc()).first() #this is a list
    # return(str(h_notes.version),str(type(h_notes)),str(type(h_notes.version)))
    # return (str(type(h_notes)))
    if in_note:
        note = Notes.query.get(note_id)
        if note:
            new_hist = History( title=note.title,\
                                content=note.content,
                                created =note.created,
                                modified =datetime.utcnow(),
                                ref_id = note.id,
                                version = h_notes.version + 1 if h_notes else 1
                        )
            db.session.add(new_hist)
            for key,val in in_note.items():
                setattr(note,key,val)
                db.session.add(note)
                db.session.commit()
            return ({"MESSAGE":"entry modified"},str(201))
        else:
            return ({"MESSAGE":"entry not found"},str(404))

    else:
        return ({"MESSAGE":"Bad Request"},str(400))

    


@app.route('/notes/<int:note_id>', methods = ['DELETE'])
def delete(note_id):
    h_notes = History.query.filter(History.ref_id == note_id).order_by(History.version.desc()).first()
    note = Notes.query.get(note_id)
    if note:

        new_hist = History(  title=note.title,\
                            content=note.content,
                            created =note.created,
                            modified =note.modified,
                            ref_id = note.id,
                            version = h_notes.version + 1 if h_notes else 1
                        )
        db.session.add(new_hist)

        db.session.delete(note)
        db.session.commit()
    else:
        return jsonify({"MESSAGE":"entry not found"},str(404))
    return jsonify({"MESSAGE":"entry deleted"},str(204))




if __name__ == '__main__':
    app.run(debug=True)