from flask import Flask, render_template, url_for
import pandas as pd
from BrowserTableGenerator import BrowserTableGenerator
app = Flask(__name__)

meta_df=pd.read_csv('./data/MTB_genomes_metadata_202308.tsv', sep='\t')
tablTables = BrowserTableGenerator(meta_df)

with open('data/Tree_of_MTB.svg')as f:
    treeSVG=f.read()

cities="""[{title: 'Sweden: Oskarshamn\nUncultured_microorganism_SbSrfc_SA12_01_D19', latitude: 57.4354483, longitude: 16.6691272},
 {title: 'USA: Nevada\nOmnitrophica_bacterium_SCGC_AG-290-C17', latitude: 37.1312714, longitude: -116.8425033},
 {title: 'Greece: Etoliko Lagoon\nRhodospirillaceae_bacterium_MAG_01419_mvb_30', latitude: 38.4884872, longitude: 21.2875175},
 {title: 'USA: Sakinaw Lake\nLatescibacteria_bacterium_SCGC_AAA252-B13', latitude: 49.95898915, longitude: -123.8279332},]"""

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