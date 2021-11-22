import math
import operator

class DocumentProcessor:
  def call(self, df, colname):
    temp_dict = self.__get_document_frequency(df, colname)
    sorted_temp_dict = self.__sort_dict_by_value(temp_dict)
    document_count = len(df.index)
    return self.__add_inverse_document_frequency_to_dict(sorted_temp_dict, document_count)
  
  
  def __get_document_frequency(self, df, colname):
    result = {}
    for record in df[colname]:
      for word in set(record):
        if word in result:
          result[word] += 1
        else:
          result[word] = 1
    
    return result
    

  def __sort_dict_by_value(self, my_dict):
    return dict(sorted(my_dict.items(), key=operator.itemgetter(1), reverse=True))


  def __add_inverse_document_frequency_to_dict(self, df_dict, document_count):
    result = {}
    for key, value in df_dict.items():
      result[key] = {
        'df': value,
        'idf': math.log(document_count / value, 10)
      }

    return result
