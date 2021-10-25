import logging
# set up a root logger before importing any of our code. 


logger = logging.getLogger('root')
logger.setLevel(logging.INFO)

# create a handler and set level to info
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)