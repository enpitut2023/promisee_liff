// LIFF初期化後のコード
liff.init({
    liffId: '2002096181-Ryql27BY',
    withLoginOnExternalBrowser: true,
}).then(() => {
    // 初期化成功時の処理

    // 新しいURLにリダイレクト
    window.location.href = '新しいURL';
}).catch((error) => {
    // 初期化失敗時の処理
    console.error('LIFF initialization failed', error);
});