
def BrowserTableGenerator(meta_df):
    colFea = ['Assembly accession','Name','Completeness', 'Contamination','quality', '# contigs', 'Largest contig','Total length', 'GC (%)', 'N50','Assembly level',]
    colClassi = ['Assembly accession','Name','NCBI taxonomy', 'GTDB taxonomy (r214)', 'External link 1','External link 2',]
    colRefere = ['Assembly accession','Name', 'Biosample accession', 'Bioproject accession', 'WGS accession', 'Sequencing platform', 'Submission date',
                'Submitter','Title','PMID', 'DOI','Publish_date','Author',]
    colEnv = ['Assembly accession','Name','Geographic location', 'Environment']
    
    colTables=[colFea, colClassi, colRefere, colEnv]
    tablTables=[]
    for i in colTables:
        dftmp=meta_df.loc[:,i]
        tablTable=dftmp.to_html(index=None, escape=False).replace(
            '<table border="1" class="dataframe">',
            '<table class="table table-sm table-striped table-hover table table-fluid" id="myTable">'
            ).replace(
            '<thead>','<thead class="table-dark align-middle">'
            )
        tablTables.append(tablTable)
    return tablTables