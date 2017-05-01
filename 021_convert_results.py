 # -*- coding: utf-8 -*-
"""
    Convert logcluster results to format used in evaluation
"""
import re
variable_char = "º"


assigned_signatures_filename = "c020/results/assigned_signatures.logsig"
found_signatures_filename = "c020/results/found_signatures.logsig"

found_signatures_file = open(found_signatures_filename, "w")


signatures_regexes = []
for line in list(open("c020/results/logclustr.txt","r")):
    if line.startswith("Support:") or len(line.strip())==0:
        continue

    lc_signature = line[:-1]
    print(lc_signature)
    # replace *{1,1} tags with variable char.
    # we  also replace also tags that are longer than 1
    # for example, *{1,2} will group
    split_lc  = re.split(r"\*\{[0-9]+,[0-9]+\}", lc_signature)
    tag_parts = re.findall(r"\*\{[0-9]+,[0-9]+\}",lc_signature)
    signature_regex = ""
    for i, tag_part in enumerate(tag_parts):
        signature_regex += re.escape(split_lc[i])
        lower_repeat = int(tag_part.replace("*{","").replace("}","").split(",")[0])
        higher_repeat = int(tag_part.replace("*{","").replace("}","").split(",")[1])
        if lower_repeat==1 and higher_repeat==1:
            tag_part_regex = ".+?"
        else:
            tag_part_regex = "(.+?\s){%i,%i}"%(lower_repeat,higher_repeat)

        signature_regex += tag_part_regex

    signature_regex += re.escape(split_lc[-1])
    print ("",split_lc[-1])
    print ("",re.escape(split_lc[-1]))
    signature_regex = re.compile(signature_regex)
    signature = variable_char.join(split_lc)

    if not signature[-1]=="\n":
        signature += "\n"
    found_signatures_file.write(signature)
    signatures_regexes.append( (signature_regex, signature))

found_signatures_file.close()


# assing found clusters
# gather assigned signatures
assigned_signatures_file = open(assigned_signatures_filename, "w")
for line in list(open("data/test_logfile.txt"))[:]:

    print "Matching line: %s"%line[:-1]

    matched_signatures = []
    for regex_signature_pair in signatures_regexes:
        matched = bool(re.match(regex_signature_pair[0], line[:-1]))
        if matched:
            matched_signatures.append(regex_signature_pair)
        print ("\t %s\t%s %s"%(line[:-1],matched, regex_signature_pair[0].pattern))

    if len(matched_signatures)==0:
        print ValueError("No signatures found for line(%s)\n"%line[:-1])
        assigned_signatures_file.write("NONE\n")
        continue # check next signature
    if len(matched_signatures)>1: # sanity check
        print("Multiple signatures(%s) matched, selecting most specific one"%(matched_signatures) )
        matched_signatures = sorted(matched_signatures, key=lambda sig: len(sig[0].pattern), reverse=True)
    assigned_signatures_file.write(matched_signatures[0][1]+"\n")
    # write the one signature that matched the line

assigned_signatures_file.close()
