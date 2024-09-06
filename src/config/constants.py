from enum import IntEnum

class Targets(IntEnum): #チャプターファイルの目標列、GUIのコンボボックスの値と合わせる.
        FACE = 0,
        HAND = 1,

class Directon(IntEnum): #チャプターファイルの方向列、GUIのコンボボックスの値と合わせる.
        TOP_BOTTOM = 0,
        BOTTOM_TOP = 1,
        RIGHT_LEFT = 2,
        LEFT_RIGHT = 3,
        TOPRIGHT_BOTTOMLEFT = 4,
        BOTTOMLEFT_TOPRIGHT = 5,
        BOTTOMRIGHT_TOPLEFT = 6,
        TOPLEFT_BOTTOMRIGHT = 7,

TEXT_EN = {
    "videoFile": "Video",
    "chapterFile": "Chapter",
    "openVideo":"Open video file...",
    "openChapter":"Open chapter file...",
    "target":"Tracking target",
    "trackingDir":"Tracking direction\n(In case there is no chapter list or the list does not have a directional element.)",
    "autoSampling" : "Auto downsampling",
    "run":"Run",
    "resultDone":"Output to :\n{}",
    "topBottom":"Top/Bottom", 
    "bottomTop": "Bottom/Top",
    "rightLeft":"Right/Left", 
    "leftRight": "Left/Right",
    "topRightBottomLeft":"Top Right/Bottom Left", 
    "bottomLeftTopRight": "Bottom Left/Top Right",
    "bottomRightTopLeft": "Bottom Right/Top Left",
    "topLeftBottomRight":"Top Left/Bottom Right", 
}

TEXT_JP = {
    "videoFile": "動画",
    "chapterFile": "チャプター",
    "openVideo":"動画を開く...",
    "openChapter":"チャプターファイルを開く...",
    "target":"トラッキング目標",
    "trackingDir":"トラッキング方向\n(チャプターファイルがない、もしくはファイル内で方向が指定されていない場合)",
    "autoSampling" : "自動ダウンサンプリング",
    "run":"実行",
    "resultDone":"{}\nに保存しました。",
    "topBottom":"上/下", 
    "bottomTop": "下/上",
    "rightLeft":"右/左", 
    "leftRight": "左/右",
    "topRightBottomLeft":"右上/左下", 
    "bottomLeftTopRight": "左下/右上",
    "bottomRightTopLeft": "右下/左上",
    "topLeftBottomRight":"左上/右下", 
}
