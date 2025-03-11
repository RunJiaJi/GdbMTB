from Bio import Entrez
import time
import sys
import pandas as pd

Entrez.email = "XXX@Xmail.com" #please input your valid email in here

inputfile = sys.argv[1]

def obtain_pmid(assembly_accession):
  # Step 1: Search for the genome assembly
  time.sleep(1)
  search_handle = Entrez.esearch(db="assembly", term=assembly_accession)
  search_results = Entrez.read(search_handle)
  search_handle.close()

  if search_results['IdList']:
    assembly_id = search_results['IdList'][0]

    # Step 2: Find linked publications in PubMed
    link_handle = Entrez.elink(dbfrom="assembly", id=assembly_id, db="pubmed")
    link_results = Entrez.read(link_handle)
    link_handle.close()

    pmids = []
    for linkset in link_results:
        if 'LinkSetDb' in linkset:
            for link in linkset['LinkSetDb']:
                if 'Link' in link:
                    for item in link['Link']:
                        pmids.append(item['Id'])
  # time.sleep(0.5)

  return pmids

def fetch_pubmed_metadata(nr_choosed_pmid_list):
  metadata = {
          "Title": [],
          "Publish_date": [],
          "DOI": [],
          "Author_list": [],
          "Author": [],
          "Journal": [],
          "Abstract": [],

      }
  for pmid in nr_choosed_pmid_list:
    if pmid == '-':
      for key,value in metadata.items():
        value.append('-')
    else:
      print(pmid)
      time.sleep(1)
      handle = Entrez.efetch(db="pubmed", id=pmid, retmode="xml")
      records = Entrez.read(handle)
      handle.close()

      record = records['PubmedArticle'][0]

      metadata["Title"].append(record['MedlineCitation']['Article']['ArticleTitle'])
      metadata["Publish_date"].append(record['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate'].get('Year')),
      metadata["Journal"].append(record['MedlineCitation']['Article']['Journal']['ISOAbbreviation']),


      for article_id in record['PubmedData']['ArticleIdList']:
          if article_id.attributes['IdType'] == 'doi':
              metadata["DOI"].append(str(article_id))

      authors=[]
      for author in record['MedlineCitation']['Article']['AuthorList']:
          if 'ForeName' in author and 'LastName' in author:
              authors.append(f"{author['ForeName']} {author['LastName']}")
      metadata["Author_list"].append(authors)
      metadata["Author"].append(authors[0]+' et al.')

      if 'Abstract' in record['MedlineCitation']['Article']:
          metadata["Abstract"].append(record['MedlineCitation']['Article']['Abstract']['AbstractText'][0])

      # time.sleep(0.5)
  metadata_df = pd.DataFrame.from_dict(metadata)
  metadata_df['nrPMID'] = nr_choosed_pmid_list
  metadata_df.set_index('nrPMID',inplace=True)
  return metadata_df


with open(inputfile) as f:
  accs=[i.strip() for i in f.readlines()]

tmpdict = {}
tmpdict['Assembly_accession'] = accs

pmids_list=[]
for acc in accs:
  print(acc)
  pmids=obtain_pmid(acc)
  print(pmids)
  pmids_list.append(pmids)
len(pmids_list)


tmpdict['PMID_check_list']=pmids_list
tmpdict['PMID']=[i[0] if i else '-' for i in pmids_list] # Choosing the first article as the representative of the genome is risky and requires manual reconfirmation

choosed_pmid_list = tmpdict['PMID']
nr_choosed_pmid_list = list(set(choosed_pmid_list))
metadata_df = fetch_pubmed_metadata(nr_choosed_pmid_list)
metadata_df_sorted = metadata_df.loc[choosed_pmid_list,:]
tmpdict['Publish_date'] = metadata_df_sorted["Publish_date"].tolist()
tmpdict['Title'] = metadata_df_sorted["Title"].tolist()
tmpdict['Author_list'] = metadata_df_sorted["Author_list"].tolist()
tmpdict['Author'] = metadata_df_sorted["Author"].tolist()
tmpdict['DOI'] = metadata_df_sorted["DOI"].tolist()
tmpdict['Journal'] = metadata_df_sorted["Journal"].tolist()
tmpdict['Abstract'] = metadata_df_sorted["Abstract"].tolist()

df = pd.DataFrame(tmpdict)

output = 'Resolved_reference.csv'
df.to_csv(output, index=None)