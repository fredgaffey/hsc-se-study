# import flask
# flask_dict = flask.__dict__
# for i in flask_dict:
#     print(i)
from flask import render_template, Flask, request
import ollama
app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def main():
    if request.method == "GET":
        return render_template("main.html")



@app.route("/ai_question",methods=["POST","GET"])
def ask_question():
    question = request.form.get("ai_question")

    answer = get_response_from_ollama(question)
    return render_template("chat.html", question = question, answer = answer)

def get_response_from_ollama(user_input):
    # Get the response from the locally running Ollama model
    response = ollama.chat(model="gemma3:4b", messages=[{"role": "user", "content": user_input}])

    if 'message' in response:
        return response['message']['content']
    else:
        return 'Sorry, something went wrong.'

if __name__ == '__main__':
	app.run()