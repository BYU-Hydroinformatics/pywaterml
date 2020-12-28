#!/bin/bash
# this script uses the ANACONDA_TOKEN env var.
# to create a token:
# >>> anaconda login
# >>> anaconda auth -c -n travis --max-age 307584000 --url https://anaconda.org/USERNAME/PACKAGENAME --scopes "api:write api:read"
set -e
export PKG_NAME
export PKG_VERSION
export PKG_BUILD_STRING
echo "Converting conda package..."
conda convert --platform all $HOME/envs/test-environment/conda-bld/linux-64/$PKG_NAME-$PKG_VERSION-$PKG_BUILD_STRING*.tar.bz2 --output-dir conda-bld/

echo "Deploying to Anaconda.org..."
anaconda -t $ANACONDA_TOKEN upload conda-bld/**/$PKG_NAME-$PKG_VERSION-$PKG_BUILD_STRING*.tar.bz2

echo "Successfully deployed to Anaconda.org."
exit 0
