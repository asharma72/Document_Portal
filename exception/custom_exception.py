
import sys
import traceback

from logger.custom_logger import CustomLogger
logger =CustomLogger().get_logger(__file__)

class DocumentPortalException(Exception):
    def __init__(self,error_message=str, error_detail=sys):
        _,_,exb_tb = error_detail.exc_info()
        self.file_name = exb_tb.tb_frame.f_code.co_filename
        self.line_number = exb_tb.tb_lineno
        self.error_message = str(error_message)
        self.traceback_str = ''.join(traceback.format_exception(*error_detail.exc_info()))
        
    def __str__(self):
        return f"""
        Error occurred in file [{self.file_name}] at line [{self.line_number}]
        Error message: {self.error_message}
        Traceback: {self.traceback_str}
        """
if __name__ == "__main__":
    try:
        a = 1/0
        print(a)
    except Exception as e:
        app_exc = DocumentPortalException(e, sys)
        logger.error(app_exc)
        raise app_exc