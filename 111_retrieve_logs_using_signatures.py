 # -*- coding: utf-8 -*-
from c110.hyperparameters import *
from approaches.signatures import assign_retrieved_logs
variable_char = "º"
import re

#from approaches.signatures import extract_signatures_vanilla
#extract_signatures_vanilla(
#test_logsfile_name,
#result_tags_filename,
#assigned_signatures_filename,
#found_signatures_filename,
#combined_signatures_filename)
retrieved_logs_filename = join(results_dir, "retrieved_logs.logsig")



assign_retrieved_logs(test_logsfile_name,found_signatures_filename,retrieved_logs_filename,variable_char="º" )
