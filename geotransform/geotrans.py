"""Geodetic transformation"""
import numpy as np
from pyproj import Proj
from pyproj import Transformer


class Epsg:
    wgs84 = 4326  # WGS84: 地理座標系, GPSで得られる位置, 緯度経度
    jgd2000 = 4612  # JGD2000: 地理座標系, 世界測地系, 経度緯度
    jgd2011 = 6668  # JGD2011: 地理座標系, 世界測地系, 経度緯度
    tokyo = 4301  # 日本測地系TOKYO: 地理座標系, 日本測地系, 経度緯度


class GeoTrans:
    """
    :type _from_epsg: Proj
    :type _to_epsg: Proj
    :type _transformer: Transformer
    """

    def __init__(self, from_epsg=Epsg.tokyo, to_epsg=Epsg.jgd2011):
        """
        :type from_epsg: int
        :type to_epsg: int
        :param from_epsg: EPSG code of conversion source
        :param to_epsg: EPSG code of destination
        """
        self._from_epsg = Proj(f"epsg:{from_epsg}")
        self._to_epsg = Proj(f"epsg:{to_epsg}")
        self._transformer = Transformer.from_proj(
            self._from_epsg, self._to_epsg, always_xy=True)

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
