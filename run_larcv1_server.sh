#!/bin/bash

workdir=$PWD
repodir=$1

cd $repodir/larlite
source config/setup.sh

cd $repodir/larcv1
source configure.sh

cd $repodir/serverfeed
source setenv.sh

cd $workdir

python start_server_larcv1.py
