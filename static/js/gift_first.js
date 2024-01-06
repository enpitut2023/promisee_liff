// LIFF初期化後のコード
liff.init({
    liffId: '2002642249-Lq0RX2ZN',
    withLoginOnExternalBrowser: true,
}).then(() => {
    // 初期化成功時の処理

    // ページをリロード
    window.location.reload();
}).catch((error) => {
    // 初期化失敗時の処理
    console.error('LIFF initialization failed', error);
});
