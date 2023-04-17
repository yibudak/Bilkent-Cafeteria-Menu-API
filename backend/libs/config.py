# Copyright 2023 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import configparser


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class Config:
    def __init__(self, path):

        config = configparser.ConfigParser(interpolation=None)
        config.optionxform = str
        config.sections()
        config.read(path)

        # Database
        self.db = Struct(**dict(config["DB"]))
        self.app = Struct(**dict(config["APP"]))
