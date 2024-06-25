import pandas as pd
import re

col_names = ['seqid', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attributes']
df = pd.read_csv('Homo_sapiens.GRCh38.85.gff3.gz', compression='gzip',
                         sep='\t', comment='#', low_memory=False,
                         header=None, names=col_names)
# interesantes:

# In [15]:  df.phase.unique()
#df.type.unique()
#df.seqid.unique()
#In [11]: len(df)
#Out[11]: 2601849

edf = df[df.source.isin(['ensembl', 'havana', 'ensembl_havana'])]
ndf = edf[edf.type == 'gene']
ndf = ndf.copy()


RE_GENE_NAME = re.compile(r'Name=(?P<gene_name>.+?);')
def extract_gene_name(attributes_str):
    res = RE_GENE_NAME.search(attributes_str)
    return res.group('gene_name')


ndf['gene_name'] = ndf.attributes.apply(extract_gene_name)
RE_GENE_ID = re.compile(r'gene_id=(?P<gene_id>ENSG.+?);')
def extract_gene_id(attributes_str):
    res = RE_GENE_ID.search(attributes_str)
    return res.group('gene_id')


ndf['gene_id'] = ndf.attributes.apply(extract_gene_id)


RE_DESC = re.compile('description=(?P<desc>.+?);')
def extract_description(attributes_str):
    res = RE_DESC.search(attributes_str)
    if res is None:
        return ''
    else:
        return res.group('desc')


ndf['desc'] = ndf.attributes.apply(extract_description)


ndf.drop('attributes', axis=1, inplace=True)

ndf.to_pickle('gene_data.pkl')

