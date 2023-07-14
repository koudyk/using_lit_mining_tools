from pathlib import Path

from lxml import etree
import pandas as pd
import spacy

from pubget import _utils

data = {}
parent =  (
    Path(__file__).resolve().parents[1] 
    / "data"
    / "pubget_parkinsons"
    / "articles"
)
for article_path in parent.glob("**/article.xml"): 
    xml = etree.parse(article_path)
    pmcid = _utils.get_pmcid(xml)
    article_meta = xml.xpath("//article/front/article-meta")[0]
    aff = article_meta.xpath("aff//text()")
    aff = (' ').join(aff).strip().split('\n')[-1]
    if len(aff) < 2:
        aff = article_meta.xpath("//contrib-group//aff//text()")
        aff = (' ').join(aff).strip().split('\n')[-1]
    data[pmcid] = aff.strip()

df = pd.DataFrame.from_dict(data, orient="index", columns=["affiliation"])
df = df.dropna()


detect_entities = spacy.load("en_core_web_sm")
cities_path = Path(__file__).resolve().parents[1] / "data" / "worldcities.csv"
cities = pd.read_csv(cities_path)
countries_set = set(list(cities["country"]))
countries_set = {x for x in countries_set if pd.notna(x)}
cities_set = set(list(cities["city"]))
cities_set = {x for x in cities_set if pd.notna(x)}
country_mapping = {
    "UK": "United Kingdom",
    "USA": "United States",
    "South Korea": "Korea, South",
}


for pmcid, row in df.iterrows():
    ents_set = set(
        str(row.affiliation).replace("/", "").replace("(", "").replace(")", "").split(", ")
    )
    country = countries_set.intersection(ents_set)
    if len(country) < 1:
        for before, after in country_mapping.items():
            if before in list(ents_set):
                country = {after}
    
    if len(country) < 1:
        for ent in list(ents_set):
            for c in list(countries_set):
                if c in ent:
                    country = {c}

    if len(country) > 0:
        country = list(country)[0]
        df.at[pmcid, "country"] = country

        subset = cities[cities["country"] == country]

        df.at[pmcid, "iso3"] = subset.iloc[0]["iso3"]
        df.at[pmcid, "longitude"] = subset.iloc[0]["lng"]
        df.at[pmcid, "latitude"] = subset.iloc[0]["lat"]

    city = cities_set.intersection(ents_set)
    if len(city) < 1:
        for ent in list(ents_set):
            for c in list(cities_set):
                if c in ent:
                    city = {c}

    if len(city) > 0:
        city = list(city)[0]
        df.at[pmcid, "city"] = city

        subset = cities[cities["city"] == city]
        df.at[pmcid, "longitude"] = subset.iloc[0]["lng"]
        df.at[pmcid, "latitude"] = subset.iloc[0]["lat"]
    
df = df.dropna()

destination = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "pubextract_author_locations.csv"
)
df.to_csv(destination)


