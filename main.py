import cohere
from flask import Flask, request, render_template
from prompt_mutator import *
from multiprocessing import Pool
from image_generator import *

app=Flask(__name__)
#co = cohere.Client('NGFlhn3qAO03wpB8B3I66DW6BTLZbnDSWJXusfpH', '2021-11-08')

co = cohere.Client('NGFlhn3qAO03wpB8B3I66DW6BTLZbnDSWJXusfpH')
#default_settings = {"model":"large", "max_tokens":200}
default_settings = {"model":'large',
    "prompt":'{}', 
    "max_tokens":200,
    "temperature":0.8,
    "k":0,
    "p":1,
    "frequency_penalty":0,
    "presence_penalty":0,
    "stop_sequences":["--"],
    "return_likelihoods":'NONE'}

text_message_settings = {"model":'large',
        "prompt":'Command: Thank Sid for the gift cards\nEmail: Hey Sid, Thank you so much for the gift cards. I really appreciate it. I hope to see you soon\n--\nCommand: Invoice Nicole $500 for financial modeling\nEmail: Dear Nicole, This is my invoice for $500 for the financial modeling. It was a pleasure to work with you\n--\nCommand: Tell Kiyan that they made it to the next round\nEmail: Hey Kiyan, You\'ve moved forward to the next round of interviews. The team is looking forward to seeing you again\n--\nCommand: Ask Adrien for a coffee chat\nEmail: Hey Adrien, Long time no see! Let\'s catch up and grab coffee. What\'s your schedule look like?\n--\nCommand: {}\nEmail:',
        "max_tokens":100,
        "temperature":0.7,
        "k":0,
        "p":0.75,
        "frequency_penalty":0,
        "presence_penalty":0,
        "stop_sequences":["--"],
        "return_likelihoods":'NONE'}

pro_email_settings = {"model":'large',
        "prompt":"""Command: Thank Karim for the job interview\nEmail: Dear Karim, Thank you for meeting with me today to discuss the [job title] position at [company]. It was a pleasure to meet you, and I enjoyed discussing [reference to interview conversation]. I'm excited about the opportunity to lend my skills and [industry or education] experience to the [department] team, as I believe I could be a valuable asset in your [project] work. I look forward to hearing from you soon. Please let me know if you need any additional information. Best regards, [Name]\n--\n
        Command: Ask Emma for clarification about her email\nEmail: Hello Emma, Thank you for taking the time to reach out to me. Could you please provide me with some additional information so I can better understand your request? I'd like to assist you as quickly as possible. If you could please detail the three most important points that you need my help with, that would help speed up the process. Once I have this clarification, I'll be able to assist you more effectively. Thank you, [Name]\n--\n
        Command: Offer a 30% discount to Amanda\nEmail:Hi Amanda, Thank you so much for being a customer of [your company name]. It’s because of people like you we have been able to be in business for such a long time. To thank you, we have created a discount coupon especially for you. Use the code [unique code number] to get a discount of 30% from any product in our store [insert link to your online shop]. But hurry! The offer is only available for the first [add number or time limit] people who make the purchase. Thank you, [Your signature]\n--\n
        Command: Decline the job offer at Petco\nEmail: Dear [Name], Thank you for offering me the position at Petco. I appreciate you taking the time to consider me for this job. After careful consideration, I've realized that this is not the best fit for my goals at this time. I've decided to accept another position. Thank you again for your time and support. I wish you the best in finding the right employee for this position. Regards, [Name]\n--\n
        Command: Invite Bob to my event\nEmail: Hi Bob, It is that time of the year again when we have our [name of the event]. It is a day where we [describe your event in about two lines]. You have become a valued part of our company, we would love it if you’re able to come, but we understand if you can’t. Please click this invitation link [insert link] and RSVP yes or no. Thank you, [Your signature]\n--\n
        Command: {}\nEmail: """,
        "max_tokens":300,
        "temperature":0.7,
        "k":0,
        "p":0.75,
        "frequency_penalty":0,
        "presence_penalty":0,
        "stop_sequences":["--"],
        "return_likelihoods":'NONE'}

@app.route('/')
def homepage():
    """prompt='Once upon a time in a magical land called'
    response = co.generate(prompt=prompt)
    return f'Prediction: {prompt} <b>{response.generations[0].text}<b>'"""
    return render_template("temp.html")

@app.route('/results/', methods = ["POST"])
def result_page():
    start = time()
    max_number = 5
    form_data = request.form
    generator_type = "Images"
    propositions = ""
    prompt=form_data["Prompt"]
    settings = default_settings
    mutated_prompts = [prompt] + generate_mutations(prompt, max_number)

    if generator_type == "Text":
        for id, text in enumerate(mutated_prompts):
            mutated_prompts[id]=[text, settings]

        with Pool(max_number+1) as p:
            results = p.starmap(edit_prompt_and_generate, mutated_prompts)

        for id, result in enumerate(results):
            propositions += f"<p>{mutated_prompts[id][0]} <b>{result}</b></p>"
    
    elif generator_type == "Images":
        with Pool(max_number+1) as p:
            results = p.map(generate_image, mutated_prompts)
        
        for id, result in enumerate(results):
            propositions += f'<p>{mutated_prompts[id]} <img src="{result["output_url"]}"></p>\n'

    print(time()-start)
    return f"<p>{prompt}...</p>\n\n{propositions}"

def edit_prompt_and_generate(prompt, settings):
    return co.generate(
        model=settings["model"],
        prompt=settings["prompt"].format(prompt),
        max_tokens=settings["max_tokens"],
        temperature=settings["temperature"],
        k=settings["k"],
        p=settings["p"],
        frequency_penalty=settings["frequency_penalty"],
        presence_penalty=settings["presence_penalty"],
        stop_sequences=settings["stop_sequences"],
        return_likelihoods=settings["return_likelihoods"]).generations[0].text

if __name__=='__main__':
    app.run()