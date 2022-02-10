#
# (c) 2021 Sven Lieber
# KBR Brussels
#
import csv
from optparse import OptionParser
import utils
import json

# -----------------------------------------------------------------------------
def getOutputHeaders():

  return ['targetTextKBRIdentifier','sourceTextKBRIdentifier','targetTextBnFIdentifier','targetTextThesaurusBB','translationType','targetTextTitle','sourceTextTitle','targetTextEdition','targetTextCollectionIdentifier','targetTextCollectionName','targetTextBindingType','targetTextCountryOfPublication','targetTextYearOfPublication','targetTextPlaceOfPublication','targetTextResponsibilityStatement','sourceTextLanguage','targetTextLanguage','sourceTextISBN','targetTextISBN','authorIdentifier','authorISNI','authorNationality','authorGender','authorGenderISNI','authorFamilyName','authorGivenName','authorBirthDate','authorBirthDateISNI','authorDeathDate','authorDeathDateISNI','translatorIdentifier','translatorFamilyName','translatorGivenName','translatorISNI','translatorNationality','translatorGender', 'translatorGenderISNI','translatorBirthDate','translatorBirthDateISNI','translatorDeathDate','translatorDeathDateISNI','targetTextPublisherCertainty','targetPublisherIdentifier','targetPublisherISNI','targetPublisherName','targetPublisherLocation','targetPublisherRegion','targetPublisherCountry','illustratorIdentifier','illustratorISNI','illustratorNationality','illustratorGender', 'illustratorGenderISNI','illustratorFamilyName','illustratorGivenName','illustratorBirthDate','illustratorBirthDateISNI','illustratorDeathDate','illustratorDeathDateISNI','scenaristIdentifier','scenaristFamilyName','scenaristGivenName','scenaristISNI','scenaristNationality','scenaristGender', 'scenaristGenderISNI','scenaristBirthDate','scenaristBirthDateISNI','scenaristDeathDate','scenaristDeathDateISNI']

# -----------------------------------------------------------------------------
def main():
  """This script filters the SPARQL query result of the integrated data."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-k', '--input-file-kbr', action='store', help='The input file containing CSV data from KBR')
  parser.add_option('-b', '--input-file-bnf', action='store', help='The input file containing CSV data from BnF')
  parser.add_option('-o', '--output-file', action='store', help='The file in which content with new headers is stored')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file_kbr) or (not options.input_file_bnf) or (not options.output_file) ):
    parser.print_help()
    exit(1)

  #
  # Open input file with encoding 'utf-8-sig' (instead of 'utf-8') because the Syracuse export contains Byte Order marks (BOM)
  #
  with open(options.input_file_kbr, 'r', encoding="utf-8") as inFileKBR, \
       open(options.input_file_bnf, 'r', encoding="utf-8") as inFileBnF, \
       open(options.output_file, 'w', encoding="utf-8") as outFile:

    inputReaderKBR = csv.DictReader(inFileKBR, delimiter=',')
    inputReaderBnF = csv.DictReader(inFileBnF, delimiter=',')
    headers = inputReaderKBR.fieldnames.copy()

    # In the output we only want a single birth date and a single death date column
    # thus first remove the respective columns from different data sources
    headersToRemove = ['authorBirthDateKBR', 'authorDeathDateKBR', 'authorBirthDateISNI', 'authorDeathDateISNI',
                       'translatorBirthDateKBR', 'translatorDeathDateKBR', 'translatorBirthDateISNI', 'translatorDeathDateISNI',
                       'illustratorBirthDateKBR', 'illustratorDeathDateKBR', 'illustratorBirthDateISNI', 'illustratorDeathDateISNI',
                       'scenaristBirthDateKBR', 'scenaristDeathDateKBR', 'scenaristBirthDateISNI', 'scenaristDeathDateISNI']
    for r in headersToRemove:
      headers.remove(r)

    # and then add the single columns we want
    headers.extend(['authorBirthDate', 'authorDeathDate', 
                   'translatorBirthDate', 'translatorDeathDate',
                   'illustratorBirthDate', 'illustratorDeathDate',
                   'scenaristBirthDate', 'scenaristDeathDate'])

    allOutputHeaders = getOutputHeaders()

    outputWriter = csv.DictWriter(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=allOutputHeaders)

    outputWriter.writeheader()

    belgian = 'Belgium'

    # used to parse certain columns based on their name, e.g. authorBirthDateKBR and authorBirthDateISNI
    sources = ['KBR', 'ISNI']
    mismatchLog = {}

    
    dataSources = [inputReaderKBR, inputReaderBnF]
    # write relevant data to output
    for dsReader in dataSources:
      for row in dsReader:

        if( row['authorNationality'] == belgian or row['illustratorNationality'] == belgian or row['scenaristNationality'] == belgian):

          # This is a relevant row, we process it further before writing it
          utils.selectDate(row, 'author', 'Birth', sources, 'authorIdentifier', mismatchLog)
          utils.selectDate(row, 'illustrator', 'Birth', sources, 'illustratorIdentifier', mismatchLog)
          utils.selectDate(row, 'translator', 'Birth', sources, 'translatorIdentifier', mismatchLog)
          utils.selectDate(row, 'scenarist', 'Birth', sources, 'scenaristIdentifier', mismatchLog)

          utils.selectDate(row, 'author', 'Death', sources, 'authorIdentifier', mismatchLog)
          utils.selectDate(row, 'illustrator', 'Death', sources, 'illustratorIdentifier', mismatchLog)
          utils.selectDate(row, 'translator', 'Death', sources, 'translatorIdentifier', mismatchLog)
          utils.selectDate(row, 'scenarist', 'Death', sources, 'scenaristIdentifier', mismatchLog)

          outputWriter.writerow(utils.addKeysWithoutValueToDict(row, allOutputHeaders))


  # print statistics
  for dateType in mismatchLog:
    for contributorType in mismatchLog[dateType]:
      numberMismatches = len(mismatchLog[dateType][contributorType])
      print(f'{dateType}, {contributorType} = {numberMismatches} mismatches')

  # print mismatch log
  print(f'dateType, contributorType, contributor, KBR, ISNI')
  for dateType in mismatchLog:
    for contributorType in mismatchLog[dateType]:
      for c in mismatchLog[dateType][contributorType]:
        d = mismatchLog[dateType][contributorType][c]
        kbrValue = next(iter(d['KBR'])) if 'KBR' in d else ''
        isniValue = next(iter(d['ISNI'])) if 'ISNI' in d else ''
        print(f'{dateType}, {contributorType}, {c}, {kbrValue}, {isniValue}')
      

main()
