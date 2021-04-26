import random
from captcha.audio import AudioCaptcha
from captcha.image import ImageCaptcha
from random import randint

def random_numbers():
    for num in range(random.randint(4,6)):
        yield random.randint(0,9)

if __name__ == '__main__':

    num_string_list = [str(num) for num in random_numbers()]
    num_string = ''.join(num_string_list)

    audio = AudioCaptcha()
    image = ImageCaptcha()

    data = audio.generate(num_string)
    audio.write(num_string, 'captcha.wav')

    data = image.generate(num_string)
    image.write(num_string, 'captcha.png')