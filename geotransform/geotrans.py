"""Geodetic transformation"""
import numpy as np
from pyproj import Proj
from pyproj import Transformer


class GeoTrans:
    """
    :type _from_proj: Proj
    :type _to_proj: Proj
    :type _transformer: Transformer
    """
    _EPSG_CODE = {
        '4326': {'name': 'WGS84', 'type': 'GeodeticCRS', 'area': 'World'},
        '4612': {'name': 'JGD2000', 'type': 'GeodeticCRS', 'area': 'Japan'},
        '6668': {'name': 'JGD2011', 'type': 'GeodeticCRS', 'area': 'Japan'},
        '4301': {'name': 'Tokyo', 'type': 'GeodeticCRS', 'area': 'Japan'}
    }

    def __init__(self, from_epsg=4301, to_epsg=6668):
        """
        :type from_epsg: int
        :type to_epsg: int
        :param from_epsg: EPSG code of conversion source
        :param to_epsg: EPSG code of destination
        """
        self._from_proj = Proj(f"epsg:{from_epsg}")
        self._to_proj = Proj(f"epsg:{to_epsg}")
        self._transformer = Transformer.from_proj(
            proj_from=self._from_proj,
            proj_to=self._to_proj,
            always_xy=True
        )

    def print_epsg_info(self):
        info_from = self._get_epsg_info(self._from_proj)
        info_to = self._get_epsg_info(self._to_proj)

        print("EPSG from: {0}    Name: {1}".format(*info_from))
        print("EPSG to  : {0}    Name: {1}".format(*info_to))

    @classmethod
    def _get_epsg_info(cls, proj):
        """
        :type proj: Proj
        :rtype tuple[str]
        """
        if 'epsg' not in str(proj.crs):
            raise KeyError(proj.crs)

        epsg = str(proj.crs).replace('epsg:', '')

        if epsg in cls._EPSG_CODE:
            return epsg, cls._EPSG_CODE[epsg]['name']

        return epsg, f"Not expect in <class {cls.__name__}>"

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
