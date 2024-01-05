from flask import Flask, render_template, request, jsonify, redirect, session, url_for, flash, get_flashed_messages, session
import firebase_admin
from firebase_admin import credentials,firestore
import requests
import secrets
import string
from datetime import timedelta, datetime
import pytz

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
        # URLからクエリパラメータ 'time' の値を取得
        time_param = request.args.get('time') 
        # 文字列からdatetimeオブジェクトに変換
        time_param = datetime.strptime(time_param, "%Y-%m-%d %H:%M:%S")

        session.permanent = True  # セッションを永続的に設定する
        app.permanent_session_lifetime = timedelta(days=30)  # 期限を30日に設定
        session['group_id'] = group_id  # group_id をセッションにセット
        if time_param is not None:
            current_time = datetime.now(pytz.timezone('Asia/Tokyo'))
            time_diff = current_time - time_param
            if time_diff > timedelta(minutes=10):
                return render_template('error.html')
            else:
                return render_template('index.html')
            
        else:
            # time_paramがNoneの場合の処理
            print("time_param is None")


@app.route('/submit_response',methods=["POST"])
def submit():
    username = request.form.get('username')
    answer = request.form.get('answer')

    group_id = session['group_id'] 
    doc = doc_ref.document(group_id)

    # 同じユーザーがすでにデータベースに格納されていないかを判定
    usernames = doc.get().to_dict()["username"]

    if username not in usernames:

        # 既存データを取得し、存在しない場合は空の辞書をセット
        existing_data = doc.get().to_dict() or {}

        # それぞれのリストを取得し、存在しない場合は空のリストをセットする
        username_list = existing_data.get('username', [])
        answer_list = existing_data.get('answer', [])

        # 新しい要素をそれぞれのリストに追加
        username_list.append(username)
        answer_list.append(answer)
        # ドキュメントにデータを更新
        doc.set({'username': username_list, 'answer': answer_list}, merge=True)

    group_count=doc.get().to_dict()["group_count"]
    member_count=len(doc.get().to_dict()["username"])
    # 人数分集まったかを判定
    if member_count==group_count:
        # ギフトを送る
        if answer=='yes':
            return jsonify({'result': True, 'message': 'yes','judge':1})
        else:
            return jsonify({'result': True, 'message': 'no','judge':1})
    else:
        if answer=='yes':
            return jsonify({'result': True, 'message': 'yes','judge':0})
        else:
            return jsonify({'result': True, 'message': 'no','judge':0})


if __name__ == '__main__':
    app.run(debug=True)
