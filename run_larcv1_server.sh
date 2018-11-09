#!/bin/bash

workdir=$PWD
repodir=$1
filename=$2
productlist=${@:3}

# needed for meitner
#source /usr/local/bin/thisroot.sh

cd $repodir/larlite
source config/setup.sh

cd $repodir/larcv1
source configure.sh

cd $repodir/serverfeed
source setenv.sh

cd $workdir

python start_server_larcv1.py ${filename} ${productlist}
