import requests
import os
import csv
from dotenv import load_dotenv
from tools import utils as toolsUtils
import utils
from datetime import date
import time
from tqdm import tqdm
import xml.etree.ElementTree as ET
import urllib
from argparse import ArgumentParser

NS_SRW = 'http://www.loc.gov/zing/srw/'
ALL_NS = {'srw': NS_SRW}

# -----------------------------------------------------------------------------
def extractIdentifier(xmlContent, identifierName):
  """This function tries to extract the identifier with the given name. If not found it returns None."""

  root = ET.fromstring(xmlContent)

  for record in root.findall('srw:records/srw:record/srw:recordData/responseRecord/', ALL_NS):
    sourceTags = record.findall('./ISNIMetadata/sources')

    if sourceTags:
      for source in sourceTags:
 
        sourceName = utils.getElementValue(source.find('codeOfSource'))
        identifier = utils.getElementValue(source.find('sourceIdentifier'))

        if sourceName == identifierName:
          return identifier

    # if this statement is reached nothing was found so we return None
    return None



     
# -----------------------------------------------------------------------------
def main():

  parser = ArgumentParser(description='This script reads a CSV file and requests for each found ISNI identifier (in the column specified with --column-name-isni) the identifier(s) specified with --identifier')
  parser.add_argument('-i', '--input-file', action='store', required=True, help='A CSV file that contains records about contributors')
  parser.add_argument('-o', '--output-file', action='store', required=True, help='The CSV file in which the enriched records are stored')
  parser.add_argument('--identifiers', metavar='KEY=VALUE', required=True, nargs='+', help='A key value pair where the key is the name of the identifier column in the input that should be fetched and the value is the name of the identifier as stated in the ISNI database.')
  parser.add_argument('--column-name-isni', action='store', required=True, help='The name of the column in the input file that contains the ISNI identifier to lookup')
  parser.add_argument('--wait', action='store', type=float, default = 1, help='The number of seconds to wait in between API requests')
  parser.add_argument('-d', '--delimiter', action='store', default=',', help='The delimiter of the input CSV')
  args = parser.parse_args()


  #
  # load environment variables from .env file
  #
  load_dotenv()

  USERNAME = os.getenv('ISNI_SRU_USERNAME')
  PASSWORD = os.getenv('ISNI_SRU_PASSWORD')
  authValue = os.getenv('ISNI_API_AUTH_TEMP')

  delimiter = args.delimiter
  secondsBetweenAPIRequests = args.wait
  isniColumnName = args.column_name_isni
  identifiers = dict(map(lambda s: s.split('='), args.identifiers))

  with open(args.input_file, 'r') as inFile, \
       open(args.output_file, 'w') as outFile:

    # Count some stats and reset the file pointer afterwards
    countReader = csv.DictReader(inFile, delimiter=delimiter)
    counters = utils.initializeCounters(countReader, identifiers, isniColumnName)
    inFile.seek(0, 0)
    
    numberRowsAtLeastOneIdentifierMissing = counters['numberRowsAtLeastOneIdentifierMissing']
    inputRowCountAll = counters['numberRows']
    inputRowCountISNI = counters['numberRowsHaveISNI']
    isniPercentage = (inputRowCountISNI*100)/inputRowCountAll
    print()
    print(f'In total, the file contains {inputRowCountAll} lines from which {inputRowCountISNI} have an ISNI ({isniPercentage:.2f}%)')
    for column, isniSourceName in identifiers.items():
      inputRowCountMissing = counters[isniSourceName]['numberMissingIdentifierRows']
      inputRowCountMissingAndISNI = counters[isniSourceName]['numberRowsToBeEnriched']
      missingPercentage = (inputRowCountMissing*100)/inputRowCountAll
      missingChancePercentage = (inputRowCountMissingAndISNI*100)/inputRowCountMissing
      print(f'Stats for column "{column}" that should be enriched via "{isniSourceName}" field from the ISNI database')
      print(f'{inputRowCountMissing} {isniSourceName} identifiers are missing and we want to get them ({missingPercentage:.2f}%).')
      print(f'From those {inputRowCountMissing} missing, we could enrich {inputRowCountMissingAndISNI}, because they have an ISNI ({missingChancePercentage:.2f}%)')
      print()
    print()

    inputReader = csv.DictReader(inFile, delimiter=delimiter)

    # the CSV should at least contain columns for the ISNI identifier and the local identifier we want to enrich
    minNeededColumns = [isniColumnName] + identifiers.keys()
    toolsUtils.checkIfColumnsExist(inputReader.fieldnames, minNeededColumns)

    outputWriter = csv.DictWriter(outFile, fieldnames=inputReader.fieldnames)
    outputWriter.writeheader()

    # the payload for each request (the actual query will be appended for each request)
    payload = {'operation': 'searchRetrieve', 'version': '1.1', 'recordSchema': 'isni-e', 'sortKeys': 'none'}
    baseURL = 'https://isni-m.oclc.org/sru'
    url = f'{baseURL}/username={USERNAME}/password={PASSWORD}/DB=1.3'

    skippedRows = 0
    # instantiating tqdm separately, such that we can add a description
    # The total number of lines is the one we have to make requests for
    requestLog = tqdm(position=0, total=numberRowsAtLeastOneIdentifierMissing)

    for row in inputReader:

      # we are not interested in rows that already have values for identifier we look for
      if not atLeastOneIdentifierMissing(row, minNeededColumns):
        skippedRows += 1
        outputWriter.writerow(row)
        continue
      isniRaw = row[isniColumnName]

      # if there is no ISNI there is also nothing we can do
      if isniRaw == '':
        outputWriter.writerow(row)
        continue
      else:
        isniList = isniRaw.split(';') if ';' in isniRaw else [isniRaw]

      descriptions = []
      for identifierColumn, identifierNameISNI in identifiers.items():
        description.append(f'{identifierNameISNI} ' + counters[identifierNameISNI]['numberFoundISNIRows'])
      requestLog.set_description(f'found ' + ','.join(descriptions))

      foundIdentifiers = {}
      rowAlreadyProcessed = False
      for isni in isniList:
        query = f'pica.isn = "{isni}"'
        payload['query'] = query
        try: 
          payloadStr = urllib.parse.urlencode(payload, safe=',+*\\')
          r = requests.get(url, params=payloadStr)
          r.raise_for_status()

          for identifierColumn, identifierNameISNI in identifiers.items():
            # Only enrich it when the currently looked for identifier is missing
            # note: in the future we could think of an 'update' functionality
            if row[identifierColumn] == '':
        
              foundIdentifier = extractIdentifier(r.content, identifierNameISNI)

              if foundIdentifier:
                if not rowAlreadyProcessed:
                  counters[identifierNameISNI]['numberFoundISNIRows'] += 1
                  rowAlreadyProcessed = True
                if identifierNameISNI in foundIdentifiers: 
                  foundIdentifiers[identifierNameISNI].append(foundIdentifier)
                else:
                  foundIdentifiers[identifierNameISNI] = [foundIdentifier]
                counters[identifierNameISNI]['numberFoundISNIs'] += 1

        except requests.exceptions.Timeout:
          print(f'There was a timeout in iteration {counter}')
        except requests.exceptions.TooManyRedirects:
          print(f'There were too many redirects in iteration {counter}')
        except requests.exceptions.HTTPError as err:
          print(f'There was an HTTP response code which is not 200 in iteration {counter}')
        except requests.exceptions.RequestException as e:
          print(f'There was an exception in the request')
        except Exception as e:
          print(f'There was a general exception!')
          print(e)

      for identifierColumn, identifierNameISNI in identifiers.items():
        row[identifierColumn] = ';'.join(foundIdentifiers)
      requestLog.update(1)


      outputWriter.writerow(row)
      time.sleep(secondsBetweenAPIRequests)

  for identifierColumn, identifierNameISNI in identifiers.items():
    counterFound = counters[identifierNameISNI]['numberFoundISNIRows']
    inputRowCountMissingAndISNI = counters[identifierNameISNI]['numberMissingIdentifierRows']
    counterFoundISNI = counters[identifierNameISNI]['numberFoundISNIs']
    percentage = (counterFound*100)/inputRowCountMissingAndISNI
    print()
    print(f'{counterFound} from possible {inputRowCountMissingAndISNI} records ({percentage:.2f}%) could be enriched with {args.identifier_name_isni} identifiers!')
    print(f'(In total {counterFoundISNI} were found (this number might be higher, because there can be more than one ISNI per row)')
    print()

main()
