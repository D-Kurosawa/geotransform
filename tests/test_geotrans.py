import numpy as np
import pytest

from geotransform import geotrans


def test_transform():
    lng = np.array([139.691750, 141.346806, 127.680917])
    lat = np.array([35.689472, 43.064611, 26.212389])

    jgd2tky = geotrans.GeoTrans(geotrans.Epsg.jgd2011, geotrans.Epsg.tokyo)
    x, y = jgd2tky.transform(lng, lat)

    tky2jgd = geotrans.GeoTrans()
    x, y = tky2jgd.transform(x, y)

    for i in range(3):
        assert round(x[i], 6) == lng[i]
        assert round(y[i], 6) == lat[i]


if __name__ == '__main__':
    pytest.main()
