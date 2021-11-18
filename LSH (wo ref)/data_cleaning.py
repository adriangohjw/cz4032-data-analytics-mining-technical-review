from gensim.parsing.preprocessing import remove_stopwords
import re

class QueryCleaner:
  def call(self, query):
    new_query = query
    new_query = self.remove_stop_words(new_query)
    new_query = self.remove_special_chars(new_query)
    new_query = self.trim(new_query)
    new_query = self.lowercase(new_query)
    return new_query
  
  def remove_stop_words(self, query):
    return remove_stopwords(query)
  
  def remove_special_chars(self, query):
    return re.sub('[^a-zA-Z0-9 \n\.]', ' ', query)
  
  def trim(self, query):
    return ' '.join(query.split())
  
  def lowercase(self, query):
    return query.lower()


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
    df[colname] = df[colname].apply(lambda x: re.sub('[^a-zA-Z0-9 \n\.]', ' ', x))
    return df

  # def trim(self, df, colname):
  #   df[colname] = df[colname].apply(lambda x: ' '.join(x.split()))
  #   return df

  def lowercase(self, df, colname):
    df[colname] = df[colname].apply(lambda x: x.lower())
    return df
