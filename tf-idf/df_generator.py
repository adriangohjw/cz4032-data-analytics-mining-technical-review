import math
import operator

class DocumentProcessor:
  def call(self, df, colname):
    temp_dict = {}
    for cell in list(df[colname]):
      for word in cell.split():
        if word in temp_dict:
          temp_dict[word] += 1
        else:
          temp_dict[word] = 1

    sorted_temp_dict = self.sort_dict_by_value(temp_dict)
    document_count = len(df.index)
    return self.add_inverse_document_frequency_to_dict(sorted_temp_dict, document_count)
    

  def sort_dict_by_value(self, my_dict):
    return dict(sorted(my_dict.items(), key=operator.itemgetter(1),reverse=True))


  def add_inverse_document_frequency_to_dict(self, df_dict, document_count):
    result = {}
    for key, value in df_dict.items():
      result[key] = {
        'df': value,
        'idf': math.log(document_count / value, 10)
      }

    return result
