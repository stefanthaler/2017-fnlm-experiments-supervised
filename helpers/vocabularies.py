UNK="<UNK>"
def create_vocabulary_from(file_name, add_unk=False, ignore_newline=False ):
    vocabulary = {}
    with open(file_name, "r") as input_file:
        for line in input_file:
            line = line[:-1] if ignore_newline else line
            for char in line:
                if char in vocabulary.keys(): continue # we already know this token, so try next one
                vocabulary[char] = len(vocabulary)+1 # index starts from 1
    if add_unk: # id for unknown tokens
        vocabulary[UNK]=len(vocabulary)+1

    return vocabulary
