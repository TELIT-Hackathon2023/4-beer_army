import openai
import os
import re
import requests
import sys
from num2words import num2words
import os
import pandas as pd
import numpy as np
import time
from openai.embeddings_utils import get_embedding, cosine_similarity
import tiktoken
from tenacity import retry, stop_after_attempt, wait_fixed

API_KEY = os.getenv("AZURE_OPENAI_API_KEY") 
RESOURCE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") 

openai.api_type = "azure"
openai.api_key = API_KEY
openai.api_base = RESOURCE_ENDPOINT
openai.api_version = "2022-12-01"

url = openai.api_base + "/openai/deployments?api-version=2022-12-01" 

r = requests.get(url, headers={"api-key": API_KEY})

df=pd.read_csv(os.path.join(os.getcwd(),'Data-full-NEW.csv')) # This assumes that you have placed the bill_sum_data.csv in the same directory you are running Jupyter Notebooks
print(df)
df_bills = df[['full_data']]

# print(df_bills)
pd.options.mode.chained_assignment = None #https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#evaluation-order-matters


tokenizer = tiktoken.get_encoding("cl100k_base")
df_bills['n_tokens'] = df_bills["full_data"].apply(lambda x: len(tokenizer.encode(x)))
df_bills = df_bills[df_bills.n_tokens<8192]
df_bills.to_csv('final_NOembedded.csv', index=False)

sample_encode = tokenizer.encode(df_bills.full_data[0]) 
decode = tokenizer.decode_tokens_bytes(sample_encode)



@retry(stop=stop_after_attempt(5), wait=wait_fixed(1))
def get_embedding_with_retry(text, engine):
    return get_embedding(text, engine=engine)

try:
    df_bills['ada_v2'] = df_bills["full_data"].apply(lambda x: get_embedding_with_retry(x, engine='embeddings-GreenBox'))
except Exception as e:
    print("Failed to get embeddings after several attempts:", e)


df_bills.to_csv('final_embedded.csv', index=False)
print(df_bills)

def search_docs(df, user_query, top_n=3, to_print=True):
    embedding = get_embedding(
        user_query,
        engine="text-embedding-ada-002" # engine should be set to the deployment name you chose when you deployed the text-embedding-ada-002 (Version 2) model
    )
    df["similarities"] = df.ada_v2.apply(lambda x: cosine_similarity(x, embedding))

    res = (
        df.sort_values("similarities", ascending=False)
        .head(top_n)
    )
    if to_print:
        print(res)
    return res
