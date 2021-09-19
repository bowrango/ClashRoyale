import torch
import torch.nn as nn

from utils.constants import LayerType

class GATLayer(nn.Module):
    """
    Base class for all inheriting GAT implementations 
    """
    def __init__(self, num_in_features, num_out_features, num_of_heads, layer_type, concat=True, activation=nn.ELU(), dropout_prob=0.6, add_skip_connection=True, bias=True, log_attention_weights=False):

        super().__init__()

        # save for forward propagation in children layers (imp1/2/3)
        self.num_of_heads = num_of_heads
        self.num_out_features = num_out_features
        self.concat = concat  # whether we should concatenate or average the attention heads
        self.add_skip_connection = add_skip_connection

        # Trainable Weights:
        #   - linear projection matrix; denoted as "W"
        #   - attention target/source; denoted as "a"
        #   - bias; not in paper

        if layer_type == LayerType.IMP1:            
            self.proj_param = nn.Parameter(torch.Tensor(num_of_heads, num_of_heads*num_out_features, bias=False))
        else:
            self.linear_proj = nn.Linear(num_in_features, num_of_heads*num_out_features, bias=False)


class GATLayer2(GATLayer):

    def __init__(self, num_in_features, num_out_features, num_of_heads, concat=True, activation=nn.ELU(), dropout_prob=0.6, add_skip_connection=True, bias=True, log_attention_weights=False):

        super().__init__(num_in_features, num_out_features, num_of_heads, LayerType.IMP2, concat, activation, dropout_prob, add_skip_connection, bias, log_attention_weights)

    def forward(self, data):
        pass
