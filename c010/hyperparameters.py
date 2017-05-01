from os.path import join

data_dir = "data"
results_dir = join("c010","results")
train_logfile = join(data_dir, 'train_logfile.txt')
test_logsfile_name  = join(data_dir,"test_logfile.txt")
result_tags_filename = join(results_dir,"result_tagsfile.logtags")


result_tags_filename = join(join("c100","results"),"result_tagsfile.logtags")
found_signatures_filename = join(results_dir,"found_signatures.logsig")
assigned_signatures_filename = join(results_dir,"assigned_signatures.logsig")

loglines = list(open(train_logfile,"r"))
