import cohere
from flask import Flask, request, render_template
from prompt_mutator import *
from random import sample

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
    propositions = ""
    prompt=form_data["Prompt"]
    options = generate_mutations(prompt)
    options = sample(options, min(len(options), 6))
    for x in options:
        response = co.generate(prompt=x, max_tokens=200)
        propositions += f"<p>{x} <b>{response.generations[0].text}</b></p>"
    return f"<p>{prompt}...</p>\n\n{propositions}"


if __name__=='__main__':
    app.run()