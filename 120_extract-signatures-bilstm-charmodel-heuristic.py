 # -*- coding: utf-8 -*-
"""
    Extracts signatures from a given log file using a neural model to tag the fixed and variable part

    Uses a heuristic to correct tags. Splits the annotated lines into words, and checks if some of the tags can be corrected_sal

    For example, a "VFV" tag for "999" can be most likely corrected to VVV.

"""


"""
    hyperparameters
"""
from c120.hyperparameters import *
from helpers.logs import *
import re
import sys

variable_char = "º"

from approaches.signatures import extract_signatures_heuristic
extract_signatures_heuristic(test_logsfile_name,result_tags_filename,assigned_signatures_filename,found_signatures_filename)
