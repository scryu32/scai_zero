from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get('SCAI_KEY'),
)

def fetch_assistant_response(messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
        max_tokens=1600,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content

