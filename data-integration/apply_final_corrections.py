import os
import csv
import sys
import argparse
import datetime

# To redirect stdout/stderr of utils_sparql
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

from tools.string import utils_string
from tools import utils
from tools.sparql import utils_sparql

# -----------------------------------------------------------------------------
def main(finalChangesFile, outputFile, url, dry_run):

  auth = utils_sparql.get_auth('.env') 

  with open(finalChangesFile, 'r', encoding='utf-8-sig') as inputCSV,\
       open(outputFile, 'w') as outputCSV:

    inputReader = csv.DictReader(inputCSV)

    # The output CSV file should contain all input columns + two query-related columns
    outputColumns = list(inputReader.fieldnames + ['executed', 'execution_time', 'execution_log'])

    outputWriter = csv.DictWriter(outputCSV,fieldnames=outputColumns)
    outputWriter.writeheader()

    for row in inputReader:

      query = row['query']
      outputRow = row
      outputRow['executed'] = 'No'

      if dry_run:
        print(f'Calling "utils_sparql.sparqlUpdate(url, query, fileFormat="application/sparql-update", queryName="{row["To do"]}: {row["Targetidentifier"]} - {row["query counter"]}", auth=auth)')
      else:
        # Call without try: sparqlUpdate already handles exceptions and stops if necessary
        stdout = StringIO()

        try:
          with redirect_stdout(stdout):
            utils_sparql.sparqlUpdate(
                url,
                query,
                fileFormat='application/sparql-update',
                queryName=f'{row["To do"]}: {row["Targetidentifier"]} - {row["query counter"]}',
                auth=auth
            )

          outputRow['execution_log'] = stdout.getvalue()
          outputRow['executed'] = 'Yes'
        except SystemExit as e:
          print("sparqlUpdate failed:")
          print(stdout.getvalue(), end="")
          print(f"Exit code: {e.code}")

          outputRow["executed"] = "No"
          sys.exit(1)


      outputRow['execution_time'] = str(datetime.datetime.now())
      outputWriter.writerow(outputRow)


# -----------------------------------------------------------------------------
def parseArguments():
  parser = argparse.ArgumentParser()
  parser.add_argument('finalChangesFile', help='A CSV file with the final corrections and generated SPARQL queries')
  parser.add_argument('-u', '--url', action='store', required=True, help='The URL of the SPARQL endpoint')
  parser.add_argument('-d', '--dry-run', action='store_true', help='If set, no SPARQL queries are executed')
  parser.add_argument('-o', '--output-csv', action='store', required=True, help='The output CSV file, enriched with SPARQL queries')
  options = parser.parse_args()
  return options

# -----------------------------------------------------------------------------
if __name__ == '__main__':
  args = parseArguments()
  main(args.finalChangesFile, args.output_csv, args.url, args.dry_run)
