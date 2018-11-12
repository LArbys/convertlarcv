import os,sys

from larcv import larcv
from ROOT import Long

import numpy as np

from serverfeed.larcvserver import LArCVServerClient
from decode_data_larcv2 import decode_larcv2_productdict

output = sys.argv[1]
jobtag="test"
if len(sys.argv)==3:
    jobtag=sys.argv[2]

client = LArCVServerClient( 0, "ipc:///tmp/feed{}/".format(jobtag) )

io = larcv.IOManager(larcv.IOManager.kWRITE)
io.set_out_file(output)
io.initialize()
    
more = True
while more:
    ok  = client.send_receive()
    if not ok:
        break
    data = client.products
    for d,a in data.items():
        print d,type(a)
    rse = data["rse"].reshape( (3) )
    io.set_id( rse[0], rse[1], rse[2] )
    print "saving entry: ",data["entry"][0,0,0,0]," of ",data["entry"][0,0,0,1],". RSE=",rse
    decode_larcv2_productdict( io, data )
    io.save_entry()    
    if data["entry"][0,0,0,0]+1==data["entry"][0,0,0,1]:
        more = False


io.finalize()

    
