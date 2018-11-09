import os,sys,time

from serverfeed.larcvserver import LArCVServer
from serverfeed.loaderfunction import LoaderFunction

class LoadLArCV1(LoaderFunction):
    def __init__(self,productdict):
        super(LoadLArCV1,self).__init__()
        self.productdict = productdict
        
    def loadevent( self, io ):
        """ example of data loader function. we provide dictionary with numpy arrays (no batch) """
        from larcv import larcv
        import numpy as np
        from load_data_larcv1 import load_data_larcv1        

        data = load_data_larcv1( io, self.productdict )
        
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
    #inputfile = "../../nutufts/larflow/testdata/larcv1_data/larcv_wholeview_2e59dbd4-a395-4296-8d81-f84c4a7e474b.root"
    inputfile = sys.argv[1]
    productlist = sys.argv[2:]

    productdict = {}
    for arg in produclist:
        productdict[ arg.split(":")[0] ] = arg.split(":")[-1]
    
    feeder = LArCVServer(batchsize,"test",LoaderFunction(productdict),inputfile,nworkers,server_verbosity=0,worker_verbosity=0,queuesize=1,randomaccess=False)

    print "Server Started"
    while True:
        time.sleep(1)
        
    print "server stopped"
    
