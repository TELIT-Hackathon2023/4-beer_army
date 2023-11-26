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

API_KEY = "Api"
RESOURCE_ENDPOINT = "sourse"

openai.api_type = "azure"
openai.api_key = API_KEY
openai.api_base = RESOURCE_ENDPOINT
openai.api_version = "2022-12-01"

url = openai.api_base + "/openai/deployments?api-version=2022-12-01" 

r = requests.get(url, headers={"api-key": API_KEY})

# df=pd.read_csv(os.path.join(os.getcwd(),'Data-full-NEW.csv')) # This assumes that you have placed the bill_sum_data.csv in the same directory you are running Jupyter Notebooks
# print(df)
# df_bills = df[['full_data']]

# # print(df_bills)
# pd.options.mode.chained_assignment = None #https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#evaluation-order-matters


# tokenizer = tiktoken.get_encoding("cl100k_base")
# df_bills['n_tokens'] = df_bills["full_data"].apply(lambda x: len(tokenizer.encode(x)))
# df_bills = df_bills[df_bills.n_tokens<8192]
# df_bills.to_csv('final_NOembedded.csv', index=False)

# sample_encode = tokenizer.encode(df_bills.full_data[0]) 
# decode = tokenizer.decode_tokens_bytes(sample_encode)



# @retry(stop=stop_after_attempt(5), wait=wait_fixed(1))
# def get_embedding_with_retry(text, engine):
#     print('GG')
#     return get_embedding(text, engine=engine)

# try:
#     df_bills['ada_v2'] = df_bills["full_data"].apply(lambda x: get_embedding_with_retry(x, engine='embeddings-GreenBox'))
# except Exception as e:
#     print("Failed to get embeddings after several attempts:", e)


# df_bills.to_csv('final_embedded.csv', index=False)
# print(df_bills)





def search_docs(user_query, to_print=True):
    df = pd.read_csv('final_embedded.csv')
    embedding = get_embedding(
        user_query,
        engine="embeddings-GreenBox" # This line assumes you have access to a function that retrieves the embedding
    )

    # Ensure the embedding is a NumPy array
    embedding = np.array(embedding)

    def safe_cosine_similarity(x):
        # Convert x to a numpy array and check for shape mismatch
        x = np.array(x)
        if x.shape != embedding.shape:
            return 0
        return cosine_similarity(x, embedding)

    df["similarities"] = df.ada_v2.apply(safe_cosine_similarity)

    res = df.sort_values("similarities", ascending=False).head(10)
    # if to_print:
    #     print(res)
    return res['full_data']


# res = search_docs('Who is Germiona?')