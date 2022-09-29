from flask import Flask, render_template
from flask import request
from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex

import pandas as pd
import random
import unicodedata
import re
from pathlib import Path

BASE_DIR=Path(__file__).resolve(strict=True).parent

search_index = AnnoyIndex(384, 'angular')
search_index.load(f"{BASE_DIR}/IN_patents3.ann")
model= SentenceTransformer(f"{BASE_DIR}/sent_bert_model")

app = Flask(__name__)


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


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        query = request.form.get("query")
        query_embed = model.encode(clean_text(query))
        similar_item_ids = search_index.get_nns_by_vector(query_embed,50,
                                                include_distances=True)
        results = pd.DataFrame(data={'Application Number': df.iloc[similar_item_ids[0]]['Application Number'].values, 
                                     'Title': df.iloc[similar_item_ids[0]]['Title'].values,
                                     'App Date': df.iloc[similar_item_ids[0]]['Application Date'].values})
        return render_template('table.html', tables=[results.to_html()], titles=[''])
    return render_template('table.html')
 

    



if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0')