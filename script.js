liff.init({
    liffId: '2002096181-Ryql27BY', // Use own liffId
    withLoginOnExternalBrowser: true, // Enable automatic login process
}).then(() => {
    // Start to use liff's api
    runApp();
});


function runApp() {
    liff.getProfile().then(profile => {
        const userName = profile.displayName;

        liff.getGeolocation()
            .then(location => {
                const userLocationText = `Latitude: ${location.latitude}, Longitude: ${location.longitude}`;

                // Display user information on the page
                document.getElementById('userName').innerText = `User: ${userName}`;
                document.getElementById('userLocation').innerText = `Location: ${userLocationText}`;
            })
            .catch(error => {
                console.error('Error getting location', error);
            });
    });
}