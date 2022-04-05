import utils
import csv

# -----------------------------------------------------------------------------
def getOutputHeaders():

  return ['targetTextKBRIdentifier', 'sourceTextKBRIdentifier', 'targetTextBnFIdentifier', 'targetTextThesaurusBB', 'translationType', 'targetTextTitle', 'sourceTextTitle', 'targetTextEdition', 'targetTextBindingType', 'targetTextCollectionIdentifier', 'targetTextCountryOfPublication', 'targetTextYearOfPublication', 'targetTextPlaceOfPublication', 'targetTextResponsibilityStatement', 'sourceTextLanguage', 'targetTextLanguage', 'sourceTextISBN', 'targetTextISBN', 'authorIdentifier', 'translatorIdentifier', 'targetPublisherIdentifier', 'illustratorIdentifier', 'scenaristIdentifier']

# -----------------------------------------------------------------------------
def combineAggregatedResults(kbrAgg, bnfAgg, outAgg):
  """This function reads in two CSV files, performs postprocessing and creates a single output CSV."""

  with open(kbrAgg, 'r', encoding="utf-8") as inFileKBR, \
       open(bnfAgg, 'r', encoding="utf-8") as inFileBnF, \
       open(outAgg, 'w', encoding="utf-8") as outFile:

    inputReaderKBR = csv.DictReader(inFileKBR, delimiter=',')
    inputReaderBnF = csv.DictReader(inFileBnF, delimiter=',')

    allOutputHeaders = getOutputHeaders()
    outputWriter = csv.DictWriter(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=allOutputHeaders)

    outputWriter.writeheader()
    dataSources = [inputReaderKBR, inputReaderBnF]

    # write relevant data to output (filters were already applied in the SPARQL query, thus we can write directly)
    for dsReader in dataSources:
      for row in dsReader:
          outputWriter.writerow(utils.addKeysWithoutValueToDict(row, allOutputHeaders))


