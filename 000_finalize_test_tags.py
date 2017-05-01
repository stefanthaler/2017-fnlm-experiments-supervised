"""
    Remove filtered lines from tags file.
"""
import os
from os.path import join
from os.path import exists
import shutil
import argparse     # parse command line ptions

being_checked_tags = open("data/test_tagsandlogs.logtags", "r")
checked_tags = open("data/test_tagsfile.logtags", "w")

for lid, line in enumerate(being_checked_tags):
    if not lid%3 == 0: continue # that was the log line
    checked_tags.write(line)

checked_tags.close()
being_checked_tags.close()
