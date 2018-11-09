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

    evout = io.get_data("chstatus", producername)
    for p in xrange(3):
        evout.insert( evout.status(p) )

    return
    

def decode_larcv2_productdict( io, datadict ):

    # we need to find img+meta pairs
    # if we find other products we simply convert them
    
    img2dict = {}

    # collect image components, store other products
    for dataname,obj in datadict.items():
        name = dataname.split("_")[0].strip()
        producername = dataname.split("_")[1].strip()
        if "image2d" in name or "imagemeta" in name:
            if producername not in img2dict:
                img2dict[producername] = {"image2d":None,"imagemeta":None}
            if "image2d" in name:
                img2dict[produername]["image2d"] = obj
            elif "imagemeta" in name:
                img2dict[produername]["imagemeta"] = obj

        elif "chstatus" in name:
            decode_larcv2_productdict( io, producername, obj )

    # now process the images
    for producer,arrays in img2dict:
        decode_larcv2_evimage2d( io, producer, arrays["image2d"], arrays["imagemeta"]  )

    return
            
            
