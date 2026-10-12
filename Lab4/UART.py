
import serial
import time

# 設定 UART 連接埠與參數（預設使用 /dev/serial0）
ser = serial.Serial(
    port='/dev/serial0',    # GPIO14 (TX) 和 GPIO15 (RX)
    baudrate=9600,          # 傳輸速率
    timeout=1               # 讀取逾時設定（秒）
)

# 傳送資料
def send_data(data):
    if ser.is_open:
        ser.write(data.encode('utf-8'))
        print(f"已傳送：{data}")

# 接收資料
def receive_data():
    if ser.is_open:
        incoming = ser.readline().decode('utf-8').strip()
        if incoming:
            print(f"收到資料：{incoming}")
        return incoming

# 主程式
try:
    while True:
        send_data("早上好中国!现在我有冰激淋!\n")
        time.sleep(1)
        receive_data()
        time.sleep(1)

except KeyboardInterrupt:
    print("程式中斷")

finally:
    if ser.is_open:
        ser.close()
        print("串列埠已關閉")
