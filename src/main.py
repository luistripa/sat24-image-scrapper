from PIL import Image
import requests
from io import BytesIO
import numpy as np
import cv2
import argparse


class ImageDelegate:

    def __init__(self):
        self.imageSequences = dict()
        self.current = 0

    def update(self):
        print('Updating image sequences for {}...'.format(self.areaID), end='')
        for url in self.urlDict:

            # Get images from the Sat24 API
            content = requests.get(self.urlDict[url], timeout=30).content
            img = Image.open(BytesIO(content))

            # Create an image sequence list
            frame_sequence = list()
            for frame_n in range(0, img.n_frames):
                img.seek(frame_n)
                frame_sequence.append(np.asarray(img))
            self.imageSequences[url] = frame_sequence
        print('done')
        return self.imageSequences

    def next(self):
        """
        Shows the next frame in the sequences.

        :return: None
        """

        if len(self.imageSequences) == 0:
            raise ValueError("There are no images in the sequences. Run update() before running next()")

        if self.current == len(self.imageSequences.values().__iter__().__next__())-1:
            self.current = 0

        for img_type in self.imageSequences:
            cv2.imshow(self.areaID+'_'+img_type, self.imageSequences[img_type][self.current])
        self.current += 1


class Africa(ImageDelegate):

    def __init__(self):
        self.areaID = 'Africa'
        self.urlDict = {'Infrared': 'https://api.sat24.com/animated/AF/infraPolair/2/GMT%20Standard%20Time/',
                        'Rain': 'https://api.sat24.com/animated/AF/rain/2/GMT%20Standard%20Time/',
                        'Visible': 'https://api.sat24.com/animated/AF/visual/2/GMT%20Standard%20Time/'}
        super(Africa, self).__init__()


class Europe(ImageDelegate):

    def __init__(self):
        self.areaID = 'Europe'
        self.urlDict = {'Infrared': 'https://api.sat24.com/animated/EU/infraPolair/2/GMT%20Standard%20Time/',
                        'Rain': 'https://api.sat24.com/animated/EU/rainTMC/2/GMT%20Standard%20Time/',
                        'Visible': 'https://api.sat24.com/animated/EU/visual/2/GMT%20Standard%20Time/'}
        super(Europe, self).__init__()


class Oceania(ImageDelegate):
    
    def __init__(self):
        self.areaID = 'Oceania'
        self.urlDict = {'Infrared': 'https://api.sat24.com/animated/OCE/infraPolair/2/GMT%20Standard%20Time/',
                        'Visible': 'https://api.sat24.com/animated/OCE/visual/2/GMT%20Standard%20Time/'}
        super(Oceania, self).__init__()
        

class Sat24:

    def __init__(self, show_africa=None, show_europe=None, show_oceania=None):
        self.africa = None
        self.europe = None
        self.oceania = None

        if show_africa:
            self.africa = Africa()
        if show_europe:
            self.europe = Europe()
        if show_oceania:
            self.oceania = Oceania()

        self.number_of_images = 0
        self.current = 0

    def update(self):
        """
        Updates all images from all selected areas.

        :return: dict() of all images
        """
        image_sequences = dict()

        if self.africa is not None:
            image_sequences['Africa'] = self.africa.update()
        if self.europe is not None:
            image_sequences['Europe'] = self.europe.update()
        if self.oceania is not None:
            image_sequences['Oceania'] = self.oceania.update()

        return image_sequences

    def next(self):
        """
        Show the next image in the sequence

        :return: None
        """
        if self.africa is not None:
            self.africa.next()
        if self.europe is not None:
            self.europe.next()
        if self.oceania is not None:
            self.oceania.next()

    def get_selected_areas(self):
        pass


parser = argparse.ArgumentParser()
parser.add_argument('--africa', help='Show images for Africa', action='store_true')
parser.add_argument('--europe', help='Show images for Europe', action='store_true')
parser.add_argument('--oceania', help='Show images for Oceania', action='store_true')

args = parser.parse_args()

if args.africa or args.europe or args.oceania:
    sat24 = Sat24(show_africa=args.africa, show_europe=args.europe, show_oceania=args.oceania)
else:
    raise Exception('Not enough params! Use --help to find a list of params')

try:
    sat24.update()
    while True:
        sat24.next()
        pressedKey = cv2.waitKey(1000)
        if pressedKey == ord('u'):  # Update images
            sat24.update()
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
