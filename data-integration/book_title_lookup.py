import csv
import statistics
from utils_string import getNormalizedString

class BookTitleLookup():
    """This class offers a simple lookup of values with some added features such as keeping count of certain statistics"""

    def __init__(self, lookupFile, idColumn, titleColumn, similarityThreshold):
        self.stats = {
            'numberTitles': 0,
            'duplicateTitles': [],
            'duplicateTitlesUnique': set(),
            'averageDuplicates': 0,
            'mediumDuplicates': 0
        }

        self.records = {}

        with open(lookupFile, 'r', encoding='utf-8') as inFile:
            lookupReader = csv.DictReader(inFile)
            for bookRecord in lookupReader:
                identifier = bookRecord[idColumn]
                title = getNormalizedString(bookRecord[titleColumn])
                if title in self.records:
                    self.records[title].add(identifier)
                    self.stats['duplicateTitles'].append(title)
                    self.stats['duplicateTitlesUnique'].add(title)
                else:
                    self.records[title] = set([identifier])

        duplicateIDs = []
        duplicateIDSum = 0
        for record in self.records:
            duplicateIDs.append(len(self.records[record]))
            duplicateIDSum += len(self.records[record])
        self.stats['numberTitles'] = len(self.records.keys())
        self.stats['averageDuplicates'] = duplicateIDSum/self.stats['numberTitles']
        self.stats['medianDuplicates'] = statistics.median(duplicateIDs)

    def getNumberTitles(self):
        return self.stats['numberTitles']

    def getNumberOfDuplicates(self):
        return len(self.stats['duplicateTitles'])

    def getAverageNumberOfDuplicates(self):
        return self.stats['averageDuplicates']

    def getMedianNumberOfDuplicates(self):
        return self.stats['medianDuplicates']

    def contains(self, title):
        return True if title in self.records else False

    def containsSingleIdentifier(self, title):
        if title in self.records:
            return True if len(self.records[title]) == 1 else False
        else:
            return False

    def getIdentifier(self, title):
        if title in self.records:
            return self.records[title]
        else:
            return ''

    def getItems(self):
        for (key, value) in self.records.items():
            yield (key, value)




