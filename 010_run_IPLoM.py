from c010.IPLoM import *
from helpers import *
from c010.hyperparameters import *

results_dir = './c010/results/'
clean_create_dir(results_dir)

test_logsfile_name = "data/test_logfile.txt-ln.log"

para=Para(path='./', logname=test_logsfile_name, savePath=results_dir)

myparser=IPLoM(para)
time=myparser.mainProcess()
print ('The running time of IPLoM is', time)
