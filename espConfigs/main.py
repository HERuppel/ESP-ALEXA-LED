from machine import Pin
import utime
from umqtt.simple import MQTTClient

utime.sleep(5)

led = Pin(5, Pin.OUT)

def subs(topic, msg):
  print(topic, msg)

  if msg == b'0':
    led.value(0)
  elif msg == b'1':
    led.value(1)


c = MQTTClient("umqtt_client", "192.168.0.104")
c.set_callback(subs)
c.connect()
c.subscribe(b"led1")

while True:
  c.wait_msg()



