import math

class QueryProcessor:
  def call(self, query):
    result = {}

    for word in query.split():
      if word not in result:
        result[word] = 0 
      result[word] += 1
    
    return self.add_term_frequency_log_to_dict(result)
  

  def add_term_frequency_log_to_dict(self, tf_dict):
    result = {}
    for key, value in tf_dict.items():
      result[key] = {
        'tf': value,
        'tf-log': 1 + math.log(value)
      }
      
    return result
