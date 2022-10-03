# coding: utf-8

"""VITY Logging
    Handles logging output for Py processes
    @see https://docs.python.org/3/library/logging.html
    @see https://docs.python.org/3/howto/logging.html
"""
import logging

logging.basicConfig(
    filename='../error-logs/prediction.log',
    filemode='a',
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

logging.captureWarnings(True)
# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.CRITICAL)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)-12s %(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)
