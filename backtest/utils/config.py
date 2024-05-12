"""
@File         : config.py
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2024-05-11 11:45:26
@Email        : cuixuanstephen@gmail.com
@Description  : 
"""

from configparser import ConfigParser


class TAConfig:
    def __init__(self, config_file) -> None:
        self.parser = ConfigParser()
        self.parser.read(config_file, encoding="utf-8")

    def get_params(self, section, option):
        return self.parser.get(section, option)
