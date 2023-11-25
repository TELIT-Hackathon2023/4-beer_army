import openai
import os
import re
import requests
import sys
from num2words import num2words
import os
import pandas as pd
import numpy as np
from openai.embeddings_utils import get_embedding, cosine_similarity
import tiktoken

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
df_bills = df['full_data']

# print(df_bills)
pd.options.mode.chained_assignment = None #https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#evaluation-order-matters


tokenizer = tiktoken.get_encoding("cl100k_base")
df_bills['n_tokens'] = df_bills["full_data"].apply(lambda x: len(tokenizer.encode(x)))
df_bills = df_bills[df_bills.n_tokens<8192]


sample_encode = tokenizer.encode(df_bills.full_data[0]) 
decode = tokenizer.decode_tokens_bytes(sample_encode)

df_bills['ada_v2'] = df_bills["full_data"].apply(lambda x : get_embedding(x, engine = 'embeddings-GreenBox')) # engine should be set to the deployment name you chose when you deployed the text-embedding-ada-002 (Version 2) model


print(df_bills)