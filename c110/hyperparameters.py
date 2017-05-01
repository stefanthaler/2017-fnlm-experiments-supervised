from os.path import join

data_dir = "data"
test_logsfile_name  = join(data_dir,"test_logfile.txt")
results_dir = join("c110","results")
result_tags_filename = join(join("c100","results"),"result_tagsfile.logtags")
found_signatures_filename = join(results_dir,"found_signatures.logsig")
assigned_signatures_filename = join(results_dir,"assigned_signatures.logsig")
combined_signatures_filename = join(results_dir,"combined_signatures.logsig")
