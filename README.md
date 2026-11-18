# イベント向けキャラクターAR

QRコードを読み取り、ブラウザからイベントキャラクターをAR表示するGitHub Pages用サイトです。サーバー契約や専用アプリのインストールは不要です。

## 現在の内容

- Android向け `assets/character.glb` とiPhone Quick Look向け `assets/character.usdz` に新しいキャラクターを適用しています。
- 古い箱モデルも `assets/test_box.glb` / `assets/test_box.usdz` として残しています。
- QRごとの設定は `spots.json` に13件あります。本文や見出し、モデル、表示サイズ、解説の時間差、追加モデルを場所ごとに指定できます。
- URLは `https://<ユーザー名>.github.io/<リポジトリ名>/?spot=01` のようにし、末尾を `01` から `13` に変えてQRコードを作ります。
- QRからARの紹介画面やプレビュー画面を挟まず、このスポット専用の開始画面を開きます。ブラウザの安全制限によりAR起動には利用者のタップが1回必要です。

## QRごとの説明を設定する

`spots.json` をVS Codeで開き、該当する番号の項目を編集します。

- `title`: ページの見出し
- `intro`: 開始前の短い案内
- `explanation`: 配置後に吹き出しで出す文章（空欄なら表示しません）
- `explanationDelayMs`: 配置してから説明を出すまでの時間（ミリ秒。`2500` は2.5秒）
- `modelGlb` / `modelUsdz`: その場所で使うAndroid用 / iPhone用モデル
- `modelScale`: Android用モデルの倍率。新しいキャラクターは実寸に合わせて `1`
- `companionModelGlb`: キャラクターのそばに追加表示するAndroid用GLB。使わない場所は `null`
- `companionScale` / `companionYOffset`: 追加モデルの倍率とキャラクターからの高さ

例：

```json
"01": {
  "label": "スポット01",
  "title": "建物の歴史",
  "intro": "この場所の見どころを紹介します。",
  "modelGlb": "assets/character.glb",
  "modelUsdz": "assets/character.usdz",
  "modelScale": 1,
  "explanation": "この建物は……",
  "explanationDelayMs": 3000,
  "companionModelGlb": null,
  "companionScale": 1,
  "companionYOffset": 0.12,
  "version": "20261118"
}
```

追加モデルを使う場合はGLBを `assets` 内に置き、`companionModelGlb` を `assets/speech_bubble.glb` のように設定します。iPhoneのQuick LookではWebページ上の吹き出しをARカメラ内に重ねられません。iPhoneでも3D吹き出しを表示する場合は、吹き出しを含めたUSDZを作り、該当スポットの `modelUsdz` に指定してください。

## QRコード

公開後のURLの末尾に `?spot=01` 〜 `?spot=13` を付けて各QRコードを作成します。リポジトリのトップURLと13種類のスポット番号を表にまとめて管理してください。QRコードを印刷する前に、スマートフォンで各コードを読み、番号に対応したページが出ることを確認します。

## モデルの差し替え

Android用GLBとiPhone用USDZを `assets` に置き、`spots.json` の各項目にファイル名を書きます。iPhone用USDZはQuick Lookで使う実寸にして書き出します。元のBlenderファイルやテストモデルは上書きせず、更新前のファイルを別名で保管してください。

新キャラクターは `中産連ビルEVENT/blender/smothmouse2.blend` から書き出しました。Blender内の画像素材を使い、キャラクター以外の離れた補助平面は出力から除外しています。元の `.blend` は変更していません。

## GitHub Pagesで公開

1. このフォルダの中身をGitHubリポジトリへアップロードします。
2. リポジトリの **Settings → Pages** を開きます。
3. **Deploy from a branch**、`main`、`/(root)` を選び保存します。
4. 公開URLに `?spot=01` を付けて開き、Android ChromeとiPhone Safariで確認します。
5. 各スポットの内容を調整したら変更をGitHubへ同期し、公開ページを再確認します。

## 確認事項と制約

- AndroidはChromeのWebXRで床や机を検出してタップ配置します。タップ前に自動で配置される問題は未対応です。
- iPhoneはSafariからQuick Lookを開きます。Quick Lookへの移動はタップ操作が必要です。
- GitHub Pagesは静的ファイル公開です。イベント参加者の情報保存、編集画面、管理機能はありません。
- ページの表示とARにはインターネット接続が必要です。`model-viewer` はGoogle CDN、Three.jsはjsDelivrから読み込みます。
- 端末やOSの更新状況により動作が異なるため、当日使用する端末と会場で事前に確認します。
