import pandas as pd
from venn import venn

# -----------------------------------------------------------------------------
def readCorrelationList(filename):
    dfPersons = pd.read_csv(filename, 
                index_col='contributorID',
               dtype = {'names': str, 'kbrIDs': str, 'isniIDs': str},
               parse_dates=['birthDate', 'deathDate'],
               keep_default_na=True)
    return dfPersons

# -----------------------------------------------------------------------------
def createBELTRANSVennDiagram(df, fig=None):       
    dfKBRPersons = df[~df['kbrIDs'].isna()]
    dfBnFPersons = df[~df['bnfIDs'].isna()]
    dfNTAPersons = df[~df['ntaIDs'].isna()]
    dfUnescoPersons = df[~df['unescoIDs'].isna()]
    
    identifiers = {
    "KBR": set(dfKBRPersons.index),
    "BnF": set(dfBnFPersons.index),
    "NTA": set(dfNTAPersons.index),
    "Unesco": set(dfUnescoPersons.index)
    }
    if fig:
        venn(identifiers, ax=fig)
    else:
        venn(identifiers)

# -----------------------------------------------------------------------------
def countDuplicateDifference(df1, df2, columnName):
    before = df1[~df1[columnName].isna()].duplicated().sum()
    after = df2[~df2[columnName].isna()].duplicated().sum()
    print(f'Duplicate {columnName} before: {before} and after {after}')

# -----------------------------------------------------------------------------
def prepareMissingNationalityList(df, identifierName, explodedIdentifierName):
    # Only get the records for which we have at least one given identifier
    # and for which we do not have a nationality
    correlationList = df[(~df[identifierName].isna()) & (df['nationalities'].isna())].copy()
    print(f'Number of missing {identifierName} nationalities: {correlationList.shape[0]}')
    
    # first make the semicolon-separated string a Python list
    correlationList[explodedIdentifierName] = correlationList[identifierName].str.split(';', expand=False)
    
    # now explode the list created in the last step
    correlationListExploded = correlationList.explode(explodedIdentifierName)
    print(f'Number of missing {identifierName} nationalities (after exploding): {correlationListExploded.shape[0]}')
    return correlationListExploded

# -----------------------------------------------------------------------------
def createExplodedList(df, column, explodedColumnName, delimiter=';'):
    selection = df.loc[~df[column].isna(), [column]].copy()
    selection[explodedColumnName] = selection[column].str.split(delimiter, expand=False)
    print(f'Number of non empty {column} values: {selection.shape[0]}')
    
    explodedDf = selection.explode(explodedColumnName)
    print(f'Number of non empty {column} values (after exploding): {explodedDf.shape[0]}')
    return explodedDf

# -----------------------------------------------------------------------------
def computeLocalBnFIdentifier(df, bnfIDColumn):
    identifiers = []
    fullIdentifierRaw = str(df[bnfIDColumn])
    if fullIdentifierRaw == '' or fullIdentifierRaw == 'nan':
        return ''
    if ';' in fullIdentifierRaw:
        localIdentifiers = []
        identifiers = fullIdentifierRaw.split(';')
        for i in identifiers:
            localIdentifiers.append(i[2:10])
        return ';'.join(localIdentifiers)
    else:
        return fullIdentifierRaw[2:10]

# -----------------------------------------------------------------------------
def removeSeperatedStringDuplicates(df):
  pass
