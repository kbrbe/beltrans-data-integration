import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

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
def plotNumberTimeline(df, columns, title):
  df[columns].plot(title=title,
                   marker='o',
                   kind='line',
                   alpha=0.75,
                   rot=25).legend(loc='center left',
                                  bbox_to_anchor=(
                                    1.0, 0.5),
                                  prop={'size': 10})

# -----------------------------------------------------------------------------
def plotPercentageTimeline(df, columns, title, totalNumberColumn):

  percentColumns = []
  for col in columns:
      percentName = f'{col}_percent'
      df[percentName] = (df[col].astype('int')*100)/df[totalNumberColumn].astype('int')
      percentColumns.append(percentName)

  ax = df[percentColumns].plot(title=title,
                   marker='o',
                   kind='line',
                   alpha=0.75,
                   rot=25)
  ax.legend(loc='center left',
                                  bbox_to_anchor=(
                                    1.0, 0.5),
                                  prop={'size': 10})
  ax.yaxis.set_major_formatter(mtick.PercentFormatter(100.0))

# -----------------------------------------------------------------------------
def plotTranslationStatsIdentifiers(df, statsName):
  """This function plots different graphs related to statistics of the corpus."""

  selectionSources = ['numberTranslations', 'withKBRIdentifier', 'withBnFIdentifier', 'withKBIdentifier']
  plotNumberTimeline(df, selectionSources, statsName)

# -----------------------------------------------------------------------------
def plotTranslationStatsIdentifiersOverlap(df, statsName):
  """This function plots different graphs related to statistics of the corpus."""

  selectionSources = ['withKBRBnFAndKBIdentifier', 'withKBRAndBnFIdentifier', 'withKBRAndKBIdentifier',
                      'withBnFAndKBIdentifier']
  plotNumberTimeline(df, selectionSources, statsName)
# -----------------------------------------------------------------------------
def plotTranslationStatsIdentifiersOverlapWithoutKBRAndKB(df, statsName):
  """This function plots different graphs related to statistics of the corpus."""

  selectionSources = ['withKBRBnFAndKBIdentifier', 'withKBRAndBnFIdentifier',
                      'withBnFAndKBIdentifier']
  plotNumberTimeline(df, selectionSources, statsName)

# -----------------------------------------------------------------------------
def plotTranslationStatsISBN(df, statsName):
  """This function plots different graphs related to statistics of the corpus."""

  selectionTargetISBN = ['numberTranslations', 'withTargetISBN10', 'withTargetISBN13']
  plotNumberTimeline(df, selectionTargetISBN, statsName)
# -----------------------------------------------------------------------------
def plotTranslationStatsSources(df, statsName):
  """This function plots different graphs related to statistics of the corpus."""

  selectionSourceInfo = ['numberTranslations', 'withKBRSourceTitle', 'withKBSourceTitle', 'withSourceISBN10',
                         'withSourceISBN13']

  plotNumberTimeline(df, selectionSourceInfo, statsName)

# -----------------------------------------------------------------------------
def plotContributorStatsIdentifiers(df, statsName):
  """This function plots different graphs related to statistics of the corpus."""

  selectionSources = ['numberContributors', 'withKBRIdentifier', 'withBnFIdentifier', 'withKBIdentifier']
  plotNumberTimeline(df, selectionSources, statsName)


# -----------------------------------------------------------------------------
def plotContributorStatsIdentifiersOverlap(df, statsName):
  """This function plots different graphs related to overlapping identifiers."""

  selectionSources = ['withKBRBnFAndKBIdentifier', 'withKBRAndBnFIdentifier', 'withKBRAndKBIdentifier',
                      'withBnFAndKBIdentifier']
  plotNumberTimeline(df, selectionSources, statsName)

# -----------------------------------------------------------------------------
def plotContributorStatsInternationalIdentifiers(df, statsName):
  """This function plots different graphs related to overlapping identifiers."""

  selectionSources = ['numberContributors', 'withISNIIdentifier', 'withVIAFIdentifier', 'withWikidataIdentifier']
  plotNumberTimeline(df, selectionSources, statsName)

# -----------------------------------------------------------------------------
def plotContributorStatsMultipleIdentifiers(df, statsName):
  """This function plots different graphs related to overlapping identifiers."""

  selectionSources = ['withMultipleKBRIdentifiers', 'withMultipleBnFIdentifiers', 'withMultipleNTAIdentifiers',
                      'withMultipleISNIIdentifiers', 'withMultipleVIAFIdentifiers', 'withMultipleWikidataIdentifiers']
  plotNumberTimeline(df, selectionSources, statsName)

# -----------------------------------------------------------------------------
def plotContributorStatsNationality(df, statsName):
  """This function plots different graphs related to overlapping identifiers."""

  selectionSources = ['numberContributors', 'withNationality', 'withMultipleNationalities']
  plotNumberTimeline(df, selectionSources, statsName)

# -----------------------------------------------------------------------------
def plotContributorStatsMissingNationality(df, statsName):
  """This function plots different graphs related to overlapping identifiers."""

  selectionSources = ['numberContributors', 'withISNIButWithoutNationality', 'withWikidataButWithoutNationality',
                      'withISNIAndWikidataButWithoutNationality']
  plotNumberTimeline(df, selectionSources, statsName)

# -----------------------------------------------------------------------------
def plotContributorStatsBirthDeathDates(df, statsName):
  """This function plots different graphs related to overlapping identifiers."""

  selectionSources = ['numberContributors', 'withBirthDate', 'withDeathDate']
  plotNumberTimeline(df, selectionSources, statsName)

# -----------------------------------------------------------------------------
def plotContributorStatsContradictingBirthDeathDates(df, statsName):
  """This function plots different graphs related to overlapping identifiers."""

  selectionSources = ['withMultipleBirthDates', 'withMultipleDeathDates']
  plotNumberTimeline(df, selectionSources, statsName)

# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
