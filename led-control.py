from flask import Flask
from flask_ask import Ask, statement, question
import paho.mqtt.publish as publish

clientId = "PythonPublisher"
host = "192.168.0.104"
port = 1883
topic = "led1"

app = Flask(__name__)
ask = Ask(app, '/')


@ask.launch
def launch():
    return question("Bem-vindo à Skill que controla o LED. Você pode dizer Ligar LED, ou, Desligar LED")

@ask.intent('AMAZON.FallbackIntent')
def fallback():
    return question("Você quer ligar ou desligar seu LED?")


@ask.intent('OnOffIntent', mapping={'OnOff': 'OnOff'})
def gpio_control(OnOff):
    command = OnOff

    if command is None:
        return question("Você quer ligar ou desligar seu LED?")
    elif command == "ligar" or command == "desligar":
        if command == "desligar": 
            publish.single(topic=topic, payload=0, hostname=host)
        elif command == "ligar":
            publish.single(topic=topic, payload=1, hostname=host)
        response_text = f"Seu LED está a {command}"
        return statement(response_text).simple_card('Comando', response_text)
    else:
        return question("Você quer ligar ou desligar seu LED?")


if __name__ == "__main__":
	app.run()

