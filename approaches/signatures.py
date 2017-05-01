# -*- coding: utf-8 -*-
import re
import sys
from helpers.logs import split_logline

"""
    Used in 110
"""
def extract_signatures_vanilla(test_logsfile_name,result_tags_filename,assigned_signatures_filename,found_signatures_filename,combined_signatures_filename,variable_char = "º"):
    logsfile = list(open(test_logsfile_name,"r"))
    tagsfile = list(open(result_tags_filename,"r"))


    assigned_signatures = []
    print ("Extracting signature for %i taglines and %i loglines (should be same)"%(len(tagsfile),len(logsfile)))
    found_signatures = []
    for current_line, tagline in enumerate(tagsfile):
        signature_chars = []
        print(tagline[:-1])
        print(logsfile[current_line])
        print("Line: %i Tags: %i, Chars:%i\n"%(current_line, len(tagline[:-1]), len(logsfile[current_line])))
        for current_char_pos, tag in enumerate(tagline[:-1]): # don't use newline of tags file
            log_char = logsfile[current_line][current_char_pos]
            if tag=="F":
                signature_chars.append(log_char)
            else: # tag == V
                if current_char_pos==0 or tagline[current_char_pos-1]=="F":
                    signature_chars.append(variable_char)
                else:
                    # we want to squash the variable parts of the signature to length 1
                    # in this case, the previous tag was a variable character, which means we will ignore this part.
                    pass

        signature = "".join(signature_chars)
        if not signature[-1] == "\n": # this is the case if the last characters were variable
            signature += "\n"

        found_signatures.append(signature)
        assigned_signatures.append(signature)

    combined_signatures_file = open(combined_signatures_filename,"w")

    with open(assigned_signatures_filename,"w") as f:
        for i,ass in enumerate(assigned_signatures):
            f.write(ass)
            combined_signatures_file.write(logsfile[i])
            combined_signatures_file.write(ass)
            combined_signatures_file.write("\n")


    # write found siqnatures
    found_signatures_file = open(found_signatures_filename,"w")
    found_signatures = set(found_signatures) # make them unique
    for found_signature in found_signatures:
        found_signatures_file.write(found_signature)
    found_signatures_file.close()

    print ("Found %i signatures"%len(list(open(found_signatures_filename))))
    print ("Assigned %i signatures to %s "%(len(list(open(assigned_signatures_filename,"r"))), assigned_signatures_filename) )


"""
    Used in 120
"""
def extract_signatures_heuristic(test_logsfile_name,result_tags_filename,assigned_signatures_filename,found_signatures_filename,variable_char = "º"):
    """
        Split annotated lines
    """
    # assign tags per split word.
    # so what we want to have are the split lines with the associated tags for each characters
    # an example for such a line would be: [ ...  ("pid", "FFF"), ("=","F"),(893,"VVV") .... ]
    split_annotated_lines = []
    tag_lines = list(open(result_tags_filename,"r"))

    for line_nr, line in enumerate(open(test_logsfile_name, "r")):
        # split line into tokens
        tags = tag_lines[line_nr]
        line_tokens = split_logline(line)
        token_tag_pairs = []
        pos = 0
        for token in line_tokens:
            token_tags = tags[pos:pos+len(token)]
            pos += len(token)

            token_tag_pairs.append(
                (token, token_tags)
            )

        split_annotated_lines.append(token_tag_pairs)

    for sal in split_annotated_lines:
        tokens = zip(*sal)[0]
        tags = zip(*sal)[1]

        print(" ".join(tokens[:-1]))
        print(" ".join(tags)+"\n")

    """
        Correct split annotated lines
    """
    corrected_annotated_lines = []
    for sal in split_annotated_lines:
        corrected_sal = []
        for token_tag_pair in sal:
            word = token_tag_pair[0]
            tags = token_tag_pair[1]
            f_count = float(tags.count("F"))
            v_count = float(tags.count("V"))
            # corrections
            if v_count >= f_count: # more variable parts than fixed parts and word is all numbers. example:  "34" and "FV"
                tags = len(tags)*"V"
            else:
                tags = len(tags)*"F"
            corrected_token_pair = (word,tags)
            corrected_sal.append(corrected_token_pair)
        corrected_annotated_lines.append(corrected_sal)



    print ("CORRECTED VERSION \n\n")
    for sal in corrected_annotated_lines:
        tokens = zip(*sal)[0]
        tags = zip(*sal)[1]

        print(" ".join(tokens[:-1]))
        print(" ".join(tags)+"\n")

    """
        Step 3 - Extract signature candidates
    """
    class Signature(object):
        def __init__(self, sal):
            self.raw_sal = sal

            self.signature_pairs = []
            for pair in sal:
                tag = "V" if pair[1].count("V") >= pair[1].count("F") else "F" # collapse tags on majority

                if len(self.signature_pairs) == 0:
                    self.signature_pairs.append( (pair[0], tag)  )
                else:
                    if self.signature_pairs[-1][1]==tag: # tag is similar to previous one
                        # append current pair to previous one, merge words, keep tag
                        self.signature_pairs[-1] = ( self.signature_pairs[-1][0]+pair[0], tag )
                    else:
                        # start new tag
                        self.signature_pairs.append( (pair[0], tag)  )

        def signature(self):
            sig = []
            for pair in self.raw_sal:
                for pos, tag in enumerate(pair[1]):
                    if tag=="V":
                        if len(sig)==0 or not sig[len(sig)-1]==variable_char:
                            sig.append(variable_char)
                        else:
                            #don't need to add that
                            pass
                    else:
                        sig.append(pair[0][pos])
            return "".join(sig)

        def __eq__(self, other):
            print("Comparing \n\t{} to\n\t{}".format(self.signature_pairs, other.signature_pairs))
            # length of singature pairs have to be the same
            if not len(self.signature_pairs) == len(other.signature_pairs):
                #TODO this acutally prohipbits us to find multi word variables that are separated by a space
                print("\t Not same amount of signature pairs")

                return False

            # now check
            # if all signature parts have the same labeling
            # if all fixed parts are the same
            for i, sp  in enumerate(self.signature_pairs):
                if not sp[1] == other.signature_pairs[i][1]:
                    print("\t {} th signature pair is different: {} vs {} ".format(i,sp[1],other.signature_pairs[i][1]))
                    return False
                if sp[1]=="V": # variable part may differ, both parts are variable parts, so we can carry on
                    continue
                if not sp[0] == other.signature_pairs[i][0]: # two fixed parts are not equal, so not same line
                    print("\t {}th signature pair is fixed and different: {} vs {}".format(i, sp[0],other.signature_pairs[i][0]))
                    return False
            # all good
            return True


    # replace
    signature_groups = []
    assigned_signatures_file = open(assigned_signatures_filename, "w")
    found_signatures_file = open(found_signatures_filename, "w")

    for sal in corrected_annotated_lines:
        new_signature = Signature(sal)
        signature_has_been_added = False

        for signature_group in signature_groups:
            if new_signature == signature_group[0]:
                signature_group.append(new_signature)
                signature_has_been_added = True

                assigned_signatures_file.write(signature_group[0].signature())
                if not signature_group[0].signature()[-1] == "\n":
                    assigned_signatures_file.write("\n")
                break

        if not signature_has_been_added:
            assigned_signatures_file.write(new_signature.signature())
            if not new_signature.signature()[-1] == "\n":
                assigned_signatures_file.write("\n")

            signature_groups.append([new_signature]) # create a new group
            found_signatures_file.write(new_signature.signature())
    found_signatures_file.close()
    assigned_signatures_file.close()

"""
"""
def group_signatures_vanilla(test_logsfile_name,result_tags_filename,assigned_signatures_filename,found_signatures_filename,combined_signatures_filename, variable_char = "º"):
    tagsfile = list(open(result_tags_filename,"r"))
    logsfile = list(open(test_logsfile_name,"r"))
    assigned_signatures = open(assigned_signatures_filename,"w")

    combined_signatures_file = open(combined_signatures_filename,"w")

    found_signatures = []
    for current_line, tagline in enumerate(tagsfile):
        signature = re.sub(r"(\xc2\xba)+",variable_char, tagline) # squash variable chars
        found_signatures.append(signature)
        assigned_signatures.write(signature)

        combined_signatures_file.write(logsfile[current_line])
        combined_signatures_file.write(signature)
        combined_signatures_file.write("\n")
    # write found siqnatures
    found_signatures_file = open(found_signatures_filename,"w")
    found_signatures = set(found_signatures) # make them unique
    for found_signature in found_signatures:
        found_signatures_file.write(found_signature)
    found_signatures_file.close()

    print ("Processed %i tagged lines"%i(len(tagsfile)))
    print ("%i Signatures extracted "%len(list(open(found_signatures_filename))))


"""
"""
def group_signatures_heuristic(test_logsfile_name,result_tags_filename,assigned_signatures_filename,found_signatures_filename,variable_char = "º"):
    split_annotated_lines = []
    tag_lines = list(open(result_tags_filename,"r"))
    original_logfile  = list(open(test_logsfile_name,"r"))
    assigned_signatures = open(assigned_signatures_filename,"w")
    # split annotated lines
    found_signatures = []

    for line_nr, line in enumerate(tag_lines):
        line_tokens = split_logline(line)
        line_pos = 0
        corrected_tokens = []
        for i, token in enumerate(line_tokens):
            v_count = float(token.count(variable_char))
            f_count = len(token) - v_count
            token_len = int(len(token) - v_count) # because variable char will be count as two
            # corrections
            original_token = original_logfile[line_nr][line_pos:(line_pos+token_len)]

            if v_count >= f_count: # more variable parts than fixed parts and word is all numbers. example:  "34" and "FV"
                corrected_token = token_len*variable_char
            else: # restore original token
                corrected_token = original_token
            line_pos += token_len # + 1 because of delimiter from splitting
            corrected_tokens.append(corrected_token)
            #print("Token(%s) => Corrected(%s), original_token(%s)"%(token, corrected_token, original_token))
        signature = "".join(corrected_tokens)
        signature = re.sub(r"(\xc2\xba)+",variable_char, signature) # squash variable chars

        if not signature[-1]=="\n":
            signature+="\n"

        found_signatures.append(signature)
        assigned_signatures.write(signature)
    assigned_signatures.close()
    # write found siqnatures
    found_signatures_file = open(found_signatures_filename,"w")
    found_signatures = set(found_signatures) # make them unique
    for found_signature in found_signatures:
        found_signatures_file.write(found_signature)
    found_signatures_file.close()


def assign_retrieved_logs(test_logsfile_name,found_signatures_filename,retrieved_logs_filename,variable_char="º" ):
    # for each signature
    found_signatures = list(open(found_signatures_filename,"r"))
    test_logslines = list(open(test_logsfile_name,"r"))
    print("assigning %i signaturs to %i log lines "%(len(found_signatures), len(test_logslines)))

    retrieved_logs_per_signature = {}

    tagged_lines = 0

    for signature in sorted(found_signatures):
        matched_logs = []
        if signature[-1]=="\n": signature = signature[:-1]
        for logline in test_logslines:
            # \xc2\xba
            signature_parts = signature.split(variable_char)
            signature_parts = [re.escape(p) for p in signature_parts]
            signature_re = re.compile(".*?".join(signature_parts))
            print(signature_re.pattern)
            print(logline)
            logline_matches_signature = re.match(signature_re, logline)
            if logline_matches_signature: # :
                matched_logs.append(logline)

        tagged_lines += len(matched_logs)
        retrieved_logs_per_signature[signature] = matched_logs

    retrieved_logs_file = open(retrieved_logs_filename, "w")
    for signature, assigned_logs in retrieved_logs_per_signature.iteritems():
        retrieved_logs_file.write(signature)
        for logline in assigned_logs:
            retrieved_logs_file.write("\t%s"%logline)
        retrieved_logs_file.write("\n")
    retrieved_logs_file.close()
    print("Assigned %i tags"%tagged_lines)
