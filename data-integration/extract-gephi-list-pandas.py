import pandas as pd

# -----------------------------------------------------------------------------
def main():

  # Please provide the name of the input file and output files
  inputFile = 'corpus-versions/2024-07-03/corpus-data.xlsx'
  edgeListFilename = 'edge-list.csv'
  nodeListFilename = 'node-list.csv'

  # all beltrans genre prefixes "81|83|84|85|86|900|92|93|95|96|97"

  # Select which genre filter should be used (comment the others with a leading #)
  genrePrefixes = "84|900|92|93|95|96|97" # history
  #genrePrefixes = "85" # Comics
  #genrePrefixes = "81" # Poetry
  #genrePrefixes = "86" # juvenile literature
  #genrePrefixes = "83|84" # novels

  minYear = pd.to_numeric('1970')
  maxYear = pd.to_numeric('2020')

  # if set to True source/target publishers will be replaced by their respective main publisher
  # otherwise set to False
  considerImprintRelation = True

  # Identifiers of imprints that should not be replaced with their main publisher (in case there is any specified)
  # This is a list, when adding new entries, please put a comma after the string and before the comment, e.g. before "# pastel"
  imprintMappingExceptions = [
    '9e29c2cd-b380-49e3-82d6-141914ff35c0' # pastel
  ]

  # Begin of the code
  #
  print(f'read translations from Excel...')
  dfTranslations = pd.read_excel(inputFile, sheet_name='translations')

  print(f'read organization list from Excel ...')
  dfOrgs = pd.read_excel(inputFile, sheet_name='all orgs')

  # store the mapping in a separate data structure so we can reuse it
  imprintMapping = dfOrgs[['contributorID', 'isImprintFrom']].copy()

  # no imprintMapping needed for the following function, because the mapping information is already in dfOrgs
  createNodeList(dfOrgs, nodeListFilename, considerImprintRelation, imprintMappingExceptions)

  # create edge list with information from the nodes (needed for correct mapping of imprints)
  createEdgeList(dfTranslations, edgeListFilename, genrePrefixes, minYear, maxYear, considerImprintRelation, imprintMapping, imprintMappingExceptions)



# -----------------------------------------------------------------------------
def createNodeList(dfOrgs, nodeListFilename, considerImprintRelation, imprintMappingExceptions):

  columnsToKeep = ['contributorID', 'name', 'country']
  dfOrgs[columnsToKeep].to_csv(nodeListFilename, index=False)

  # for now the country of the publisher record (not always filled in)
  #
  # in case we want country information from the translation list,
  # dfTranslations should be given as a parameter,
  # then we would have to select all countries of each dfOrgs['contributorID'] in an exploded version of dfTranslations
  # and add it
  # is this what we want? Like this we might get wrong country information, especially for translations with multiple publishers and thus publishing places
    
# -----------------------------------------------------------------------------
def createEdgeList(dfTranslations, edgeListFilename, genrePrefixes, minYear, maxYear, considerImprintRelation, imprintMapping, imprintMappingExceptions):


  sourceTargetColumns = ['sourcePublisherIdentifiers', 'targetPublisherIdentifiers']
  genreColumn = 'targetThesaurusBB'
  additionalInfoColumns = ['targetYearOfPublication']


  # We want one row = one source-target relation
  edgeDfExploded = dfTranslations.explode(sourceTargetColumns).reset_index().copy()

  # We also only want a subset of the columns
  edgeDfExploded = edgeDfExploded.fillna('')
  edgeDf = edgeDfExploded.loc[edgeDfExploded[genreColumn].str.contains(genrePrefixes), sourceTargetColumns + additionalInfoColumns]

  # extract identifiers
  edgeDf['sourceID'] = edgeDf[sourceTargetColumns[0]].str.extract(r'.*\((.*)\).*')
  edgeDf['targetID'] = edgeDf[sourceTargetColumns[1]].str.extract(r'.*\((.*)\).*')

  # replace source and target identifiers with main publisher in case we should take the imprint relation into account
  if considerImprintRelation:
    mergedDf = pd.merge(edgeDf, imprintMapping, left_on='sourceID', right_on='contributorID', how='left')
    mergedDf['sourceID'] = mergedDf.apply(replaceImprint, axis=1, imprintIDColumn='sourceID', mainIDColumn='isImprintFrom', replaceColumn='isImprintFrom', keepColumn='sourceID', exceptions=imprintMappingExceptions)
    mergedDf.drop(['contributorID', 'isImprintFrom'], axis=1, inplace=True)

    mergedDf = pd.merge(mergedDf, imprintMapping, left_on='targetID', right_on='contributorID', how='left')
    mergedDf['targetID'] = mergedDf.apply(replaceImprint, axis=1, imprintIDColumn='targetID', mainIDColumn='isImprintFrom', replaceColumn='isImprintFrom', keepColumn='targetID', exceptions=imprintMappingExceptions)
    mergedDf.drop(['contributorID', 'isImprintFrom'], axis=1, inplace=True)

    edgeDf = mergedDf.copy()

  # finally only selecting a specific date range
  edgeDf['targetYearOfPublication'] = pd.to_numeric(edgeDf['targetYearOfPublication'], errors='coerce', downcast='integer')
  edgeDf = edgeDf.loc[(edgeDf['targetYearOfPublication'].notna()) & (edgeDf['targetYearOfPublication'] >= minYear) & (edgeDf['targetYearOfPublication'] <= maxYear)]
  

  edgeDf = edgeDf.fillna('')
  edgeDf['targetYearOfPublication'] = edgeDf['targetYearOfPublication'].astype(int)
  edgeDf.loc[(edgeDf['sourceID'] != '') & (edgeDf['targetID'] != ''),['sourceID','targetID'] + additionalInfoColumns].to_csv(edgeListFilename, index=False)


# -----------------------------------------------------------------------------
def replaceImprint(row, imprintIDColumn, mainIDColumn, replaceColumn, keepColumn, exceptions):
  """This function can be called for each row, it will return the value of the replaceColumn in case there is a mainID column and in case the imprintID is not in the exception list
     otherwise the value of the keepColumn is returned.
  """

  imprintID = row[imprintIDColumn]
  mainID = row[mainIDColumn]

  if mainID in exceptions:
    # do not replace
    return row[keepColumn]
  else:
    if pd.notna(mainID):
      # replace
      return row[replaceColumn]
    else:
      # nothing to replace with
      return row[keepColumn]



# execute main function
main()
