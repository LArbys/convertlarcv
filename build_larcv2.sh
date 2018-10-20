#!/bin/bash

cd larlite
source config/setup.sh
cd ../

cd larcv2
source configure.sh
make -j4
