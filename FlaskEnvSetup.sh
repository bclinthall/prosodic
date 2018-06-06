#!/bin/bash

APP_NAME=${1:-prosodic}

FLASK_ENV=${2:-development}
echo "Environment type: $FLASK_ENV"


echo "Creating environment for $APP_NAME"
echo "conda create --name ${APP_NAME}_env python=2.7 flask"
conda create --name ${APP_NAME}_env python=2.7 flask

CONDA_DIR=$(dirname $(dirname $(which conda)))
ACTIVATE_DIR="$CONDA_DIR/envs/${APP_NAME}_env/etc/conda/activate.d"
DEACTIVATE_DIR="$CONDA_DIR/envs/${APP_NAME}_env/etc/conda/deactivate.d"

mkdir -p $ACTIVATE_DIR
mkdir -p $DEACTIVATE_DIR

echo "#!/bin/sh

export FLASK_APP=$APP_NAME
export FLASK_ENV=$FLASK_ENV" > $ACTIVATE_DIR/env_vars.sh

echo "#!/bin/sh

unset FLASK_APP
unset FLASK_ENV" > $DEACTIVATE_DIR/env_vars.sh

echo "Environment includes FLASK_APP=$APP_NAME and FLASK_ENV=$FLASK_ENV"

