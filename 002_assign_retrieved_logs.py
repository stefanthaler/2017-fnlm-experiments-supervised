 # -*- coding: utf-8 -*-

from os.path import join
from approaches.signatures import assign_retrieved_logs

variable_char = "º"
data_dir = "data"

# input
test_logsfile_name  = join(data_dir,"test_logfile.txt")
found_signatures_filename = join(data_dir,"test_found_signatures.logsig")
retrieved_logs_filename = join(data_dir,"retrieved_logs.logsig")

assign_retrieved_logs(test_logsfile_name,found_signatures_filename,retrieved_logs_filename)
