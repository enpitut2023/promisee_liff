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
group_doc_ref = db.collection('groups')
schedules_doc_ref = db.collection('schedules')
# タイムゾーンを日本時間に設定
jp_timezone = pytz.timezone('Asia/Tokyo')

def generate_secret_key(length=24):
    characters = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(secrets.choice(characters) for _ in range(length))
    return secret_key

app = Flask(__name__)
app.secret_key = generate_secret_key()  # セッション用の秘密鍵を設定



@app.route('/question')
def index():

    # クエリパラメータから schedule_id を取得
    schedule_id = request.args.get('schedule_id', default='', type=str)
    if schedule_id == '':
        return render_template('first.html')
    # 指定されたドキュメントIDに基づいてドキュメントを取得
    schedules_doc = schedules_doc_ref.document(schedule_id)
        
    # ドキュメントが存在するか確認
    if schedules_doc.get().exists:
        session.permanent = True  # セッションを永続的に設定する
        app.permanent_session_lifetime = timedelta(days=30)  # 期限を30日に設定
        session['schedule_id'] = schedule_id  # schedule_id をセッションにセット
        # 発行時刻を取得 
        time=schedules_doc.get().to_dict()["datetime"]
        print(schedule_id)
        time=jp_timezone.localize(datetime.strptime(time, "%Y年%m月%d日%H時%M分"))
        current_time = datetime.now(pytz.timezone('Asia/Tokyo'))
        diff = current_time-time
        if diff < timedelta(minutes=7):
            return render_template('index.html')
        else:   # 時間が過ぎた時

            return render_template('error.html')
    else:
        print(f"スケジュール {schedule_id} は存在しません。")
        return render_template('error.html')

            

@app.route('/gifts')
def gifts():
    # クエリパラメータを取得
    min_price = request.args.get('min_price', default=0, type=int)
    max_price = request.args.get('max_price', default=1000, type=int)

    gifts_data = db.collection('gifts').get() # ギフトデータ取得
    print(max_price)
    print(min_price)

    # テスト用ギフトデータ出力
    # for gift in gifts_data:
    #     gift_dict = gift.to_dict()
    return render_template('gifts.html', gifts=gifts_data, min_price=min_price, max_price=max_price)

@app.route('/submit_response',methods=["POST"])
def submit():
    username = request.form.get('username')
    answer = request.form.get('answer')

    schedule_id = session['schedule_id'] 
    schedules_doc = schedules_doc_ref.document(schedule_id)

    # 同じユーザーがすでにデータベースに格納されていないかを判定
    usernames = schedules_doc.get().to_dict()["username"]

    if username not in usernames:

        # 既存データを取得し、存在しない場合は空の辞書をセット
        existing_data = schedules_doc.get().to_dict() or {}

        # それぞれのリストを取得し、存在しない場合は空のリストをセットする
        username_list = existing_data.get('username', [])
        answer_list = existing_data.get('answer', [])

        # 新しい要素をそれぞれのリストに追加
        username_list.append(username)
        answer_list.append(answer)
        # ドキュメントにデータを更新
        schedules_doc.set({'username': username_list, 'answer': answer_list}, merge=True)

    group_count=schedules_doc.get().to_dict()["group_count"]
    member_count=len(schedules_doc.get().to_dict()["username"])
    # 人数分集まったかを判定
    if member_count==group_count:
        
        # 人数分集まった
        # 一人でも間に合わなかった場合
        if 'no' in answer_list:
            schedules_doc.delete()
            print(f"スケジュール {schedule_id} が削除されました。")
            if answer=='yes':
                return jsonify({'result': True, 'message': 'yes','judge':2})
            else:
                return jsonify({'result': True, 'message': 'no','judge':2})
        # 全員間に合った場合
        else:
            schedules_doc.delete()
            print(f"スケジュール {schedule_id} が削除されました。")
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
