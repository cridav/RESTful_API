#!/usr/bin/env python3


from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, abort, Api, Resource
from datetime import datetime
from flask_marshmallow import Marshmallow 

app = Flask(__name__)
ma = Marshmallow(app)
# api = Api(app)

# now define a DATABASE

# /// means relative path, //// means absolute path
# this is where the database is going to be and its name (posts)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_BINDS']={'record':'sqlite:///record.db'}
#in-memory
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
# app.config['SQLALCHEMY_ENGINE_OPTIONS']= create_engine('sqlite://')

# db = SQLAlchemy(app).create_engine('sqlite://','SQLALCHEMY_ENGINE_OPTIONS')
db = SQLAlchemy(app)
db.create_engine('sqlite://',{})

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



class ProductSchema(ma.Schema):
  class Meta:
      fields = ('id','title','content','created','modified')
# products_schema = ProductSchema(many=True, strict=True)
products_schema = ProductSchema()


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
        return in_note
        # return str(type(in_note))
        return jsonify({"THIS WAS":"CREATED"})
    else:
        all_notes = Notes.query.all() #this is a list
        output = []
        for note in all_notes:
            notes = {}
            # notes['id'] = note.id
            # notes[note.id]={}
            # notes[note.id]['title'],notes[note.id]['content'],notes[note.id]['created'],notes[note.id]['modified']= (note.title,note.content,note.created,note.modified)
            notes['id'] = note.id
            notes['title'] = note.title
            notes['content'] = note.content
            notes['created'] = note.created
            notes['modified']= note.modified

            output.append(notes)
        # return str(type(all_notes))
        # return str(all_notes[1].id)
        # return {str(type(all_notes[1])):str(all_notes[1].id)}
        return jsonify({'notes':output})


@app.route('/record', methods = ['GET'])
def record():
    all_notes = History.query.all() #this is a list
    output = []
    for note in all_notes:
        notes = {}
        # notes['id'] = note.id
        # notes[note.id]={}
        # notes[note.id]['title'],notes[note.id]['content'],notes[note.id]['created'],notes[note.id]['modified']= (note.title,note.content,note.created,note.modified)
        notes['id'] = note.id
        notes['title'] = note.title
        notes['content'] = note.content
        notes['created'] = note.created
        notes['modified']= note.modified
        notes['ref_id'] =  note.ref_id
        notes['version'] = note.version

        output.append(notes)
    # return str(type(all_notes))
    # return str(all_notes[1].id)
    # return {str(type(all_notes[1])):str(all_notes[1].id)}
    return jsonify({'notes':output})



@app.route('/notes/<int:note_id>', methods = ['PUT'])
def modify(note_id):
    in_note = request.get_json(force=True)
    if in_note:
        note = Notes.query.get(note_id)
        if note:

            new_hist = History(  title=note.title,\
                            content=note.content,
                            created =note.created,
                            modified =note.modified,
                            ref_id = note.id,
                            version =+ 1
                        )
            db.session.add(new_hist)


            for key,val in in_note.items():
                setattr(note,key,val)
                db.session.add(note)
                db.session.commit()
                return {"MESSAGE":"entry modified"},201
        else:
            return {"MESSAGE":"entry not found"},404

    else:
        return {"MESSAGE":"Bad Request"},400
    # note = Notes.query.filter_by(public_id=public_id).first()
    # if not note:
    #     return jsonify({'Message':'Note not found'})

    


@app.route('/notes/<int:note_id>', methods = ['DELETE'])
def delete(note_id):

    note = Notes.query.get(note_id)
    if note:

        new_hist = History(  title=note.title,\
                            content=note.content,
                            created =note.created,
                            modified =note.modified,
                            ref_id = note.id,
                            version =+ 1
                        )
        db.session.add(new_hist)

        db.session.delete(note)
        db.session.commit()
    else:
        return {"MESSAGE":"entry not found"},404
    return {"MESSAGE":"data deleted"},204




if __name__ == '__main__':
    app.run(debug=True)