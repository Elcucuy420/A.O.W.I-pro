import logging, sys, os, json
from pythonjsonlogger import jsonlogger

class JsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        log_record['logger'] = record.name

def setup_logging():
    handler = logging.StreamHandler(sys.stdout)
    fmt = JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    handler.setFormatter(fmt)
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(os.getenv('LOG_LEVEL','INFO'))
