from flask import Flask, render_template, request, jsonify, redirect, session, url_for, flash, get_flashed_messages
import pyrebase
import firebase_admin
from firebase_admin import credentials,firestore
import requests

# データベースの準備等
cred = credentials.Certificate("key.json")

firebase_admin.initialize_app(cred)
db = firestore.client()

doc_ref = db.collection('question')


app = Flask(__name__)


format={
    "username":None,
    "answer":None,
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit_response',methods=["POST"])
def submit():
    user_name = request.form.get('user_name')
    response_type = request.form.get('response_type')

    format['username']=user_name
    format['answer']=response_type
    doc = doc_ref.document()
    doc.set(format)
    if response_type=='yes':
        return jsonify({'result': True, 'message': 'yes'})
    else:
        return jsonify({'result': True, 'message': 'no'})


if __name__ == '__main__':
    app.run(debug=True)
