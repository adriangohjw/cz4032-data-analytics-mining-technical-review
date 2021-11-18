from data_processor import load_dataset
import ranked_retrieval

def func(query, data_source, delimiter=","):
  df = load_dataset(data_source, delimiter)
  result = ranked_retrieval.RankedRetrieval(query, df, 'description').call()
  #print(result)
  
data_sources = [
  'data/mcf_data_500.csv',
  'data/mcf_data_1000.csv',
  'data/mcf_data_2000.csv',
  'data/mcf_data_3000.csv',
  'data/mcf_data_4000.csv',
  'data/mcf_data_5000.csv',
  'data/mcf_data_10000.csv'
]

for data_source in data_sources:
  query = 'java javascript react'
  func(query, data_source)
  print()
