# -*- coding: utf-8 -*-
"""
@author: Fabrizio Pascucci
"""

import csv
from utils_string import getNormalizedString
from rapidfuzz.distance import Indel
import pandas as pd
from optparse import OptionParser

def main():

    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option('-w', '--original_works', action='store', help='CSV containing original works')
    parser.add_option('-t', '--translations', action='store', help='CSV containing translations')
    parser.add_option('-o', '--output_file', action='store', help='The output as CSV')
    (options, args) = parser.parse_args()

    if( (not options.original_works) or (not options.translations) or (not options.output_file) ):
      parser.print_help()
      exit(1)

    column_names = ['KBRID', 'title', 'originalTitle', 'candidates']

    df=pd.DataFrame(columns=column_names)

    """Open source file. Create a dictionary with normalized 'title' as key and 'KBRID' as value"""

    sources = {}
    with open(options.original_works, newline='', encoding='utf-8') as csvfile:
        sourcereader = csv.DictReader(csvfile)

        for source in sourcereader:
            title_normalized = getNormalizedString(source['title'])
            KBRID = source['KBRID']
            sources[title_normalized] = KBRID

    """Open target file. If 'source title' is empty, search normalized 'original title' in the dictionary that we just named 'sources' """


    with open(options.translations, newline='', encoding='utf-8') as csvfile:
        targetreader = csv.DictReader(csvfile)

        for target in targetreader:
            original_title_normalized = getNormalizedString(target['originalTitle'])
            if target['sourceTitle'] == '' and target['originalTitle'] != '':
                if original_title_normalized in sources:
                    KBRID = sources[original_title_normalized]
                    match = original_title_normalized+'('+str(KBRID)+')'

                else:
                    candidates = []
                    for key, KBRID in sources.items():
                        if Indel.normalized_similarity(original_title_normalized, key) > 0.90:
                            candidate = key+'('+str(KBRID)+')'
                            candidates.append(candidate)
                    match = ';'.join(candidates)
                KBRID_target = target['KBRID']
                title_target = target['title']
                original_title = target['originalTitle']

                new_row = {'KBRID':KBRID_target, 'title':title_target, 'originalTitle':original_title, 'candidates':match}
                df = df.append(new_row, ignore_index=True)
    df.to_csv(options.output_file, index = False, sep = ',')

main()

# python find-originals.py -w Original_works/fr-nl_fr-works.csv -t Translations/fr-nl_translations-works.csv -o fr-nl.csv
# python find-originals.py -w Original_works/nl-fr_nl-works.csv -t Translations/nl-fr_translations-works.csv -o nl-fr.csv
