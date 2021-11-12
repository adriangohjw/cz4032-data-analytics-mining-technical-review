import pandas as pd

def load_dataset(filename, delimiter):
  return pd.read_csv(filename, index_col=False, delimiter=delimiter)
