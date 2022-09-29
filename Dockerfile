# syntax=docker/dockerfile:1

FROM python:3.9
WORKDIR /IN_PATENT_SEARCH

COPY requirements.txt requirements.txt
COPY sent_bert_model sent_bert_model
COPY templates templates
COPY df_pt_titles.csv df_pt_titles.csv
COPY IN_patents3.ann IN_patents3.ann
COPY main.py main.py


RUN pip3 install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["main.py"]