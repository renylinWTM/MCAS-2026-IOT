
import time
import adafruit_dht
import board

# DHT11 接在 GPIO4（實體 Pin 7）
dht_device = adafruit_dht.DHT11(board.D4)

try:
    while True:
        try:
            temperature_c = dht_device.temperature
            temperature_f = temperature_c * (9 / 5) + 32

            humidity = dht_device.humidity

            print("Temp:{:.1f} C / {:.1f} F    Humidity: {}%".format(
                temperature_c, temperature_f, humidity
            ))

        except RuntimeError as err:
            print(err.args[0])

        time.sleep(2.0)

except KeyboardInterrupt:
    print("程式已停止")

finally:
    dht_device.exit()
