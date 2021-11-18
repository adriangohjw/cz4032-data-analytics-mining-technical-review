import pandas as pd
import requests
import re

class SaveMyCareersFutureDataJob:
  def __init__(self, size):
    self.size = size
    self.limit = 100

    
  def call(self):
    results = []
    for i in range(0, int(self.size / self.limit)):
      print(i)
      results.extend(self.__get_mcf_data('', i))
      if len(results) >= self.size:
        break

    results = results[0:self.size]
      
    df = pd.DataFrame(results, columns=['uuid', 'title', 'description'])
        
    self.__save_to_csv(df, 'mcf_data_{data_size}.csv'.format(data_size=self.size))

  
  def __get_mcf_data(self, search_term, page):
    url = 'https://api.mycareersfuture.gov.sg/v2/jobs'
    params = dict(
      search=search_term,
      page=page,
      limit=self.limit
    )
    
    resp = requests.get(url=url, params=params)
    results = resp.json()['results']
    
    row_list = []
    for result in results:
      row_list.append(
        [
          result['uuid'],
          result['title'],
          self.__sanitize_text(result['description'])
        ]
      )
      
    return row_list

      
  def __save_to_csv(self, df, file_name):
    df.to_csv(file_name, index=False)
  
  
  def __sanitize_text(self, text):
    CLEANER = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    text_without_html_tags = re.sub(CLEANER, '', text)
    return text_without_html_tags.replace("\n", "").strip()
