import os
from tracker.tracker import Tracker
import file_handler.file_handler as fh
from config import constants as const

class CLI:

    def __init__(self, video_path, target, direction, auto_sample, chapter_path):
        self.__video_path = video_path
        self.__auto_sample = auto_sample
        self.__chapter_path = chapter_path

        if target < len(const.Targets) and 0 <= target:
            self.__target = target
        else :
            print("Invalid target value. Set to Face mode.")
            self.__target = 0
        if direction < len(const.Directon) and 0 <= direction:
            self.__direction = direction
        else :
            print("Invalid direction value. Set to Top/Down mode.")
            self.__direction = 0

        self.__dirname = os.path.dirname(video_path)
        self.__basename = os.path.splitext(os.path.basename(video_path))[0]

        # チャプターファイルが未指定のときは動画と同名のtxtファイルがあるか調べる.
        if not chapter_path:
            chapter_filename = self.__basename + ".txt"
            chapter_path = os.path.join(self.__dirname, chapter_filename)
            if os.path.exists(chapter_path):
                self.__chapter_path = chapter_path

    # トラッキングを実行
    def run(self):
        if not os.path.exists(self.__video_path):
            print(self.__video_path + " : Video file not found.")
            return

        tracker = Tracker(self.__video_path
                        , self.__target
                        , self.__direction
                        , self.__auto_sample
                        , self.__chapter_path) 
        
        # json形式で出力.
        je = fh.JsonFileExporter(*tracker.track())
        export_result = je.export(self.__dirname, self.__basename, self.__target)
        if not export_result:
            del tracker
            return
        if not export_result:
            print("Export failed.")
        else :print("Exported to : " + export_result)
        del tracker
