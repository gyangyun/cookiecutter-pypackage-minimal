import logging
import argparse
{% if cookiecutter.use_config == 'y' %}
from {{ cookiecutter.package_name }} import config
import os.path
{% endif %}
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

args = None

def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--log_file',
                        metavar='LOG_FILE',
                        default='',
                        help='log file')
    parser.add_argument('-l', '--log_level',
                        metavar='LOG_LEVEL',
                        default='info',
                        help='log level')
    {% if cookiecutter.use_config == 'y' %}
    parser.add_argument('-c', '--config_file',
                        metavar='CONFIG_FILE',
                        default='config.json',
                        help='config file')
    {% endif %}
    global args
    args = parser.parse_args()

{% if cookiecutter.use_config == 'y' %}
def init_config():
    cfg_file = args.config_file
    _, ext = os.path.splitext(cfg_file)
    if ext == '.json':
        cfg = config.Config.from_json(cfg_file)
    elif ext == '.py':
        cfg = config.Config.from_pyfile(cfg_file)
    else:
        raise Exception('还未实现该配置文件格式的读取方法')
    cfg.from_mapping(args._get_kwargs())
    config.cfg = cfg

def init_logger():
    cfg = config.cfg
    log_level_str = cfg.get('log_level')
    log_file_str = cfg.get('log_file')
    log_level = logging.INFO
    log_format = '%(asctime)s %(levelname)s %(message)s'
    if log_level_str == 'debug':
        log_level = logging.DEBUG
        log_format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    elif log_level_str == 'info':
        log_level = logging.INFO
    elif log_level_str == 'warning':
        log_level = logging.WARNING
    elif log_level_str == 'error':
        log_level = logging.ERROR
    elif log_level_str == 'critical':
        log_level = logging.CRITICAL

    if log_file_str:
        logging.basicConfig(level=log_level,
                            format=log_format,
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename=log_file_str,
                            filemode='a',
                            )
    else:
        logging.basicConfig(level=log_level,
                            format=log_format,
                            datefmt='%a, %d %b %Y %H:%M:%S'
                            )
{% else %}
def init_logger():
    log_level_str = args.log_level
    log_file_str = args.log_file
    log_level = logging.INFO
    log_format = '%(asctime)s %(levelname)s %(message)s'
    if log_level_str == 'debug':
        log_level = logging.DEBUG
        log_format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    elif log_level_str == 'info':
        log_level = logging.INFO
    elif log_level_str == 'warning':
        log_level = logging.WARNING
    elif log_level_str == 'error':
        log_level = logging.ERROR
    elif log_level_str == 'critical':
        log_level = logging.CRITICAL

    if log_file_str:
        logging.basicConfig(level=log_level,
                            format=log_format,
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename= args.log_file,
                            filemode='a',
                            )
    else:
        logging.basicConfig(level=log_level,
                            format=log_format,
                            datefmt='%a, %d %b %Y %H:%M:%S'
                            )
{% endif %}

def main():
    init_argparse()
    {% if cookiecutter.use_config == 'y' %}
    init_config()
    init_logger()
    {% else %}
    init_logger()
    {% endif %}

if __name__ == '__main__':
    main()
