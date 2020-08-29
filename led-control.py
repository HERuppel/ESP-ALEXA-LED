from flask import Flask, render_template
from flask_ask import Ask, statement, question
import json
import os

app = Flask(__name__)
ask = Ask(app, '/')


@ask.launch
def launch():
    welcome_text = render_template('welcome_text')
    return question(welcome_text)

@ask.intent('AMAZON.FallbackIntent')
def fallback():
    reprompt_text = render_template('command_reprompt')
    return question(reprompt_text)


@ask.intent('OnOffIntent', mapping={'OnOff': 'OnOff'})
def gpio_control(OnOff):
    command = OnOff

    if command is None:
        # == NULL
        reprompt_text = render_template('command_reprompt')
        return question(reprompt_text)
    elif command == "ligar" or command == "desligar":
        if command == "desligar": 
            s = {
                "led": "off"
            }   
            fname = os.path.join(app.static_folder, "status.json")
            with open(fname, "w") as outfile:
                json.dump(s, outfile) 
        else: 
            s = {
                "led": "on"
            }   
            fname = os.path.join(app.static_folder, "status.json")
            with open(fname, "w") as outfile:
                json.dump(s, outfile) 

        response_text = render_template('command', onOffCommand=command)
        return statement(response_text).simple_card('Comando', response_text)
    else:
        reprompt_text = render_template('command_reprompt')
        return question(reprompt_text)


@app.route("/read")
def readJSON():
	fname = os.path.join(app.static_folder, "status.json")

	with open(fname, "r") as openfile:
		json_obj = json.load(openfile)

	return json_obj['led']

if __name__ == "__main__":
	app.run()

