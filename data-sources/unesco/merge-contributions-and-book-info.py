import pandas as pd
from argparse import ArgumentParser

parser = ArgumentParser(description='This sript merges two CSV files')
parser.add_argument('--csv-1', action='store', required=True, help='The first CSV file')
parser.add_argument('--csv-2', action='store', required=True, help='The second CSV file')
parser.add_argument('--merge-column-left', action='store', required=True, help='The name of the column in the first CSV file that is used for the merge')
parser.add_argument('--merge-column-right', action='store', required=True, help='The name of the column in the second CSV file that is used for the merge')
parser.add_argument('--output-csv', action='store', required=True, help='The name of the output CSV file')

args = parser.parse_args()

contributions = pd.read_csv(args.csv_1)
bookInfo = pd.read_csv(args.csv_2)

mergedDf = pd.merge(contributions, bookInfo, left_on='id', right_on='id')
mergedDf.to_csv(args.output_csv, index=False)
