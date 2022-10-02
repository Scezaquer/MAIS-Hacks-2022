import requests

def generate_image(prompt):
    return requests.post(
        "https://api.deepai.org/api/text2img",
        data={
            'text': prompt,
        },
        headers={'api-key': '9f12c7c2-d85a-479c-9ac6-dd6b4784b6fc'}
    ).json()