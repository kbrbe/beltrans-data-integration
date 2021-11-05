#
# (c) 2021 Sven Lieber
# KBR Brussels
#
import xml.etree.ElementTree as ET
import json
import itertools
import csv
from optparse import OptionParser
import utils

NS_MARCSLIM = 'http://www.loc.gov/MARC21/slim'

# -----------------------------------------------------------------------------
def addRoleStat(stats, role):
  if role in stats:
    stats[role] += 1
  else:
    stats[role] = 1



# -----------------------------------------------------------------------------
def main():
  """This script reads an XML file in MARC slim format and generates statistics about used fields."""

  parser = OptionParser(usage="usage: %prog [options]")
  parser.add_option('-i', '--input-file', action='store', help='The input file containing MARC slim XML records')
  parser.add_option('-p', '--pattern', action='store', help='The pattern for the name of the output files, e.g. "2021-10-export" which could result in files such as "2021-10-export-pbl.csv" for publishers')
  parser.add_option('-r', '--roles', action='append', help='A list of possible roles for which output files should be generated, see list of MARC roles. Possible values are "pbl" for publisher or "trl" for translator')
  parser.add_option('-s', '--stats', action='store_true', help='Only collect statistics of used contributor roles')
  (options, args) = parser.parse_args()

  #
  # Check if we got all required arguments
  #
  if( (not options.input_file) or (not options.pattern) or (not options.roles) ):
    # no input, pattern, or roles given, the user could still be interested in stats only
    if ( (not options.input_file) or (not options.stats) ):
      parser.print_help()
      exit(1)
  elif( options.stats and (options.pattern or options.roles) ):
    print("If you use stats no pattern or roles can be provided")
    parser.print_help()
    exit(1)

  #
  # Set the default namespace for the collection (and thus also for all child records)
  #
  ET.register_namespace('', 'http://www.loc.gov/MARC21/slim')

  stats = {}
  roleStats = {'person': {}, 'org': {}}
  counter = 0
  #
  # Instead of loading everything to main memory, stream over the XML using iterparse
  #
  for event, elem in ET.iterparse(options.input_file, events=('start', 'end')):

    #
    # The parser finished reading one MARC SLIM record, get information and then discard the record
    #
    if  event == 'end' and elem.tag == ET.QName(NS_MARCSLIM, 'record'):
      counter += 1
      recordID = ''
      date = ''
      contributors = list()
      for datafield in elem:

        #
        # get the ID of the bibliographic record
        #
        if(datafield.tag == ET.QName(NS_MARCSLIM, 'controlfield') and datafield.attrib['tag'] == '001'):
          recordID = datafield.text

        #
        # get the date so we can later filter on the date
        #
        if(datafield.tag == ET.QName(NS_MARCSLIM, 'datafield') and datafield.attrib['tag'] == '264'):

          #
          # iterate over subfields to find the actual date in MARC subfield $c, stop looking in subfields when found
          #
          for sf in datafield.iter():
            if(sf.tag == ET.QName(NS_MARCSLIM, 'subfield') and sf.attrib['code'] == 'c' and sf.text is not None):
              date = sf.text
              break


        #
        # Get the contributor, their name and their role
        #
        if(datafield.tag == ET.QName(NS_MARCSLIM, 'datafield') and ( datafield.attrib['tag'] == '700' or datafield.attrib['tag'] == '710') ):
          contributor = 'NO_IDENTIFIER'
          role = 'NO_ROLE'
          for sf in datafield.iter():
            if(sf.tag == ET.QName(NS_MARCSLIM, 'subfield')):
              code = sf.attrib['code']
              if(code == '*'):
                contributorID = sf.text
              if(code == 'a'):
                contributorName = sf.text
              if(code == '4'):
                role = sf.text
          if(datafield.attrib['tag'] == '700'):
            addRoleStat(roleStats['person'], role)
          elif(datafield.attrib['tag'] == '710'):
            addRoleStat(roleStats['org'], role)
          contributors.append((contributorID, contributorName, role))
      #
      # We are done iterating over all datafields, store the data we collected
      #
      if(date != '' and date.startswith(('197', '198', '199', '200', '201', '2020')) ):
        for (cID, cN, r) in contributors:
          if(r in stats):
            if(recordID in stats[r]):
              stats[r][recordID].append((cID, cN))
            else:
              stats[r][recordID] = [(cID, cN)]
          else:
            stats[r] = {recordID: [(cID, cN)]}


      elem.clear()

  #print(json.dumps(stats, indent=4))
  print("Found roles: ")
  printRoleStats(roleStats)

  if(not options.stats):
    #
    # Create CSV files for some of the selected roles
    #
    for role in options.roles:
      if role in stats.keys():
        outputFilename = options.pattern + '-' + role + ".csv"
        with open(outputFilename, 'w', encoding='utf-8') as outFile:
          writer = csv.writer(outFile, delimiter=',')
          writer.writerow(['role', 'bibID', 'contributorID', 'contributorName'])
          for bibID in stats[role]:
            for contributor in stats[role][bibID]:
              writer.writerow([role, bibID, contributor[0], contributor[1]])
        print("Created file '" + outputFilename + "' for role '" + role + "'")
      else:
        print("Skipping '" + role + "', no contributors found with that role!")


# -----------------------------------------------------------------------------
def printRoleStats(stats):

  markRelators = {"abr": "Abridger","acp": "Art copyist","act": "Actor","adi": "Art director","adp": "Adapter","aft": "Author of afterword, colophon, etc.","anl": "Analyst","anm": "Animator","ann": "Annotator","ant": "Bibliographic antecedent","ape": "Appellee","apl": "Appellant","app": "Applicant","aqt": "Author in quotations or text abstracts","arc": "Architect","ard": "Artistic director","arr": "Arranger","art": "Artist","asg": "Assignee","asn": "Associated name","ato": "Autographer","att": "Attributed name","auc": "Auctioneer","aud": "Author of dialog","aui": "Author of introduction, etc.","aus": "Screenwriter","aut": "Author","bdd": "Binding designer","bjd": "Bookjacket designer","bkd": "Book designer","bkp": "Book producer","blw": "Blurb writer","bnd": "Binder","bpd": "Bookplate designer","brd": "Broadcaster","brl": "Braille embosser","bsl": "Bookseller","cas": "Caster","ccp": "Conceptor","chr": "Choreographer","-clb": "Collaborator","cli": "Client","cll": "Calligrapher","clr": "Colorist","clt": "Collotyper","cmm": "Commentator","cmp": "Composer","cmt": "Compositor","cnd": "Conductor","cng": "Cinematographer","cns": "Censor","coe": "Contestant-appellee","col": "Collector","com": "Compiler","con": "Conservator","cor": "Collection registrar","cos": "Contestant","cot": "Contestant-appellant","cou": "Court governed","cov": "Cover designer","cpc": "Copyright claimant","cpe": "Complainant-appellee","cph": "Copyright holder","cpl": "Complainant","cpt": "Complainant-appellant","cre": "Creator","crp": "Correspondent","crr": "Corrector","crt": "Court reporter","csl": "Consultant","csp": "Consultant to a project","cst": "Costume designer","ctb": "Contributor","cte": "Contestee-appellee","ctg": "Cartographer","ctr": "Contractor","cts": "Contestee","ctt": "Contestee-appellant","cur": "Curator","cwt": "Commentator for written text","dbp": "Distribution place","dfd": "Defendant","dfe": "Defendant-appellee","dft": "Defendant-appellant","dgc": "Degree committee member","dgg": "Degree granting institution","dgs": "Degree supervisor","dis": "Dissertant","dln": "Delineator","dnc": "Dancer","dnr": "Donor","dpc": "Depicted","dpt": "Depositor","drm": "Draftsman","drt": "Director","dsr": "Designer","dst": "Distributor","dtc": "Data contributor","dte": "Dedicatee","dtm": "Data manager","dto": "Dedicator","dub": "Dubious author","edc": "Editor of compilation","edm": "Editor of moving image work","edt": "Editor","egr": "Engraver","elg": "Electrician","elt": "Electrotyper","eng": "Engineer","enj": "Enacting jurisdiction","etr": "Etcher","evp": "Event place","exp": "Expert","fac": "Facsimilist","fds": "Film distributor","fld": "Field director","flm": "Film editor","fmd": "Film director","fmk": "Filmmaker","fmo": "Former owner","fmp": "Film producer","fnd": "Funder","fpy": "First party","frg": "Forger","gis": "Geographic information specialist","-grt": "Graphic technician","his": "Host institution","hnr": "Honoree","hst": "Host","ill": "Illustrator","ilu": "Illuminator","ins": "Inscriber","inv": "Inventor","isb": "Issuing body","itr": "Instrumentalist","ive": "Interviewee","ivr": "Interviewer","jud": "Judge","jug": "Jurisdiction governed","lbr": "Laboratory","lbt": "Librettist","ldr": "Laboratory director","led": "Lead","lee": "Libelee-appellee","lel": "Libelee","len": "Lender","let": "Libelee-appellant","lgd": "Lighting designer","lie": "Libelant-appellee","lil": "Libelant","lit": "Libelant-appellant","lsa": "Landscape architect","lse": "Licensee","lso": "Licensor","ltg": "Lithographer","lyr": "Lyricist","mcp": "Music copyist","mdc": "Metadata contact","med": "Medium","mfp": "Manufacture place","mfr": "Manufacturer","mod": "Moderator","mon": "Monitor","mrb": "Marbler","mrk": "Markup editor","msd": "Musical director","mte": "Metal-engraver","mtk": "Minute taker","mus": "Musician","nrt": "Narrator","opn": "Opponent","org": "Originator","orm": "Organizer","osp": "Onscreen presenter","oth": "Other","own": "Owner","pad": "Place of address","pan": "Panelist","pat": "Patron","pbd": "Publishing director","pbl": "Publisher","pdr": "Project director","pfr": "Proofreader","pht": "Photographer","plt": "Platemaker","pma": "Permitting agency","pmn": "Production manager","pop": "Printer of plates","ppm": "Papermaker","ppt": "Puppeteer","pra": "Praeses","prc": "Process contact","prd": "Production personnel","pre": "Presenter","prf": "Performer","prg": "Programmer","prm": "Printmaker","prn": "Production company","pro": "Producer","prp": "Production place","prs": "Production designer","prt": "Printer","prv": "Provider","pta": "Patent applicant","pte": "Plaintiff-appellee","ptf": "Plaintiff","pth": "Patent holder","ptt": "Plaintiff-appellant","pup": "Publication place","rbr": "Rubricator","rcd": "Recordist","rce": "Recording engineer","rcp": "Addressee","rdd": "Radio director","red": "Redaktor","ren": "Renderer","res": "Researcher","rev": "Reviewer","rpc": "Radio producer","rps": "Repository","rpt": "Reporter","rpy": "Responsible party","rse": "Respondent-appellee","rsg": "Restager","rsp": "Respondent","rsr": "Restorationist","rst": "Respondent-appellant","rth": "Research team head","rtm": "Research team member","sad": "Scientific advisor","sce": "Scenarist","scl": "Sculptor","scr": "Scribe","sds": "Sound designer","sec": "Secretary","sgd": "Stage director","sgn": "Signer","sht": "Supporting host","sll": "Seller","sng": "Singer","spk": "Speaker","spn": "Sponsor","spy": "Second party","srv": "Surveyor","std": "Set designer","stg": "Setting","stl": "Storyteller","stm": "Stage manager","stn": "Standards body","str": "Stereotyper","tcd": "Technical director","tch": "Teacher","ths": "Thesis advisor","tld": "Television director","tlp": "Television producer","trc": "Transcriber","trl": "Translator","tyd": "Type designer","tyg": "Typographer","uvp": "University place","vac": "Voice actor","vdg": "Videographer","-voc": "Vocalist","wac": "Writer of added commentary","wal": "Writer of added lyrics","wam": "Writer of accompanying material","wat": "Writer of added text","wdc": "Woodcutter","wde": "Wood engraver","win": "Writer of introduction","wit": "Witness","wpr": "Writer of preface","wst": "Writer of supplementary textual content"}

  print("Persons")
  for role in stats['person']:
    s = stats['person']
    if role in markRelators:
      print("\t" + markRelators[role] + ": " + str(s[role]))
    else:
      print("\tNon-valid MARC relator code '" + role + "': " + str(s[role]))

  print("Organizations")
  for role in stats['org']:
    s = stats['org']
    if role in markRelators:
      print("\t" + markRelators[role] + ": " + str(s[role]))
    else:
      print("\tNon-valid MARC relator code '" + role + "': " + str(s[role]))
main()
