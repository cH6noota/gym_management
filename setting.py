# coding: UTF-8
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

API_KEY = os.environ.get("API_KEY") 
Authorization = os.environ.get("Authorization")

HOST = os.environ.get("HOST")
USER = os.environ.get("USER")
PASS = os.environ.get("PASS")
DBNAME = os.environ.get("DBNAME")
