"""Documents"""
from .conf import ConfigLoader
from .geotrans import GeoTrans
from .mypkg import exectime


@exectime.app_time
def main():
    print('Load configure file')
    conf = ConfigLoader()
    conf.load()

    print('Transform coordinates')
    tky2jgd2011 = GeoTrans(conf.setting.from_epsg, conf.setting.to_epsg)

    for i, crd in enumerate(conf.loads.coordinates, 1):
        file = str(conf.saves.basename).format(BASE_NAME=str(i))
        xx, yy = tky2jgd2011.transform(crd[0], crd[1])

        with open(file, 'w') as f:
            f.write(f"EPSG:{conf.setting.from_epsg}\t\t"
                    f"EPSG:{conf.setting.to_epsg}\t\n")
            f.write(f"lat\tlng\tlat\tlng\n")

            for coords in zip(crd[1], crd[0], yy, xx):
                f.write('\t'.join([f"{c:.6f}" for c in coords]) + '\n')


if __name__ == '__main__':
    main()
