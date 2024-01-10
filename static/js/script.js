liff.init({
    liffId: '2002096181-Ryql27BY',
    withLoginOnExternalBrowser: true,
})


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
            if(data.judge==2){
                liff.sendMessages([
                    {
                        "type":"text",
                        "text":"https://gift.line.me/item/6517019"
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

            // Close the LIFF window
            liff.closeWindow();
        })
        .catch(error => {
            console.error('Error submitting response', error);
        });
    });
}

function GiftSettingResponse(name, url, price, img) {
    fetch('/submit_giftsettingresponse', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'gift_name': name,
            'gift_url': url,
            'gift_price': price,
            'gift_img_url': img,
        }),
    })
}
