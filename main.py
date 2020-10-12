from tkinter import *
from PIL import Image
import os
from pickle import load
from numpy import asarray


class Paint(object):
    def __init__(self, classifier):
        self.classifier = classifier
        self.root = Tk()
        self.root.title('Digit Estimator')

        self.c = Canvas(self.root, bg='white', width=400, height=400, highlightthickness=1, highlightbackground="black")
        self.c.grid(row=0, columnspan=5)

        self.saveButton = Button(self.root, text='Save', command=self.save)
        self.saveButton.grid(row=1, column=0)

        self.classifyButton = Button(self.root, text='Classify', command=self.classify)
        self.classifyButton.grid(row=1, column=1)

        self.text = Text(self.root, state='disabled', width= 10, height= 1, highlightthickness=1, highlightbackground="black")
        # self.text = Text(self.root, width= 10, height= 1, highlightthickness=1, highlightbackground="black")
        self.text.grid(row=1, column=2)

        self.clearButton = Button(self.root, text='Clear Canvas', command=self.clear)
        self.clearButton.grid(row=1, column=3)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None

        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def paint(self, event):

        self.line_width = 30
        paint_color = 'black'
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color, capstyle=ROUND)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def save(self):
        self.c.postscript(file='image.ps')
        os.system('convert image.ps image.png')
        os.system('rm image.ps')
        image = Image.open('image.png')
        newImage = image.resize((28, 28))
        newImage.save('image28x28.png', optimize=True)

    def clear(self):
        self.c.delete('all')

    def classify(self):
        self.save()

        model = load(open('model.pkl', 'rb'))
        image = Image.open('image28x28.png')

        imageArray = asarray(image)

        imageListFlattened = []
        for row in range(28):
            for col in range(28):
                imageListFlattened.append(imageArray[row][col][1])

        imageArray = asarray(imageListFlattened)

        prediction = model.predict([imageArray])
        self.text.configure(state='normal')
        self.text.delete(1.0, 'end')
        self.text.insert(1.0, prediction[0])
        self.text.configure(state='disabled')


if __name__ == '__main__':
    classifier = None
    Paint(classifier)