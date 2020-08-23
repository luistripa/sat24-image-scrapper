from PIL import Image
import requests
from io import BytesIO
import numpy as np
import cv2


class Sat24:

    def __init__(self):
        self.urlDict = {"Infrared": "https://api.sat24.com/animated/EU/infraPolair/2/GMT%20Standard%20Time/",
                        "Rain": "https://api.sat24.com/animated/EU/rainTMC/2/GMT%20Standard%20Time/",
                        "Visible": "https://api.sat24.com/animated/EU/visual/2/GMT%20Standard%20Time/"
                        }
        self.imageSequences = {}
        self.number_of_images = 0
        self.current = 0

    @staticmethod
    def get_image(url):
        """
        Gets the image from the given URL.

        The timeout is set, by default, to 30 seconds.

        :param url: The image url
        :return: The image as a PIL's Image object
        """
        content = requests.get(url, timeout=30).content
        return Image.open(BytesIO(content))

    def append_image(self, key, img):
        """
        Add all image frames to a given array inside imageSequences dict

        :param key: The key to which the frame will be added
        :param img: The image object
        :return: None
        """
        seq = []
        try:
            for frame in range(0, img.n_frames):
                img.seek(frame)
                img_array = np.asarray(img)
                seq.append(img_array)
            self.imageSequences[key] = seq
        except EOFError:
            pass

    def update_image_sequences(self):
        """
        Updates all image sequences to include new sequences if there is any

        :return: None
        """
        if len(self.urlDict) != 0:
            for key in self.urlDict:
                img = self.get_image(self.urlDict[key])
                self.append_image(key, img)

            # Get length of sequences. All sequences have the same length
            self.number_of_images = len(self.imageSequences.get(list(self.imageSequences.keys())[0]))
        else:
            print('error. There are no urls to get!')

    def show_next_image(self):
        """
        Show the next image in the sequence

        :return: None
        """
        if self.current == self.number_of_images:
            self.current = 0
        for key in self.imageSequences:
            cv2.imshow(key, self.imageSequences[key][self.current])
        self.current += 1


sat24 = Sat24()

try:
    print('Updating image sequences... ', end='')
    sat24.update_image_sequences()
    print('done')
    while True:
        sat24.show_next_image()
        pressedKey = cv2.waitKey(1000)
        if pressedKey == ord('u'):
            sat24.update_image_sequences()
        if pressedKey == 27:  # Escape character
            break

except KeyboardInterrupt:
    print('keyboard interrupt')
    print('Exiting....')
except requests.exceptions.ConnectionError:
    print('connection error')
except requests.exceptions.ReadTimeout:
    print('timeout')
# except:
#    print("Unknown error")
