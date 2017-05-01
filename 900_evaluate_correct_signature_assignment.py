 # -*- coding: utf-8 -*-
import argparse                     # for parsing command line options
from os.path import join
import re

# variable_char = "º"
parser = argparse.ArgumentParser(description='Evaluates the amount of correct signature assigments')
parser.add_argument('-e',  '--experiment', type=str, default="c110", help='The directory where the outputs of the experiment are stored. It will look for ')
parser.add_argument('-b',  '--beta', type=float, default=1.0, help='Beta for f_beta score. Default is f1. The higher, the more weight is put on recall than on precision')
args = parser.parse_args()

def assign_retrieved_logs(test_logsfile_name,found_signatures_filename,variable_char="º" ):
    # for each signature
    found_signatures = list(open(found_signatures_filename,"r"))
    test_logslines = list(open(test_logsfile_name,"r"))

    retrieved_logs_per_signature = {}

    tagged_lines = 0

    for signature in sorted(found_signatures):
        matched_logs = []
        for logline in test_logslines:
            # \xc2\xba
            signature_parts = signature.split(variable_char)
            signature_parts = [re.escape(p) for p in signature_parts]
            signature_re = re.compile(".*?".join(signature_parts))
            logline_matches_signature = re.match(signature_re, logline)
            if logline_matches_signature: # :
                matched_logs.append(logline)

        tagged_lines += len(matched_logs)
        retrieved_logs_per_signature[signature] = matched_logs
    return retrieved_logs_per_signature

test_logsfile_name  = join("data","test_logfile.txt")
true_signatures_filename = join("data","test_found_signatures.logsig")

found_signatures_filename =  join(args.experiment, "results",  "found_signatures.logsig")

true_clusters =  assign_retrieved_logs(test_logsfile_name, true_signatures_filename)
evaluate_clusters = assign_retrieved_logs(test_logsfile_name, found_signatures_filename)

print len(true_clusters)
print len(evaluate_clusters)

correct_assignments = 0 #
partially_correct_assignments = 0 #
wrong_assignments = 0 #
total_eval_assignments = 0
total_true_assignments = 0

for true_signature, true_loglines in true_clusters.iteritems():
        true_loglines = set(true_loglines)
        total_true_assignments += len(true_loglines)

used_true_clusters = []

for eval_signature, eval_loglines in evaluate_clusters.iteritems():
    print("\nEvaluating Cluster:%s"%eval_signature[:-1])
    eval_loglines = set(eval_loglines)
    total_eval_assignments += len(eval_loglines)
    for l in eval_loglines: print("\t%s"%l[:-1])

    if len(eval_loglines)==0:
        print("\t no signatures in cluster, continuing")
        continue


    for true_signature, true_loglines in true_clusters.iteritems():
            true_loglines = set(true_loglines)
            if true_loglines == eval_loglines: # found an identical cluster
                # entirely correct cluster
                if not true_signature in used_true_clusters:
                    correct_assignments += len(eval_loglines)
                    used_true_clusters.append(true_signature)
                else: #
                    partially_correct_assignments += len(eval_loglines)
                print ("Matched:%s" %true_signature[:-1])
                for l in eval_loglines: print("\t%s"%l[:-1])
                break
            elif true_loglines.issuperset(eval_loglines): # found a subcluster
                print ("Partially Matched:%s" %true_signature[:-1])
                for l in true_loglines: print("\t%s"%l[:-1])
                partially_correct_assignments += len(eval_loglines)
                break
            elif not true_loglines.isdisjoint(eval_loglines): # found a partially overlapping cluster
                print ("Wrong Assignment:%s" %true_signature[:-1])
                for l in true_loglines: print("\t%s"%l[:-1])
                mutual_lines = len(true_loglines.intersection(eval_loglines))
                partially_correct_assignments += mutual_lines
                wrong_assignments += len(eval_loglines) - mutual_lines
                break

print("\n\n\nEvaluating correct assignments of loglines to signatures of experiment %s"%args.experiment)

print ("Total eval assignments\t: %i"%total_eval_assignments )
print ("Total true assignments\t: %i"%total_true_assignments)
print ("Correct\t: %i \t %0.4f"%(correct_assignments,100*correct_assignments/float(total_eval_assignments)) )
print ("Partially\t: %i \t %0.4f"%(partially_correct_assignments,100*partially_correct_assignments/float(total_eval_assignments)))
print ("Wrong\t: %i \t %0.4f"%(wrong_assignments,100*wrong_assignments/float(total_eval_assignments)))
print ("Total\t: %i"%(correct_assignments+partially_correct_assignments+wrong_assignments))
