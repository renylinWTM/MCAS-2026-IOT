import RPi.GPIO as GPIO
import time

PIN2 = 11       # 實體腳位？？（填你自己的腳位號碼）
PIN_LED = 13    # LED腳位
freq = 523      # 頻率 (523Hz，大約是 C5)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN2, GPIO.OUT)
GPIO.setup(PIN_LED, GPIO.OUT)

# 建立 PWM 物件，設定頻率 freq
voice = GPIO.PWM(PIN2, freq)

tik = 0.2

def play_sos():

    #S
    voice.start(50)   # duty 50%，發聲
    GPIO.output(PIN_LED, GPIO.HIGH)
    time.sleep(tik)   # 持續 0.2 秒
    voice.stop()      # 停止發聲
    GPIO.output(PIN_LED, GPIO.LOW)
    time.sleep(tik)   # 停 0.2 秒再響

    voice.start(50)   # duty 50%，發聲
    GPIO.output(PIN_LED, GPIO.HIGH)
    time.sleep(tik)   # 持續 0.2 秒
    voice.stop()      # 停止發聲
    GPIO.output(PIN_LED, GPIO.LOW)
    time.sleep(tik)   # 停 0.2 秒再響

    voice.start(50)   # duty 50%，發聲
    GPIO.output(PIN_LED, GPIO.HIGH)
    time.sleep(tik)   # 持續 0.2 秒
    voice.stop()      # 停止發聲
    GPIO.output(PIN_LED, GPIO.LOW)

    time.sleep(tik*3) # 停 0.6 秒再響

    #O
    voice.start(50)   # duty 50%，發聲
    GPIO.output(PIN_LED, GPIO.HIGH)
    time.sleep(tik*3)     # 持續 0.6 秒
    voice.stop()      # 停止發聲
    GPIO.output(PIN_LED, GPIO.LOW)
    time.sleep(tik*3)     # 停 0.6 秒再響

    voice.start(50)   # duty 50%，發聲
    GPIO.output(PIN_LED, GPIO.HIGH)
    time.sleep(tik*3)     # 持續 0.6 秒
    voice.stop()      # 停止發聲
    GPIO.output(PIN_LED, GPIO.LOW)
    time.sleep(tik*3)     # 停 0.6 秒再響

    voice.start(50)   # duty 50%，發聲
    GPIO.output(PIN_LED, GPIO.HIGH)
    time.sleep(tik*3)     # 持續 0.6 秒
    voice.stop()      # 停止發聲
    GPIO.output(PIN_LED, GPIO.LOW)
    time.sleep(tik*3) # 停 0.6 秒再響

    #S
    voice.start(50)   # duty 50%，發聲
    GPIO.output(PIN_LED, GPIO.HIGH)
    time.sleep(tik)   # 持續 0.2 秒
    voice.stop()      # 停止發聲
    GPIO.output(PIN_LED, GPIO.LOW)
    time.sleep(tik)   # 停 0.2 秒再響

    voice.start(50)   # duty 50%，發聲
    GPIO.output(PIN_LED, GPIO.HIGH)
    time.sleep(tik)   # 持續 0.2 秒
    voice.stop()      # 停止發聲
    GPIO.output(PIN_LED, GPIO.LOW)
    time.sleep(tik)   # 停 0.2 秒再響

    voice.start(50)   # duty 50%，發聲
    GPIO.output(PIN_LED, GPIO.HIGH)
    time.sleep(tik)   # 持續 0.2 秒
    voice.stop()      # 停止發聲
    GPIO.output(PIN_LED, GPIO.LOW)

    time.sleep(tik*3) # 停 0.6 秒再響

try:
    while True:
        play_sos()
except KeyboardInterrupt:
    pass
finally:
    voice.stop()
    GPIO.cleanup()

