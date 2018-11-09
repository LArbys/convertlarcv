import os,sys
import numpy as np

# =====================================================
# ROUTINES HERE LOAD LArCV1 Objects into numpy arrays
# ----------------------------------------------------

def convert_image2d( producername, evimage2d ):
    # input
    # -----
    # evimage2d: larcv::EventImage2D instance
    #
    # output
    # ------
    # dictionary with data in it

    meta  = evimage2d.Image2DArray().front().meta()
    nimgs = evimage2d.Image2DArray().size()
    imgdata_np = np.zeros( (nimgs,meta.cols(),meta.rows()), dtype=np.float32 )
    imgmeta_np = np.zeros( (nimgs,1,7), dtype=np.float )
        
    for i in xrange( evimage2d.Image2DArray().size() ):
        img = evimage2d.Image2DArray().at(i)
        imgdata_np[i,:,:] = larcv.as_ndarray( img  )
        meta = img.meta()            
        imgmeta_np[i,0,0] = meta.cols()
        imgmeta_np[i,0,1] = meta.rows()
        imgmeta_np[i,0,2] = meta.min_x()
        imgmeta_np[i,0,3] = meta.min_y()
        imgmeta_np[i,0,4] = meta.max_x()
        imgmeta_np[i,0,5] = meta.max_y()
        imgmeta_np[i,0,6] = meta.plane()

    data = {}
    data["image2d_%s"%(producername)]   = imgdata_np
    data["imagemeta_%s"%(producername)] = imgmeta_np

    return data

def convert_chstatus( producername, evchstatus ):

    status_np = larcv.as_ndarray( evchstatus )
    data = {"chstatus_%s"%(producername):status_np}

    return data

def load_data_larcv1( io, product_dict ):
    # input
    # -----
    # product_dict: expects to be a dictionary with producer name as key and data type as value

    data = {}
    for ktype,vproducer in product_dict.items():
        if ktype=="image2d":
            products = convert_image2d(  vproducer, io.get_data( larcv.kProductImage2D,  vproducer ) )
        elif ktype=="chstatus":
            products = convert_chstatus( vproducer, io.get_data( larcv.kProductChStatus, vproducer ) )
        else:
            raise RuntimeError("Unrecognized product type")

        data.update(products)

    return data
    
if __name__ == "__main__":

    import ROOT as rt
    from larcv import larcv
    
    larcv1_fname = sys.argv[1]
    
    product_dict = {}
    for arg in sys.argv[2:]:
        product_dict[arg.split(":")[0]] = arg.split(":")[-1]


    io = larcv.IOManager( larcv.IOManager.kREAD )
    io.add_in_file(larcv1_fname)
    io.initialize()
    nentries = io.get_n_entries()

    num_errors1 = 0
    num_errors2 = 0
    for ientry in xrange(nentries):
        io.read_entry(ientry)
        
        data = load_data_larcv1( io, product_dict )

        print "[ENTRY %d]"%(ientry)
        for kproducer,arr in data.items():
            print "  ",kproducer,arr.shape

        # compare
        evchstatus = io.get_data( larcv.kProductChStatus, "wire" )
        num_diff1 = 0
        num_diff2 = 0
        for p in xrange(3):
            chstatus_np = larcv.as_ndarray( evchstatus.Status(p) )
            for i in xrange(0,evchstatus.Status(p).as_vector().size()):
                diff1 = evchstatus.Status(p).as_vector()[i] - data["chstatus_wire"][p,i]
                diff2 = evchstatus.Status(p).as_vector()[i] - chstatus_np[i]
                if diff1!=0:
                    num_diff1 += 1
                if diff2!=0:
                    num_diff2 += 1
            #print "np: ",data["chstatus_wire"][2,i],",  larcv:",evchstatus.Status(2).as_vector()[i]," chstatus: ",chstatus_np[i]," diff1:",diff1," diff2:",diff2
        print "   Num differences: ",num_diff1," ",num_diff2
        if num_diff1!=0:
            num_errors1 += 1
        if num_diff2!=0:
            num_errors2 += 1
    print "Number events with errors: ",num_errors1," ",num_errors2

    print "DONE"
