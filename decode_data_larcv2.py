import os,sys

import ROOT as rt
from ROOT import Long
from larcv import larcv

import numpy as np

def decode_larcv2_evimage2d( io, producername, imgdata_np, imgmeta_np ):
    
    # make evcontainer
    evout = io.get_data("image2d", producername )

    # make meta
    nimgs = imgdata_np.shape[1]
    for i in xrange( nimgs ):
        nrows   = Long( imgmeta_np[0,i,0,1] )
        ncols   = Long( imgmeta_np[0,i,0,0] )
        planeid = Long( imgmeta_np[0,i,0,6] )
            
        lcvmeta = larcv.ImageMeta( imgmeta_np[0,i,0,2], imgmeta_np[0,i,0,3], imgmeta_np[0,i,0,4], imgmeta_np[0,i,0,5], nrows, ncols, planeid  )
        # convert image
        outarr = np.flip( imgdata_np[0,i,:,:].transpose((1,0)), 0 )
        lcvimg = larcv.as_image2d_meta( outarr , lcvmeta )
        evout.append( lcvimg )

    return

def decode_larcv2_evstatus( io, producername, evstatus_np ):
    shape = evstatus_np.shape
    evstatus_np = evstatus_np.reshape( (shape[2],shape[3]) )
    evout = io.get_data("chstatus", producername)
    nchs = evstatus_np.shape[0]
    evstatus_lcv = larcv.as_eventchstatus( evstatus_np )
    for p in xrange(nchs):
        evout.insert( evstatus_lcv.status(p) )

    return
    

def decode_larcv2_productdict( io, datadict ):

    # we need to find img+meta pairs
    # if we find other products we simply convert them
    
    img2dict = {}

    # collect image components, store other products
    for dataname,obj in datadict.items():
        print "decode ",dataname,":",type(obj),
        if type(obj) is np.ndarray:
            print obj.shape
        else:
            print
            
        name = dataname.split("_")[0].strip()
        producername = dataname.split("_")[-1].strip()
        if "image2d" in name or "imagemeta" in name:
            if producername not in img2dict:
                img2dict[producername] = {"image2d":None,"imagemeta":None}
            if "image2d" in name:
                img2dict[producername]["image2d"] = obj
            elif "imagemeta" in name:
                img2dict[producername]["imagemeta"] = obj

        elif "chstatus" in name:
            decode_larcv2_evstatus( io, producername, obj )

    # now process the images
    for producer,arrays in img2dict.items():
        decode_larcv2_evimage2d( io, producer, arrays["image2d"], arrays["imagemeta"]  )

    return
            
            
