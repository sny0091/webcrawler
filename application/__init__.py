from flask import Flask
import os
  
file_path = os.path.abspath(os.getcwd())+"/todo.db"
print(file_path)
app = Flask(__name__)
  
  
from app import routes