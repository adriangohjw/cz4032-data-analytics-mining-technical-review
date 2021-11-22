import sys

class DF:
  def __init__(self, df):
    self.df = df

  def get_df_memory_size_in_bytes(self):
    return self.df.memory_usage(deep=True).sum()


class OneNestedDictionary:
  def __init__(self, dict):
    self.dict = dict

  def get_df_memory_size_in_bytes(self):
    return sys.getsizeof(self.dict.keys()) + \
      sum(NonNestedDictionary(v).get_df_memory_size_in_bytes() for v in self.dict.values())
  

class NonNestedDictionary:
  def __init__(self, dict):
    self.dict = dict
  
  def get_df_memory_size_in_bytes(self):
    return sys.getsizeof(self.dict.keys()) + sys.getsizeof(self.dict.values())
