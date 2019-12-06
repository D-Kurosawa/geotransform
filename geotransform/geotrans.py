"""Geodetic transformation"""
import numpy as np
from pyproj import Proj
from pyproj import Transformer


class GeoTrans:
    """
    :type _from_epsg: int
    :type _to_epsg: int
    :type _transformer: Transformer
    """
    _EPSG_CODE = {
        4326: {'name': 'WGS84', 'type': 'GeodeticCRS', 'area': 'World'},
        4612: {'name': 'JGD2000', 'type': 'GeodeticCRS', 'area': 'Japan'},
        6668: {'name': 'JGD2011', 'type': 'GeodeticCRS', 'area': 'Japan'},
        4301: {'name': 'Tokyo', 'type': 'GeodeticCRS', 'area': 'Japan'}
    }

    def __init__(self, from_epsg=4301, to_epsg=6668):
        """
        :type from_epsg: int
        :type to_epsg: int
        :param from_epsg: EPSG code of conversion source
        :param to_epsg: EPSG code of destination
        """
        self._from_epsg = from_epsg
        self._to_epsg = to_epsg
        self._transformer = Transformer.from_proj(
            proj_from=Proj(f"epsg:{from_epsg}"),
            proj_to=Proj(f"epsg:{to_epsg}"),
            always_xy=True
        )

    def epsg_info(self):
        print(f"EPSG from: {self._from_epsg}"
              f"    Name: {self._get_epsg_name(self._from_epsg)}")
        print(f"EPSG to  : {self._to_epsg}"
              f"    Name: {self._get_epsg_name(self._to_epsg)}")

    @classmethod
    def _get_epsg_name(cls, code):
        """
        :type code: int
        :rtype str
        """
        if code in cls._EPSG_CODE:
            return cls._EPSG_CODE[code]['name']

        return f"Not expect in <class {cls.__name__}>"

    def transform(self, lng, lat):
        """
        :type lng: float | list[float] | np.ndarray[np.float]
        :type lat: float | list[float] | np.ndarray[np.float]
        :rtype tuple
        :return: tuple[lng, lat]
        """
        return self._transformer.transform(xx=lng, yy=lat)


if __name__ == '__main__':
    pass
