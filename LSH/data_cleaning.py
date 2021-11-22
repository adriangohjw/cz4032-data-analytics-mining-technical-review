from gensim.parsing.preprocessing import remove_stopwords
import re

class DocumentsCleaner:
  def call(self, df, colname):
    cleaned_colname = colname + "_cleaned"
    df = self.duplicate_col(df, colname)
    df = self.remove_stop_words(df, cleaned_colname)
    df = self.remove_special_chars(df, cleaned_colname)
    df = self.lowercase(df, cleaned_colname)
    return df

  def duplicate_col(self, df, colname):
    df[colname + "_cleaned"] = df[colname]
    return df

  def remove_stop_words(self, df, colname):
    df[colname] = df[colname].apply(lambda x: remove_stopwords(x))
    return df

  def remove_special_chars(self, df, colname):
    df[colname] = df[colname].apply(lambda x: re.sub('[^A-Za-z0-9]+', ' ', x))
    return df

  def lowercase(self, df, colname):
    df[colname] = df[colname].apply(lambda x: x.lower())
    return df
