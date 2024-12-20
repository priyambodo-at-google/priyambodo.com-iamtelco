import logging
import os

import yaml

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def load_config_file(config_file='config.yml'):
    """
   :param config_file: The path and name to our configuration YAML.
   :return: Config dictionary for other functions and methods to use.
   """
    logger.info("Loading config %s", config_file)

    try:
        with open(config_file) as config_str:
            if config_file.endswith('.tmpl'):
                import jinja2
                template = jinja2.Template(config_str.read())
                config = yaml.load(template.render(env=os.environ), Loader=yaml.Loader)
            else:
                config = yaml.load(config_str, Loader=yaml.Loader)
    except (IOError, FileNotFoundError):
        logger.exception("Failed to open config file %s", config_file)
    else:
        return config

#@cache
def get_config():
    config = os.getenv('CONFIG_FILE', 'config.yml')
    return load_config_file(config)

if __name__ == '__main__':
    config = get_config()