#!/bin/bash

workdir=$PWD
repodir=$1
output=$2

cd $repodir/larlite
source config/setup.sh

cd $repodir/larcv2
source configure.sh

cd $repodir/serverfeed
source setenv.sh

cd $workdir

python start_larcv2_client.py $2
