import logging
import os


def init_log():
    __file__ = "./model.log"
    log_file = os.path.realpath(__file__)

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=log_file,
                        filemode='a')


