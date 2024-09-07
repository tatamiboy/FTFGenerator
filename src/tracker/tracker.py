import cv2, math, os
import numpy as np
import mediapipe as mp

from tracker import utils, visualizer as vs
from file_handler import file_handler as fh
import config.settings as settings
from config.constants import Targets ,Directon

print(cv2.__version__)

class Tracker :

    __tracker = None
    __sample_epsilon = settings.INITIAL_SAMPLE_EPSILON

    def __init__(self, video_path:str, target = int(Targets.FACE), direction = int(Directon.TOP_BOTTOM), auto_sample = False, chapter_path:str = None):
        self.__video_path = video_path
        self.__auto_sample = auto_sample
        self.__default_direction = direction
        self.__chapter_list = fh.read_chapters(chapter_path)

        if target ==  Targets.FACE:
            proto_path = settings.PROTOTYPE_PATH
            caffe_path = settings.CAFFEMODEL_PATH
            if not os.path.isabs(proto_path): # 相対パスはmain.pyから.
                dirname = os.path.dirname(__file__)
                rootDir = os.path.dirname(dirname)
                proto_path = os.path.join(rootDir, proto_path)
            if not os.path.isabs(caffe_path):
                dirname = os.path.dirname(__file__)
                rootDir = os.path.dirname(dirname)
                caffe_path = os.path.join(rootDir, caffe_path)

            if not os.path.exists(proto_path) or not os.path.exists(caffe_path):
                print("Model data not found.")
            self.__dnn_net = cv2.dnn.readNetFromCaffe(proto_path, caffe_path)
            self.__detection_mode = "DNN"
        # elif target == self.__Target.FACE_CASCADE:
        #     dirname = os.path.dirname(__file__)
        #     self.__cascade = cv2.CascadeClassifier(os.path.join(dirname, settings.CASCADE_FACE_CASCADE_PATH))
        #     self.__detection_mode = "cascade"
        elif target == Targets.HAND:
            self.__mp_hands = mp.solutions.hands
            self.__hands = self.__mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
            self.__detection_mode = "mp_hands"

    # トラッキング対象を検出してトラッカーを初期化.
    def __initialize_tracker(self, frame) -> tuple:
        (fh, fw) = frame.shape[:2]
        (x ,y, w, h) = None, None, None, None  # return value
        self.__tracker = cv2.TrackerCSRT_create()
        if self.__detection_mode == "DNN":
            # DNNを使って顔検出
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
            self.__dnn_net.setInput(blob)
            detections = self.__dnn_net.forward()
            if detections.shape[2] > 0:
                confidence = detections[0, 0, 0, 2]
                if confidence > 0.3:  # 信頼度
                    box = detections[0, 0, 0, 3:7] * np.array([fw, fh, fw, fh])
                    (x, y, x2, y2) = box.astype("int")
                    x, y, w, h = min(x, x2), min(y, y2), abs(x2 - x), abs(y2 - y)            
                
        # elif self.__detection_mode == "cascade" :
        #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #     faces = self.__cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))     
        #     if len(faces) > 0:
        #         (x, y, w, h) = faces[0]
        
        # ボックスがフレーム外に出ないかチェックしてからトラッカーに設定.
        if all((x ,y, w, h)):
            x = max(0, x)
            y = max(0, y)
            w = min(w, fw - x)
            h = min(h, fh -y)
            self.__tracker.init(frame, (x ,y, w, h))
            return x ,y, w, h
    
    def __track_hand(self, frame):
        (fh, fw) = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.__hands.process(rgb)
        if results.multi_hand_landmarks:
            mp_draw = mp.solutions.drawing_utils
            x, y = None, None
            for hand_landmarks in results.multi_hand_landmarks: 
                #hand_landmarks.landmark[2],   # 親指の付け根
                #hand_landmarks.landmark[5],   # 人差し指の付け根
                x = hand_landmarks.landmark[9].x   # 中指の付け根
                y = hand_landmarks.landmark[9].y   # 中指の付け根
                #hand_landmarks.landmark[13],  # 薬指の付け根
                #hand_landmarks.landmark[17]   # 小指の付け根
                mp_draw.draw_landmarks(frame, hand_landmarks, self.__mp_hands.HAND_CONNECTIONS)

            # フレーム内座標に変換.
            return int(x * fw), int(y * fh)
        return None

    def track(self) -> tuple:
        time_list, pos_list = [], [] # for return

        cap = cv2.VideoCapture(self.__video_path)
        if not cap.isOpened():
            print("Video open error: {__video_path} is not a video file.")
            return None, None

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        quit = False

        if not self.__chapter_list: # チャプターリストが空の場合は全フレーム対象.
            self.__chapter_list = [(0, int(frame_count / fps), self.__default_direction)]
        for idx, chapter in enumerate(self.__chapter_list):
            pos_x = []
            pos_y = []
            at = []
            start_at, end_at = chapter[:2]
            direction = int(chapter[2]) if 3 <= len(chapter) else self.__default_direction
            
            # 開始と終了フレーム
            start_frame = int(start_at * fps)
            end_frame = int(end_at * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            print("Chapter : " + str(idx + 1))
            print("Start frame : " + str(start_frame))
            print("End frame : " + str(end_frame))
            print("Direction : " + list(Directon.__members__.keys())[direction])

            initialized = False
            while True:
                ret, frame = cap.read()
                if 0 < settings.PROC_FRAME_WIDTH:
                    frame = cv2.resize(frame, (int(settings.PROC_FRAME_WIDTH), int(frame.shape[0] * settings.PROC_FRAME_WIDTH / frame.shape[1])))
                if not ret:
                    break

                # 手はトラッキングがうまくいかなかったので全フレームを画像認識.
                if self.__detection_mode == "mp_hands":
                    results = self.__track_hand(frame)
                    if results :
                        at.append(math.floor(cap.get(cv2.CAP_PROP_POS_MSEC)) - settings.DEFAULT_OFFSET)
                        pos_x.append(results[0])
                        pos_y.append(results[1])
                        cv2.circle(frame, results, 8, (255, 0, 0), -1)

                # 追跡対象が見つかるまでは画像認識にかける.
                elif not initialized:
                    bbox = self.__initialize_tracker(frame)
                    if bbox is not None:
                        initialized = True
                        print("Detected")
                else:
                    # トラッカーを使って顔を追跡.
                    success, bbox = self.__tracker.update(frame)
                    if success:
                        (x, y, w, h) = [int(v) for v in bbox]
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                        center = int(x + w / 2), int(y + h / 2)
                        at.append(math.floor(cap.get(cv2.CAP_PROP_POS_MSEC)) - settings.DEFAULT_OFFSET)
                        pos_x.append(center[0])
                        pos_y.append(center[1])
                        cv2.circle(frame, center, 8, (255, 0, 0), -1)
                    else:
                        cv2.putText(frame, "Tracking failure", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 2)
                        initialized = False

                current_frame_count = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                # 現在の再生時間を取得（ミリ秒単位）
                current_time_msec = cap.get(cv2.CAP_PROP_POS_MSEC)
                current_time_sec = current_time_msec / 1000.0

                # フレーム番号と時間を表示
                font_height = int(frame.shape[0] / 50) # フォントの高さをフレーム高の1/10に.
                font_scale = cv2.getFontScaleFromHeight(cv2.FONT_HERSHEY_SIMPLEX, font_height)
                cv2.putText(frame, f"Direction: {list(Directon.__members__.keys())[direction]}", (10, (font_height + 5)), cv2.FONT_HERSHEY_SIMPLEX, font_scale, settings.FONT_COLOR, 2)
                cv2.putText(frame, f"Chapter: {idx + 1}", (10, (font_height + 5) * 2), cv2.FONT_HERSHEY_SIMPLEX, font_scale, settings.FONT_COLOR, 2)
                cv2.putText(frame, f"Frame: {current_frame_count} / {frame_count}", (10, (font_height + 5) * 3), cv2.FONT_HERSHEY_SIMPLEX, font_scale, settings.FONT_COLOR, 2)
                cv2.putText(frame, f"Time: {current_time_sec:.2f} sec", (10, (font_height + 5) * 4), cv2.FONT_HERSHEY_SIMPLEX, font_scale, settings.FONT_COLOR, 2)
                cv2.putText(frame, "Press \"q\" to stop tracking.", (10, (font_height + 5) * 5), cv2.FONT_HERSHEY_SIMPLEX, font_scale, settings.FONT_COLOR, 2)
                cv2.putText(frame, "Press \"r\" to reset detection. (face mode only)", (10, (font_height + 5) * 6), cv2.FONT_HERSHEY_SIMPLEX, font_scale, settings.FONT_COLOR, 2)

                frame = cv2.resize(frame, (settings.PREVIEW_WINDOW_WIDTH, settings.PREVIEW_WINDOW_HEGHT))
                cv2.imshow('Preview', frame)
                key = cv2.waitKey(1) & 0xFF

                # 終了フレームまで来たら終了
                if current_frame_count == end_frame:
                    break
                # qキーで終了
                if key == ord("q"):
                    quit = True
                    print("Interrupted.")
                    break
                # rキーで顔認識をリセット.
                if key == ord("r"):
                    print("Reset face recognition.")
                    initialized = False

            # トラッキングできたフレームが20未満のときは無視.
            if len(at) < 20 :
                continue

            # 指定した方向の動きだけ拾う. チャプターファイル or デフォルト値の方向によって分岐
            pos = []
            pos = utils.calculate_moving_distance(direction, np.array((pos_x, pos_y)), [frame.shape[1], frame.shape[0]])
            if pos is None:
                break
            
            tracked_positions = None
            # 自動サンプル時はウィンドウ表示せずに初期値でダウンサンプリング. Listのタプルにしておく.
            if self.__auto_sample :
                sampled_points = utils.downsample(np.array(at), pos, self.__sample_epsilon)
                tracked_positions = [point[0] for point in sampled_points], [point[1] for point in sampled_points]
            # それ以外では グラフを表示する
            else : 
                cv2.destroyWindow('Preview')
                tracked_positions = vs.Visualizer().plot(np.array(at), pos)

            if tracked_positions:
                time_list.extend(tracked_positions[0])
                pos_list.extend(tracked_positions[1])
            if quit :
                break
            
        cap.release()
        cv2.destroyAllWindows()
        return time_list, pos_list
    
    
    

    
        
