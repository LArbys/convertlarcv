#!/bin/bash

cd larlite
source config/setup.sh
cd ../

cd larcv1
source configure.sh
make -j4
