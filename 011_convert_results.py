# -*- coding: utf-8 -*-
"""
    Convert IPLoM results to format used in evaluation
"""
from c010.hyperparameters import *
variable_char = "º"

from os import listdir
import re

# convert found signatures
logsig_signatures = {}
found_signatures_file = open(found_signatures_filename, "w")
for logsig_signature in list(open("c010/results/logTemplates.txt","r")):
    line = re.split(r"\t: ",logsig_signature)
    signature_id = line[0]
    signature = line[1]
    signature = signature.replace("*",variable_char)
    logsig_signatures[signature_id]=signature
    found_signatures_file.write(signature)
found_signatures_file.close()

# gather assigned signatures
assigned_lines = {}
for file_name in listdir("c010/results"):
    if not file_name.startswith("template"):
        continue
    signature_id = file_name.replace("template","").replace(".txt","")
    for line in list(open("c010/results/"+file_name)):
        l = re.split(r"\t: ",line)
        l_id = l[0]
        assigned_lines[l_id] = logsig_signatures[signature_id]

# write assigned signatures
assigned_signatures_file = open(assigned_signatures_filename, "w")
for line_id in sorted(assigned_lines.keys()):
    assigned_signatures_file.write(assigned_lines[line_id])

assigned_signatures_file.close()
