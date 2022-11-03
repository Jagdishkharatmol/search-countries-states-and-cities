import json
from urllib.request import urlopen
import pandas as pd
from sqlalchemy import create_engine



link_to_data='https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/countries%2Bstates%2Bcities.json'

class InsertDataInDatabase:
  def __init__(self,link,creds):
    self.link=link
    self.creds=creds

  def fetch_data(self):
    response = urlopen(self.link)
    db_data=json.loads(response.read())
    return db_data

  def insert_data(self):
    try: 
        engine = create_engine('mysql+pymysql://username:password@localhost/idea')
    except Exception as e:
          engine.dispose()
          print("Error",e)
          return 0
    
    print("Database connected !")
    
    try:
        db_data=InsertDataInDatabase.fetch_data(self)
        df_country_info = pd.DataFrame.from_dict(db_data)
        df_country_info = df_country_info.applymap(str)
        df_country_info.to_sql('country_info',if_exists='append',con=engine)
    except Exception as e:
          engine.dispose()
          print("Error",e)
          return 0
        
    print(f'Inserted records in database !')

    return 1



insert_data_obj=InsertDataInDatabase(link_to_data,creds)
insert_data_obj.insert_data()
