#!/bin/bash

YARRRML_PARSER="./yarrrml-parser/bin/parser.js"
RML_MAPPER="rmlmapper.jar"
COMUNICA_SPARQL_FILE="comunica-sparql-file"
JAVA="java -Xmx4g"
FORMAT="turtle"


if [ "$#" -ne 2 ];
then
  echo "use 'bash map.sh <input yarrrml file> <output $FORMAT file>"
  exit 1
fi

if [ ! -f $YARRRML_PARSER ];
then
  echo "yarrrml parser not found at '$YARRRML_PARSER', installing it ..."
  git clone --branch feature/env-variables https://github.com/SvenLieber/yarrrml-parser.git \
  && cd yarrrml-parser \
  && npm i
  cd -
fi

if [ ! -f $RML_MAPPER ]
then
  echo "rml mapper not found at '$RML_MAPPER', downloading it ..."
  wget https://github.com/RMLio/rmlmapper-java/releases/download/v4.13.0/rmlmapper-4.13.0-r359-all.jar -O $RML_MAPPER
fi


yarrrml_file=$1
output_file=$2
rml_file=`basename $yarrrml_file .yml`"-rml.ttl"


if [ ! -f $yarrrml_file ];
then
  echo "No YARRRML file named '$yarrrml_file' found!"
  exit 1
fi


echo "Generate RML ..."
node $YARRRML_PARSER -i $yarrrml_file -o $rml_file


if [ $? -eq 0 ]
then
  echo "Execute RML mapping ..."
  echo "time java -jar $RML_MAPPER -m $rml_file -s $FORMAT > $output_file"
  output_and_error=$(
  { 
    time $JAVA -jar $RML_MAPPER -m $rml_file -s $FORMAT > $output_file 
  } 2>&1 
  )
  if echo "$output_and_error" | grep -qi "ERR";
  then
    echo "Could not map data: $output_and_error"
    exit 2
  fi
  echo "RDF created at '$output_file'"
  #if [ $? -eq 0 ]
  #then
  #  echo "RDF created at '$output_file'"

  #else
  #  echo "Could not map data"
  #  exit 2
  #fi
else
  echo "Issues during yarrrml-parsing, could not generate RML"
  exit 1
fi
