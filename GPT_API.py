from openai import OpenAI
from embedded import search_docs
client = OpenAI()

def ask_GPT(prompt, quesiton):
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": prompt},
      {"role": "user", "content": quesiton}
    ]
  )
  return completion.choice[0].message


qwestion = "Who is Harry Potter?"
prompt = search_docs(qwestion)

print(ask_GPT(prompt, qwestion))

