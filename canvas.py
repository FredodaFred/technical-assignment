import tkinter as tk
from PIL import ImageTk, Image
from DrawShapes import Pen
import os

# main screen
root = tk.Tk()
root.title("Draw Shapes")
root.geometry('700x700+0+0') #700 pix by 700, frame appears at 0,0 on screen
root.resizable(False, False)
current_dir = os.getcwd()

class ChecklistBox(tk.Frame):
    def __init__(self, parent, choices):
        tk.Frame.__init__(self, parent, width = 100, height = 600)
        self.vars = []
        bg = self.cget("background") #background color
        self.cb_pointer = []
        for choice in choices:
            var = tk.StringVar(value=choice)
            self.vars.append(var)
            cb = tk.Checkbutton(self, var=var, text=choice,
                                onvalue=choice, offvalue="",
                                anchor="w", width=20, background=bg,
                                relief="flat", highlightthickness=0
            )
            cb.pack(side="top", fill="x", anchor="w")
            self.cb_pointer.append(cb)
            cb.deselect()

    def getCheckedItems(self):
        values = []
        for var in self.vars:
            value =  var.get()
            if value:
                values.append(value)
        return values
    def deselectAll(self):
        for cb in self.cb_pointer:
            cb.deselect()

class ImageFrame(tk.Frame):
    """
    This class displays our image
    """
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height = 600, width = 600, bg = 'black')
        self.imageBox = tk.Label()
        self.imageBox.grid(row = 0, column = 1, columnspan = 2)
        self.imgs = [] #The image objects themselves
        self.paths = [] #The paths in which the image objects were made from
        self.index = 0 #keeps track of where we are in the list so we can use prev and next
    def setImgs(self, paths):
        'Just gives the paths'
        self.paths = paths
    def addImgs(self, paths):
        'takes paths, checks for repeats, then adds an image object as well as the path'
        os.chdir('output')
        for path in paths:
            if not path in self.paths:
                new_img = ImageTk.PhotoImage(Image.open(path))
                self.imgs.append(new_img)
                self.paths.append(path)
        os.chdir(current_dir)
    def next(self):
        if self.index < len(self.imgs) - 1: #making sure at least one to the right
            self.index += 1
            self._displayImg(self.index)
    def prev(self):
        if self.index > 0:
            self.index -= 1
            self._displayImg(self.index)
    def initImgs(self):
        'Here we actually create + instantiate the photo image objects'
        os.chdir('output')
        if self.paths is not None:
            for path in self.paths:
                new_img = ImageTk.PhotoImage(Image.open(path))
                self.imgs.append(new_img)
            self.imageBox.configure(image=self.imgs[0])
        os.chdir(current_dir)
    def _displayImg(self, index):
        if len(self.imgs) > index:
            self.imageBox.configure(image = self.imgs[index])

def getImages():
    """
    finds all the pngs in the output directory, returns a
    list of ImageTk.PhotoImages of all the images.
    """
    imgs = []
    if not os.path.isdir('output'):
        print("No current output directory. Creating one, must generate images")
        os.mkdir('output')
        return
    os.chdir('output')
    files = os.listdir()
    for file in files:
        if file[-3:] == 'png':
            imgs.append(file)
    os.chdir(current_dir) #return from the output dir
    return imgs

checklist = ChecklistBox(root, ['circle', 'square', 'rectangle', 'parallelogram', 'triangle', 'trapezoid', 'arc', 'sectional'])
checklist.grid(row = 0, column = 0)

imgs = getImages()
imgBox = ImageFrame(root)
imgBox.grid(row = 0, column = 1, columnspan = 2)
imgBox.setImgs(imgs)

def genClick():
    pen = Pen()
    pen.read_list(checklist.getCheckedItems())
    if imgBox.paths is None:
        imgBox.setImgs(getImages())
        imgBox.initImgs()
    else:
        imgBox.addImgs(getImages())
    checklist.deselectAll()

genImages = tk.Button(root, text = "Generate Images", command = genClick, anchor = 'w')
genImages.grid(row = 1, column = 0)

nextImg = tk.Button(root, text = ">>", command = imgBox.next )
prevImg = tk.Button(root, text = "<<", command = imgBox.prev)
nextImg.grid(row = 1, column = 2)
prevImg.grid(row = 1, column =  1)

imgBox.initImgs()

root.mainloop()
