from machine import Pin
import urequests as requests
import time

led = Pin(5, Pin.OUT)

while True:
  try:
    resp = requests.get(url = "http://ec2263c8db22.ngrok.io/read")
    print(resp.text)
    if resp.text == "on":
      led.value(1)
      time.sleep(1)
    else:
      led.value(0)
      time.sleep(1)
  except:
    pass



