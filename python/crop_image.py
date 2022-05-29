import cv2
import numpy as np

class cropImage:
    # 画像を回転させる
    def rotate_img(self, directory, name):

        # 画像を読込
        src = cv2.imread(directory+name, cv2.IMREAD_COLOR)
        # 出力用画像
        src_w = cv2.imread(directory+name, cv2.IMREAD_COLOR)
        # 画像の大きさ
        height, width, channels = src.shape[:3]
        
        # グレースケール画像へ変換
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

        # 2値化
        retval, bw = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        #cv2.imwrite('python/images/bin.jpg', bw)
        
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
            
            # 外接矩形（回転を含む）
            if len(contours[i]) > 0:
                #rect = contours[i]
                rect = cv2.minAreaRect(contours[i])
                #print(rect)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                #im = cv2.drawContours(src,[box],0,(0,0,255),2)
                
                #外接矩形の角度を求める
                if (rect[2] > 0 and rect[2] < 45) or (rect[2] > 90 and rect[2] < 135):
                    angle = -rect[2]
                elif rect[2] > 45 and rect[2] < 90:
                    angle = - 90 + rect[2]
                elif rect[2] > 135 and rect[2] < 180:    
                    angle = -180 + rect[2]
                else:
                    angle = 0            
                
                #scaleは倍率
                scale = 1
                mat = cv2.getRotationMatrix2D((width/2, height/2), angle, scale)
                
                #画像の回転
                affine_img = cv2.warpAffine(src, mat, (width, height), borderValue = (255,255,255))
                affine_img_w = cv2.warpAffine(src_w, mat, (width, height), borderValue = (255,255,255))
                #cv2.imwrite('python/images/affine.jpg', affine_img)
        
        
        #画像をトリミングする
        def detect_contour(directory, name, img, img_w):
            height, width, channels = img.shape[:3]
        
            # グレースケール画像へ変換
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # 2値化
            retval, bw = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
            
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
                
                #外接矩形をもう一度取る（角度なし)
                x, y, w, h = cv2.boundingRect(contours[i])
                
                if len(contours[i]) > 0:
                    cv2.rectangle(src, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # 余白を考慮して画像を保存
                    if x - w * 0.15 >= 0 and x + w * 1.15 < width:#横幅の確保ができるとき
                        if y - h * 0.15 >= 0 and y + h * 1.15 < height:#縦幅の確保ができるとき
                            if width == height:#すでに正方形だったら
                                cv2.imwrite(directory + str(detect_count) + name, affine_img_w[y - int(h * 0.15):y + int(h * 1.15), x - int(w * 0.15):x + int(w * 1.15)])
                            elif w > h:#横幅が大きければ
                                diff = (w - h)//2#余白の大きさ
                                output_img = cv2.copyMakeBorder(affine_img_w[y - int(h * 0.15):y + int(h * 1.15), x - int(w * 0.15):x + int(w * 1.15)], diff, diff, 0, 0, cv2.BORDER_CONSTANT, value = [255,255,255])
                                cv2.imwrite(directory + str(detect_count) + name, output_img)
                            else:#縦幅が大きければ
                                diff = (h - w)//2#余白の大きさ
                                output_img = cv2.copyMakeBorder(affine_img_w[y - int(h * 0.15):y + int(h * 1.15), x - int(w * 0.15):x + int(w * 1.15)], 0, 0, diff, diff, cv2.BORDER_CONSTANT, value = [255,255,255])
                                cv2.imwrite(directory + str(detect_count) + name, output_img)
                            
                        else:
                            if width == height:#すでに正方形だったら
                                cv2.imwrite(directory + str(detect_count) + name, affine_img_w[y:y + h, x - int(w * 0.15):x + int(w * 1.15)])
                            elif w > h:
                                diff = (w - h)//2#余白の大きさ
                                output_img = cv2.copyMakeBorder(affine_img_w[y:y + h, x - int(w * 0.15):x + int(w * 1.15)], diff, diff, 0, 0, cv2.BORDER_CONSTANT, value = [255,255,255])
                                cv2.imwrite(directory + str(detect_count) + name, output_img)
                            else:#縦幅が大きければ
                                diff = (h - w)//2#余白の大きさ
                                output_img = cv2.copyMakeBorder(affine_img_w[y:y + h, x - int(w * 0.15):x + int(w * 1.15)], 0, 0, diff, diff, cv2.BORDER_CONSTANT, value = [255,255,255])
                                cv2.imwrite(directory + str(detect_count) + name, output_img)
                    else:
                        if y - h * 0.15 >= 0 and y + h * 1.15 < height:#縦幅の確保ができるとき 
                            if width == height:#すでに正方形だったら
                                cv2.imwrite(directory + str(detect_count) + name, affine_img_w[y - int(h * 0.15):y + int(h * 1.15), x:x + w]) 
                            elif w > h:
                                diff = (w - h)//2#余白の大きさ
                                output_img = cv2.copyMakeBorder(affine_img_w[y - int(h * 0.15):y + int(h * 1.15), x:x + w], diff, diff, 0, 0, cv2.BORDER_CONSTANT, value = [255,255,255])
                                cv2.imwrite(directory + str(detect_count) + name, output_img)
                            else:#縦幅が大きければ
                                diff = (h - w)//2#余白の大きさ
                                output_img = cv2.copyMakeBorder(affine_img_w[y - int(h * 0.15):y + int(h * 1.15), x:x + w], 0, 0, diff, diff, cv2.BORDER_CONSTANT, value = [255,255,255])
                                cv2.imwrite(directory + str(detect_count) + name, output_img)
                                
                        else:   
                            if width == height:#すでに正方形だったら
                                cv2.imwrite(directory + str(detect_count) + name, affine_img_w[y:y + h, x:x + w])
                            elif w > h:
                                diff = (w - h)//2#余白の大きさ
                                output_img = cv2.copyMakeBorder(affine_img_w[y:y + h, x:x + w], diff, diff, 0, 0, cv2.BORDER_CONSTANT, value = [255,255,255])
                                cv2.imwrite(directory + str(detect_count) + name, output_img)
                            else:#縦幅が大きければ
                                diff = (h - w)//2#余白の大きさ
                                output_img = cv2.copyMakeBorder(affine_img_w[y:y + h, x:x + w], 0, 0, diff, diff, cv2.BORDER_CONSTANT, value = [255,255,255])
                                cv2.imwrite(directory + str(detect_count) + name, output_img)
                                    

                    detect_count = detect_count + 1
            return directory + str(detect_count-1) + name            
        return detect_contour(directory, name, affine_img, affine_img_w)
    
    def square(directory, name):#余白を考慮して画像を保存
        # 画像を読込
        src = cv2.imread(directory+name, cv2.IMREAD_COLOR)
        # 画像の大きさ
        height, width, channels = src.shape[:3]
        
        if width == height:#すでに正方形だったら
            cv2.imwrite(directory + 'sq_' + name, src)
        elif width > height:#横幅が大きければ
            diff = (width - height)//2#余白の大きさ
            output_img = cv2.copyMakeBorder(src, diff, diff, 0, 0, cv2.BORDER_CONSTANT, value = [255,255,255])
            cv2.imwrite(directory + 'sq_' + name, output_img)
        else:#縦幅が大きければ
            diff = (height - width)//2#余白の大きさ
            output_img = cv2.copyMakeBorder(src, 0, 0, diff, diff, cv2.BORDER_CONSTANT, value = [255,255,255])
            cv2.imwrite(directory + 'sq_' + name, output_img)
        return directory + 'sq_' + name
    

    # if __name__ == '__main__':
    #     rotate_img('python/pre_triming_images/mouse.jpg', 'mouse.jpg')