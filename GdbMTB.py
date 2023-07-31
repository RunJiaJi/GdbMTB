from flask import Flask, render_template, url_for
import pandas as pd
from BrowserTableGenerator import BrowserTableGenerator
app = Flask(__name__)

meta_df=pd.read_csv('./data/MTB_genomes_metadata_202307.tsv', sep='\t')
tablTables = BrowserTableGenerator(meta_df)

with open('data/Tree_of_MTB.svg')as f:
    treeSVG=f.read()

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

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

@app.route("/tree")
def tree():
    return render_template('tree.html', title='Tree', treeSVG=treeSVG)

@app.route("/statistics")
def statistics():
    return render_template('statistics.html', title='Statistics')

@app.route("/download")
def download():
    return render_template('download.html', title='Download')

@app.route("/tools")
def tools():
    return render_template('tools.html', title='Tools')
    
if __name__ == '__main__':
    app.run(debug=True)