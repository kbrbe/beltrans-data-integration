import pandas as pd
import argparse
import re
import os

# -----------------------------------------------------------------------------
def plotNumberTimeline(df, columns, title):
  plot = df[columns].plot(title=title,
                   marker='o',
                   kind='line',
                   alpha=0.75,
                   rot=25).legend(loc='center left',
                                  bbox_to_anchor=(
                                    1.0, 0.5),
                                  prop={'size': 10})

  return plot


parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='+', help="Input text file containing statistics that need to be reformatted")
options = parser.parse_args()

# Create a single pandas dataframe from all CSV measurement files
allDfs = []
for inputFile in options.files:

  dateString = re.findall(r'\d{4}-\d{2}-\d{2}', os.path.basename(inputFile))[0]

  df = pd.read_csv(inputFile)
  valueDf = df.set_index('variable').T
  valueDf['date'] = dateString
  allDfs.append(valueDf)

statsDf = pd.concat(allDfs, ignore_index=True)
statsDf.set_index('date', inplace=True)
statsDf.to_csv('stats.csv')

columnsToVisualize = ['ISNIAssigned', 'numberOfPersons', 'numberOfOrgs', 'source-KBR', 'duplicate-records-KBR', 'person-nationality-be']
plot = plotNumberTimeline(statsDf, columnsToVisualize, 'Evolution ISNI Belgians')

statsDf[columnsToVisualize].to_csv('stats-selection.csv')
plot.figure.savefig('stats.pdf', bbox_inches='tight')

