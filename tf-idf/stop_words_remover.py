from gensim.parsing.preprocessing import remove_stopwords

def remove_stop_words_from_df(df, colname):
  df[colname] = df[colname].apply(lambda x: remove_stopwords(x))
  return df
