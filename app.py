#!/usr/bin/env python3
import signal
import sys
import RPi.GPIO as GPIO
import subprocess
vol = 100
BUTTON_MIC = 23
BUTTON_VOL = 24
BUTTON_PWR = 25
ocr_running = False
vol_changing = False
mic_changing = False
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)
def run_process(command, t=False):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    arr = []
    for line in p.stdout:
        print(line)
        arr.append(line.decode('ascii'))
    p.wait()
    print("Return code for " + command + " -> " + str(p.returncode))
    if t:
        arr_str = " ".join(arr)
        run_process('espeak "' + arr_str + '"')
        modified_str = ""
        for i in arr_str:
          modified_str += i + " "
        modified_str = modified_str.strip()
        if (modified_str == ""):
            modified_str = "No text found"
        run_process('espeak "' + modified_str + '" -g 50')
def button_mic_pressed_callback(channel):
    global mic_changing
    if mic_changing:
        mic_changing = False
        return print("Double press mic")
    vol = 0 if vol != 0 else vol
    if vol != 0:
        run_process('espeak "Volume on"')
    else:
        run_process('espeak "Volume off"')
    run_process("amixer set Master toggle")
def button_vol_pressed_callback(channel):
    global vol, vol_changing
    if vol_changing:
        vol_changing = False
        return print("Double press vol")
    vol_changing = True
    vol = vol - 25
    if (vol < 0):
      vol = 100
    run_process("amixer set Master " + str(vol) + "%")
    run_process('espeak "Volume ' + str(vol) + '"')
def button_pwr_pressed_callback(channel):
    global ocr_running
    if ocr_running:
        ocr_running = False
        return print("Double press pwr")
    print("Pwr pressed, starting OCR")
    ocr_running = True
    subprocess.Popen('espeak "Processing image, please wait"', shell=True, stdout=subprocess.PIPE)
    run_process("libcamera-jpeg -o test.jpg -t 50 --width 220 --height 720")
    run_process("convert test.jpg -rotate 90 -flop +dither -colorspace gray -normalize -scale 250x test.jpg")
    run_process("tesseract test.jpg stdout", True)
if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_MIC, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_VOL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_PWR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_MIC, GPIO.FALLING,
            callback=button_mic_pressed_callback, bouncetime=100)
    GPIO.add_event_detect(BUTTON_VOL, GPIO.FALLING,
            callback=button_vol_pressed_callback, bouncetime=100)
    GPIO.add_event_detect(BUTTON_PWR, GPIO.FALLING,
            callback=button_pwr_pressed_callback, bouncetime=100)
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
