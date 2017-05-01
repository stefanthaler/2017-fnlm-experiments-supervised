 # -*- coding: utf-8 -*-
from c110.hyperparameters import *
variable_char = "º"

from approaches.signatures import extract_signatures_vanilla
extract_signatures_vanilla(test_logsfile_name,result_tags_filename,assigned_signatures_filename,found_signatures_filename,combined_signatures_filename)
