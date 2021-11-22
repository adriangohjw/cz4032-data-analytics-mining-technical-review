class DF:
  def __init__(self, df):
    self.df = df

  def get_df_memory_size_in_bytes(self):
    return self.df.memory_usage(deep=True).sum()


class Dictionary:
  def __init__(self, dict):
    self.dict = dict

  def get_df_memory_size_in_bytes(self):
    import sys
    return sys.getsizeof(self.dict)
