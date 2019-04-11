from env.importing import *
from io_.info_print import printing


class Generator(nn.Module):
    """
    Given the model prediction hidden representation predict a distribution over character vocabulary
    """
    def __init__(self, hidden_size_decoder, output_dim,
                 voc_size, verbose=0, activation=None):
        super(Generator, self).__init__()
        self.dense = nn.Linear(hidden_size_decoder, output_dim)
        self.proj = nn.Linear(output_dim, voc_size)
        self.activation = "nn.ReLU" if activation is None or activation == str(None) else activation
        self.verbose = verbose
    # TODO : check if relu is needed or not

    def forward(self, x):
        # return F.log_softmax(self.proj(x), dim=-1)
        # the log_softmax is done within the loss
        activation = eval(self.activation)
        y = activation()(self.dense(x))
        proj = self.proj(y)
        printing("TYPE  proj {} is cuda ", var=(proj.is_cuda), verbose=0, verbose_level=4)
        if self.verbose >= 3:
            print("PROJECTION {} size".format(proj.size()))
        if self.verbose >= 5:
            print("PROJECTION data {} ".format(proj))
        return proj