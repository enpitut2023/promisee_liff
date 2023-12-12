liff.init({
    liffId: '2002096181-Ryql27BY', // Use own liffId
    withLoginOnExternalBrowser: true, // Enable automatic login process
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
                'user_name': userName,
                'response_type': responseType,
            }),
        })
        .then(response => response.json())
        .then(data => {

            // Display the response with an alert
            if (data.message=='yes') {
                alert('えらいのだ!');  // 任意のメッセージを表示
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