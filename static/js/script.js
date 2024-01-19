liff.init({
    liffId: '2002096181-Ryql27BY',
    withLoginOnExternalBrowser: true,
})


function submitResponse(responseType) {
    liff.getProfile().then(profile => {
        const userName = profile.displayName;

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
            if(data.judge==2){
                min_price = data.min_price
                max_price = data.max_price
                // URLを構築
                var url = "https://liff.line.me/2002642249-Lq0RX2ZN?min_price=" + min_price + "&max_price=" + max_price;                

                liff.sendMessages([
                    {
                        "type":"text",
                        "text":"送るギフトを選ぶのだ！\n" + url 
                    }
                ])
                print(data.judge)
            } else if(data.judge==1){
                liff.sendMessages([
                    {
                        "type":"text",
                        "text":"全員間に合ってよかったのだ〜"
                    }
                ])
            }

            // Display the response with an alert
            if (data.message=='yes') {
                alert('えらいのだ!');  // 任意のメッセージを表示
                print(data.judge)
            } else {
                alert('やらかしたのだ〜');  // エラーメッセージを表示
            }
                    // ボタンを無効にする
            document.getElementById('yesButton').disabled = true;
            document.getElementById('noButton').disabled = true;

            // Close the LIFF window
            liff.closeWindow();
        })
        .catch(error => {
            console.error('Error submitting response', error);
        });
    });
}
