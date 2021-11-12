import math  

class QueryProcessor:
  def call(self, query, document_df_dict):
    result = {}

    for word in query.split():
      if word not in result:
        result[word] = 0 
      result[word] += 1
    
    return self.__get_normalized_scoring(result, document_df_dict)
  

  def __get_normalized_scoring(self, tf_dict, document_df_dict):
    result = {}

    for key, value in tf_dict.items():
      tf_log = 1 + math.log(value, 10)
      tf_idf = tf_log * self.__get_idf_from_document_df_dict_by_key(key, document_df_dict)
      result[key] = {
        'tf': value,
        'tf_log': tf_log,
        'tf_idf': tf_idf
      }

    return self.__normalize_scoring(result)

  
  def __get_idf_from_document_df_dict_by_key(self, key, document_df_dict):
    key_match = document_df_dict.get(key)
    return key_match['idf'] if key_match is not None else 0


  def __normalize_scoring(self, scoring_dict):
    sum_of_tf_idf_squared = 0
    for _, value in scoring_dict.items():
      sum_of_tf_idf_squared += value['tf_idf'] ** 2
    normalization_factor = 1 / math.sqrt(sum_of_tf_idf_squared)
    
    for key, value in scoring_dict.items():
      scoring_dict[key]['norm'] = value['tf_idf'] * normalization_factor
  
    return scoring_dict


class DocumentProcessor:
  def call(self, cleaned_query, cleaned_text):
    cleaned_text_list = cleaned_text.split()
    
    result = {}
    for term in self.__unique_terms(cleaned_query):
      result[term] = cleaned_text_list.count(term)
    
    return self.__get_normalized_scoring(result)


  def __unique_terms(self, query):
    return list(set(query.split()))

  
  def __get_normalized_scoring(self, tf_dict):
    result = {}
    for key, value in tf_dict.items():
      tf_log = 0 if value == 0 else 1 + math.log(value, 10)
      result[key] = {
        'tf': value,
        'tf_log': tf_log,
        'tf_idf': tf_log * 1
      }
      
    return self.__normalize_scoring(result)
  
  
  def __normalize_scoring(self, scoring_dict):
    sum_of_tf_idf_squared = 0
    for _, value in scoring_dict.items():
      sum_of_tf_idf_squared += value['tf_idf'] ** 2
    normalization_factor = 1 / math.sqrt(sum_of_tf_idf_squared) if sum_of_tf_idf_squared != 0 else 0
    
    for key, value in scoring_dict.items():
      scoring_dict[key]['norm'] = value['tf_idf'] * normalization_factor
  
    return scoring_dict
