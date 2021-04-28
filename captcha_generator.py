import random
import threading
from captcha.audio import AudioCaptcha
from captcha.image import ImageCaptcha
from tkinter import *
from PIL import ImageTk, Image
from winsound import *

# object of this class represents randomly generated number in form of a string
class NumString:
    def __init__(self):
        self.num_string = self.random_num_string()

    def random_numbers(self):
        for num in range(random.randint(4, 6)):
            yield random.randint(0, 9)

    def random_num_string(self):
        num_string_list = [str(num) for num in self.random_numbers()]
        return ''.join(num_string_list)

# saves image captcha in .png to current folder
def generate_image_captcha(num):
    image = ImageCaptcha()
    data = image.generate(num)
    image.write(num, 'captcha.png')

# saves audio captcha in .wav to current folder
def generate_audio_captcha(num):
    audio = AudioCaptcha()
    data = audio.generate(num)
    audio.write(num, 'captcha.wav')

# object of this class represents Graphical User Interface
class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("CAPTCHA")

        # number of times user tried to check captcha
        self.attempts = 0

        # creates image widget based on captcha image
        self.image = ImageTk.PhotoImage(Image.open('captcha.png'), master=master)
        self.label_image = Label(master, image=self.image)
        self.label_image.pack(padx=5, pady=5)

        # entry widget lets user input a number
        self.entry_box = Entry(master)
        self.entry_box.pack(pady=5)

        # once upon clicking checks for valid input
        self.check_numbers = Button(master, text="Check numbers", command=self.check_captcha, font=('Helvetica', 9))
        self.check_numbers.pack(pady=5)

        # label widget shows number of attempts
        self.label_attempts = Label(master, text=f'Times attempted: {self.attempts}. Cannot try more than 3 times!')
        self.label_attempts.config(font=('Helvetica', 9))
        self.label_attempts.pack(padx=5, pady=5)

        # label widget shows whether input was correct or not
        self.label_result = Label(master, text='')
        self.label_result.config(font=('Helvetica', 9))
        self.label_result.pack(pady=5)

        # once upon clicking plays recording based on captcha audio
        # runs on different thread to allow user to input number during recording
        self.play_recording = Button(master, text="Get audio code", command=self.PlaySound_with_threading, font=('Helvetica', 9))
        self.play_recording.pack(pady=5)

        # once upon clicking changes image and audio
        self.replace_button = Button(master, text="Different Captcha", command=self.replace_image_and_recoring, font=('Helvetica', 9))
        self.replace_button.pack(pady=5)

        # once upon clicking exits from the programm
        self.close_button = Button(master, text="Close", command=master.quit, bg='brown', fg='white', font=('Helvetica', 9, 'bold'))
        self.close_button.pack(side=RIGHT,padx=5, pady=5)

    # sets windows in the centre of the screen
    def set_geometry(self):
        # Gets the requested values of the height and widht
        window_width = self.master.winfo_reqwidth()
        window_height = self.master.winfo_reqheight()

        # Gets both half the screen width/height and window width/height
        position_right = int(self.master.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.master.winfo_screenheight() / 2 - window_height / 2)

        # Positions the window in the center of the page.
        self.master.geometry("+{}+{}".format(position_right, position_down))

    # plays recording of captcha on a diffent thread
    def PlaySound_with_threading(self):
        t1 = threading.Thread(target=PlaySound, args=("captcha.wav", SND_FILENAME))
        t1.start()

    # returns user input from the entry widget
    def get_captcha_numbers(self):
        return self.entry_box.get()

    # checks whether user input was the same as shown on image/played on audio track
    def validate_input(self):
        return True if self.get_captcha_numbers() == number else False

    def replace_image_and_recoring(self):
        number = NumString().num_string
        generate_image_captcha(number)
        generate_audio_captcha(number)
        path = 'captcha.png'

        self.image2 = ImageTk.PhotoImage(file=path)
        self.label_image.configure(image=self.image2)
        self.label_image.image = self.image2

    # shows different texts based on user input
    def check_captcha(self):
        self.attempts += 1
        if self.attempts != 4:
            # user correclty entered the number
            if self.validate_input() == True:
                self.label_attempts['text'] = f'Times attempted: {self.attempts}\n'
                self.play_recording.destroy()
                self.check_numbers.destroy()
                self.replace_button.destroy()
                self.label_result['text'] = 'Congratulations! Your are not a robot!\n'
            # user incorreclty enetered number but still has remaining attempts
            else:
                self.label_result['text'] = 'Incorrect, try again!'
                self.label_attempts['text'] = f'Times attempted: {self.attempts}. Cannot try more than 3 times! \n'
                self.replace_image_and_recoring()
        # user no longer has attempts
        else:
            self.label_attempts['text'] = f'Times attempted: {self.attempts}\n'
            self.play_recording.destroy()
            self.check_numbers.destroy()
            self.replace_button.destroy()
            self.label_result['text'] = 'No attempts remaining, You are a robot!\n'



if __name__ == '__main__':

    number = NumString().num_string
    generate_image_captcha(number)
    generate_audio_captcha(number)
    root = Tk()
    my_gui = MyFirstGUI(root)
    my_gui.set_geometry()
    root.mainloop()
