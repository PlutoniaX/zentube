import os
import dspy
from groq import Groq

# Initialize the GROQ client for the standalone function
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def groq_response(prompt, temp=0):
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="mixtral-8x7b-32768",
        temperature=temp,
    )

    return chat_completion.choices[0].message.content

# Initialize the DSPy GROQ language model
groq_lm = dspy.GROQ(
    model='mixtral-8x7b-32768',
    api_key=os.environ.get("GROQ_API_KEY")
)

# Configure DSPy to use the GROQ language model
dspy.configure(lm=groq_lm)