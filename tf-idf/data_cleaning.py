from gensim.parsing.preprocessing import remove_stopwords
import re

def clean_data(df, colname):
  cleaned_colname = colname + "_cleaned"
  df = duplicate_col(df, colname)
  df = remove_stop_words_from_df(df, cleaned_colname)
  df = remove_special_chars_from_df(df, cleaned_colname)
  df = trim_df_colname(df, cleaned_colname)
  df = lowercase_df_colname(df, cleaned_colname)
  return df

def duplicate_col(df, colname):
  df[colname + "_cleaned"] = df[colname]
  return df

def remove_stop_words_from_df(df, colname):
  df[colname] = df[colname].apply(lambda x: remove_stopwords(x))
  return df

def remove_special_chars_from_df(df, colname):
  df[colname] = df[colname].apply(lambda x: re.sub('[^a-zA-Z0-9 \n\.]', ' ', x))
  return df

def trim_df_colname(df, colname):
  df[colname] = df[colname].apply(lambda x: ' '.join(x.split()))
  return df

def lowercase_df_colname(df, colname):
  df[colname] = df[colname].apply(lambda x: x.lower())
  return df
