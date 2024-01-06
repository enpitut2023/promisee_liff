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