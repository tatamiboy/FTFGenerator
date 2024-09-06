LANG = "en" # jp or en

PROTOTYPE_PATH = "deploy.prototxt" # .prototxt file for DNN. Absolute path or relative path from "main.py". 
CAFFEMODEL_PATH = "res10_300x300_ssd_iter_140000.caffemodel" # .caffemodel for DNN. Absolute path or relative path from "main.py". 
# CASCADE_FACE_CASCADE_PATH = "haarcascade_frontalface_default.xml" # .xml path  for Haar-Cascade.

DEFAULT_OFFSET = 0 # Default time offset.(ms)
INITIAL_SAMPLE_EPSILON = 2.5 # Default down-sampling rate. 0 to keep original.
PROC_FRAME_WIDTH = -1 # You can specify the frame size to be used for processing. If you specify "-1", the processing will be done at the original size.

MAIN_WINDOW_SIZE = "640x480"
PREVIEW_WINDOW_WIDTH = 960
PREVIEW_WINDOW_HEGHT = 540
FONT_COLOR = (0, 128, 255) # Font Color in preview window. (B, G, R)
