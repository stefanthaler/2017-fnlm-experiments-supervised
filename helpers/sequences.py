from collections import deque
import numpy as np
from keras.preprocessing import sequence # padd sequences

def char2seq(line, vocabulary,lstm_length,sliding_window_stride, ignore_newline=False):
    sequences = []
    line = line[:-1] if ignore_newline else line

    if len(line)<=lstm_length: # we don't need to slide over the lstm because it is long enough
        id_sequence = []
        for char in line:
            if char in vocabulary.keys():
                id_sequence.append( vocabulary[char] )
            else:
                print "Unknown Char: '{}'".format(char)
                id_sequence.append( vocabulary[UNK] )
        sequences.append( id_sequence )

    else: # slide over tokens to create multiple sequences
        sliding_window = deque([], lstm_length)
        for tid, char in enumerate(line,1): # start at 1, because then then the tid matches the length

            if char in vocabulary.keys():
                sliding_window.append( vocabulary[char] )
            else:
                print "Unknown Char: '{}'".format(char)
                sliding_window.append( vocabulary[UNK] )

            if tid>=lstm_length: # from this moment on we have to store sequences;
                is_in_sliding_window_stride = (tid - lstm_length)%sliding_window_stride == 0
                is_last_position = tid+lstm_length-1 >= len(line)
                if is_in_sliding_window_stride or is_last_position:
                    sequences.append( list(sliding_window) )
    return sequences

def char_to_id_sequence(lines, vocabulary,lstm_length,sliding_window_stride, ignore_newline=False):
    sequences = []
    for line in lines:
        sequences = sequences + char2seq(line, vocabulary,lstm_length,sliding_window_stride, ignore_newline)
    return np.array(sequences)

def longest_line(lines):
    max_len = -1
    for line in lines:
        if len(line)>max_len:
            max_len=len(line)
    return max_len

def pad_sequence(sequences, lstm_length):
    padded_sequences = []
    for seq in sequences:
        if len(seq) % lstm_length == 0:
            padding_length = len(seq)
        else:
            padding_length = (len(seq) / lstm_length + 1) * lstm_length
        padded = sequence.pad_sequences([seq] ,maxlen=padding_length, padding="post" )
        padded_sequences.append(padded[0])
    return np.array(padded_sequences)


def lines_to_char_id(lines, vocabulary, ignore_newline=False):
    sequences = []
    for line in lines:
        if ignore_newline: line = line[:-1]
        sequence = [vocabulary[c] for c in line]
        sequences.append(sequence)
    return sequences


def id_seq2_onehot_seq(correct_tags, num_examples, max_len_tokens, number_of_tags):
    correct_tags_oh = np.ndarray(shape=(num_examples,max_len_tokens, number_of_tags ))

    for row_id, row in enumerate(correct_tags[:]):
        row_one_hot = np.zeros( (len(row), number_of_tags) )
        row_one_hot[np.arange(len(row)), row ] = 1
        correct_tags_oh[row_id]=row_one_hot

    return correct_tags_oh

"""
    Input: two arrays,
        loglines = [[this is a log 123]]
        taglines = [[FFFFFFFFFFFFFFVVV]]
        variable_char_id = The id of the tag vocabulary id that represents the variable character.
    Output: one array:
        tag = [[this is a log VVV]]
"""
def squash(loglines, taglines, variable_char_id=-1):
    out = np.ndarray(shape=loglines.shape)
    f_id = 1 # from tags vocabulary
    v_id = 2 # from tags vocabulary
    for (i,j), token_id in np.ndenumerate(loglines):
        out[i,j] = variable_char_id if taglines[i,j]==v_id else token_id
    return out


def check_dataset_sanity(train_logfile, train_tagfile, token_vocabulary, lstm_length, sliding_window_stride ):

    loglines_sanity = list(open(train_logfile,"r"))
    taglines_sanity = list(open(train_tagfile,"r"))

    for i, logline in enumerate(loglines_sanity):
        tagline = taglines_sanity[i]
        if not len(logline)+1 == len(tagline): # the newline character of the logline is also tagged
            print("lines %.4d are not equally long: logline %i, tagline %i" % (i,len(logline), len(tagline) ) )

        log_seqs = char2seq(logline, token_vocabulary, lstm_length,sliding_window_stride, False )
        tag_seqs = char2seq(tagline, token_vocabulary, lstm_length,sliding_window_stride, True  )
        if not len(log_seqs) == len(tag_seqs):
            print("line %.2d sequences is not equal: logseqs %i, tagseqs %i" % (i,len(log_seqs), len(tag_seqs) ) )
            print(logline)
            print(tagline)
            print(log_seqs)
            print(tag_seqs)
