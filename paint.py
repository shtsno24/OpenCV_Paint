#-*-coding:utf-8-*-
import os
import cv2
import numpy as np
import tkinter
import tkinter.filedialog as tkfd
import tkinter.messagebox as tkmsg

class mouse:
    def __init__(self, input_img_name):
        self.x = None
        self.y = None
        self.event = None
        self.flags = None
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


class palette:
    def __init__(self, input_img_name, input_img):
        cv2.createTrackbar('alpha', input_img_name, 0, 100, self.__CallBackFunc)
        cv2.createTrackbar("Mode", input_img_name, 0, 1, self.__CallBackFunc)
        self.cursor = mouse(input_img_name)
        self.input_img_name = input_img_name
        self.input_img = input_img
        self.color = np.array([0, 0, 0])
        self.mode = None
        self.alpha = 0.9
        self.draw = False

    def __CallBackFunc(self, pos):
        self.mode = cv2.getTrackbarPos("Mode", self.input_img_name)
        self.alpha = cv2.getTrackbarPos("alpha", self.input_img_name)

    def getColor(self):
        pos = self.cursor.getPos()
        b = self.input_img[pos[1]][pos[0]][0]
        g = self.input_img[pos[1]][pos[0]][1]
        r = self.input_img[pos[1]][pos[0]][2]
        self.color = np.array([b,g,r])
        return self.color

    def getMode(self):
        out = np.array([self.mode,self.alpha])
        return out

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

def ColorPalette():
    colors = np.array([[[0,0,0],[255,255,255]],[[255,0,0],[0,255,0]],[[0,0,255],[0,255,255]]])
    palette_size = 60
    color_palette = np.zeros((palette_size * colors.shape[0],palette_size * colors.shape[1],colors.shape[2]))

    for i in np.arange(colors.shape[0]):
       for j in np.arange(colors.shape[1]):
           Color = (int(colors[i][j][0]),int(colors[i][j][1]),int(colors[i][j][2]))                
           cv2.rectangle(color_palette,(j * palette_size,i * palette_size),((j + 1) * palette_size,(i + 1) * palette_size),Color,-1)

    return color_palette

if __name__ == "__main__":
    try:
        root = tkinter.Tk()
        root.withdraw()
        fileType = [("PNG","*.png"),("All Files",'*')]
        raw_path = "raw_img"
        bin_path = "bin_img"
        CurrentDirectory = os.path.abspath(os.path.dirname(__file__))
        bin_file = tkfd.askopenfilename(filetypes = fileType,initialdir = CurrentDirectory)
        raw_file = bin_file.replace(bin_path, raw_path)
        file_name = bin_file.split('/')[-1]
        save_flag = False

        read_raw = cv2.imread(raw_file)
        read_bin = cv2.imread(bin_file)
        out_bin = np.copy(read_bin)
        show_img = cv2.addWeighted(read_raw, 0.9, read_bin, 0.1, 0)

        window_name = "img"
        output_window_name = "output"
        palette_name = "palette"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.namedWindow(output_window_name, cv2.WINDOW_NORMAL)
        cv2.namedWindow(palette_name, cv2.WINDOW_NORMAL)

        palette_img = ColorPalette()
        mouseData = mouse(window_name)
        paletteData = palette(palette_name,palette_img)

        while True:
            
            k = cv2.waitKey(1)
            mouseevent = mouseData.getEvent()
            paletteevent = paletteData.cursor.getEvent()
            if mouseevent == cv2.EVENT_LBUTTONDOWN:
                paletteData.draw = True
                save_flag = False
            elif mouseevent == cv2.EVENT_LBUTTONUP:    
                paletteData.draw = False
            elif k == ord('Q') or k == ord('q'):# quit
                break
            elif k == ord('r') or k == ord('R'):# flip img
                read_raw = cv2.flip(read_raw,0)
                out_bin = cv2.flip(out_bin,0)
                save_flag = False
            elif paletteevent == cv2.EVENT_LBUTTONDOWN:# get color from palette
                paletteData.getColor()

            elif k == ord('o') or k == ord('O'):# open files
                CurrentDirectory = os.path.abspath(os.path.dirname(__file__))
                bin_file = tkfd.askopenfilename(filetypes = fileType,initialdir = CurrentDirectory)
                raw_file = bin_file.replace(bin_path, raw_path)
                file_name = bin_file.split('/')[-1]
                read_raw = cv2.imread(raw_file)
                out_bin = cv2.imread(bin_file)
                tkmsg.showinfo("Open file", bin_file + '\n' + raw_file)

            elif k == ord('s') or k == ord('S'):# save files
                CurrentDirectory = os.path.abspath(os.path.dirname(__file__))
                
                bin_file = tkfd.asksaveasfilename(filetypes = fileType,initialdir = CurrentDirectory,initialfile=file_name)
                if bin_file.find(".png") == -1:
                    bin_file += ".png"

                raw_file = bin_file.replace(bin_path, raw_path)
                if(bin_file.find("/.png") == -1):
                    cv2.imwrite(bin_file, out_bin)
                    cv2.imwrite(raw_file, read_raw)
                    tkmsg.showinfo("Save file", bin_file + '\n' + raw_file)
                save_flag = True

            if paletteData.draw == True:
                pos = mouseData.getPos()
                if pos[0] >= show_img.shape[1]:
                    pos[0] = show_img.shape[1] - 1
                if pos[0] < 0:
                    pos[0] = 0
                if pos[1] >= show_img.shape[0]:
                    pos[1] = show_img.shape[0] - 1
                if pos[1] < 0:
                    pos[1] = 0

                color = paletteData.color
                mode = paletteData.getMode()

                color[color >= 1] = 255
                print(pos)
                print(show_img[pos[1]][pos[0]])
                print(color)
                print(paletteData.getMode())
                if mode[0] == 0:
                    cv2.line(out_bin,(pos[0],pos[1]),(pos[0],pos[1]),(int(color[0]),int(color[1]),int(color[2])))
                elif mode[0] == 1:
                    paletteData.draw = False
                    filling(out_bin, pos, color, output_window_name)

            mode = paletteData.getMode()
            show_img = cv2.addWeighted(read_raw, float(mode[1]) / 100.0, out_bin, 1.0 - float(mode[1]) / 100.0, 0)
            cv2.imshow(window_name,show_img)
            cv2.imshow(output_window_name,out_bin)
            cv2.imshow(palette_name,palette_img)
    except:
        import traceback
        print(traceback.format_exc())
    finally:
        cv2.destroyAllWindows()
        if save_flag == False:
            flag = tkmsg.askyesno("Save", "Save this file?")
            if flag == True:
                bin_file = tkfd.asksaveasfilename(filetypes = fileType,initialdir = CurrentDirectory)
            elif flag == False:
                bin_file = ""

            if bin_file == '':
                bin_file = "No File was Saved!"
            input(bin_file)

