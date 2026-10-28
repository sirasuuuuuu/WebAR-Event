# イベント向けキャラクターAR（Web試作）

QRコードでこのページを開き、ブラウザからキャラクターをAR表示するスターターです。サーバー管理は不要で、GitHub Pagesで公開できます。

## テストモデル

- `assets/test_box.glb`：Android向けのGLBモデル。元形状は2m角で、ページ上では0.25倍して表示します
- `assets/test_box.usdc`：Blenderから書き出した元データ
- `assets/test_box.usdz`：iPhone Quick Look向け。GLBと同じシアン系マテリアルを設定し、形状自体を0.25倍して約50cm角にしたUSDZ
- ページは現在 `test_box.glb` と `test_box.usdz` を読み込みます。

Quick Lookでは `ios-src` に指定したUSDZが使われるため、ページの `scale` 属性だけではiPhone側のモデルサイズは変わりません。USDZ内の形状を目的の実寸にして書き出し、`ar-scale="fixed"` でQuick Look上の拡大縮小を無効にしています。

テストモデルは簡単な箱です。キャラクターに差し替えるときは、両モデルを `assets/character.glb` と `assets/character.usdz` に置き、`index.html` の `src` と `ios-src` をその名前に変更します。

## 先に知っておくこと

- GitHub Pagesは静的ファイルを公開するサービスです。利用者データの保存やログイン機能は含みません。
- ARの対応状況は端末・ブラウザにより異なります。イベントで使う端末で事前確認してください。
- `index.html` はmodel-viewer 4.0.0をGoogle CDN、Three.js 0.183.0をjsDelivrから読み込みます。ページの表示とARにはインターネット接続が必要です。
- 公開リポジトリには公開してよい素材だけを入れてください。

## GitHub Pagesで公開

1. GitHubに新しいリポジトリを作成し、このフォルダの中身（`index.html` と `assets` フォルダ）をアップロードします。
2. リポジトリの **Settings → Pages** を開きます。
3. Sourceを **Deploy from a branch** にし、ブランチ（通常は `main`）とフォルダ **/(root)** を選んで保存します。
4. 公開URLが表示されたら、スマートフォンで開いて動作確認します。
5. 公開URLをQRコードにし、印刷前に実際のスマートフォンで読み取りテストをします。

## 動作確認

- PCブラウザで箱の3Dモデルが表示されることを確認。
- AndroidのChromeでは、Three.jsとWebXR Hit Testでブラウザ内ARを起動し、目印をタップして配置できることを確認。iPhoneのSafariではmodel-viewerからQuick Lookを起動。
- iPhoneのSafariでARボタンを押し、Quick Lookが起動するか確認。
- QRコードから直接開く経路も試します。アプリ内ブラウザで失敗する場合は、Safari/Chromeで開く案内をします。
- 会場の照明、床、通信状況を含めてリハーサルします。
