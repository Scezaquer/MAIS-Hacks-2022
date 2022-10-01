import cohere
from flask import Flask, request, render_template

app=Flask(__name__)
co = cohere.Client('NGFlhn3qAO03wpB8B3I66DW6BTLZbnDSWJXusfpH', '2021-11-08')

@app.route('/')
def homepage():
    """prompt='Once upon a time in a magical land called'
    response = co.generate(prompt=prompt)
    return f'Prediction: {prompt} <b>{response.generations[0].text}<b>'"""
    return render_template("temp.html")

@app.route('/results/', methods = ["POST"])
def result_page():
    form_data = request.form
    print(form_data["Prompt"])
    propositions = ""
    prompt=form_data["Prompt"]
    for x in range(6):
        response = co.generate(prompt=prompt, max_tokens=200)
        propositions += f"<p>{response.generations[0].text}</p>"
    return f"<p>{prompt}...</p>\n\n<b>{propositions}</b>"


if __name__=='__main__':
    app.run()