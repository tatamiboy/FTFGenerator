from rdp import rdp
import math, numpy as np
from config.constants import Directon

def downsample(x, y, rate):  
    sampled = rdp(list(zip(x, y)), rate)
    return sampled

# 配列を0-100にマッピング.
def map_array_value(array, invert = False) :
        max = np.amax(array) if not invert else np.amin(array)
        min = np.amin(array) if not invert else np.amax(array)
        li = []
        for val in array:
            li.append(int(0 + (0 - 100) * (val - min) / (min - max)))
        return np.array(li)

# 座標配列から対角線方向の移動距離を計算.
def calculate_diagonal_moving_distance(direction, pos_array: np.array, frame_size): # pos_array: [[x, x1, ...], [y, y1, ...]], frame_size: [width, height]
    y_origin = None
    m_diagonal = None # 対角線の傾き.
    if direction == Directon.TOPLEFT_BOTTOMRIGHT or direction == Directon.BOTTOMRIGHT_TOPLEFT:
        y_origin = 0
        m_diagonal = frame_size[1] / frame_size[0]

    elif direction == Directon.TOPRIGHT_BOTTOMLEFT or direction == Directon.BOTTOMLEFT_TOPRIGHT:
        y_origin = frame_size[1]
        m_diagonal = -1 * frame_size[1] / frame_size[0]
    else : 
        return None

    m_perpendicular = -1 / m_diagonal # 対角線に対する垂線の傾き.
    
    inverted_pos_array = pos_array.T
    intersection_list = []
    for pos in inverted_pos_array:
        x, y = pos[:2]
        b = y - m_perpendicular * x # 指定点を通る垂線のy切片.
        x_intersection  = b / (m_diagonal - m_perpendicular)
        y_intersection  = m_perpendicular * x_intersection + b
        distance = math.sqrt(x_intersection ** 2 + abs(y_origin - y_intersection) ** 2)
        intersection_list.append(distance)
    if direction == Directon.TOPLEFT_BOTTOMRIGHT:
         return map_array_value(np.array(intersection_list), True)
    return map_array_value(np.array(intersection_list))


# 座標配列から水平垂直方向の移動距離を計算.
def calculate_moving_distance(direction, pos_array: np.array, frame_size = None): # pos_array: [[x, x1, ...], [y, y1, ...]], frame_size: (width, height)
    pos = None
    # 上下左右方向.
    if  direction == Directon.TOP_BOTTOM:
        pos = map_array_value(pos_array[1], True)
    elif direction == Directon.BOTTOM_TOP:
        pos = map_array_value(pos_array[1])
    elif direction == Directon.RIGHT_LEFT:
        pos = map_array_value(pos_array[0])
    elif direction == Directon.LEFT_RIGHT:
        pos = map_array_value(pos_array[0], True)
    if pos is not None : return pos

    # 対角線方向の場合.
    if frame_size is not None:
        return calculate_diagonal_moving_distance(direction, pos_array, frame_size)