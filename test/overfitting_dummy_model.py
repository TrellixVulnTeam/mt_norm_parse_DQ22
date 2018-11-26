from model.seq2seq import LexNormalizer, Generator
import torch.nn as nn
import os
import torch
from training.train import run_epoch
from io_.data_iterator import data_gen_dummy
from model.loss import LossCompute
import matplotlib.pyplot as plt
from tracking.plot_loss import simple_plot
from tqdm import tqdm
from io_.info_print import disable_tqdm_level

# hyperparameters
V = 5
lr = 0.001
model = LexNormalizer(generator=Generator, char_embedding_dim=5, hidden_size_encoder=11, voc_size=9, hidden_size_decoder=11, verbose=0)
# optimizer
adam = torch.optim.Adam(model.parameters(), lr=lr, betas=(0.9, 0.98), eps=1e-9)

verbose = 0
# reporting
training_loss = []
nbatches = 50
EPOCHS = 100
seq_len = 10
generalize_extra = 5
if __name__ == "__main__":

    for epoch in tqdm(range(EPOCHS),disable_tqdm_level(verbose=verbose, verbose_level=0)):
        model.train()
        run_epoch(data_gen_dummy(V=V, batch=2, nbatches=nbatches, seq_len=seq_len, verbose=verbose),
                  model, LossCompute(model.generator, opt=adam, verbose=verbose), verbose=verbose, i_epoch=epoch, n_epochs=EPOCHS, n_batches=nbatches)
        model.eval()
        loss = run_epoch(data_gen_dummy(V, batch=2, nbatches=10, seq_len=seq_len+generalize_extra), model, LossCompute(model.generator))
        training_loss.append(loss)
        if verbose >= 1:
            print("Final Loss {} ".format(loss))


    simple_plot(final_loss=loss, loss_ls=training_loss, save=True,show=True,epochs=EPOCHS, seq_len=seq_len, V=V,
                lr=lr, prefix="**test-dummy-fake_data.png")
