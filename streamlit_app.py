from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex
import pandas as pd
import random
import unicodedata
import re
from pathlib import Path
#from rank_bm25 import BM25Okapi
import streamlit as st
import numpy as np
import time
#import boto3


#s3 = boto3.resource('s3')
#obj = s3.Object('patent-ann-file','IN_patents3.ann')
#data=obj.get()['Body'].read()


BASE_DIR=Path(__file__).resolve(strict=True).parent

search_index = AnnoyIndex(384, 'angular')

#@st.cache(hash_funcs={annoy.Annoy: my_hash_func})
#def load_ann():
      
#      search_index.load(f"{BASE_DIR}/IN_patents3.ann")
#      return search_index
      


#load_ann()
ann_file_path="https://patent-ann-file.s3.amazonaws.com/IN_patents3.ann"
#search_index.load(f"{BASE_DIR}/IN_patents3.ann")
search_index.load(ann_file_path)

#@st.cache(hash_funcs={"MyUnhashableClass": lambda _: None})
@st.cache(allow_output_mutation=True)
def load_model():
	  return SentenceTransformer(f"{BASE_DIR}/sent_bert_model")

model = load_model()


def clean_text(s):
    # Turn a Unicode string to plain ASCII
    def unicodeToAscii(s1):
        return ''.join(
            c for c in unicodedata.normalize('NFD', s1)
            if unicodedata.category(c) != 'Mn')
    s=" ".join(unicodeToAscii(s.strip()).split())
    return s.lower()

df_patents=pd.read_csv('df_pt_titles.csv')
df=df_patents.drop_duplicates().dropna(subset=['Title'])

#df['clean_title']=df['Title'].apply(clean_text)
#corpus = df['clean_title'].values.tolist()
#tokenized_corpus = [doc.split(" ") for doc in corpus]
#bm25 = BM25Okapi(tokenized_corpus)

st.header('Search Patents filed by Indians in India by title')
#st.subheader("semantic search with sbert")
with st.form('my_form'):
    #st.subheader('**Enter you query**')
    query = st.text_input('Enter you query',"type your query here")
    option = st.selectbox(
                    'Choose the search type',
                    ('Semantic Similarity Search', 'BM25'))
    if option=='Semantic Similarity Search':
        # Every form must have a submit button
        submitted = st.form_submit_button('Submit')
        t0 = time.time()

        query_embed = model.encode(clean_text(query))
	
        similar_item_ids = search_index.get_nns_by_vector(query_embed,50,
                                                    include_distances=True)
        results = pd.DataFrame(data={'Application Number': df.iloc[similar_item_ids[0]]['Application Number'].values, 
                                         'Title': df.iloc[similar_item_ids[0]]['Title'].values,
                                         'App Date': df.iloc[similar_item_ids[0]]['Application Date'].values}) 
        t1 = time.time()
        time_taken=np.round(t1-t0,2)
    else:
        submitted = st.form_submit_button('Submit')
        t0 = time.time()
        #clean_query = clean_text(query)
        #tokenized_query = clean_query.split(" ")
        #doc_scores = bm25.get_scores(tokenized_query)
        #similar_item_ids = doc_scores.argsort()[-50:][::-1]
        #results = pd.DataFrame(data={'Application Number': df.iloc[similar_item_ids]['Application Number'].values, 
        #                                 'Title': df.iloc[similar_item_ids]['Title'].values,
        #                                 'App Date': df.iloc[similar_item_ids]['Application Date'].values}) 
        
        results = pd.DataFrame(data={'Application Number': ["Currently not implemented in the search interface owing to resource constraints"], 
                                         'Title': ['XXXXX'],
                                         'App Date': ['XX-XX-XXXX']})         
        t1 = time.time()
        time_taken=np.round(t1-t0,2)
if submitted:
    #st.write(query_embed)
    st.write("Related titles with application number and application date")
    st.write(f"Retrieved in {time_taken} seconds")
    styler = results.style.hide_index()
    st.write(styler.to_html(escape=False), unsafe_allow_html=True)
else:
    st.write('No query submitted')                                     
