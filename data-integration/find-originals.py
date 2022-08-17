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
    parser.add_option('-s', '--similarity', action='store', default=0.9, type='float', help='A length-normalized title similarity (used if no direct match can be found)')
    parser.add_option('--apply-candidate-filter', action='store_true', default=False, help='A flag indicating that the number of match candidates (if more than 1) should be tried to reduced automatically, e.g. by checking publication years')
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
def createCandidateString(title, identifiers):
    return f'{title} ({identifiers})'

# -----------------------------------------------------------------------------
def handleMultipleCandidates(sourceLookup, target, original_title_normalized, duplicateIDs,
                             candidateDelimiter, clearMatchesWriter, duplicateIDMatchesWriter, candidateFilter,
                             matchesCounter, targetYearColumn='yearOfPublication'):
    """This function determines the candidates and the respective candidateWriter for matches with several IDs.
     If the candidateFilter is True, an attempt is made to reduce the number of duplicates.
     If successfully reduced the number of duplicates to 1, the candidateWriter will be the clearMatchesWriter,
     otherwise the duplicateMatchesWriter.
    """

    outputRowCandidates = ''
    outputRowCandidateIDs = ''
    outputRowWriter = None

    # let's try some automatic filtering to reduce the number of possible candidates
    if candidateFilter and targetYearColumn in target and target[targetYearColumn] != '':
        candidateIDs = sourceLookup.filterYearIdentifiers(duplicateIDs,
                                                          target['yearOfPublication'])

        # the filtering worked! Now there is only a single match we will add to the clear match output
        if len(candidateIDs) == 1:
            matchesCounter['singleMatchAfterDuplicateRemoving'] = matchesCounter['singleMatchAfterDuplicateRemoving'] + 1
            outputRowCandidates = createCandidateString(original_title_normalized, candidateIDs[0])
            outputRowCandidateIDs = str(candidateIDs[0])
            outputRowWriter = clearMatchesWriter

        # still more than one match
        elif len(candidateIDs) > 1:
            candidateIDsString = candidateDelimiter.join(candidateIDs)
            idString = ','.join(candidateIDs)
            outputRowCandidates = createCandidateString(original_title_normalized, idString)
            outputRowCandidateIDs = candidateIDsString
            outputRowWriter = duplicateIDMatchesWriter

            if len(candidateIDs) < len(duplicateIDs):
                matchesCounter['reducedDuplicates'] = matchesCounter['reducedDuplicates'] + 1
            else:
                matchesCounter['duplicateMatch'] = matchesCounter['duplicateMatch'] + 1

        # after filtering we are left with no candidates at all
        else:
            matchesCounter['noCandidatesLeft'] = matchesCounter['noCandidatesLeft'] + 1

    # we do not want to apply automatic filtering: simply return a list of all candidates
    else:
        candidateIDs = sourceLookup.getIdentifier(original_title_normalized)
        candidateIDsString = candidateDelimiter.join(candidateIDs)
        idString = ','.join(candidateIDs)
        outputRowCandidates = original_title_normalized + ' (' + idString + ')'
        outputRowCandidateIDs = candidateIDsString
        outputRowWriter = duplicateIDMatchesWriter
        matchesCounter['duplicateMatch'] = matchesCounter['duplicateMatch'] + 1

    return (outputRowCandidates, outputRowCandidateIDs, outputRowWriter)

# -----------------------------------------------------------------------------
def performSimilarityMatching(sourceLookup, target, original_title_normalized, candidateDelimiter,
                              similarityMatchesWriter, similarityDuplicateIDMatchesWriter,
                              similarityMultipleMatchesWriter, candidateFilter, matchesCounter, similarityThreshold):

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
            candidate = createCandidateString(title, idString)
            candidateKeys.append(idString)
            candidates.append(candidate)

    outputRowCandidates = candidateDelimiter.join(candidates)
    outputRowCandidateIDs = candidateDelimiter.join(candidateKeys)
    outputRowWriter = None

    if len(candidates) == 1 and duplicateIDMatch:

        (outputRowCandidates,
         outputRowCandidateIDs,
         outputRowWriter) = handleMultipleCandidates(sourceLookup, target, original_title_normalized,
                                                     candidateKeys[0].split(','), candidateDelimiter,
                                                     similarityMatchesWriter, similarityDuplicateIDMatchesWriter,
                                                     candidateFilter, matchesCounter)


    elif len(candidates) == 1 and not duplicateIDMatch:
        matchesCounter['singleMatch'] = matchesCounter['singleMatch'] + 1
        outputRowCandidates = candidateDelimiter.join(candidates)
        outputRowCandidateIDs = candidateDelimiter.join(candidateKeys)
        outputRowWriter = similarityMatchesWriter
    elif len(candidates) > 1:
        matchesCounter['multipleMatches'] = matchesCounter['multipleMatches'] + 1
        listOfList = [id.split(',') for id in candidateKeys]
        flattenedList = [item for sublist in listOfList for item in sublist]
        outputRowCandidateIDs = candidateDelimiter.join(flattenedList)
        outputRowWriter = similarityMultipleMatchesWriter
    else:
        # no candidates found, thus no match
        pass

    return (outputRowCandidates, outputRowCandidateIDs, outputRowWriter)

# -----------------------------------------------------------------------------
def main(original_works, translations, similarityThreshold, output_file_clear_matches,
         output_file_duplicate_id_matches, output_file_similarity_matches,
         output_file_similarity_duplicate_id_matches, output_file_similarity_multiple_matches,
         candidateFilter, candidateDelimiter=';'):

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

        titleMatchCounter = {'singleMatch': 0, 'duplicateMatch': 0, 'reducedDuplicates': 0,
                             'singleMatchAfterDuplicateRemoving': 0, 'noCandidatesLeft': 0}
        similarityMatchCounter = {'singleMatch': 0, 'duplicateMatch': 0, 'reducedDuplicates': 0,
                                  'singleMatchAfterDuplicateRemoving': 0, 'multipleMatches': 0, 'noCandidatesLeft': 0}

        similarityMatches = {}

        for target in targetreader:
            original_title_normalized = getNormalizedString(target['originalTitle'])
            targetKBRID = target['KBRID']
            targetTitle = target['title']
            targetOriginalTitle = target['originalTitle']

            currentOutputWriter = None
            outputRowCandidates = ''
            outputRowCandidateIDs = ''

            if target['sourceTitle'] == '' and target['originalTitle'] != '':
                numberTargetRecordsWithOriginalTitle += 1
                # we found a matching title
                if sourceLookup.contains(original_title_normalized):

                    # we actually found only one matching title (best case)
                    if sourceLookup.containsSingleIdentifier(original_title_normalized):
                        KBRID = next(iter(sourceLookup.getIdentifier(original_title_normalized)))
                        outputRowCandidates = createCandidateString(original_title_normalized, str(KBRID))
                        outputRowCandidateIDs = str(KBRID)
                        currentOutputWriter = clearMatchesWriter
                        titleMatchCounter['singleMatch'] = titleMatchCounter['singleMatch'] + 1

                    # there are several book identifiers with the given title, further checks needed
                    else:
                        duplicateIDs = sourceLookup.getIdentifier(original_title_normalized)
                        (outputRowCandidates,
                         outputRowCandidateIDs,
                         currentOutputWriter) = handleMultipleCandidates(sourceLookup, target, original_title_normalized,
                                                                         duplicateIDs, candidateDelimiter, clearMatchesWriter,
                                                                         duplicateIDMatchesWriter, candidateFilter,
                                                                         titleMatchCounter)

                # no matching title found, let's try titles with high similarity
                else:
                    (outputRowCandidates,
                     outputRowCandidateIDs,
                     currentOutputWriter) = performSimilarityMatching(sourceLookup, target, original_title_normalized,
                                                                      candidateDelimiter, similarityMatchesWriter,
                                                                      similarityDuplicateIDMatchesWriter,
                                                                      similarityMultipleMatchesWriter, candidateFilter,
                                                                      similarityMatchCounter, similarityThreshold)


            if currentOutputWriter != None:
                outputRow = {'KBRID': targetKBRID, 'title': targetTitle, 'originalTitle': targetOriginalTitle,
                             'candidates': outputRowCandidates, 'candidatesIDs': outputRowCandidateIDs}
                currentOutputWriter.writerow(outputRow)
            numberTargetRecords += 1


    print(f'Number of target records: {numberTargetRecords}')
    print(f'Number of target records with original title (and missing identifier): {numberTargetRecordsWithOriginalTitle}')

    print(f'Number of original records: {sourceLookup.getNumberTitles()}')
    print(f'Number of duplicate records: {sourceLookup.getNumberOfDuplicates()}')
    print(f'Max number of duplicates: {sourceLookup.getMaxNumberOfDuplicates()}')
    print(f'Average: {sourceLookup.getAverageNumberOfDuplicates()}')
    print(f'Median: {sourceLookup.getMedianNumberOfDuplicates()}')

    print('Exact title match:')
    print(titleMatchCounter)
    print(f'Similarity-based match (threshold {similarityThreshold}):')
    print(similarityMatchCounter)
    print(f'Number of clear matches: {numberClearMatches}')

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
         options.apply_candidate_filter,
         candidateDelimiter=options.candidate_delimiter)

# python find-originals.py -w Original_works/fr-nl_fr-works.csv -t Translations/fr-nl_translations-works.csv -o fr-nl.csv
# python find-originals.py -w Original_works/nl-fr_nl-works.csv -t Translations/nl-fr_translations-works.csv -o nl-fr.csv
