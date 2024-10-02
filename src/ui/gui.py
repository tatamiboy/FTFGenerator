import os
from tkinter import ttk
import tkinter as tk
import tkinter.filedialog as fd

from config import settings 
from tracker import Tracker
from file_handler import file_handler as fh

if settings.LANG == "en":
    from config.constants import TEXT_EN as TEXT
elif settings.LANG == "jp":
    from config.constants import TEXT_JP as TEXT

class GUI() :

    def __init__(self):
        self.__root = tk.Tk() 

        self.__root.geometry(settings.MAIN_WINDOW_SIZE)
        self.__root.title("FTFGenerator")

        self.__root.update()

        direction = [TEXT["topBottom"],
                     TEXT["bottomTop"],
                     TEXT["rightLeft"],
                     TEXT["leftRight"],
                     TEXT["topRightBottomLeft"],
                     TEXT["bottomLeftTopRight"],
                     TEXT["bottomRightTopLeft"],
                     TEXT["topLeftBottomRight"],
                     ]
        targets = ["Face", "Hand"]

        self.__sv_video = tk.StringVar()
        self.__sv_chapter = tk.StringVar()
        self.__sv_result = tk.StringVar()
        self.__state_autosampling = tk.BooleanVar()

        btn_frame = tk.Frame(self.__root)
        btn_open = tk.Button(btn_frame, text=TEXT["openVideo"], command=self.__on_open_clicked)
        btn_open.pack(side="left", pady=5)
        btn_open_chapter = tk.Button(btn_frame, text=TEXT["openChapter"], command=self.__on_open_chapter_clicked)
        btn_open_chapter.pack(side="left", pady=5)
        btn_frame.pack()

        video_wrapper = tk.Frame(self.__root)
        video_wrapper.pack(fill="x")
        video_label = tk.Label(video_wrapper, text=TEXT["videoFile"], width=10)
        video_label.pack(side="left", padx=10)
        video_txt = tk.Entry(video_wrapper, state="readonly", textvariable=self.__sv_video)
        video_txt.pack(side="left",fill="x", expand=True, padx=10)
        chapter_wrapper = tk.Frame(self.__root)
        chapter_wrapper.pack(fill=tk.X)
        chapter_label = tk.Label(chapter_wrapper, text=TEXT["chapterFile"], width=10)
        chapter_label.pack(side="left", padx=10)
        self.__chapter_txt = tk.Entry(chapter_wrapper, state="readonly", textvariable=self.__sv_chapter)
        self.__chapter_txt.pack(side="left",fill=tk.X, expand=True, padx=10)

        target_wrapper = tk.Frame(self.__root)
        target_label = tk.Label(target_wrapper, text=TEXT["target"], wraplength=int(self.__root.winfo_width() * 0.8))
        target_label.pack()
        self.__combobox_target = ttk.Combobox(target_wrapper, values=targets, state="readonly")
        self.__combobox_target.current(0)
        self.__combobox_target.pack()
        target_wrapper.pack(pady=10)

        tk.Label(self.__root, text=TEXT["trackingDir"]
                 , wraplength=int(self.__root.winfo_width() * 0.8)).pack()
        dir_wrapper = tk.Frame(self.__root, bg="red")
        tk.Label(dir_wrapper, text="100 <- ", justify="center").pack(side="left")
        self.__combobox_direction = ttk.Combobox(dir_wrapper
                                               , values=direction, state="readonly"
                                               , justify="center")
        self.__combobox_direction.current(0)
        self.__combobox_direction.pack(side="left")
        tk.Label(dir_wrapper, text=" -> 0", justify="center").pack(side="left")
        dir_wrapper.pack(pady=10)
        
        checkbox_autosampling = tk.Checkbutton(self.__root, text=TEXT["autoSampling"], variable=self.__state_autosampling)
        checkbox_autosampling.pack()
        btn_run = tk.Button(self.__root, text=TEXT["run"], command=self.__on_run_clicked)
        btn_run.pack(pady=10)
        result_label = tk.Label(self.__root, textvariable=self.__sv_result, wraplength=int(self.__root.winfo_width() * 0.8))
        result_label.pack()

    # 動画ファイルを開く
    def __on_open_clicked(self) -> list:
        filter = ("Video Files", "*.avi *.mp4 *.mov *.mkv") if os.name == "nt" \
                 else ("Video Files", "*.avi *.mp4 *.mov *.mkv")
        video_path = fd.askopenfilename(filetypes=[
            filter,
            ("All Files", "*.*")
        ])
        if not video_path:
            return 
        self.__dirname = os.path.dirname(video_path)
        self.__basename = os.path.splitext(os.path.basename(video_path))[0]
        chapter_filename = self.__basename + ".txt"
        chapter_path = os.path.join(self.__dirname, chapter_filename)

        self.__sv_video.set(video_path)
        if os.path.exists(chapter_path):
            self.__sv_chapter.set(chapter_path)
        else : self.__sv_chapter.set("")
        self.__sv_result.set("")
        
    def __on_open_chapter_clicked(self):
        chapter_path = fd.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not chapter_path:
            self.__sv_chapter.set("")
            return
        self.__sv_chapter.set(chapter_path)
        self.__sv_result.set("")

    # トラッキングを実行
    def __on_run_clicked(self):
        self.__sv_result.set("")
        if not os.path.exists(self.__sv_video.get()):
            print("Video file not found.")
            return

        self.__root.withdraw() 
        tracker = Tracker(self.__sv_video.get(),
                          self.__combobox_target.current(),
                          self.__combobox_direction.current(),
                          self.__state_autosampling.get(),
                          self.__chapter_txt.get()) 
        
        # json形式で出力.
        je = fh.JsonFileExporter(*tracker.track())
        export_result = je.export(self.__dirname, self.__basename, self.__combobox_target.current())
        self.__root.deiconify()
        if export_result:
            self.__sv_result.set(str.format(TEXT["resultDone"], export_result))        
        del tracker
    
    def start(self):
        self.__root.mainloop()