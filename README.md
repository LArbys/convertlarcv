# Convert LArCV

The code in this repository is meant to convert files created using LArCV1 into LArCV2-compatible files.

LArCV1 and LArCV2 cannot be setup in the same shell environment, so we create different
processes that talk to one another through ZMQ.

The data is converted from larcv1 into a numpy array and serialized using msgpack-numpy.

## Setup

The primary external dependency is [CERN ROOT](https://github.com/root-project/root).

When first checking out the repository, first get the dependencies included here through
submodules.

    git submodule init
    git submodule update

Next we need to build `larlite`, `larcv1`, `larcv2`.

    python setup.py


## Running

* Customize the script as needed that loads larcv1 data and converts it into a dictionary of numpy arrays.
  See `start_server_larcv1.py`, specifically the `load_data_larcv1` method near the start of the module.
  This module also has the name of the *input file* hard-coded into it.

* Modify `start_larcv2_client.py` as needed to convert the incoming numpy arrays into larcv2 data products.
  See `start_larcv2_client.py` as an example.
  This module laos has the name of the *output file* hard-coded into it.
  
* Perform the conversion by running

        python convert_larcv1_to_larcv2.py

  This script just runs the server and client scripts.



