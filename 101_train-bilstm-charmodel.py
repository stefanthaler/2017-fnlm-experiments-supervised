"""
    Import
"""
import numpy as np # numpy datastructures
np.random.seed(2)  # for reproducibility
from sklearn.model_selection import train_test_split

import re # for splitting loglines
from os.path import join # for joining pathes
import os
from collections import deque
import shutil
from os.path import exists
# keras layers
from keras.preprocessing import sequence
from keras.models import Model
from keras.layers import Dense, Dropout, Embedding, LSTM, Input, Bidirectional, merge, TimeDistributed
from keras.callbacks import ModelCheckpoint # for saving checkpoints
from keras.layers.normalization import BatchNormalization
from keras.models import load_model
from helpers import *
"""
    Hyper Parameters
"""
from c100.hyperparameters import *

clean_create_dir(results_dir)

# need np array for cross fold validation
loglines = np.array(loglines)
taglines = np.array(taglines)

"""
    Create Vocbaularies
"""
# create vocabulary for log lines
token_vocabulary = create_vocabulary_from( vocab_file , add_unk=True )
vocabulary_size = len(token_vocabulary)
tags_vocabulary =  {"V":1 ,"F":2} # create_vocabulary_from( train_tagfile, ignore_newline = True)
print("Loaded {} logline characters and {} tags".format(len(token_vocabulary), len(tags_vocabulary)))

"""
    Sanity Checks for dataset
"""
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

"""
    Input Embedding
"""
def create_bilstm_model():
    # sequence of word ids, e.g: [ 12, 15, 17, 9, 5 ], one for each example of the batch
    split_logline_seq = Input(
        shape=(lstm_length,), # [number of cells, batch_size]
        dtype='int32'
    )
    # embed word id to vector, i.g. 12 will be mapped to the 12th row vector of the embedding matrix
    embedded = Embedding(
        input_dim=vocabulary_size,
        output_dim=lstm_input_size,
        input_length=lstm_length, # number of subsequent rnn cells
        mask_zero=True
    )(split_logline_seq)

    """
        Many to Many LSTM Model
    """

    # forward lstm
    forward_lstm = LSTM(
        output_dim=lstm_input_size, # input size
        return_sequences=True # returns full sequence; set to false, returns only the last output
    )(embedded)
    # backward lstm
    backword_lstm = LSTM(
        output_dim=lstm_input_size,
        return_sequences=True,
        go_backwards=True
    )(embedded)
    # concatenate the outputs of the 2 LSTMs
    merged_lstm_outputs = merge([forward_lstm, backword_lstm], mode='concat', concat_axis=-1)
    dropped_lstm_outputs = Dropout(dropout)(merged_lstm_outputs)

    """
        Softmax Layer
    """

    predicted_tags = TimeDistributed(
        Dense(output_dim=number_of_tags, activation='softmax')
    )(dropped_lstm_outputs)

    """
        optimizer
    """
    from keras.optimizers import RMSprop
    otimizer = RMSprop(lr=learning_rate, rho=0.9, epsilon=1e-08, decay=0.05)
    """
        Finalize Model
    """
    model = Model(input=split_logline_seq, output=predicted_tags)

    # try using different optimizers and different optimizer configs
    # loss=binary_crossentropy, optimizer=rmsprop
    model.compile(
        loss=loss_function,
        metrics=['accuracy'],
        optimizer=otimizer,
        sample_weight_mode='temporal'
    )
    model.summary()
    return model

# stringin window over training lines
split_loglines_train = char_to_id_sequence(loglines, token_vocabulary,lstm_length,sliding_window_stride) # X_train, shape=[num_trainings_examples, max_len]
correct_tags_train =   char_to_id_sequence(taglines, tags_vocabulary,lstm_length,sliding_window_stride, ignore_newline=True) # y_train, shape=[num_trainings_examples, max_len]

# pad training and test sequenes
split_loglines_train = sequence.pad_sequences(split_loglines_train, maxlen=lstm_length, padding="post")
correct_tags_train =   sequence.pad_sequences(correct_tags_train, maxlen=lstm_length, padding="post")

# One Hot Encode Trainings Sequences
num_train_examples = correct_tags_train.shape[0]
batch_size = num_train_examples / 200
correct_tags_oh_train = id_seq2_onehot_seq(correct_tags_train, num_train_examples, lstm_length, number_of_tags)

model = create_bilstm_model()
# # checkpoint

filepath=join(results_dir,"bilstm-char-ep{epoch:02d}-acc{acc:.3f}.hdf5")
create_chekpoint = ModelCheckpoint(filepath, monitor='acc', verbose=1, save_best_only=True, mode='max')

# train model
history = model.fit(
    split_loglines_train, correct_tags_oh_train,
    #validation_split=validation_split,
    batch_size=batch_size,
    nb_epoch=number_of_epochs,
    callbacks=[create_chekpoint]
    #shuffle=True # shuffle training data after each epoch
)

print(history.history)
