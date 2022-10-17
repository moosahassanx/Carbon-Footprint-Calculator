# deal with tensors
import torch   
import torch.nn as nn

from sklearn.metrics import accuracy_score

# handling text data
from torchtext.legacy import data

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import time

# import data
test_ds, train_ds, validate_ds = pd.read_json("ready-dataset.json", lines=True)

print(train_ds)