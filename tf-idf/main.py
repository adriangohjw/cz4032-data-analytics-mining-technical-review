from data_processor import load_dataset
import ranked_retrieval

DATA_SOURCE = 'data/mcf_data.csv'
DELIMITER = ','

df = load_dataset(DATA_SOURCE, DELIMITER)
query = 'java javascript react'
results = ranked_retrieval.RankedRetrieval(query, df, 'description').call()
print(results)
