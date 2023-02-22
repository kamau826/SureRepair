import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'justloveJesus'
    #SQLALCHEMY_DATABASE_URI = 'postgresql://vbrnxqyfjgsbgt:d617f660feb8cabba76189f942cc16b26c1a43814c13df1e9f3885c6d091c5ac@ec2-54-85-56-210.compute-1.amazonaws.com:5432/defm02tgd6cba6'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'repairShop.db')
