liff.init({
    liffId: '2002096181-Ryql27BY',
    withLoginOnExternalBrowser: true,
}).then(() => {
    // liff.stateの値を取得
    const liffState = liff.getOS().query;

    // バックエンドにデータを送信
    fetch('/question', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        // liff.stateをschedule_idとして送信
        // 他にも必要なデータがあればここに追加
        credentials: 'include', // クッキーを含むリクエストを有効にする
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Error fetching data', error);
    });

}).catch((error) => {
    console.error('LIFF initialization failed', error);
});


function submitResponse(responseType) {
    liff.getProfile().then(profile => {
        const userName = profile.displayName;
        // ボタンを無効にする
        document.getElementById('yesButton').disabled = true;
        document.getElementById('noButton').disabled = true;
        // Send data to Flask backend
        fetch('/submit_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'username': userName,
                'answer': responseType,
            }),
        })
        .then(response => response.json())
        .then(data => {
            if(data.judge==1){
                liff.sendMessages([
                    {
                        "type":"text",
                        "text":"https://gift.line.me/item/6517019"
                    }
                ])
                print(data.judge)
            }

            // Display the response with an alert
            if (data.message=='yes') {
                alert('えらいのだ!');  // 任意のメッセージを表示
                print(data.judge)
            } else {
                alert('やらかしたのだ〜');  // エラーメッセージを表示
            }

            // Close the LIFF window
            liff.closeWindow();
        })
        .catch(error => {
            console.error('Error submitting response', error);
        });
    });
}
