import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'justloveJesus'
    SQLALCHEMY_DATABASE_URI = 'postgres://tjckjhlcczudoz:c1f8b346c9c6089944b84c008dbde3d9de09ce92e090e97032e298af8f713f96@ec2-3-214-2-141.compute-1.amazonaws.com:5432/dbs6pkd91t2if7'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
     #                         'sqlite:///' + os.path.join(basedir, 'repairShop.db')