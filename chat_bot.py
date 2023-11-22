import openai
import requests
from termcolor import colored

# Define the URL of the API endpoint
url = 'http://127.0.0.1:5000/query'

# Initialize the OpenAI client
client = openai.OpenAI(api_key="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")

while True:
    question = input("Enter your question (or type 'exit' to quit): ")
    if question.lower() == 'exit':
        break

    # Define the parameters for the query
    params = {
        'query': question,
        'n_results': '1'
    }

    # Make the GET request
    response = requests.get(url, params=params)
    results = None
    if response.status_code == 200:
        results = response.json()
    else:
        print("Error:", response.status_code, response.text)
        continue

    messages = [
        {
            "role": "user",
            "content": f"""You are a chatbot, answering questions about healthcare topics based on the information of the NHS. 
               You answer always consists of a summary of the provided information answering the question, and the source of the information, which is the link to the NHS site.
               This is your question: 
               {question}
               And this is the information the NHS has about it:
               {results.__str__()}
               """,
        },
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo",
        stream=True,
    )

    for i in chat_completion:
        print(i.choices[0].delta.content, end='')
    print("--------")
