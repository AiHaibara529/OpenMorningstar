# https://www.cnblogs.com/yyds/p/6901864.html
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
# NOTE: 一个一次性的简单配置工具使，也就是说只有在第一次调用该函数时会起作用，后续再次调用该函数时完全不会产生任何操作的，多次调用的设置并不是累加操作。
logging.basicConfig(filename='my.log', level=logging.DEBUG,
                    format=LOG_FORMAT, datefmt=DATE_FORMAT)

logging.debug("This is a debug log.")
logging.info("This is a info log.")
# exec_info: 异常信息是否添加
logging.warning("Some one delete the log file.", exc_info=True,
                stack_info=True, extra={'user': 'Tom', 'ip': '47.98.53.222'})
logging.error("This is a error log.")
logging.critical("This is a critical log.")
