import matplotlib.pyplot as plt


# -----------------------------------------------------------------------------
def plotTranslationStats(df, statsName):
  """This function plots different graphs related to statistics of the corpus."""
  fig, axs = plt.subplots(2, 2, figsize=(10,5))
  selectionSources = ['numberTranslations', 'withKBRIdentifier', 'withBnFIdentifier', 'withKBIdentifier']
  selectionTargetISBN = ['numberTranslations', 'withTargetISBN10', 'withTargetISBN13']
  selectionSourceInfo = ['numberTranslations', 'withKBRSourceTitle', 'withKBSourceTitle', 'withSourceISBN10', 'withSourceISBN13']

  df[selectionSources].plot(ax=axs[0, 0], marker='o', kind='line', alpha=0.75, rot=25, legend=None)
  df[selectionTargetISBN].plot(ax=axs[0,1], marker='o', kind='line', alpha=0.75, rot=25, legend=None)
  df[selectionSourceInfo].plot(ax=axs[1,0], marker='o', kind='line', alpha=0.75, rot=25, legend=None)

  #plt.subplots_adjust(bottom=0.5)
  fig.suptitle(statsName)
  fig.tight_layout()
  fig.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), prop={'size': 10})

# -----------------------------------------------------------------------------
def plotTranslationStatsIdentifiers(df, statsName):
  """This function plots different graphs related to statistics of the corpus."""

  selectionSources = ['numberTranslations', 'withKBRIdentifier', 'withBnFIdentifier', 'withKBIdentifier']
  df[selectionSources].plot(title=statsName, marker='o', kind='line', alpha=0.75, rot=25).legend(loc='center left', bbox_to_anchor=(1.0, 0.5), prop={'size': 10})

# -----------------------------------------------------------------------------
def plotTranslationStatsIdentifiersOverlap(df, statsName):
  """This function plots different graphs related to statistics of the corpus."""

  selectionSources = ['withKBRBnFAndKBIdentifier', 'withKBRAndBnFIdentifier', 'withKBRAndKBIdentifier',
                      'withBnFAndKBIdentifier']
  df[selectionSources].plot(title=statsName, marker='o', kind='line', alpha=0.75, rot=25).legend(loc='center left', bbox_to_anchor=(1.0, 0.5), prop={'size': 10})

# -----------------------------------------------------------------------------
def plotTranslationStatsIdentifiersOverlapWithoutKBRAndKB(df, statsName):
  """This function plots different graphs related to statistics of the corpus."""

  selectionSources = ['withKBRBnFAndKBIdentifier', 'withKBRAndBnFIdentifier',
                      'withBnFAndKBIdentifier']
  df[selectionSources].plot(title=statsName, marker='o', kind='line', alpha=0.75, rot=25).legend(loc='center left', bbox_to_anchor=(1.0, 0.5), prop={'size': 10})


# -----------------------------------------------------------------------------
def plotTranslationStatsISBN(df, statsName):
  """This function plots different graphs related to statistics of the corpus."""

  selectionTargetISBN = ['numberTranslations', 'withTargetISBN10', 'withTargetISBN13']
  df[selectionTargetISBN].plot(title=statsName, marker='o', kind='line', alpha=0.75, rot=25).legend(loc='center left', bbox_to_anchor=(1.0, 0.5), prop={'size': 10})

# -----------------------------------------------------------------------------
def plotTranslationStatsSources(df, statsName):
  """This function plots different graphs related to statistics of the corpus."""

  selectionSourceInfo = ['numberTranslations', 'withKBRSourceTitle', 'withKBSourceTitle', 'withSourceISBN10',
                         'withSourceISBN13']

  df[selectionSourceInfo].plot(title=statsName, marker='o', kind='line', alpha=0.75, rot=25).legend(loc='center left', bbox_to_anchor=(1.0, 0.5), prop={'size': 10})

# -----------------------------------------------------------------------------
def plotContributorStats(df, statsName):
  pass

# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
