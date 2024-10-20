import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_debug(fn):
    def wrapper(*args, **kwargs):
        logging.debug(f"Enter to function {fn.__name__}")
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            logging.error(f"Function {fn.__name__} failed with error: {e}")
            raise
        finally:
            logging.debug(f"Exit from function {fn.__name__}")

    return wrapper
