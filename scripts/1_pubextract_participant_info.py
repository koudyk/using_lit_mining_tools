from pathlib import Path

import pandas as pd

from pubextract.participants import _information_extraction

# load documents in labelbuddy format
labelbuddy_docs = (
    Path(__file__).resolve().parents[1]
    /"data"
    /"pubget_parkinsons"
    /"subset_allArticles_labelbuddyData"
    /"documents_00001.jsonl"
)
docs_df = pd.read_json(labelbuddy_docs, lines=True, orient='records')

# extract participant information
docs_dict = docs_df.to_dict('index')
docs_list_dicts = [doc_dict for doc_dict in docs_dict.values()]
annotated = list(_information_extraction.annotate_labelbuddy_docs(docs_list_dicts))

# save file
datafile = Path(__file__).resolve().parents[1] / "data" / "pubextract_annotations.jsonl"
df = pd.DataFrame(annotated)
df.to_json(datafile, lines=True, orient='records')

datafile_la = (
    Path(__file__).resolve().parents[2] 
    / "labelbuddy-annotation"
    / "projects"
    / "parkinsons"
    / "annotations"
    / "pubextract_annotations.jsonl"
)
df.to_json(datafile, lines=True, orient='records')
