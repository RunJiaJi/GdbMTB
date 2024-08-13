from flask import Flask, render_template, url_for
import pandas as pd
from BrowserTableGenerator import resolve_externalLinks, BrowserTableGenerator

app = Flask(__name__)

meta_df = pd.read_csv('./data/MTB_348_metadata_all_PRIVATE.csv')
meta_df = resolve_externalLinks(meta_df)
tablTables = BrowserTableGenerator(meta_df)

with open('data/Tree_of_MTB_.svg')as f:
    treeSVG=f.read()

cities = []

locs=meta_df['Geographic location'].tolist()
gNames=meta_df['Organism Name'].tolist()
lats=meta_df['latitude'].tolist()
longs=meta_df['longitude'].tolist()

for idx in range(len(gNames)):
    ele = {'title':locs[idx]+'\n'+gNames[idx], 'latitude':lats[idx], 'longitude':longs[idx]}
    cities.append(ele)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', cities=cities)

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
    return render_template('tree-taxa.html', title='Tree', treeSVG=treeSVG)

@app.route("/tree-tree")
def tree_tree():
    return render_template('tree-tree.html', title='Tree', treeSVG=treeSVG)

@app.route("/statistics")
def statistics():
    return render_template('statistics.html', title='Statistics')

@app.route("/downloads")
def download():
    return render_template('downloads.html', title='Download')

@app.route("/about")
def tools():
    return render_template('about.html', title='Tools')
    
if __name__ == '__main__':
    app.run(debug=True)