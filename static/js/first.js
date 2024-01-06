liff.init({
    liffId: '2002096181-Ryql27BY',
    withLoginOnExternalBrowser: true,
}).then(() => {
    // liff.stateの値を取得
    const liffStateValue = decodeURIComponent(window.location.search).replace('?liff.state=', '');

    // バックエンドにデータを送信
    fetch(`/question${liffStateValue}`, {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
    },
    credentials: 'include',
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