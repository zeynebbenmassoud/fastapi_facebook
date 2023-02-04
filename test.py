from fastapi import FastAPI
import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True, index=True)
    created_time = Column(String)
    message = Column(String)
   

app = FastAPI()

url = "https://graph.facebook.com/v16.0/334721190331469?fields=posts&access_token=EAAI0AMDTyRABAA4JkdPtaIDWRhGFvZAeaOU1wBC2YDEANbQ1Pj4agZCtiiZAW2T5m7jC7seM0YOUOFfyHZBfd9FemZCs2XReDXDDZBZBNAMI2JZBaOBLhh79XZAIdxTIr3sAMZB4OzZB06lJ95ukwccQLRZAzewdf58EHobDDughiagqOB7ZB0InyGZCUh1XCndUYcsSxmIIwMmHRq3GVZAX31sfoZAJ"
db_url = 'sqlite:///./srap_fdata.sqlite3'

engine = create_engine(db_url)
Base.metadata.create_all(engine)  
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
        
