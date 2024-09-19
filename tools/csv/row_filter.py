class RowFilter():

  def __init__(self, filterArray):
    self.filterCriteria = []
    self.numberChecked = 0
    self.numberPassed = 0

    for (column, criterion, value) in filterArray:
      self.filterCriteria.append((column, criterion, value))

  def passFilter(self, row):
    """Checks if the row passes the filter by checking the column values."""

    self.numberChecked += 1
    filterPass = True
    for (column, criterion, value) in self.filterCriteria:
      if column in row:
        if criterion == '=':
          if row[column] != value:
            filterPass = False
        elif criterion == 'stringContains':
          if value not in row[column]:
            filterPass = False

    if filterPass:
      self.numberPassed += 1
    return filterPass
