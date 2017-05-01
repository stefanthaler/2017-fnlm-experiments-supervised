"""
    Extracts signatures from a given log file using a neural model to tag the fixed and variable part
"""
"""
    Imports
"""
import numpy as np # numpy datastructures
np.random.seed(1)  # for reproducibility

import re # for splitting loglines
import os
from os.path import join # for joining pathes
from os.path import exists
from collections import deque
import operator
# keras layers
from keras.preprocessing import sequence
from keras.models import Model
from keras.layers import Dense, Dropout, Embedding, LSTM, Input, Bidirectional, merge, TimeDistributed
from keras.models import load_model
from helpers import *
import datetime as dt


"""
    hyperparameters
"""
from c100.hyperparameters import *


"""
    Step 1 - Tag fixed parts and variable parts
"""
# Load Vocabulary
token_vocabulary = create_vocabulary_from( vocab_file , add_unk=True )
vocabulary_size = len(token_vocabulary)
tags_vocabulary =  {"V":1 ,"F":2} # create_vocabulary_from( train_tagfile, ignore_newline = True)
print("\nLoaded {} logline characters and {} tags".format(len(token_vocabulary), len(tags_vocabulary)))

# Load Model
best_model_path = best_model(results_dir ,"bilstm-char")
# best_model_path = "model.keras"
model = load_model(best_model_path)
print("\nModel '%s' loaded\n"%best_model_path)

"""
    Tag testfile
"""
tagsfile = open(result_tags_filename,"w")
sorted_reverse_tag_vocabulary = ["P"]+[e[0] for e in sorted(tags_vocabulary.items(), key=operator.itemgetter(1))]
print(sorted_reverse_tag_vocabulary)


start_time  = dt.datetime.now()
with open(test_logsfile_name,"r") as f: # create_vocabulary_from( train_tagfile, ignore_newline = True) "r") as f:
    for lid, line in enumerate(f):
        input_sequences = char2seq(line, token_vocabulary, lstm_length,sliding_window_stride)
        padded_input_sequences = sequence.pad_sequences(input_sequences, maxlen=lstm_length, padding="post")
        estimated_tags_oh = model.predict(padded_input_sequences, batch_size=len(padded_input_sequences))

        # flatten
        flatted_oh_tags = np.ndarray(shape=(len(line),number_of_tags))
        for i in xrange(min(len(line), lstm_length)):
            flatted_oh_tags[i]=estimated_tags_oh[0][i]

        for i, estimated_tag_oh in enumerate(estimated_tags_oh[1:]):
             flatted_oh_tags[lstm_length+i] = estimated_tag_oh[-1] # add the prediction of last sequence

        tags = []
        for one_hot_vector in flatted_oh_tags:
            tags.append(sorted_reverse_tag_vocabulary[np.argmax(one_hot_vector)])

        # write lines
        tagline = "".join(tags)
        tagsfile.write(tagline+"\n")
tagsfile.close()

end_time = dt.datetime.now()

print("Tagging file took %fms"%( (end_time - start_time).microseconds/1e3))
