
The code implementations herein are largely adapted from [1] and [2]. The goal here is to understand how attention works and experiment with different types of graph networks.

The plan is to implement some type of graph network for meta-learning within Clash Royale. I have methods to aquire data, but there are different ways in which I can feed it into a network (e.g. statically, or sequences of graghs captured at different times). The latter is preferred as I'd like to capture temporal correlations in the usages. 

I want to look more into GATs for this application, and this is a nice place to start. Some meaningful notes from the original GAT paper [3]:

- "GNNs consist of an iterative process, which propagates the node states until equilibrium; followed by a neural network, which produces an output for each node based on its state"

- "the model is directly applicable to inductive learning problems, including tasks where the model has to generalize to completely unseen graphs"



# References 

[1] https://github.com/gordicaleksa/pytorch-GAT

[2] https://github.com/PetarV-/GAT

[3] https://arxiv.org/abs/1710.10903