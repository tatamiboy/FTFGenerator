import os, json, datetime

from config.constants import Targets
from config import settings

def read_chapters(filepath) -> list:
    chapter_list = []
    if filepath and os.path.exists(filepath):
        with open(filepath, mode="r") as file:
            for line in file.readlines() :
                if line.strip():
                    chapter_list.append(tuple([float(var) for var in str.split(line, ":")]))
    return chapter_list

class JsonFileExporter:
    __json_obj = None
    def __init__(self, time_list, pos_list) -> None:
        # 配列からjsonを構築.
        if not time_list or not pos_list:
            return
        dict_list = [{"at": int(t), "pos": int(p)} for t, p in zip(time_list, pos_list)]
        dict_list = sorted(dict_list, key=lambda x:x['at'])
        di =  {"actions" : dict_list}
        self.__json_obj = json.dumps(di)

    # ファイルに出力.
    def export(self, dir, basename, type = Targets.FACE) -> str | None: #return output filename
        if not self.__json_obj:
            return None
        
        suffix = ""
        if type == Targets.FACE:
            suffix = ".face"
        elif type == Targets.HAND:
            suffix = ".hand"
        scriptname = os.path.join(dir, basename + suffix + ".funscript")
        if os.path.exists(scriptname) :
            scriptname = os.path.join(dir, basename + "." + str(datetime.datetime.now()) + suffix + ".funscript")
        if os.name == "nt":
            scriptname = str.replace(scriptname, ":", "-")
        with open(scriptname, "w") as file:
            if file.write(self.__json_obj):
                return scriptname
            else : return None
