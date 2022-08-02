import csv
import statistics

from utils_string import getNormalizedString
from utils_date import yearSmallerOrEqual

class BookTitleLookup():
    """This class offers a simple lookup of values with some added features such as keeping count of certain statistics"""

    # -------------------------------------------------------------------------
    def __init__(self, lookupFile, idColumn, titleColumn, similarityThreshold):
        self.stats = {
            'numberTitles': 0,
            'duplicateTitles': [],
            'duplicateTitlesUnique': set(),
            'averageDuplicates': 0,
            'mediumDuplicates': 0
        }

        self.records = {}
        self.publicationYears = {}

        with open(lookupFile, 'r', encoding='utf-8') as inFile:
            lookupReader = csv.DictReader(inFile)
            for bookRecord in lookupReader:
                identifier = bookRecord[idColumn]
                title = getNormalizedString(bookRecord[titleColumn])

                # add the identifier and title for an identifier lookup based on title
                if title in self.records:
                    self.records[title].add(identifier)
                    self.stats['duplicateTitles'].append(title)
                    self.stats['duplicateTitlesUnique'].add(title)
                else:
                    self.records[title] = set([identifier])

                # add the publication year for a publication year lookup based on identifier
                self.publicationYears[identifier] = bookRecord['yearOfPublication']

        duplicateIDs = []
        duplicateIDSum = 0
        for record in self.records:
            duplicateIDs.append(len(self.records[record]))
            duplicateIDSum += len(self.records[record])
        self.stats['numberTitles'] = len(self.records.keys())
        self.stats['averageDuplicates'] = duplicateIDSum/self.stats['numberTitles']
        self.stats['maxDuplicates'] = max(duplicateIDs)
        self.stats['medianDuplicates'] = statistics.median(duplicateIDs)

    # -------------------------------------------------------------------------
    def getNumberTitles(self):
        return self.stats['numberTitles']

    # -------------------------------------------------------------------------
    def getNumberOfDuplicates(self):
        return len(self.stats['duplicateTitles'])

    # -------------------------------------------------------------------------
    def getMaxNumberOfDuplicates(self):
        return self.stats['maxDuplicates']

    # -------------------------------------------------------------------------
    def getAverageNumberOfDuplicates(self):
        return self.stats['averageDuplicates']

    # -------------------------------------------------------------------------
    def getMedianNumberOfDuplicates(self):
        return self.stats['medianDuplicates']

    # -------------------------------------------------------------------------
    def contains(self, title):
        return True if title in self.records else False

    # -------------------------------------------------------------------------
    def containsSingleIdentifier(self, title):
        if title in self.records:
            return True if len(self.records[title]) == 1 else False
        else:
            return False

    # -------------------------------------------------------------------------
    def getIdentifier(self, title):
        if title in self.records:
            return sorted(self.records[title])
        else:
            return ''

    # -------------------------------------------------------------------------
    def getYearFilteredIdentifiers(self, title, year):
        filteredCandidates = []
        if title in self.records:
            candidates = self.records[title]
            for candidateID in candidates:
                if candidateID in self.publicationYears:
                    # the publication year of the original cannot be after the one of the translation
                    if yearSmallerOrEqual(self.publicationYears[candidateID], year):
                        filteredCandidates.append(candidateID)
        return sorted(filteredCandidates)

    # -------------------------------------------------------------------------
    def filterYearIdentifiers(self, identifiers, year):
        filteredCandidates = []
        for candidateID in identifiers:
            if candidateID in self.publicationYears:
                # the publication year of the original cannot be after the one of the translation
                if yearSmallerOrEqual(self.publicationYears[candidateID], year):
                    filteredCandidates.append(candidateID)
        return sorted(filteredCandidates)

    # -------------------------------------------------------------------------
    def getItems(self):
        for (key, value) in self.records.items():
            yield (key, value)




# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
