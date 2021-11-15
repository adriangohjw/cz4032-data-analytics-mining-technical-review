import data_cleaning
import df_generator
import score_calculator

class RankedRetrieval:
  def __init__(self, query, documents, colname):
    self.query = query
    self.documents = documents
    self.colname = colname
    self.cleaned_query = data_cleaning.QueryCleaner().call(self.query)
    self.cleaned_documents = data_cleaning.DocumentsCleaner().call(documents, colname)
    self.document_df_dict = df_generator.DocumentProcessor().call(self.cleaned_documents, self.colname + '_cleaned')
    self.query_tf_dict = score_calculator.QueryProcessor().call(self.cleaned_query, self.document_df_dict)
    self.__calculate_score_for_all_documents()
    self.__ranked_documents()
  

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
