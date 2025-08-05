import pandas as pd
import utils_string
import re

# -----------------------------------------------------------------------------
def extractLocationFromLocationCountryString(value):
  """This function extracts the location from a string where the country is additionally indicates.
  >>> extractLocationFromLocationCountryString('Gent (Belgium)')
  'Gent'
  >>> extractLocationFromLocationCountryString('Gent')
  'Gent'
  >>> extractLocationFromLocationCountryString('(Belgium)')
  '(Belgium)'
  """
  if value.endswith(')') and not value.startswith('('):
    found = re.search(r'^(.*)\(.*', value)
    if found:
      return found.group(1).strip()
  else:
    return value

# -----------------------------------------------------------------------------
def getGeoNamesMainSpellingFromDataFrame(df, identifier):
  """This function extracts the main spelling from a pandas dataframe filled with geonames data.
  >>> data1 = [
  ... ["6693370","Bruxelles-Capitale","Bruxelles-Capitale","BRU,Brussel-Hoofdstad,Bruxelas-Capital","50.84877","4.34664","A","ADM2","BE","","BRU","BRU","","",0,"","26","Europe/Brussels","2016-12-19"],
  ... ["2797657","Gent","Gent","44021,Arrondissement de Gand,Gand,Gent,Ghent","51.07304","3.73664","A","ADM4","BE","","VLG","VOV","44","44021","262219","",4,"Europe/Brussels","2020-04-04"],
  ... ["2797659","Genovabeek","Genovabeek","Genovabeek,Genovevabeek","50.83222","5.01696","H","STM","BE","","VLG","","","",0,"","30","Europe/Brussels","2012-01-18"]]
  >>> getGeoNamesMainSpellingFromDataFrame(pd.DataFrame(data1), "2797657")
  'Gent'
  """
  return (df.loc[df[0] == identifier, 1]).item()

# -----------------------------------------------------------------------------
def getGeoNamesLatitude(df, identifier):
  """This function extracts the main spelling from a pandas dataframe filled with geonames data.
  >>> data1 = [
  ... ["6693370","Bruxelles-Capitale","Bruxelles-Capitale","BRU,Brussel-Hoofdstad,Bruxelas-Capital","50.84877","4.34664","A","ADM2","BE","","BRU","BRU","","",0,"","26","Europe/Brussels","2016-12-19"],
  ... ["2797657","Gent","Gent","44021,Arrondissement de Gand,Gand,Gent,Ghent","51.07304","3.73664","A","ADM4","BE","","VLG","VOV","44","44021","262219","",4,"Europe/Brussels","2020-04-04"],
  ... ["2797659","Genovabeek","Genovabeek","Genovabeek,Genovevabeek","50.83222","5.01696","H","STM","BE","","VLG","","","",0,"","30","Europe/Brussels","2012-01-18"]]
  >>> getGeoNamesLatitude(pd.DataFrame(data1), "2797657")
  '51.07304'
  """
  return (df.loc[df[0] == identifier, 4]).item()

# -----------------------------------------------------------------------------
def getGeoNamesLongitude(df, identifier):
  """This function extracts the main spelling from a pandas dataframe filled with geonames data.
  >>> data1 = [
  ... ["6693370","Bruxelles-Capitale","Bruxelles-Capitale","BRU,Brussel-Hoofdstad,Bruxelas-Capital","50.84877","4.34664","A","ADM2","BE","","BRU","BRU","","",0,"","26","Europe/Brussels","2016-12-19"],
  ... ["2797657","Gent","Gent","44021,Arrondissement de Gand,Gand,Gent,Ghent","51.07304","3.73664","A","ADM4","BE","","VLG","VOV","44","44021","262219","",4,"Europe/Brussels","2020-04-04"],
  ... ["2797659","Genovabeek","Genovabeek","Genovabeek,Genovevabeek","50.83222","5.01696","H","STM","BE","","VLG","","","",0,"","30","Europe/Brussels","2012-01-18"]]
  >>> getGeoNamesLongitude(pd.DataFrame(data1), "2797657")
  '3.73664'
  """
  return (df.loc[df[0] == identifier, 5]).item()

# -----------------------------------------------------------------------------
def extract_geonames(inputDataframe):
    """This function creates a lookup dictionary based on geonames data where possible spellings of a place are the keys and their IDs the value.
    >>> data1 = [
    ... ["2800866","Brussels","Brussels","An Bhruiseil,An Bhruiséil,BRU,Brasels,Breissel,Brisel,Brisele,Briuselis,Brjuksel,Brjusel',Brjussel',Brueksel,Bruessel,Bruesszel,Bruiseal,Bruksel,Bruksela,Brukseli,Brukselo,Brusehl',Brusel,Brusela,Bruselas,Bruseles,Bruselj,Bruselo,Brusel·les,Brussel,Brussele,Brussels,Brussel·les,Bruxel,Bruxelas,Bruxellae,Bruxelles,Brwsel,Bryssel,Bryusel,Bryxelles,Bréissel,Brüksel,Brüssel,Brüsszel,Citta di Bruxelles,Città di Bruxelles,City of Brussels,Kota Brusel,beulwisel,bi lu xi,braselasa,braselsa,brassels,briuseli,brwksl,brysl,bu lu sai er,buryusseru,Βρυξέλλες,Брисел,Брусэль,Брюксел,Брюсель,Брюссель,Բրյուսել,בריסל,ﺏﺭﻮﻜﺴﻟ,ﺏﺭﻮﮑﺴﻟ,ﺏﺮﻳۇﺲﺳېﻝ,ܒܪܘܟܣܠ,ब्रसेल्स,ব্রাসেলস,บรัสเซลส์,ბრიუსელი,ブリュッセル,布魯塞爾,布鲁塞尔,比律悉,브뤼셀","50.85045","4.34878","P","PPLC","BE","BRU","BRU","21","21004","1019022","28","Europe/Brussels","2022-03-09"],
    ... ["2797656","Gent","Gent","GNE,Gaent,Gand,Gandavum,Gandawa,Gande,Gant,Gante,Ganti,Gent,Gentas,Gente,Gento,Ghent,Gint,Gænt,gen te,genta,ghnt,gnt,henteu,hento,jenta,jnt,ken t,khenta,khnt,Γάνδη,Гент,Գենտ,גנט,ﺞﻨﺗ,ﺦﻨﺗ,ﻎﻨﺗ,ﻎﯿﻧٹ,खेंट,गेंट,জেন্ট,เกนต์,ဂင့်မြိ,გენტი,ヘント,根特,헨트","51.05","3.71667","P","PPL","BE","VLG","VOV","44","44021","231493","10","Europe/Brussels","2019-09-"],
    ... ["2797657","Gent","Gent","44021,Arrondissement de Gand,Gand,Gent,Ghent","51.07304","3.73664","A","ADM4","BE","","VLG","VOV","44","44021","262219","",4,"Europe/Brussels","2020-04-04"],
    ... ["2797659","Genovabeek","Genovabeek","Genovabeek,Genovevabeek","50.83222","5.01696","H","STM","BE","","VLG","","","",0,"","30","Europe/Brussels","2012-01-18"]]
    >>> mapping = extract_geonames(pd.DataFrame(data1))
    >>> mapping['gent']
    '2797656'
    >>> mapping['ghent']
    '2797656'
    >>> mapping['bruxelles']
    '2800866'
    """
    geo_ids = {}

    # we are only interested in cities not administrative units (starting with AD)
    # for example we want PPL (place), PPLC (capital of political entity) or PPLA2 (seat of second-order administrative division)
    g = inputDataframe[inputDataframe[7].astype(str).str.startswith('PP')]

    # Add the column with all the alternate spellings (comma-separated list) to the lookup
    #
    messy_column = dict(zip(g[3], g[0]))

    for key, value in messy_column.items():
        if isinstance(key, str):
            new_keys = key.split(",")
            for new_key in new_keys:
                geo_ids[new_key] = value

    # Also add the two main spellings to the lookup
    #
    geo_ids.update(dict(zip(g[1], g[0])))
    geo_ids.update(dict(zip(g[2], g[0])))

    geo_ids_normalized = {}

    for key, value in geo_ids.items():
        key_normalized = utils_string.getNormalizedString(key)
        geo_ids_normalized[key_normalized] = value

    return geo_ids_normalized

def extract_places_tsv(df, columnname_places, columnname_countries):
    """This function extracts places from the given dataframe
    >>> data1 = pd.DataFrame([{"place": "Arles;Montréal", "country": ""},{"place": "", "country": ""},{"place": "Gent", "country": ""}, {"place": "Brussels ; Paris", "country": ""}, {"place": "[Marcinelle]", "country": ""}])
    >>> extract_places_tsv(data1, "place", "country")
    [('arles;montreal', ''), ('', ''), ('gent', ''), ('brussels ; paris', ''), ('marcinelle', '')]
    """
    places = df[columnname_places].replace(to_replace=r'\[|\]|(\(.*?\))', value='', regex=True)
    countries = df[columnname_countries]
    places = list(places)
    countries = list(countries)

    places_clean = []
    for place in places:
        if type(place) is not float:
            place = utils_string.getNormalizedString(place)
            if ". - " in place:
                place = place.replace(". - ", " ; ")
            elif " - " in place:
                place = place.replace(" - ", " ; ")
            places_clean.append(place.strip())
        else:
            places_clean.append("")

    place_country = list(zip(places_clean, countries))

    return place_country

# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import doctest
  doctest.testmod()
