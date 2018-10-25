import os,sys,time

from serverfeed.larcvserver import LArCVServer

def load_data_larcv1( io ):
    """ example of data loader function. we provide dictionary with numpy arrays (no batch) """
    from larcv import larcv
    import numpy as np
    
    index = (1,0)
    #products = ["larflow_y2v"]
    #products = ["adc","larflow_y2u"]
    products = ["wire"]
    evimage2d  = {} 
    for p in products:
        evimage2d[p] = io.get_data(larcv.kProductImage2D,p)

    data = {}
    for p in products:
        if evimage2d[p].Image2DArray().size()==0:
            continue
        allmeta = evimage2d[p].Image2DArray().front().meta()
        nimgs = evimage2d[p].Image2DArray().size()
        data[p] = np.zeros( (nimgs,allmeta.cols(),allmeta.rows()), dtype=np.float32 )
        
        data["%s_meta"%(p)] = np.zeros( (nimgs,1,7), dtype=np.float )
        
        for i in xrange( evimage2d[p].Image2DArray().size() ):
            img = evimage2d[p].Image2DArray().at(i)
            data[p][i,:,:] = larcv.as_ndarray( img  )
            meta = img.meta()            
            data["%s_meta"%(p)][i,0,0] = meta.cols()
            data["%s_meta"%(p)][i,0,1] = meta.rows()
            data["%s_meta"%(p)][i,0,2] = meta.min_x()
            data["%s_meta"%(p)][i,0,3] = meta.min_y()
            data["%s_meta"%(p)][i,0,4] = meta.max_x()
            data["%s_meta"%(p)][i,0,5] = meta.max_y()
            data["%s_meta"%(p)][i,0,6] = meta.plane()

    data["rse"] = np.zeros( (3),dtype=np.int )
    evid = io.event_id()
    data["rse"][0] = evid.run()
    data["rse"][1] = evid.subrun()
    data["rse"][2] = evid.event()
    data["rse"] = data["rse"].reshape( (1,1,3) )

    data["entry"] = np.zeros( (2), dtype=np.int )
    data["entry"][0] = io.current_entry()
    data["entry"][1] = io.get_n_entries()
    data["entry"] = data["entry"].reshape( (1,1,2) )

    print "prepared entry",data["entry"][0,0,0]," of ",data["entry"][0,0,1]," w rse=",data["rse"][0,0,:]
            
    return data
    

if __name__ == "__main__":

    batchsize = 1
    nworkers  = 1
    print "start feeders"
    #inputfile = "larcv1_larflow_y2u_bnbext_mcc9.root"
    #inputfile = "larcv1_larflow_y2v_bnbext_mcc9.root"
    inputfile = "../../nutufts/larflow/testdata/larcv1_data/larcv_wholeview_2e59dbd4-a395-4296-8d81-f84c4a7e474b.root"
    feeder = LArCVServer(batchsize,"test",load_data_larcv1,inputfile,nworkers,server_verbosity=0,worker_verbosity=0,queuesize=1,randomaccess=False)

    print "Server Started"
    while True:
        time.sleep(1)
        
    print "server stopped"
    
