
def BrowserTableGenerator(meta_df):
    colFea = ['Accession',
            'Organism Name',
            'Size (bp)',
            'GC (%)',
            'Assembly level',
            'N50',
            'Number_of_contigs',
            'Number of CDS',
            'Number of tRNAs',
            'tRNAs',
            'Number of rRNA genes',
            'Number of 5S rRNA gene',
            'Number of 16S rRNA gene',
            'Number of 23S rRNA gene',
            'CheckM completeness(%)',
            'CheckM contamination(%)',
            'CheckM2 completeness(%)(GB_model)',
            'CheckM2 completeness(%)(NN_model)',
            'CheckM2 contamination(%)',
            'BUSCO completeness(%)',
            'BUSCO contamination(%)',
            'pass.GUNC'
            ]
    # colClassi = ['Assembly accession','Name','NCBI taxonomy', 'GTDB taxonomy (r214)', 'External link 1','External link 2',]
    colClassi = ['Accession', 'Organism Name', 'GTDB_r220_classification']
    colRefere = ['Accession',
            'Organism Name',
            'Bioproject accession',
            'Biosample accession',
            'WGS accession',
            'Sequencing platform',
            'Submission date',
            'Submitter',
            'PMID',
            'Publish_date',
            'Title',
            'Author',
            'DOI',
            'Journal',
            'recognized_as_MTB_through_magnetic_cell_enrichment',
            'recognized_as_putative_MTB_through_MGC_identification'
            ]
    colEnv = ['Accession',
            'Organism Name',
            'Geographic location',
            'Geographic coordinates',
            'Environment',
            'Environment (note)'
            ]
    
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