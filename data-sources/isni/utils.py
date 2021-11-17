
# -----------------------------------------------------------------------------
def count(stats, counter):
  """ This function simply adds to the given counter or creates it if not yet existing in 'stats'.

  >>> stats = {}
  >>> count(stats, 'myCounter')
  >>> stats['myCounter']
  1
  """
  if counter in stats:
    stats[counter] += 1
  else:
    stats[counter] = 1

# -----------------------------------------------------------------------------
def countStat(stats, counter, value):
  """ This function logs the value 'value' in the dictionary 'stats' under the key 'counter'. Additionally min, max and number are stored.

  An empty stats dictionary is filled.
  >>> stats = {}
  >>> countStat(stats, 'myCounter', 1)
  >>> stats['myCounter']
  {'min': 1, 'max': 1, 'avg': 1, 'number': 1, 'values': [1]}

  Stats are correctly computed and added for already existing counters.
  >>> stats =  { 'myCounter': {'min': 1, 'max': 3, 'avg': 2, 'number': 3, 'values': [1, 2, 3]}}
  >>> countStat(stats, 'myCounter', 7)
  >>> stats['myCounter']
  {'min': 1, 'max': 7, 'avg': 3.25, 'number': 4, 'values': [1, 2, 3, 7]}
  """
  if counter in stats:
    stats[counter]['values'].append(value)
    stats[counter]['number'] += 1
    stats[counter]['min'] = min(stats[counter]['min'], value)
    stats[counter]['max'] = max(stats[counter]['max'], value)
    stats[counter]['avg'] = sum(stats[counter]['values'])/len(stats[counter]['values'])
  else:
    stats[counter] = {'min': value, 'max': value, 'avg': value, 'number': value, 'values': [value]}



# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
