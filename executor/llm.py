import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=api_key)

def run_task(task, parameters, model="gpt-4o", temperature=1):
    response = client.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": task.system_instruction},
            {"role": "user", "content": json.dumps(parameters)},
        ],
        temperature=temperature,
        response_format=task.output_schema
    )

    # When using .parse(), the parsed object is available at message.parsed
    parsed = response.choices[0].message.parsed
    if parsed is None:
        raise ValueError("Failed to parse response from OpenAI API")
    return parsed
