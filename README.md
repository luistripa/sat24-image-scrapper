# Sat24-image-scrapper

A simple python script to extract Sat24 satellite images of Europe's weather.

The images will have a 15 minute refresh interval.

## Requirements
    numpy (tested on version 1.19.1)
    opencv2 (tested on version 4.4.0.42)
    pillow (tested on  version 7.2.0)
    requests (tested on version 2.24.0)
To install the requirements run (**this will install the versions above**):
    
    pip3 install -r requirements.txt

A virtual environment is recommended to avoid overriding any existing versions.
    
## Controls

Press `u` to update all images. This may take a while.

Press `ESC` to exit the application

## Images

The following images will be displayed:

<br>

**Infrared**

<img src="src/images/Infrared.png" alt="Sat24 infrared image"/>

<br>

**Rain**

<img src="src/images/Rain.png" alt="Sat24 rain image"/>

<br>

**Visible**

<img src="src/images/Visible.png" alt="Sat24 visible image"/>

## Fix me!

The downloaded images are automatically converted to gray.<br>
This is an unintended "feature". Work in progress...

## Aditional info

The images present in this repository may be subject to copyright
