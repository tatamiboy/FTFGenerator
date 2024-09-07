# FTFGenerator<br/>

*※素人プログラマーがChatGPTに聞きながら趣味で作ったソフトです。使用したことにより発生した損害などへの補償は一切できません。自己責任で使用してください。*  
*※公開にあたり何か問題がある場合はお知らせください。また、予告なく公開を停止する場合があります。*
<br/>

## 概要
画像認識とモーショントラッキングを利用したfunscript作成補助ツールです。画面内の顔or手を検出し、その動きを追跡します。
トラッキング方向は上下左右、対角線方向とそれぞれの反転に対応しています。    

チャプターファイル(txt)を利用することで、動画内の特定のシーンを処理することが可能です。
チャプターファイルを作成するためのOFS拡張機能も付属しています。

## 準備
Python3と必要なライブラリをインストールしてください。  
```pip install -r requirements.txt```    

顔検出用の学習済みのモデルデータが必要です。各自で用意してください。  
私は以下のページのものを使用させていただきましたが、他のモデルデータでも代用可能だと思います。  
  
.prototxtファイル, .caffemodelファイルをmain.pyと同じディレクトリに配置してください。  
[Github: kgautam01/DNN-Based-Face-Detection](https://github.com/keyurr2/face-detection/)

## OFSエクステンションの使い方:
1. 日本語化する場合は "main.lua" 内の `_lang = "en"` を `_lang = "jp"` に変更してください。
1. chapter-makerフォルダをOFSのエクステンションフォルダーにコピーし、拡張機能を有効化します。
1. 拡張機能のウィンドウのボタンでチャプター開始と終了をセットします。
1. 出力ディレクトリを指定し、保存ボタンを押すと "動画ファイル名.txt" が出力されます。

## FTFGeneratorの使い方:
1. main.pyを起動し、動画ファイルを開きます。
1. トラッキング目標、トラッキング方向を選び実行ボタンを押すと、トラッキングが開始されます。
1. トラッキングを終えるとダウンサンプリング画面が表示されるので、スライダーでサンプリングレートを調節します。
1. OKボタンを押すと動画ファイルと同じディレクトリに "動画名.face(hand).funscript" が保存されます。(既に同名ファイルがある場合は末尾に保存時刻が付加されます。)
1. OFSなどで確認、調整します。

## チャプターファイルの使い方:
1. 動画ファイルとチャプターファイルを開きます。
1. トラッキング目標を指定し実行ボタンを押すと、チャプターファイルで指定された時間に対してトラッキングが始まります。
1. 複数のチャプターがある場合は、1チャプターごとにサンプリング画面が表示されます。OKを押すと保存、キャンセルを押すとそのチャプターのデータは保存されません。
1. すべてのチャプターを終えると、動画ファイルと同じディレクトリに "動画名.face(hand).funscript" が出力されます。

## オプション:
* CLIモード: `--cli` でメインウィンドウを表示せずに実行できます。CLIモードのオプションは`--help`を見てください。トラッキング中のプレビュー画面は引き続き表示されます。
* 自動サンプリング: サンプリング画面を表示せずにデフォルトのサンプリングレートで保存します。上記のcliモードと組み合わせることでバッチ処理が可能です。 `-a` `--auto-sampling`
* 各種設定: ウィンドウサイズやデフォルトのサンプリングレートは config/settings.py 内で変更できます。適当に書き換えてください。モデルデータのパスもここで指定してください。

## 注意:
* 手のトラッキングは中指の付け根が基準です。手に関しては検出が飛んだり荒ぶることがあります。
* 1チャプター中にトラッキングできたフレームが20未満の場合は保存されません。
* 顔検出はすべてのフレームで行っているわけではなく、最初に検出した顔の位置の物体を、以降のフレームでは追跡しています。そのため1チャプターが長いと徐々にトラッキング位置がズレていきます。完全に見失った場合は再度検出を試みますが、その前に適度にチャプターを区切ると良い結果が得やすいです。また、プレビュー画面でrキーを押すことで顔検出をリセットできます。
* 手についてはすべてのフレームで画像認識を行っています。検出する手は1つのみで、確信度の高いものが優先されます。徐々にずれるということはありませんが、動いていない方の手が認識されるといったことがあるので、こちらも適度に区切って不要な部分は破棄していくのがいいと思います。
<br/>
<br/>

# FTFGenerator (English)
*※This software was created by an newbie programmer as a hobby while asking questions to ChatGPT. I cannot compensate for any damage caused by its use. Use at your own risk.*  
*※If there are any problems with the release, please let us know. I may also stop the release without notice.*
 <br/>

## Overview
This is a funscript creation assistant tool that uses image recognition and motion tracking.  
 It recognizes a face or hand on the screen and tracks its motion. The tracking directions are up/down, left/right, diagonal, and inverted.  
Using chapter file (txt), it is possible to process specific scenes in a video.
An OFS extension for creating chapter files is also included.

## Requirements
Install Python3 and required libraries.  
```pip install -r requirements.txt```    

You will need trained model data for face detection. Please prepare it yourself.  
I used the data on the following page, but I think you can use other model data instead.  

Download "deploy.prototxt", "dnn_model.caffemodel" and place it in the same directory as "main.py".  
[Github: kgautam01/DNN-Based-Face-Detection](https://github.com/kgautam01/DNN-Based-Face-Detection)

## How to use OFS extension:
1. Copy the included "chapter-maker" folder into the OFS extension folder and activate the extension.
1. In the scene you want to process in FTFGenerator, put 0 for the start frame and 100 for the end frame. (Chapters must not overlap each other and the start and end points must be properly closed.)
1. Specify the export directory and tracking direction, and press the "Export" button to export a "videoname.face(hand).txt" file.

## How to use FTFGenerator:
1. Start "main.py" and open the video file.
1. Select the tracking target, tracking direction, and press the Run button to start tracking.
1. When tracking is finished, the downsampling screen will appear, and you can adjust the sampling rate with the slider.
1. Click OK button to export "videoname.funscript" to the same directory as the video file.
1. Check and adjust by OFS, etc.

## How to use FTFGenerator with chapter files:
1. Open video and chapter files.
1. Select a tracking target and press the Run button to start tracking.
1. If there are multiple chapters, the sampling screen will appear for each chapter.
Press OK to save and proceed to the next chapter. If you press Cancel, the data for that chapter will not be saved.
1. When all chapters are finished, a "videoname.face(hand).funscript" will be export in the same directory as the video file.

## Options:
* CLI mode: You can run it without displaying the main window with the `--cli` option. See `--help` for CLI mode options. The preview window will continue to be displayed during tracking.
* Auto Downsampling: Saves at the default sampling rate without displaying the sampling screen. This is useful when you want to process multiple chapters at once. Batch processing is possible in combination with the cli mode described above. `-a` `--auto-sampling`
* Settings: Window size, default sampling rate, etc. can be changed in config/settings.py. Rewrite as you see fit. The path to the model data should also be specified here.

## Note:
* Hand tracking is based on the base of the middle finger. The hand may skip recognition or be rough.
* If less than 20 frames are tracked in a chapter, they will not be saved.
* Face recognition is not performed in every frame, but the object at the position of the first recognized face is tracked in subsequent frames. Therefore, if one chapter is long, the tracking position will gradually shift. It is easier to obtain good results if you break the chapter appropriately and perform face recognition again. You can also reset the face recognition by pressing the "r" key in the preview screen.
* Hands are image recognized in every frame. Only one hand is recognized. If more than one hand is captured, the one with the highest level of confidence is given priority. Although there is no gradual shift in recognition, there are cases where the hand that is not moving is recognized, so it is recommended that the unnecessary parts be discarded by dividing them appropriately.
