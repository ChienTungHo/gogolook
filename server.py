import bottle
import logging
import time
import datetime
import sys
import transaction
from bottle import HTTPError, HTTPResponse
from bottle import request

# customize library
from setting import HostSetting
from module.codeGenerator import codeGenerator
from module.emailValidation import validateEmail
from sql.schema import *
  
app = bottle.Bottle()
app.install(plugin)

# set logging to log all information during the http request
logging.basicConfig(filename='error.log', format=logging.BASIC_FORMAT, level=logging.ERROR)
#logging.basicConfig(filename='warning.log', format=logging.BASIC_FORMAT, level=logging.)


''' 
Get email adress and generate redeem_code

Use http get method with following parameters:
  'email': 'xxx@gmail.com'
  'item_no': 1

'''
@app.get('/GenRedeem')
def GenRedeem(db):
  try:
    log_time = time.asctime( time.localtime(time.time()) )
   
    # Get parameters from client
    email = request.GET.get('email')
    item_no = request.GET.get('item_no')
    if email is None or item_no is None:
      logging.error('[Insufficient Parameters] %s %s - %s' % (email, item_no, log_time))
      return HTTPError(403, 'Insufficient request parameters.')

    if validateEmail(email) == 0:
      logging.error('[Invalid Email] %s %s - %s' % (email, item_no, log_time))
      return HTTPError(403, 'Invalid email address.')
      

    # Check the email is existed or not
    try:
      entity = db.query(Redeem).filter_by(owner_email=email).first()
      if entity:
        return HTTPResponse('%s already registered before!\n Your code here:%s' % (email, 
                                                                                   entity.redeem_code))
      else:
        # Generate redeem_code and add to Mysql
        with transaction.manager:
          # Generate the 'unique' redeem_code
          redeem_code = codeGenerator(8)
          while(db.query(Redeem).filter_by(redeem_code=redeem_code).first() != None):
            redeem_code = codeGenerator(8)
          entity = Redeem(email, redeem_code, item_no)
          db.add(entity)
        return HTTPResponse('%s registeres success! Your code here:%s' % (email, redeem_code))
      
    except:
      logging.error('[SQL Insert Error] %s - %s' % (sys.exc_info()[0], log_time))
      return HTTPError(599, 'Server is busy.')
      
  except:
    logging.error('[Server Error] %s - %s' % (sys.exc_info()[0], log_time))
    return HTTPError(599, 'Server is busy.')

'''
Receive redeem

Use http get method with following parameters:
  'receiver_email': 'xxx@gamil.com'
  'redeem_code': 'xxxxxxxx' (8 characters)
'''
@app.get('/RecRedeem')
def RecRedeem(db):
  try:
    log_time = time.asctime ( time.localtime(time.time()) )
    
    # Get parameters from client
    receiver_email = request.GET.get('receiver_email')
    redeem_code = request.GET.get('redeem_code')
    if receiver_email is None or redeem_code is None:
      logging.error('[Insufficient Parameters] %s %s - %s' % (receiver_email, redeem_code, log_time))
      return HTTPError(403, 'Insufficient request parameters.')
    
    if validateEmail(receiver_email) == 0:
      logging.error('[Invalid Email] %s %s - %s' % (receiver_email, redeem_code, log_time))
      return HTTPError(403, 'Invalid email address.')
    
    try:  
      # The system have to check four condictions
      # 1. Whether the user receive more than three redeem codes
      # 2. Validate the redeem code
      # 3. Can not send to myself
      # 4. Only can use one time
      with transaction.manager:
        # Whether the user receive more than three redeem code
        entityCount = db.query(Redeem).filter_by(receiver_email=receiver_email).count()
        if entityCount >= 3:
          logging.error('[Exceed Redeem Code Limitation] %s %s - %s' % (receiver_email, 
                                                                        redeem_code, 
                                                                        log_time))
          return HTTPError(403, 'Can not get more than three redeem codes.')
        else:
          # Validate the redeem code
          entity = db.query(Redeem).filter_by(redeem_code=redeem_code).first()
          if entity:
            # Can not send to myself
            if entity.owner_email == receiver_email:
              logging.error('[Send to Myself] %s - %s' % (receiver_email, log_time))
              return HTTPError(403, 'Can not send to yourself.')
            # Only can use one time
            elif entity.receiver_email is not None:
              logging.error('[Redeem Code Exceed Limitation] %s %s - %s' % (receiver_email, 
                                                                            redeem_code,
                                                                            log_time))
              return HTTPError(403, 'Redeem code is already used.')
            # Record the receive information
            else:
              entity.receiver_email = receiver_email
              entity.receive_ip = request.remote_addr
              entity.receive_time = datetime.datetime.utcnow()
              return HTTPResponse('Congraduation! Your item here:%s' % (entity.item_no))
          else:
            logging.error('[Invalid redeem code] %s %s %s - %s' % (receiver_email, 
                                                                  redeem_code, 
                                                                  request.remote_addr, 
                                                                  log_time))
            return HTTPError(403, 'Input the error code? %s' % (redeem_code))
    except:
      logging.error('[SQL Server Error] %s - %s' % (sys.exc_info()[0], log_time))
      return HTTPError(599, 'Server is busy.')
 
  except:
    logging.error('[Server Error] %s - %s' % (sys.exc_info()[0], log_time))
    return HTTPError(599, 'Server is busy.')

bottle.run(app, host=HostSetting.HostName, port=HostSetting.HostPort)
