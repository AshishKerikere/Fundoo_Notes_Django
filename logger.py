import logging
def set_logger():
    logging.basicConfig(filename='fundoo_notes.log', encoding='utf-8',level=logging.DEBUG,
                        format='%(asctime)s:%(filename)s:%(levelname)s:%(lineno)d:%(message)s')
    logger = logging.getLogger()
    return logger