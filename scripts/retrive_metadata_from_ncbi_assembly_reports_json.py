import pandas as pd
import json
import sys

json_files = sys.argv[1:]

def naming(organism):
    if 'infraspecific_names' not in organism:
        return organism['organism_name'].replace(' ','_')
    elif 'isolate' in organism['infraspecific_names']:
        if organism['infraspecific_names']['isolate'] in organism['organism_name']:
            return organism['organism_name'].replace(' ','_')
        else:
            return (organism['organism_name'] + '_'+ organism['infraspecific_names']['isolate']).replace(' ','_')
    elif 'strain' in organism['infraspecific_names']:
        if organism['infraspecific_names']['strain'] in organism['organism_name']:
            return organism['organism_name'].replace(' ','_')
        else:
            return (organism['organism_name'] + '_'+ organism['infraspecific_names']['strain']).replace(' ','_')

def retrive_meta_from_ncbi_json(json_file):
    with open(json_file)as f:
        content=json.load(f)
    df=pd.DataFrame.from_dict(content['reports'])
    dftmp = pd.DataFrame()
    dftmp['Assembly accession'] = df.accession

    name = df.apply(lambda x: naming(x.organism),axis=1)
    dftmp['Organism Name'] = name

    bioproject_acc = df.apply(lambda x: x.assembly_info['bioproject_accession'] if 'bioproject_accession' in x.assembly_info else 
        x.assembly_info['bioproject_lineage'][0]['bioprojects'][0]['accession'], axis=1)
    dftmp['Bioproject accession'] = bioproject_acc

    biosample_acc = df.apply(lambda x: x.assembly_info['biosample']['accession'],axis=1)
    dftmp['Biosample accession']=biosample_acc

    if 'wgs_info' in df:
        WGS_accession = df.apply(lambda x: x.wgs_info['master_wgs_url'].split('/')[-1].split('.')[0] if isinstance(x.wgs_info, dict) else '-',axis=1) #
        dftmp['WGS accession'] = WGS_accession

    assembly_level=df.apply(lambda x: x.assembly_info['assembly_level'], axis=1)
    dftmp['Assembly level'] = assembly_level

    # length = df.apply(lambda x: x.assembly_stats['total_sequence_length'],axis=1)
    # dftmp['Length'] = length

    # number_of_contigs = df.apply(lambda x: x.assembly_stats['number_of_contigs'],axis=1)
    # dftmp['Number of contigs'] = number_of_contigs

    # N50 = df.apply(lambda x: x.assembly_stats['contig_n50'],axis=1)
    # dftmp['N50'] = N50

    sequencing_tech = df.apply(lambda x: x.assembly_info['sequencing_tech'] if 'sequencing_tech' in x.assembly_info else '-',axis=1)
    dftmp['Sequencing platform']=sequencing_tech

    submission_date = df.apply(lambda x: x.assembly_info['biosample']['submission_date'] ,axis=1)
    dftmp['Submission date']=submission_date

    submitter = df.apply(lambda x: x.assembly_info['submitter'],axis=1)
    dftmp['Submitter']=submitter

    # csv_file_name=json_file.replace('.json','.csv')
    # dftmp.to_csv(csv_file_name, index=None)
    return dftmp

dfs=[]
for json_file in json_files:
    dfs.append(retrive_meta_from_ncbi_json(json_file))

df = pd.concat(dfs)
df.sort_values('Submission date', inplace=True)
df.to_csv('all_metadata.csv', index=None)
