import random
from captcha.audio import AudioCaptcha
from captcha.image import ImageCaptcha
from tkinter import *
from PIL import ImageTk, Image
from winsound import *


def random_numbers():
    for num in range(random.randint(4, 6)):
        yield random.randint(0, 9)


num_string_list = [str(num) for num in random_numbers()]
num_string = ''.join(num_string_list)

audio = AudioCaptcha()
image = ImageCaptcha()

data = audio.generate(num_string)
audio.write(num_string, 'captcha.wav')

data = image.generate(num_string)
image.write(num_string, 'captcha.png')


class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("CAPTCHA")

        self.image = ImageTk.PhotoImage(Image.open('captcha.png'), master=master)
        self.label_image = Label(master, image=self.image)
        self.label_image.pack()

        self.play_recording = Button(master, text="Get audio code", command=lambda: PlaySound("captcha.wav", SND_FILENAME))
        self.play_recording.pack()

        self.entry_box = Entry(master)
        self.entry_box.pack()

        self.check_numbers = Button(master, text="Check numbers", command=self.get_captcha_numbers)
        self.check_numbers.pack()

        self.close_button = Button(master, text="Close", command=master.quit, bg='brown', fg='white', font=('Helvetica', 9, 'bold'))
        self.close_button.pack()

    def get_captcha_numbers(self):
        numbers = self.entry_box.get()
        self.label_numbers = Label(self.master, text=numbers)
        self.label_numbers.pack()


root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
