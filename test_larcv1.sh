#!/bin/bash

workdir=$PWD
repodir=$1

source /usr/local/bin/thisroot.sh

cd $repodir/larlite
source config/setup.sh

cd $repodir/larcv1
source configure.sh

cd $workdir

python load_data_larcv1.py ${@:2}
