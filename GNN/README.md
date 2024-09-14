
The plan is to implement some type of graph network for meta-learning within Clash Royale. I have methods to aquire data, but I can experiment with various batching techniques (e.g. statically, or discrete-time). The latter is preferred as I'd like to capture temporal correlations in the usages. Processing the information this way is referred to as discrete-time dynamic graphs (DTDG).

# Objectives

1. I want to obtain data periodically; perhaps automatically constructing the usages matrix for the top-1000 on discrete-time intervals.

2. This would require some scheduling framework that shouldn't be too complicated.

3. Populating the data matrices can be optimized (i.e., rewrite the data-retrieving methods for RoyaleAPI.Client).

4. To build a true bot, however, I really should write some screen-capture code and record Youtube gameplay. This would be easier than setting it up on IOS and playing myself. 

5. What about reinforcement learning?

# Graph Attention Networks 

The code implementations herein are largely adapted from [1] and [2]. The goal here is to understand how attention works and generally experiment with different types of graph networks.

I want to look more into GATs for this application, and this is a nice place to start. Some meaningful notes from the original GAT paper [3]:

- "GNNs consist of an iterative process, which propagates the node states until equilibrium; followed by a neural network, which produces an output for each node based on its state"

- "the model is directly applicable to inductive learning problems, including tasks where the model has to generalize to completely unseen graphs"

# References 

[1] https://github.com/gordicaleksa/pytorch-GAT

[2] https://github.com/PetarV-/GAT

[3] https://arxiv.org/abs/1710.10903