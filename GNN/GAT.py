import torch
import torch.nn as nn

from utils.constants import LayerType


class GATLayer(nn.Module):
    """
    Base class for all inheriting GAT implementations: see Section 2.1.
    """
    def __init__(self, num_in_features, num_out_features, num_of_heads, layer_type, concat=True, activation=nn.ELU(), dropout_prob=0.6, add_skip_connection=True, bias=True, log_attention_weights=False):

        super().__init__()

        # save for forward propagation in children layers (imp1/2/3)
        self.num_of_heads = num_of_heads
        self.num_out_features = num_out_features
        self.concat = concat  # whether we should concatenate or average the attention heads
        self.add_skip_connection = add_skip_connection

        # === Trainable Weights ===

        #   - linear projection matrix; denoted as "W"
        #   - attention target/source; denoted as "a"
        #   - bias; not in paper

        if layer_type == LayerType.IMP1:            
            self.proj_param = nn.Parameter(torch.Tensor(num_of_heads, num_of_heads*num_out_features, bias=False))
        else:
            self.linear_proj = nn.Linear(num_in_features, num_of_heads*num_out_features, bias=False)

        # After concatenating target i and source j, we apply the additive scoring function which gives the 
        # un-normalized score e_ij; see Eq. 2.

        # Instead of [h1, h2] (concatenation of node feature vectors) and dot product with "a", we do:
        # dot(h1, a_left) + dot(h2, a_right).
        self.scoring_fn_target = nn.Parameter(torch.Tensor(1, num_of_heads, num_out_features))
        self.scoring_fn_source = nn.Parameter(torch.Tensor(1, num_of_heads, num_out_features))

        # Simple reshaping; TODO: compare this to Imp2.
        if layer_type == LayerType.IMP1:
            self.scoring_fn_target = nn.Parameter(self.scoring_fn_target.reshape(num_of_heads, num_out_features, 1))
            self.scoring_fn_source = nn.Parameter(self.scoring_fn_source.reshape(num_of_heads, num_out_features, 1))

        # TODO: understand this
        if bias and concat:
            self.bias = nn.Parameter(torch.Tensor(num_of_heads * num_out_features))
        elif bias and not concat:
            self.bias = nn.Parameter(torch.Tensor(num_out_features))
        else:
            self.register_parameter('bias', None)

        # TODO: understand this
        if add_skip_connection:
            self.skip_proj = nn.Linear(num_in_features, num_of_heads * num_out_features, bias=False)
        else:
            self.register_parameter('skip_proj', None)

        # === End of Trainable Weights ===

        self.leakyReLu = nn.LeakyReLU(0.2)
        self.softmax = nn.Softmax(dim=-1) # apply log-softmax along last dimension
        self.activation = activation
        # TODO: understand this better
        self.dropout = nn.Dropout(p=dropout_prob)

        self.log_attention_weights = log_attention_weights  
        self.attention_weights = None  # for later visualization purposes; cache the weights here

        self.init_params(layer_type)

    def init_params(self, layer_type):
        """
        Initialize with Glorot (Xavier uniform) weight distributions for "W", "a", and bias. This is used 
        to mimic the original implementation, which was developed in TensorFlow.
        """
        nn.init.xavier_uniform_(self.proj_param if layer_type == LayerType.IMP1 else self.linear_proj.weight)
        nn.init.xavier_uniform_(self.scoring_fn_target)
        nn.init.xavier_uniform_(self.scoring_fn_source)

        if self.bias is not None:
            nn.init.zeros_(self.bias)
        
    # TODO: understand this; seems mostly related to handling feature dimensions 
    def skip_concat_bias(self, attention_coefficients, in_nodes_features, out_nodes_features):
        if self.log_attention_weights:  # potentially log for later visualization in playground.py
            self.attention_weights = attention_coefficients

        # if the tensor is not contiguously stored in memory we'll get an error after we try to do certain ops like view
        # only imp1 will enter this one
        if not out_nodes_features.is_contiguous():
            out_nodes_features = out_nodes_features.contiguous()

        if self.add_skip_connection:  # add skip or residual connection
            if out_nodes_features.shape[-1] == in_nodes_features.shape[-1]:  # if FIN == FOUT
                # unsqueeze does this: (N, FIN) -> (N, 1, FIN), out features are (N, NH, FOUT) so 1 gets broadcast to NH
                # thus we're basically copying input vectors NH times and adding to processed vectors
                out_nodes_features += in_nodes_features.unsqueeze(1)
            else:
                # FIN != FOUT so we need to project input feature vectors into dimension that can be added to output
                # feature vectors. skip_proj adds lots of additional capacity which may cause overfitting.
                out_nodes_features += self.skip_proj(in_nodes_features).view(-1, self.num_of_heads, self.num_out_features)

        if self.concat:
            # shape = (N, NH, FOUT) -> (N, NH*FOUT)
            out_nodes_features = out_nodes_features.view(-1, self.num_of_heads * self.num_out_features)
        else:
            # shape = (N, NH, FOUT) -> (N, FOUT)
            out_nodes_features = out_nodes_features.mean(dim=self.head_dim)

        if self.bias is not None:
            out_nodes_features += self.bias

        return out_nodes_features if self.activation is None else self.activation(out_nodes_features)


class GATLayer2(GATLayer):

    def __init__(self, num_in_features, num_out_features, num_of_heads, concat=True, activation=nn.ELU(), dropout_prob=0.6, add_skip_connection=True, bias=True, log_attention_weights=False):

        super().__init__(num_in_features, num_out_features, num_of_heads, LayerType.IMP2, concat, activation, dropout_prob, add_skip_connection, bias, log_attention_weights)

    def forward(self, data):
        pass
