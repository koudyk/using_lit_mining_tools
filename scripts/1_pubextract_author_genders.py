from pathlib import Path

import pandas as pd

from pubextract.authors import authors

# load the csv with the authors for each paper
csv_path = (
    Path(__file__).resolve().parents[1]
    /"data"
    /"pubget_parkinsons"
    /"subset_allArticles_extractedData"
    /"authors.csv"
)
df = pd.read_csv(csv_path)

# get the first and last authors' first names,
# guess their gender from their name, 
# and categorize the papers in one of these author-gender catgories:
# man-man(man first author, man last author),
# man-woman, woman-man, or woman-woman
df = authors.paper_gender_categories(df)

# save output
gender_csv = (
    Path(__file__).resolve().parents[1]
    /"data"
    /"author_genders.csv"
)
df.to_csv(gender_csv, index=False)
