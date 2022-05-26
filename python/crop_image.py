import cv2
import numpy as np

# 指定した画像(path)の物体を検出し、外接矩形の画像を出力します
def detect_contour(path):

    # 画像を読込
    src = cv2.imread(path, cv2.IMREAD_COLOR)
    # 出力用画像
    src_w = cv2.imread(path, cv2.IMREAD_COLOR)
    # 画像の大きさ
    height, width, channels = src.shape[:3]
    
    # グレースケール画像へ変換
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    # 2値化
    retval, bw = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite('images/bin_ball.jpg', bw)
    
    # 輪郭抽出
    contours, hierarchy = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    # 生成画像のカウント
    detect_count = 0

    for i in range(0, len(contours)):
        # 輪郭の面積
        area = cv2.contourArea(contours[i])

        #　ノイズ除去
        if area < 1e3:
            continue
        
        # 外接矩形
        if len(contours[i]) > 0:
            rect = contours[i]
            x, y, w, h = cv2.boundingRect(rect)
        
            cv2.rectangle(src, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # 余白を考慮して画像を保存
            if x - w * 0.15 >= 0 and x + w * 1.15 < width:#横幅の確保ができるとき
                if y - h * 0.15 >= 0 and y + h * 1.15 < height:#縦幅の確保ができるとき
                    cv2.imwrite('images/' + str(detect_count) + 'ball.jpg', src_w[y - int(h * 0.15):y + int(h * 1.15), x - int(w * 0.15):x + int(w * 1.15)])
                else:
                    cv2.imwrite('images/' + str(detect_count) + 'ball.jpg', src_w[y:y + h, x - int(w * 0.15):x + int(w * 1.15)])
            else:
                if y - h * 0.15 >= 0 and y + h * 1.15 < height:#縦幅の確保ができるとき 
                    cv2.imwrite('images/' + str(detect_count) + 'ball.jpg', src_w[y - int(h * 0.15):y + int(h * 1.15), x:x + w]) 
                else:   
                    cv2.imwrite('images/' + str(detect_count) + 'ball.jpg', src_w[y:y + h, x:x + w])

            detect_count = detect_count + 1

if __name__ == '__main__':
    detect_contour('images/ball.jpg')