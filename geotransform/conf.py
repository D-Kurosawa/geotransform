"""Load application configure file"""
import json
import sys
from abc import ABCMeta
from abc import abstractmethod
from pathlib import Path

import numpy as np


class ConfigLoader:
    """
    :type setting: AppSettings
    :type loads: AppLoadings
    :type saves: AppSavings
    """

    def __init__(self):
        conf = JsonCmdLineArg.load()
        self.setting = AppSettings(conf['set'])
        self.loads = AppLoadings(conf['load'])
        self.saves = AppSavings(conf['save'])

    def load(self):
        self.setting.set()
        self.loads.set()
        self.saves.set()

    def walk(self):
        for key, val in self._walk_generator(self.__dict__):
            print(f"{key:<40}: {val}")

    def _walk_generator(self, dic):
        """
        :type dic: dict
        """
        for key, val in dic.items():
            yield key, val
            try:
                nest_value = val.__dict__  # type: dict
            except AttributeError:
                pass
            else:
                for child_key, child_val in self._walk_generator(nest_value):
                    yield key + ' -> ' + child_key, child_val


class _ConfMeta(metaclass=ABCMeta):
    """
    :type _dic: dict
    """

    def __init__(self, dic=None):
        """
        :type dic: dict | None
        """
        if dic is not None:
            self._dic = dic

    @abstractmethod
    def set(self):
        pass


class AppSettings(_ConfMeta):
    """
    :type from_epsg: int
    :type to_epsg: int
    """

    def __init__(self, dic):
        """
        :type dic: dict
        """
        super().__init__(dic)
        self.from_epsg = int()
        self.to_epsg = int()

    def set(self):
        self.from_epsg = self._dic['epsg']['from']
        self.to_epsg = self._dic['epsg']['to']


class AppLoadings(_ConfMeta):
    """
    :type coordinates: list[tuple[np.ndarray[np.float]]]
    """

    def __init__(self, dic):
        """
        :type dic: dict
        """
        super().__init__(dic)
        self.coordinates = []

    def set(self):
        for coord in self._dic['coordinates']:
            self.coordinates.append(LoadCoordinateInfo(coord).set())


class LoadCoordinateInfo(_ConfMeta):

    def set(self):
        lng = np.array(self._dic['lng'])
        lat = np.array(self._dic['lat'])

        if len(lng) != len(lat):
            raise IndexError

        return lng, lat


class AppSavings(_ConfMeta):
    """
    :type basename: Path
    """

    def __init__(self, dic):
        """
        :type dic: dict
        """
        super().__init__(dic)
        self.basename = Path()

    def set(self):
        self.basename = FileMaker.base(self._dic['transform'])


class JsonCmdLineArg:

    @staticmethod
    def _get_cmd_line_arg():
        """
        :rtype: str
        """
        try:
            arg = sys.argv[1]
        except IndexError:
            raise IndexError('Not found command line arguments')
        except Exception:
            raise Exception
        return arg

    @classmethod
    def load(cls):
        """
        :rtype: dict
        """
        with open(cls._get_cmd_line_arg(), 'r', encoding='utf-8') as j:
            return json.load(j)


class FileMaker:

    @staticmethod
    def _has_key(dic, *args):
        """
        :type dic: dict
        """
        for arg in args:
            if arg not in dic:
                raise KeyError(f"Not in key : {arg}")

    @staticmethod
    def _exists_path(path):
        """
        :type path: str
        :rtype: Path
        """
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(path)

        return p

    @classmethod
    def load(cls, dic):
        """
        :type dic: dict
        :rtype: Path
        """
        cls._has_key(dic, 'path', 'file')

        p = cls._exists_path(dic['path'])
        file = p / dic['file']

        if not file.exists():
            raise FileNotFoundError(dic['file'])

        return file

    @classmethod
    def find(cls, dic):
        """
        :type dic: dict
        :rtype: list[Path]
        """
        cls._has_key(dic, 'path', 'pattern')

        p = cls._exists_path(dic['path'])
        files = [f for f in p.glob(f"**/{dic['pattern']}")]

        if not files:
            raise FileNotFoundError(files)

        return files

    @classmethod
    def save(cls, dic):
        """
        :type dic: dict
        :rtype: Path
        """
        cls._has_key(dic, 'path', 'file')

        p = cls._exists_path(dic['path'])
        return p / dic['file']

    @classmethod
    def base(cls, dic):
        """
        :type dic: dict
        :rtype: Path
        """
        cls._has_key(dic, 'path', 'base_name')

        p = cls._exists_path(dic['path'])
        return p / dic['base_name']


if __name__ == '__main__':
    def _main():
        conf = ConfigLoader()
        conf.load()
        conf.walk()


    _main()
