 # -*- coding: utf-8 -*-

from os.path import join
from approaches.signatures import extract_signatures_vanilla

variable_char = "º"
data_dir = "data"

# input
test_logsfile_name  = join(data_dir,"test_logfile.txt")
result_tags_filename = join(data_dir,"test_tagsfile.logtags")
# output
found_signatures_filename = join(data_dir,"test_found_signatures.logsig")
assigned_signatures_filename = join(data_dir,"test_assigned_signatures.logsig")
combined_signatures_filename = join(data_dir,"combined_signatures.logsig")


extract_signatures_vanilla(test_logsfile_name,result_tags_filename,assigned_signatures_filename,found_signatures_filename,combined_signatures_filename)
