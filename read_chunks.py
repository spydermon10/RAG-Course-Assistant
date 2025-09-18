# jsons are stored in embeddings using joblib

import requests 
import json
import os
import pandas as pd
import numpy as np
import joblib

def create_embedding(text_list):
    r=requests.post("http://localhost:11434/api/embed",json={
        "model" : "bge-m3",
        "input" : text_list
    })

    embedding=r.json()["embeddings"]
    return embedding

jsons =    os.listdir("jsons")


my_dicts=[]
chunk_id=0

for json_file in jsons:
    with open(f"jsons/{json_file}") as f:
        content = json.load(f)
    print(f"creating embedding for {json_file}")    
    embeddings=create_embedding([c["text"] for c in content["chunks"]])    

    for i,chunk in enumerate(content['chunks']):
        chunk["chunk_id"]=chunk_id
        chunk_id=chunk_id+1
        chunk["embedding"]=embeddings[i]
        my_dicts.append(chunk)
        
    
        
        
        
df=pd.DataFrame.from_records(my_dicts)
joblib.dump(df,"embeddings.joblib")



