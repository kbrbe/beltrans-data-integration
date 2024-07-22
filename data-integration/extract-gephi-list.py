
import openpyxl # needed to parse Excel files
import re # needed to extract identifiers from contributor strings
import csv # needed to create output CSV file
from itertools import product # needed to create pairs of all sources with all targets

# -----------------------------------------------------------------------------
def main():

  # Please provide the name of the input file and output files
  inputFile = 'corpus-versions/2024-06-28/corpus-data.xlsx'
  edgeListFilename = 'edge-list.csv'
  nodeListFilename = 'node-list.csv'

  # all beltrans genre prefixes "81|83|84|85|86|900|92|93|95|96|97"

  # Select which genre filter should be used (comment the others with a leading #)
  #genrePrefixes = "84|900|92|93|95|96|97" # history
  #genrePrefixes = "85" # Comics
  #genrePrefixes = "81" # Poetry
  #genrePrefixes = "86" # juvenile literature
  genrePrefixes = "83|84" # novels

  translationSheetName = 'translations'
  columns = ['sourcePublisherIdentifiers', 'targetPublisherIdentifiers']
  additionalInfoColumns = ['targetYearOfPublication']
  valueSeparator = ';'

  print(f'Parse workbook ...')
  wb = openpyxl.load_workbook(inputFile)
  translationList = wb[translationSheetName]

  with open(edgeListFilename, 'w') as edgeFile:
    edgeListWriter = csv.DictWriter(edgeFile, columns + additionalInfoColumns)
    edgeListWriter.writeheader()

    # getValues is a generator function and emits values of specified columns for every row
    for row in getValues(translationList, columns + additionalInfoColumns):
      # there might be several contributors for each column, so first split
      rowValues = {c: row[c].split(valueSeparator) if row[c] != '' else [] for c in columns}

      firstValue = rowValues[columns[0]]
      secondValue = rowValues[columns[1]]

      # Build the cartesian product, i.e. each source with each target
      # nothing if source or target are empty
      for source,target in product(firstValue, secondValue):
        # Try to extract the identifiers, show warning if string is wrongly formatted
        try:
          (sourceID, targetID) = getIdentifiers(source, target)
         
          # We want the source and target in the output CSV ...
          outputRow = {columns[0]: sourceID, columns[1]: targetID}

          # ... but also the values of additionally fetched columns
          outputRow.update({c: row[c] for c in additionalInfoColumns})
          edgeListWriter.writerow(outputRow)
        except Exception as e:
          print(e)
          continue

# -----------------------------------------------------------------------------
def getIdentifiers(contributorString1, contributorString2):

  sourceRegex = re.search(r'.*\((.*)\).*', contributorString1)
  targetRegex = re.search(r'.*\((.*)\).*', contributorString2)
  sourceIdentifier = None
  targetIdentifier = None

  if sourceRegex:
    sourceIdentifier = sourceRegex.group(1)
  else:
    raise Exception(f'wrongly formatted source contributor, could not extract identifier from "{sourceRegex}", skipping row')

  if targetRegex:
    targetIdentifier = targetRegex.group(1)
  else:
    raise Exception(f'wrongly formatted target contributor, could not extract identifier from "{targetRegex}", skipping row')
   
  return sourceIdentifier, targetIdentifier


# -----------------------------------------------------------------------------
def getValues(sheet, columnNames):
  """This function will emit a dictionary with row values of the specified columns and the given sheet."""

  # iterate over the first row to get the header names
  columnIndexes = {}
  for cell in sheet[1]:
    if cell.value in columnNames:
      # store the column index, e.g. {'myColumn': 2}
      columnIndexes[cell.value] = cell.column

  # Iterate over all rows, skip the header
  for row in sheet.iter_rows(min_row=2):
    # loop over all columns that we are interested in
    rowValues = {}
    for columnName, columnIndex in columnIndexes.items():
      rowValues[columnName] = row[columnIndex-1].value
    yield rowValues

# -----------------------------------------------------------------------------
def extractContributor():
  pass


# execute main function
main()
