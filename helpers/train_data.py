import numpy as np

"""
    Input:

    train_data has dimensions: [ num_samples, sequence_length, n_features ]




     [batch_size, lstm_length, n_features]

    Example:

    batch_size = 2
    n_features = 1
    lstm_length = 2 (number of timesteps, number of unrolled cells)

    [
     [1,2, 3,4],
     [5,6, 7,8],

     [9,0, a,b],
     [c,d, e,f]
    ]

    =>

    [
     [ # batch 1
        [1,2],
        [5,6]
     ],
     [ # batch 2
        [3,4],
        [7,8]]
     ], # reset model here
     [ # batch 3
        [9,0],
        [c,d]
     ],
     [ # batch 4
        [a,b],
        [e,f],
     ]# reset model here
    ]

"""
def reorder_traindata_stateful(train_data, batch_size=2, lstm_length=2, n_features=1):
    num_samples = train_data.shape[0]
    sequence_length = train_data.shape[1]
    n_features = 1 if len(train_data.shape)==2 else train_data.shape[2] # if 3rd dimension is not set it is a tensor of size 1
    train_data = train_data.reshape(num_samples, sequence_length, n_features)

    # sanity checks
    if not num_samples % batch_size == 0:
        print("WARNING: the batch_size (%i) should divide the number of samples (%i) into equal partitions. "%(batch_size, num_samples))
        print("WARNING: cutting samples from (%i) to (%i) "%(num_samples, num_samples/batch_size ))
        train_data = train_data[0:num_samples/batch_size,:,:]
    if not sequence_length % lstm_length ==0:
        raise ValueError("LSTM Length (%i) should be a divider of sequence_length (%i). You should padd the sequences accordingly."%(lstm_length, sequence_length))

    # init results
    reset_count = sequence_length / lstm_length # reset model every reset_count'th batch
    rearranged_train_data = []

    # split array
    row_split_indizes = [i for i in xrange(batch_size, num_samples , batch_size ) ]
    col_split_indizes = [i for i in xrange(lstm_length, sequence_length,lstm_length ) ]
    row_split_train_data = np.split(train_data, row_split_indizes, axis=0)

    for train_data_row in row_split_train_data:
        col_split_td_row = np.split(train_data_row, col_split_indizes, axis=1)
        for td_col in col_split_td_row:
            next_batch = np.reshape(td_col, (batch_size, lstm_length, n_features))
            rearranged_train_data.append(next_batch)

    return reset_count, np.array(rearranged_train_data)

def stateful_id_seq2_onehot_seq(correct_tags, number_of_tags):
    # [num_batches, batch_size, lstm_length, n_features ]
    # => [num_batches, batch_size, lstm_length, number_of_tags ]
    #num_batches,batch_size,lstm_size,n_features = correct_tags.shape

    correct_tags_oh = []

    for batch_id, row in enumerate(correct_tags):
        row_one_hot = np.zeros( (len(row), number_of_tags) ) # [25, 3]
        row_one_hot[np.arange(len(row)), row ] = 1
        correct_tags_oh.append(row_one_hot)

    return np.array(correct_tags_oh)

# d = np.array([
#  [1,2, 3,4],
#  [5,6, 7,8],
#
#  [9,0, "a","b"],
#  ["c","d", "e","f"]
# ])
#
# reset_count, new_d = reorder_traindata_stateful(d, batch_size=2, lstm_length=2)
#
# print(reset_count)
# print(new_d)
# print(new_d.shape)
#
# print(new_d[0])
