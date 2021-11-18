def get_df_memory_size_in_bytes(df):
  return df.memory_usage(deep=True).sum()
