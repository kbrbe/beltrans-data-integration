# -*- coding: utf-8 -*-
"""
@author: Fabrizio Pascucci
@author: Sven Lieber
"""

import csv
from rapidfuzz.distance import Indel
import pandas as pd
from optparse import OptionParser

from utils_string import getNormalizedString
from book_title_lookup import BookTitleLookup
from csv_to_excel import main as to_excel

# -----------------------------------------------------------------------------
def checkArguments():

    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option('-w', '--original-works', action='store', help='CSV containing original works')
    parser.add_option('-t', '--translations', action='store', help='CSV containing translations')
    parser.add_option('-d', '--candidate-delimiter', action='store', default=';', help='The delimiter used to separate multiple candidates, default is a semicolon')
    parser.add_option('-s', '--similarity', action='store', default=0.9, help='A length-normalized title similarity (used if no direct match can be found)')
    parser.add_option('--output-file-clear-matches', action='store',
                      help='A CSV file containing matches based on title, match with a single record')
    parser.add_option('--output-file-duplicate-id-matches', action='store',
                      help='A CSV file containing matches based on title, match with duplicate ID records (same title)')
    parser.add_option('--output-file-similarity-duplicate-id-matches', action='store',
                      help='A CSV file containing matches based on similarity, match with duplicate ID records (same title)')
    parser.add_option('--output-file-similarity-multiple-matches', action='store',
                      help='A CSV file containing matches based on similarity, matches with several different originals')
    parser.add_option('--output-file-similarity-matches', action='store',
                      help='A CSV file with matches based on similarity, matches with a single original')
    (options, args) = parser.parse_args()

    if( (not options.original_works) or (not options.translations) or (not options.output_file_clear_matches)
        or (not options.output_file_duplicate_id_matches) or (not options.output_file_similarity_duplicate_id_matches)
        or (not options.output_file_similarity_multiple_matches) or (not options.output_file_similarity_matches)):
      parser.print_help()
      exit(1)

    return options

# -----------------------------------------------------------------------------
def main(original_works, translations, similarityThreshold, output_file_clear_matches,
         output_file_duplicate_id_matches, output_file_similarity_matches,
         output_file_similarity_duplicate_id_matches, output_file_similarity_multiple_matches, candidateDelimiter=';'):

    column_names = ['KBRID', 'title', 'originalTitle', 'candidates', 'candidatesIDs']

    """Open source file. Create a dictionary with normalized 'title' as key and 'KBRID' as value"""

    sourceLookup = BookTitleLookup(original_works, 'KBRID', 'title', similarityThreshold)

    """Open target file. If 'source title' is empty, search normalized 'original title' in the dictionary that we just named 'sources' """


    with open(translations, newline='', encoding='utf-8') as csvfile, \
         open(output_file_clear_matches, 'w', encoding='utf-8') as outFileClearMatches, \
         open(output_file_duplicate_id_matches, 'w', encoding='utf-8') as outFileDuplicateIDMatches, \
         open(output_file_similarity_matches, 'w', encoding='utf-8') as outFileSimilarityMatches, \
         open(output_file_similarity_duplicate_id_matches, 'w', encoding='utf-8') as outFileSimilarityDuplicateIDMatches, \
         open(output_file_similarity_multiple_matches, 'w', encoding='utf-8') as outFileSimilarityMultipleMatches:

        targetreader = csv.DictReader(csvfile)

        clearMatchesWriter = csv.DictWriter(outFileClearMatches, fieldnames=column_names)
        clearMatchesWriter.writeheader()

        duplicateIDMatchesWriter = csv.DictWriter(outFileDuplicateIDMatches, fieldnames=column_names)
        duplicateIDMatchesWriter.writeheader()

        similarityMatchesWriter = csv.DictWriter(outFileSimilarityMatches, fieldnames=column_names)
        similarityMatchesWriter.writeheader()

        similarityDuplicateIDMatchesWriter = csv.DictWriter(outFileSimilarityDuplicateIDMatches, fieldnames=column_names)
        similarityDuplicateIDMatchesWriter.writeheader()

        similarityMultipleMatchesWriter = csv.DictWriter(outFileSimilarityMultipleMatches, fieldnames=column_names)
        similarityMultipleMatchesWriter.writeheader()

        numberTargetRecords = 0
        numberTargetRecordsWithOriginalTitle = 0
        numberClearMatches = 0
        numberDuplicateIDMatches = 0
        numberSimilarityMatches = 0
        numberSimilarityDuplicateIDMatches = 0
        numberSimilarityMultipleMatches = 0

        similarityMatches = {}

        for target in targetreader:
            original_title_normalized = getNormalizedString(target['originalTitle'])
            targetKBRID = target['KBRID']
            targetTitle = target['title']
            targetOriginalTitle = target['originalTitle']
            if target['sourceTitle'] == '' and target['originalTitle'] != '':
                numberTargetRecordsWithOriginalTitle += 1
                # we found a matching title
                if sourceLookup.contains(original_title_normalized):

                    # we actually found only one matching title (best case)
                    if sourceLookup.containsSingleIdentifier(original_title_normalized):
                        KBRID = next(iter(sourceLookup.getIdentifier(original_title_normalized)))
                        match = original_title_normalized + ' (' + str(KBRID) + ')'
                        numberClearMatches += 1
                        clearMatchesWriter.writerow({'KBRID': targetKBRID, 'title': targetTitle,
                                                     'originalTitle': targetOriginalTitle,
                                                     'candidates': match, 'candidatesIDs': str(KBRID)})

                    # there are several book identifiers with the given title, further checks needed
                    else:
                        candidateIDs = sorted(sourceLookup.getIdentifier(original_title_normalized))
                        match = candidateDelimiter.join(candidateIDs)
                        numberDuplicateIDMatches += 1
                        duplicateIDMatchesWriter.writerow({'KBRID': targetKBRID, 'title': targetTitle,
                                                           'originalTitle': targetOriginalTitle,
                                                          'candidates': match, 'candidatesIDs': candidateIDs})

                # no matching title found, let's try titles with high similarity
                else:
                    candidates = []
                    candidateKeys = []
                    duplicateIDMatch = False
                    for title, KBRIDs in sourceLookup.getItems():
                        if Indel.normalized_similarity(original_title_normalized, title) > similarityThreshold:
                            idString = ''
                            if sourceLookup.containsSingleIdentifier(title):
                                idString = next(iter(KBRIDs))
                            else:
                                idString = ','.join(sorted(KBRIDs))
                                duplicateIDMatch = True
                            candidate = title + ' (' + idString + ')'
                            candidates.append(candidate)

                    match = candidateDelimiter.join(candidates)
                    row = {'KBRID': targetKBRID, 'title': targetTitle,
                           'originalTitle': targetOriginalTitle,
                           'candidates': match}

                    if len(candidates) == 1 and duplicateIDMatch:
                        numberSimilarityDuplicateIDMatches += 1
                        similarityDuplicateIDMatchesWriter.writerow(row)
                    elif len(candidates) == 1 and not duplicateIDMatch:
                        numberSimilarityMatches += 1
                        similarityMatchesWriter.writerow(row)
                    elif len(candidates) > 1:
                        numberSimilarityMultipleMatches += 1
                        similarityMultipleMatchesWriter.writerow(row)
                    else:
                        # no candidates found, thus no match
                        pass


            numberTargetRecords += 1
                #new_row = {'KBRID':KBRID_target, 'title':title_target, 'originalTitle':original_title, 'candidates':match}
                #df = df.append(new_row, ignore_index=True)

    #df.to_csv(output_file, index = False, sep = ',')

    print(f'Number of target records: {numberTargetRecords}')
    print(f'Number of target records with original title (and missing identifier): {numberTargetRecordsWithOriginalTitle}')
    print(f'Number of clear matches: {numberClearMatches}')
    print(f'Number of duplicate ID matches: {numberDuplicateIDMatches}')
    print(f'Number of similarity matches: {numberSimilarityMatches}')
    print(f'Number of similarity duplicateID matches: {numberSimilarityDuplicateIDMatches}')
    print(f'Number of similarity multiple matches: {numberSimilarityMultipleMatches}')
    print(f'Number of original records: {sourceLookup.getNumberTitles()}')
    print(f'Number of duplicate records: {sourceLookup.getNumberOfDuplicates()}')
    print(f'Average: {sourceLookup.getAverageNumberOfDuplicates()}')
    print(f'Median: {sourceLookup.getMedianNumberOfDuplicates()}')

# -----------------------------------------------------------------------------
if __name__ == '__main__':

    options = checkArguments()

    main(options.original_works,
         options.translations,
         options.similarity,
         options.output_file_clear_matches,
         options.output_file_duplicate_id_matches,
         options.output_file_similarity_matches,
         options.output_file_similarity_duplicate_id_matches,
         options.output_file_similarity_multiple_matches,
         candidateDelimiter=options.candidate_delimiter)

# python find-originals.py -w Original_works/fr-nl_fr-works.csv -t Translations/fr-nl_translations-works.csv -o fr-nl.csv
# python find-originals.py -w Original_works/nl-fr_nl-works.csv -t Translations/nl-fr_translations-works.csv -o nl-fr.csv
