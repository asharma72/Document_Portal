
# import logging
# import os
# from datetime import datetime

# class CustomLogger:
#     def __init__(self, log_dir ="logs"):
#         self.log_dir = os.path.join(os.getcwd(), log_dir)
#         os.makedirs(self.log_dir, exist_ok=True)

#         log_file = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
#         log_file_path = os.path.join(self.log_dir, log_file) 

#         logging.basicConfig(
#         filename=log_file_path,
#         format="[%(asctime)s] %(levelname)s %(name)s (line : %(lineno)d) - %(message)s",
#         level=logging.INFO
# )
        
#     def get_logger(self, name =__file__):
#         return logging.getLogger(os.path.basename(name))
    
# if __name__ == "__main__":
#     logger = CustomLogger()
#     logger = logger.get_logger(__file__)
#     logger.info("This is a custom logger message.")



import logging
import os
from datetime import datetime
import structlog 

class CustomLogger:
    def __init__(self, log_dir ="logs"):
        self.log_dir = os.path.join(os.getcwd(), log_dir)
        os.makedirs(self.log_dir, exist_ok=True)

        log_file = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        self.log_file_path = os.path.join(self.log_dir, log_file) 
       
        
    def get_logger(self, name =__file__):
        logger_name =  os.path.basename(name)

        #configure logging for console and file (both JSON)
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter("%(message)s")) #Raw JSON file format

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter("%(message)s")) #Raw JSON file format

        
        logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[console_handler, file_handler]
        )

        # configure structlog for JSON structured logging
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso",utc=True,key="timestamp"),
                structlog.processors.add_log_level,
                structlog.processors.EventRenamer("event"),
                structlog.processors.JSONRenderer()
            ],

            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True
        )

        return structlog.get_logger(logger_name)
        
        
# --- Usage Example ---
if __name__ == "__main__":
    logger = CustomLogger().get_logger(__file__)
    logger.info("User uploaded a file", user_id=123, filename="report.pdf")
    logger.error("Failed to process PDF", error="File not found", user_id=123)