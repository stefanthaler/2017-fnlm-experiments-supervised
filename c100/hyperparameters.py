from os.path import join

data_dir = "data"
results_dir = join("c100","results")
train_logfile = join(data_dir, 'train_logfile.txt')
train_tagfile = join(data_dir, 'train_tagsfile.logtags')
vocab_file = join(data_dir,"train_logfile.txt") # all the characters that should be in train
test_logsfile_name  = join(data_dir,"test_logfile.txt")
result_tags_filename = join(results_dir,"result_tagsfile.logtags")

loglines = list(open(train_logfile,"r"))
taglines = list(open(train_tagfile,"r"))

lines_to_tag = 50

batch_size = 10          # nubmer of training examples per batch. number influences validation accuracy
number_of_epochs = 10    # number of training epochs
embedding_size = 64    # dimension of the word embedding vectors.
lstm_length = 25     # will be assigned to the longest log line in our trainings dataset
sliding_window_stride = 1
dropout = 0.7           # dropout between lstm and dense layer see http://www.cs.toronto.edu/~rsalakhu/papers/srivastava14a.pdf
lstm_input_size = 128    # number of neurons within one lstm cell. [input x output], [output x output], [output]
number_of_tags = 3         # we have the following tags: F, V + Padding
learning_rate = 0.0005
random_seed = 0
validation_split = 0.2
k_fold = 5

optimizing_method = 'adam'      # Variant of SGD; see https://arxiv.org/pdf/1412.6980v8.pdf
loss_function = 'categorical_crossentropy' # see http://colah.github.io/posts/2015-09-Visual-Information/
