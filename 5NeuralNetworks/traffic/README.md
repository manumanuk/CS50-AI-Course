To begin, I mirrored the neural network structure from the lecture source code, using one convolution layer with 32
3x3 filters, followed by a 2x2 max pooling, a flattening layer, one hidden layer with 128 neurons, a 50% dropout layer,
and one output layer. As expected, this strategy was not optimal for this given problem, yielding an accuracy of ~5.6%
on the test data, taking ~5s per epoch to train.

Following this, I experimented with increasing the number of neurons in the hidden layer. Testing 256 neurons, the
accuracy jumped to a whopping 92%, however, at the cost of 15s per epoch to train. Interestingly, adding 512 neurons
gave a drop in accuracy to 90.6%, with a tremendous cost of 30s per epoch to train. Following this observation, I 
reduced the number of neurons back to 128, and added a second hidden layer with 128 neurons. At a cost of 12s, this
gave an accuracy of 62%. Increasing the number of neurons in these layers to 256 each, accuracy jumped to 93% at 16s
per epoch. After this, I reset the number of neurons per layer to 128, and added a third layer. This network structure
gave an accuracy of 88% for a training time of 12s per epoch.
These observations seemed to show that a moderate number of neurons in one layer was much more effective than adding
several layers with fewer neurons. Adding several layers with a moderate number of neurons was also not significantly
more effective than a single one with the same number.

After determining that I would use one hidden layer with 256 neurons, I began tweaking the number of convolution layers,
beginning by adding a copy of the original convolution layer proceeding the first one. However, this seemed to
tremendously increase the time to train (45s per epoch, albeit with an accuracy of 97.8%). To make the model less
intensive, I decided to add a max pooling layer of size 3x3 in between the convolution layers, reducing the training
time to 11s/epoch, but dropping accuracy to 85%. After experimenting with several combinations of convolution layers and
max-pooling layers, I arrived at the configuration in my submission.
My observations showed that there was merit in simplifying the complexity of the dataset at the beginning with large
filter convolution layers and more max pooling layers, then progressing to smaller filter sizes for convolution layers 
(with more filters per layer), to better recognize defining features in images. My final configuration consistently gave
an accuracy of 95%+, with a loss of >0.17.

Overall, image recognition neural networks require multiple convolutional and pooling layers to create comprehensive
feature maps, followed by a hidden layer with a moderate number of neurons. It can also be seen that pooling and
filtering in the first few layers of the network can greatly increase efficiency while maintaining accuracy.