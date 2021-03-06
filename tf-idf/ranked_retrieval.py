import data_cleaning
import df_generator
import score_calculator
import time
import performance_analyzer

class RankedRetrieval:
  def __init__(self, query, documents, colname):
    self.query = query
    self.documents = documents
    self.colname = colname
    self.original_documents_size = performance_analyzer.DF(documents).get_df_memory_size_in_bytes()
    
    overall_start = time.process_time()
  
    start = time.process_time()
    self.cleaned_query = data_cleaning.QueryCleaner().call(self.query)
    print(">>>>> Time to clean query: " + str(time.process_time() - start) + "secs")
    
    start = time.process_time()
    self.cleaned_documents = data_cleaning.DocumentsCleaner().call(documents, colname)
    print(">>>>> Time to clean document: " + str(time.process_time() - start) + "secs")
  
    start = time.process_time()
    self.document_df_dict = df_generator.DocumentProcessor().call(self.cleaned_documents, self.colname + '_cleaned')    
    self.query_tf_dict = score_calculator.QueryProcessor().call(self.cleaned_query, self.document_df_dict)
    print(">>>>> Time to generate (individual normalized tf and df): " + str(time.process_time() - start) + "secs")
    
    start = time.process_time()
    self.__calculate_score_for_all_documents()
    self.__ranked_documents()
    print(">>>>> Time to compute score for each documents: " + str(time.process_time() - start) + "secs")
    
    overall_end = time.process_time() - overall_start
    print(">>>>> Total time (sum): " + str(overall_end) + "secs")
    
    df_processed_size = performance_analyzer.DF(self.cleaned_documents).get_df_memory_size_in_bytes()
    total_memory = self.__total_additional_memory_used(df_processed_size - self.original_documents_size)
    print(">>>>> Additional memory (MB): " + str(total_memory / 1000000) + "MB")
  

  def call(self):
    return self.cleaned_documents
  
  
  def __calculate_score_for_all_documents(self):    
    for i, row in self.cleaned_documents.iterrows():
      self.cleaned_documents.at[i, 'score'] = self.__calculate_document_matching_score(row)
  
    
  def __calculate_document_matching_score(self, document):
    document_score = score_calculator.DocumentProcessor().call(
      self.cleaned_query,
      document[self.colname + '_cleaned']
    )

    total_matching_score = 0
    for key, value in self.query_tf_dict.items():
      total_matching_score += value['norm'] * document_score.get(key)['norm']
      
    return total_matching_score
    
    
  def __ranked_documents(self):
    self.cleaned_documents = self.cleaned_documents.sort_values(by='score', ascending=False)
    
    
  def __total_additional_memory_used(self, additional_memory_in_bytes):
    return \
      performance_analyzer.OneNestedDictionary(self.document_df_dict).get_df_memory_size_in_bytes() + \
      performance_analyzer.OneNestedDictionary(self.query_tf_dict).get_df_memory_size_in_bytes() + \
      additional_memory_in_bytes
