from flask import Flask, render_template, url_for
import pandas as pd
from BrowserTableGenerator import resolve_externalLinks, BrowserTableGenerator
from get_json import build_tree, get_external_links

app = Flask(__name__)

# 1. read the metadata table
meta_df = pd.read_csv('./data/MTB_365_metadata_all_PRIVATE.csv')

# 2. generate the browser tables
meta_df = resolve_externalLinks(meta_df)
tablTables = BrowserTableGenerator(meta_df)

# 3. read the tree of MTB
with open('data/1_tree_from_iTOL_for_website.svg')as f:
    treeSVG=f.read()

# 4. resolve the geographical locs and generate cities list
cities = []

locs=meta_df['Geographic location'].tolist()
gNames=meta_df['Organism Name'].tolist()
lats=meta_df['latitude'].tolist()
longs=meta_df['longitude'].tolist()

for idx in range(len(gNames)):
    ele = {'title':locs[idx]+'\n'+gNames[idx], 'latitude':lats[idx], 'longitude':longs[idx]}
    cities.append(ele)

# 5. generate the nested taxa tree
tree_json = build_tree(meta_df)
idToExternalLink = get_external_links(meta_df)

# 6. read the diversity plot
with open('static/figure/Fig1_phyla_history_plot.svg')as f:
    diversitySVG=f.read()

# 7. read the feature plot
with open('static/figure/Fig2_quality_scatter_plot.svg') as f:
    feaSVG = f.read()

# 8. read the distribution map plot
with open('static/figure/Fig3_Map_with_different_env.svg') as f:
    disSVG = f.read()

# 9. read the number of genomes
num_genomes = len(meta_df)

# 10. get the 10 most recent scientific papers
recent_papers = meta_df[['Title', 'Author', 'DOI', 'Journal', 'Publish_date']].copy()

# Filter out papers with missing or empty titles
recent_papers = recent_papers.dropna(subset=['Title', 'Publish_date'])
recent_papers = recent_papers[recent_papers['Title'].str.strip() != '']  # Remove empty titles
recent_papers = recent_papers[recent_papers['Title'] != '-']  # Remove placeholder titles

# Remove duplicates and get the 10 most recent
recent_papers = recent_papers.drop_duplicates(subset=['Title'])
recent_papers = recent_papers.sort_values('Publish_date', ascending=False).head(10)
recent_papers_list = recent_papers.to_dict('records')

# Debug: Print the papers being selected
print(f"Number of papers selected: {len(recent_papers_list)}")
for i, paper in enumerate(recent_papers_list):
    print(f"Paper {i+1}: {paper['Title'][:50]}... ({paper['Publish_date']})")


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', cities=cities, num_genomes=num_genomes, recent_papers=recent_papers_list)

@app.route("/browser/QualityandFeature")
def browser_fea():
    return render_template('browser.html', title='Browser', table=tablTables[0], tableHeader='Quality and feature')

@app.route("/browser/classification")
def browser_classi():
    return render_template('browser.html', title='Browser', table=tablTables[1], tableHeader='Classification')

@app.route("/browser/reference")
def browser_refre():
    return render_template('browser.html', title='Browser', table=tablTables[2], tableHeader='Reference')

@app.route("/browser/EnvironmentalMetadata")
def browser_env():
    return render_template('browser.html', title='Browser', table=tablTables[3], tableHeader='Environmental metadata')

@app.route("/browser/MagnetosomeGeneClusters")
def browser_mgc():
    return render_template('browser-mgc.html', title='Browser')

@app.route("/tree-taxa")
def tree_taxa():
    return render_template('tree-taxa.html', title='Tree', tree_json = tree_json, idToExternalLink=idToExternalLink)

@app.route("/tree-tree")
def tree_tree():
    return render_template('tree-tree.html', title='Tree', treeSVG=treeSVG)

@app.route("/statistics")
def statistics():
    return render_template('statistics.html', title='Statistics', diversitySVG=diversitySVG, feaSVG=feaSVG, disSVG=disSVG)

@app.route("/downloads")
def download():
    return render_template('downloads.html', title='Download')

@app.route("/about")
def tools():
    return render_template('about.html', title='Tools')
    
if __name__ == '__main__':
    app.run(debug=True)