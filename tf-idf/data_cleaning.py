from gensim.parsing.preprocessing import remove_stopwords
import re

class DocumentsCleaner:
  def call(self, df, colname):
    cleaned_colname = colname + "_cleaned"
    df = self.duplicate_col(df, colname)
    df = self.remove_stop_words_from_df(df, cleaned_colname)
    df = self.remove_special_chars_from_df(df, cleaned_colname)
    df = self.trim_df_colname(df, cleaned_colname)
    df = self.lowercase_df_colname(df, cleaned_colname)
    return df

  def duplicate_col(self, df, colname):
    df[colname + "_cleaned"] = df[colname]
    return df

  def remove_stop_words_from_df(self, df, colname):
    df[colname] = df[colname].apply(lambda x: remove_stopwords(x))
    return df

  def remove_special_chars_from_df(self, df, colname):
    df[colname] = df[colname].apply(lambda x: re.sub('[^a-zA-Z0-9 \n\.]', ' ', x))
    return df

  def trim_df_colname(self, df, colname):
    df[colname] = df[colname].apply(lambda x: ' '.join(x.split()))
    return df

  def lowercase_df_colname(self, df, colname):
    df[colname] = df[colname].apply(lambda x: x.lower())
    return df
