# activate Python virtual environment
. data-integration/py-integration-env/bin/activate

# make local Python modules available to be used via python -m tools.*
export PYTHONPATH=$(pwd)

# make environment variables available
export $(cat ./data-integration/.env | sed 's/#.*//g' | xargs)
