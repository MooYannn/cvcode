import cv2
import numpy as np

# 固定窗口大小
WIN_WIDTH, WIN_HEIGHT = 900, 700

# 颜色
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
BLUE = (89, 153, 255)
BLACK = (0, 0, 0)
GREEN = (40, 200, 40)
RED = (40, 40, 200)

# 初始HSV阈值
hsv_names = ["H_min", "H_max", "S_min", "S_max", "V_min", "V_max"]
hsv_min = [0, 0, 0]
hsv_max = [179, 255, 255]
hsv_vals = [hsv_min[0], hsv_max[0], hsv_min[1], hsv_max[1], hsv_min[2], hsv_max[2]]
hsv_lims = [0, 0, 0, 0, 0, 0]  # min for each
hsv_maxs = [179, 179, 255, 255, 255, 255]  # max for each

# 状态枚举
MENU_MAIN = 0
MENU_HSV_CONFIG = 1
MENU_HSV_SET = 2
MENU_HSV_DETECT = 3
menu_state = MENU_MAIN

# 二值化模式
binarize_mode = False

# 按钮区域定义
btns_main = [
    (320, 200, 620, 270, 'HSV Threshold Setting'),
    (320, 330, 620, 400, 'HSV Detection')
]
btns_set = [
    (50, 600, 200, 670, 'Back to Menu'),
    (700, 600, 850, 670, 'Save & Back'),
    (350, 600, 550, 670, 'Show Binary')
]
btns_detect = [
    (700, 600, 850, 670, 'Back to Menu')
]

# HSV参数显示区域
param_x0 = 670
param_y0 = 120
param_gap = 36
param_font = cv2.FONT_HERSHEY_SIMPLEX
param_font_scale = 0.65
param_font_thick = 2
param_areas = []
for i in range(6):
    y1 = param_y0 + i * param_gap
    param_areas.append((param_x0, y1 - 8, param_x0 + 140, y1 + 22))

# 单独参数的加减按钮，初始位置
adj_btns = [
    (param_x0 + 120, param_y0 - 6, param_x0 + 160, param_y0 + 18, '-'),
    (param_x0 + 180, param_y0 - 6, param_x0 + 220, param_y0 + 18, '+')
]
selected_param = -1  # 当前选中的HSV参数

def point_in_rect(x, y, rect):
    return rect[0] <= x <= rect[2] and rect[1] <= y <= rect[3]


#触摸回调函数
def mouse_callback(event, x, y, flags, param):
    global menu_state, selected_param, hsv_min, hsv_max, hsv_vals, adj_btns, binarize_mode
    if menu_state == MENU_MAIN:
        if event == cv2.EVENT_LBUTTONDOWN:
            for i, btn in enumerate(btns_main):
                if point_in_rect(x, y, btn):
                    if i == 0:
                        menu_state = MENU_HSV_CONFIG
                    elif i == 1:
                        menu_state = MENU_HSV_DETECT
    elif menu_state == MENU_HSV_CONFIG:
        if event == cv2.EVENT_LBUTTONDOWN:
            menu_state = MENU_HSV_SET
    elif menu_state == MENU_HSV_SET:
        if event == cv2.EVENT_LBUTTONDOWN:
            # 按钮
            if point_in_rect(x, y, btns_set[0]):
                menu_state = MENU_MAIN
            if point_in_rect(x, y, btns_set[1]):
                # 保存当前参数
                hsv_min[0], hsv_max[0], hsv_min[1], hsv_max[1], hsv_min[2], hsv_max[2] = hsv_vals
                menu_state = MENU_MAIN
            if point_in_rect(x, y, btns_set[2]):
                binarize_mode = not binarize_mode
            # 选择参数
            for i, rect in enumerate(param_areas):
                if point_in_rect(x, y, rect):
                    selected_param = i
                    # 更新加减按钮区域位置
                    ay = param_y0 + i * param_gap - 6
                    adj_btns[0] = (param_x0 + 150, ay, param_x0 + 180, ay + 24, '-')
                    adj_btns[1] = (param_x0 + 190, ay, param_x0 + 220, ay + 24, '+')
            # 加减
            if selected_param != -1:
                idx = selected_param
                # 减号
                if point_in_rect(x, y, adj_btns[0]):
                    step = 2
                    if idx % 2 == 1:  # Max参数
                        print("max-",idx)
                        lower = hsv_vals[idx - 1] + 1
                        hsv_vals[idx] = max(lower, hsv_vals[idx] - 5)
                    else:  # Min参数
                        print("min-",idx)
                        upper = hsv_vals[idx] - 1
                        hsv_vals[idx] = max(hsv_lims[idx], min(upper, hsv_vals[idx] -5))
                # 加号
                if point_in_rect(x, y, adj_btns[1]):
                    step = 2
                    if idx % 2 == 0:  # Min参数
                        print("min+",idx)
                        upper = hsv_vals[idx + 1] - 1
                        hsv_vals[idx] = min(upper, hsv_vals[idx] + 5)
                    else:  # Max参数
                        lower = hsv_vals[idx - 1] + 1 
                        print("max+",idx)
                        hsv_vals[idx] = min(hsv_maxs[idx], max(lower, hsv_vals[idx] +5))
    elif menu_state == MENU_HSV_DETECT:
        if event == cv2.EVENT_LBUTTONDOWN:
            if point_in_rect(x, y, btns_detect[0]):
                menu_state = MENU_MAIN

cv2.namedWindow('MultiMenu', cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback('MultiMenu', mouse_callback)
cap = cv2.VideoCapture(0)

while True:
    canvas = np.ones((WIN_HEIGHT, WIN_WIDTH, 3), np.uint8) * 255
    
    #主界面
    if menu_state == MENU_MAIN:
        cv2.putText(canvas, 'Main Menu', (WIN_WIDTH // 2 - 110, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, BLUE, 2)
        for btn in btns_main:
            cv2.rectangle(canvas, (btn[0], btn[1]), (btn[2], btn[3]), BLUE, -1)
            cv2.putText(canvas, btn[4], (btn[0] + 20, btn[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, WHITE, 2)
    elif menu_state == MENU_HSV_CONFIG:
        cv2.putText(canvas, 'Click to Enter HSV Setting', (200, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, BLACK, 2)
        cv2.rectangle(canvas, (180, 250), (WIN_WIDTH - 180, 370), BLUE, 2)
    #HSV参数设置界面
    elif menu_state == MENU_HSV_SET:
        # 摄像头画面区域：宽640，高480
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (640, 480))
            canvas[30:510, 10:650] = frame

        # HSV参数数值显示
        for i, rect in enumerate(param_areas):
            cv2.rectangle(canvas, (rect[0], rect[1]), (rect[2], rect[3]), BLUE if i == selected_param else GRAY, 2)
            text = f"{hsv_names[i]}: {hsv_vals[i]}"
            cv2.putText(canvas, text, (rect[0] + 8, rect[1] + 20), param_font, param_font_scale, BLACK, 1)

        # 仅为选中参数显示加减按钮
        if selected_param != -1:
            for btn in adj_btns:
                cv2.rectangle(canvas, (btn[0], btn[1]), (btn[2], btn[3]), BLUE, -1)
                cv2.putText(canvas, btn[4], (btn[0] + 9, btn[1] + 19), param_font, 0.95, WHITE, 2)

        # 二值化预览
        if binarize_mode and ret:
            hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(
                hsv_img,
                np.array([hsv_vals[0], hsv_vals[2], hsv_vals[4]]),
                np.array([hsv_vals[1], hsv_vals[3], hsv_vals[5]])
            )
            bin_show = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            bin_show = cv2.resize(bin_show, (640, 480))
            canvas[30:510, 10:650] = bin_show
            cv2.rectangle(canvas, (420, 520), (640, 700), RED, 2)
        # 按钮
        for btn in btns_set:
            color = RED if btn[4] == 'Show Binary' and binarize_mode else BLUE
            cv2.rectangle(canvas, (btn[0], btn[1]), (btn[2], btn[3]), color, -1)
            cv2.putText(canvas, btn[4], (btn[0] + 10, btn[1] + 40), param_font, 0.6, WHITE, 2)
    #检测界面，可在改界面下实现其他的操作
    elif menu_state == MENU_HSV_DETECT:
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (640, 480))
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(
                hsv,
                np.array(hsv_min),
                np.array(hsv_max)
            )
            result = cv2.bitwise_and(frame, frame, mask=mask)
            canvas[100:580, 130:770] = result
            cv2.rectangle(canvas, (130, 100), (770, 580), BLUE, 2)
        #绘制的返回主界面的按钮
        for btn in btns_detect:
            cv2.rectangle(canvas, (btn[0], btn[1]), (btn[2], btn[3]), RED, -1)
            cv2.putText(canvas, btn[4], (btn[0] + 10, btn[1] + 50), param_font, 1, WHITE, 2)

    cv2.imshow('MultiMenu', canvas)
    key = cv2.waitKey(30)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()