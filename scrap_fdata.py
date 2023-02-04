from fastapi import FastAPI
import requests
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True, index=True)
    created_time = Column(String)
    message = Column(String)
   


app = FastAPI()

url = "https://graph.facebook.com/v16.0/334721190331469?fields=posts&access_token=EAAI0AMDTyRABAChBpmlFRsMTp3sbiZBXjPepH7aEYTUrdTU3g1MqoGrY0kJe2yLnhHGeSGrm97LVshszRHRK6wsyBYwSVAUv2HwRO0gftjVZCzVknhZB80kWMZBmU95xjzz4JdNeqyWwm4rZCLuZC2eOnm1Qx5GgDT8qQyZCofuxocPbqOnMKzIP7ecMlH0jAdPwiEqgI6G7eaMoZAFgp8pQ"
db_url = 'mysql+pymysql://{}@{}:3306/{}'.format(
    os.getenv('MYSQL_USER', 'root'),
    #os.getenv('MYSQL_PASSWORD', 'root'),
    os.getenv('MYSQL_HOST', 'db'),
    os.getenv('MYSQL_DATABASE', 'scrap_fdata')
)

engine = create_engine(db_url)
meta = MetaData() 
#Base.metadata.create_all(engine)  

#con = engine.connect()
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
session = Session()

@app.get("/")
def scrap_facebook_data():
  response = requests.get(url).json()
  
  for i in response["posts"]["data"]:
      try:
          message = " "
          if len(i)==3 :
              try:
                  message = i["message"]
              except:
                  message = i["story"]
           
          post_data = Post(id = i["id"], 
          created_time = i["created_time"], 
          message = message
            )
          session.add(post_data)
          session.commit()
          
      except:
          #data already found  in db  
          print(message)
          break  
      
  return {"posts": response["posts"]["data"]}
        
