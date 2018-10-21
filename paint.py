#-*-coding:utf-8-*-
import cv2
import numpy as np
import time
class mouse:
    def __init__(self, input_img_name):
        self.x=None
        self.y=None
        self.event=None
        self.flags=None
        cv2.setMouseCallback(input_img_name, self.__CallBackFunc, None)

    def __CallBackFunc(self, eventType, x, y, flags, userdata):
        self.x = x
        self.y = y
        self.event = eventType    
        self.flags = flags    
    
    def getEvent(self):
        return self.event              

    def getFlags(self):
        return self.flags                

    def getX(self):
        return self.x

    def getY(self):
        return self.y 

    def getPos(self):
        return np.array((self.x,self.y))


class pencil:
    def __init__(self, input_img_name):
        cv2.createTrackbar('R', input_img_name, 0, 1, self.__CallBackFunc)
        cv2.createTrackbar('G', input_img_name, 0, 1, self.__CallBackFunc)
        cv2.createTrackbar('B', input_img_name, 0, 1, self.__CallBackFunc)
        cv2.createTrackbar("Mode", input_img_name, 0, 1, self.__CallBackFunc)
        self.input_img_name = input_img_name
        self.color = np.array([0, 0, 0])
        self.mode = None
        self.draw = False

    def __CallBackFunc(self, pos):
        r = cv2.getTrackbarPos("R", self.input_img_name)
        g = cv2.getTrackbarPos("G", self.input_img_name)
        b = cv2.getTrackbarPos("B", self.input_img_name)
        self.color = np.array([b,g,r])
        self.mode = cv2.getTrackbarPos("Mode", self.input_img_name)

    def getColor(self):
        return self.color

    def getMode(self):
        return self.mode

def filling(img, pos, color, win_name):
    """
    color : [b,g,r]
    pos : [x,y]
    """
    img_size = img.shape
    searched_img = np.zeros(img_size[0:2])
    pos_queue = []
    pos_queue.append(pos)
    buff_color = np.copy(img[pos[1]][pos[0]])
    
    while len(pos_queue) != 0:

        tmp_color = np.copy(img[pos_queue[0][1]][pos_queue[0][0]])

        if  tmp_color[0] == buff_color[0] and tmp_color[1] == buff_color[1] and tmp_color[2] == buff_color[2]:
            img[pos_queue[0][1]][pos_queue[0][0]][0] = color[0]
            img[pos_queue[0][1]][pos_queue[0][0]][1] = color[1]
            img[pos_queue[0][1]][pos_queue[0][0]][2] = color[2]
            for i in [(-1,0),(1,0),(0,-1),(0,1)]:
                    buff_pos = np.array((pos_queue[0][0] + i[0], pos_queue[0][1] + i[1]))
                    if buff_pos[0] >= img_size[1] or buff_pos[0] < 0 or buff_pos[1] >= img_size[0] or buff_pos[1] < 0:
                        pass
                    elif searched_img[buff_pos[1]][buff_pos[0]] == 0:
                        pos_queue.append(buff_pos)
                        searched_img[buff_pos[1]][buff_pos[0]] = 1
                    else:
                        pass
        pos_queue.pop(0)



if __name__ == "__main__":
    try:
        read_raw = cv2.imread("raw_img/img_432.png")
        read_bin = cv2.imread("bin_img/img_432.png")
        out_bin = np.copy(read_bin)
        show_img = cv2.addWeighted(read_raw, 0.9, read_bin, 0.1, 0)

        window_name = "img"
        output_window_name = "output"
        palette_name = "palette"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.namedWindow(output_window_name, cv2.WINDOW_NORMAL)
        cv2.namedWindow(palette_name, cv2.WINDOW_NORMAL)

        mouseData = mouse(window_name)
        pencilData = pencil(palette_name)

        while True:
            
            k = cv2.waitKey(1)
            if mouseData.getEvent() == cv2.EVENT_LBUTTONDOWN:
                pencilData.draw = True
            elif mouseData.getEvent() == cv2.EVENT_LBUTTONUP:    
                pencilData.draw = False
            elif mouseData.getEvent() == cv2.EVENT_RBUTTONDOWN or k == ord('q'):
                break
            elif k == ord('r') or k == ord('R'):
                read_raw = cv2.flip(read_raw,0)
                out_bin = cv2.flip(out_bin,0)
                show_img = cv2.addWeighted(read_raw, 0.9, out_bin, 0.1, 0)

            if pencilData.draw == True:
                pos = mouseData.getPos()
                if pos[0] >= show_img.shape[1]:
                    pos[0] = show_img.shape[1] - 1
                if pos[0] < 0:
                    pos[0] = 0
                if pos[1] >= show_img.shape[0]:
                    pos[1] = show_img.shape[0] - 1
                if pos[1] < 0:
                    pos[1] = 0

                color = pencilData.getColor()
                mode = pencilData.getMode()

                color[color >= 1] = 255
                print(pos)
                print(show_img[pos[1]][pos[0]])
                print(color)
                print(pencilData.getMode())
                if mode == 0:
                    cv2.line(out_bin,(pos[0],pos[1]),(pos[0],pos[1]),(int(color[0]),int(color[1]),int(color[2])))
                elif mode == 1:
                    pencilData.draw = False
                    filling(out_bin, pos, color, output_window_name)
                show_img = cv2.addWeighted(read_raw, 0.9, out_bin, 0.1, 0)

            cv2.imshow(window_name,show_img)
            cv2.imshow(output_window_name,out_bin)
    except:
        import traceback
        print(traceback.format_exc())
    finally:
        cv2.destroyAllWindows()
        input(">>")
