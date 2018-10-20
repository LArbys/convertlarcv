import os,sys

from larcv import larcv
from ROOT import Long
import cv2 as cv

from serverfeed.larcvserver import LArCVServerClient

client = LArCVServerClient( 0, "ipc:///tmp/feedtest/" )

io = larcv.IOManager(larcv.IOManager.kWRITE)
io.set_out_file("output_whole_view.root")
io.initialize()
    
more = True
while more:
    ok  = client.send_receive()
    if not ok:
        break
    data = client.products
    rse = data["rse"].reshape( (3) )
    io.set_id( rse[0], rse[1], rse[2] )
    print "saving entry: ",data["entry"][0,0,0,0]," of ",data["entry"][0,0,0,1],". RSE=",rse
    
    for name,arr in data.items():
        print " processing ",name
        if "meta" in name:
            continue
        if name in ["entry","rse","feeder"]:
            continue
        # should be image array
        meta_np = data["%s_meta"%(name)]

        # make evcontainer
        evout = io.get_data("image2d", name )

        # make meta
        nimgs = arr.shape[1]
        print arr.shape
        for i in xrange( nimgs ):
            nrows = Long( meta_np[0,i,0,1] )
            ncols = Long( meta_np[0,i,0,0] )
            planeid = Long( meta_np[0,i,0,6] )
            
            lcvmeta = larcv.ImageMeta( meta_np[0,i,0,2], meta_np[0,i,0,3], meta_np[0,i,0,4], meta_np[0,i,0,5], nrows, ncols, planeid  )
            # convert image            
            lcvimg = larcv.as_image2d_meta( arr[0,i,:,:].transpose((1,0)), lcvmeta )
            evout.append( lcvimg )
    #cv.imwrite("entry_%d_adc.png"%(data["entry"][0,0,0,0]),data["adc"][0,1,:,:])
            
    io.save_entry()    
    if data["entry"][0,0,0,0]+1==data["entry"][0,0,0,1]:
        more = False


io.finalize()

    
