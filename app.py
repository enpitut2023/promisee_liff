from flask import Flask, render_template, request, jsonify, redirect, session, url_for, flash, get_flashed_messages, session
import pyrebase
import firebase_admin
from firebase_admin import credentials,firestore
import requests
import secrets
import string
from datetime import timedelta

# データベースの準備等
cred = credentials.Certificate("key.json")

firebase_admin.initialize_app(cred)
db = firestore.client()

doc_ref = db.collection('groups')

def generate_secret_key(length=24):
    characters = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(secrets.choice(characters) for _ in range(length))
    return secret_key

app = Flask(__name__)
app.secret_key = generate_secret_key()  # セッション用の秘密鍵を設定

format={
    "username":None,
    "answer":None,
}



@app.route('/')
def index():
        # URL パラメータから group_id を取得
        group_id = request.args.get('group_id')       
        session.permanent = True  # セッションを永続的に設定
        app.permanent_session_lifetime = timedelta(days=30)  # 期限を30日に設定
        session['group_id'] = group_id  # group_id をセッションにセット
        return render_template('index.html')


@app.route('/submit_response',methods=["POST"])
def submit():
    username = request.form.get('username')
    answer = request.form.get('answer')

    group_id = session['group_id'] 
    doc = doc_ref.document(group_id)

    # 既存データを取得し、存在しない場合は空の辞書をセット
    existing_data = doc.get().to_dict() or {}

    # それぞれのリストを取得し、存在しない場合は空のリストをセット
    username_list = existing_data.get('username', [])
    answer_list = existing_data.get('answer', [])

    # 新しい要素をそれぞれのリストに追加
    username_list.append(username)
    answer_list.append(answer)

    # ドキュメントにデータを更新
    doc.set({'username': username_list, 'answer': answer_list}, merge=True)



    # ドキュメントを更新
    doc.set({'username': username_list, 'answer': answer_list}, merge=True)  # 実際のリストのキーを置き換える

    if response_type=='yes':
        return jsonify({'result': True, 'message': 'yes'})
    else:
        return jsonify({'result': True, 'message': 'no'})


if __name__ == '__main__':
    app.run(debug=True)
