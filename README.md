# Reader Pen Raspberry Pi Demo

![image](https://user-images.githubusercontent.com/88633866/233759655-96302937-40d1-44e6-833b-e41ca1d04253.png)

Here is the source code installed on the Raspberry Pi demo. The model is a Raspberry Pi Zero W (2017 version) with Bullseye. Attached are the Arducam OV5647 high-res MIPI camera module and a headphone jack for PWM audio. Three user buttons are wired as pullups. In our testing, we were experiencing issues with keeping the battery's JST connector in place, so we used power from a computer instead. However, all the processing is done on the RPi locally. 

The following packages need to be installed: tesseract-ocr, imagemagick, espeak

Additionally add `dtoverlay=audremap` to the end of /boot/config.txt to configure the audio output

Simply run `python3 app.py` to start. Additionally you can configure the script to run on boot, which would make it easier to begin using it. 
