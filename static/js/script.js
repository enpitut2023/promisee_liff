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
        .then(response => {

            liff.closeWindow();
                // Handle the response from the server
        })
        .catch(error => {
            console.error('Error submitting response', error);
        });
    });
}