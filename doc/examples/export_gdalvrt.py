#!/usr/bin/env python3

import os
import epr
from osgeo import gdal


epr_to_gdal_type = {
    epr.E_TID_UNKNOWN: gdal.GDT_Unknown,
    epr.E_TID_UCHAR: gdal.GDT_Byte,
    epr.E_TID_CHAR: gdal.GDT_Byte,
    epr.E_TID_USHORT: gdal.GDT_UInt16,
    epr.E_TID_SHORT: gdal.GDT_Int16,
    epr.E_TID_UINT: gdal.GDT_UInt32,
    epr.E_TID_INT: gdal.GDT_Int32,
    epr.E_TID_FLOAT: gdal.GDT_Float32,
    epr.E_TID_DOUBLE: gdal.GDT_Float64,
    #epr.E_TID_STRING: gdal.GDT_Unknown,
    #epr.E_TID_SPARE: gdal.GDT_Unknown,
    #epr.E_TID_TIME: gdal.GDT_Unknown,
}


def epr2gdal_band(band, vrt):
    product = band.product
    dataset = band.dataset
    record = dataset.read_record(0)
    field = record.get_field_at(band._field_index - 1)

    ysize = product.get_scene_height()
    xsize = product.get_scene_width()

    if isinstance(vrt, gdal.Dataset):
        if (vrt.RasterYSize, vrt.RasterXSize) != (ysize, xsize):
            raise ValueError('dataset size do not match')
        gdal_ds = vrt
    elif os.path.exists(vrt):
        gdal_ds = gdal.Open(vrt, gdal.GA_Update)
        if gdal_ds is None:
            raise RuntimeError('unable to open "{}"'.format(vrt))
        driver = gdal_ds.GetDriver()
        if driver.ShortName != 'VRT':
            raise TypeError('unexpected GDAL driver ({}). '
                            'VRT driver expected'.format(driver.ShortName))
    else:
        driver = gdal.GetDriverByName('VRT')
        if driver is None:
            raise RuntimeError('unable to get driver "VRT"')

        gdal_ds = driver.Create(vrt, xsize, ysize, 0)
        if gdal_ds is None:
            raise RuntimeError('unable to create "{}" dataset'.format(vrt))

    filename = os.pathsep.join(product.file_path.split('/'))  # denormalize
    offset = dataset.get_dsd().ds_offset + field.get_offset()
    line_offset = record.tot_size
    pixel_offset = epr.get_data_type_size(field.get_type())

    if band.sample_model == epr.E_SMOD_1OF2:
        pixel_offset *= 2
    elif band.sample_model == epr.E_SMOD_2OF2:
        offset += pixel_offset
        pixel_offset *= 2

    options = [
        'subClass=VRTRawRasterBand',
        'SourceFilename={}'.format(filename),
        'ImageOffset={}'.format(offset),
        'LineOffset={}'.format(line_offset),
        'PixelOffset={}'.format(pixel_offset),
        'ByteOrder=MSB',
    ]

    gtype = epr_to_gdal_type[field.get_type()]
    ret = gdal_ds.AddBand(gtype, options=options)
    if ret != gdal.CE_None:
        raise RuntimeError(
            'unable to add VRTRawRasterBand to "{}"'.format(vrt))

    gdal_band = gdal_ds.GetRasterBand(gdal_ds.RasterCount)
    gdal_band.SetDescription(band.description)
    metadata = {
        'name': band.get_name(),
        'dataset_name': dataset.get_name(),
        'dataset_description': dataset.description,
        'lines_mirrored': str(band.lines_mirrored),
        'sample_model': epr.get_sample_model_name(band.sample_model),
        'scaling_factor': str(band.scaling_factor),
        'scaling_offset': str(band.scaling_offset),
        'scaling_method': epr.get_scaling_method_name(band.scaling_method),
        'spectr_band_index': str(band.spectr_band_index),
        'unit': band.unit if band.unit else '',
        'bm_expr': band.bm_expr if band.bm_expr else '',
    }
    gdal_band.SetMetadata(metadata)

    return gdal_ds


def epr2gdal(product, vrt, overwrite_existing=False):
    if isinstance(product, str):
        filename = product
        product = epr.open(filename)

    ysize = product.get_scene_height()
    xsize = product.get_scene_width()

    if os.path.exists(vrt) and not overwrite_existing:
        raise ValueError('unable to create "{}". Already exists'.format(vrt))

    driver = gdal.GetDriverByName('VRT')
    if driver is None:
        raise RuntimeError('unable to get driver "VRT"')

    gdal_ds = driver.Create(vrt, xsize, ysize, 0)
    if gdal_ds is None:
        raise RuntimeError('unable to create "{}" dataset'.format(vrt))

    metadata = {
        'id_string': product.id_string,
        'meris_iodd_version': str(product.meris_iodd_version),
        'dataset_names': ','.join(product.get_dataset_names()),
        'num_datasets': str(product.get_num_datasets()),
        'num_dsds': str(product.get_num_dsds()),
    }
    gdal_ds.SetMetadata(metadata)

    mph = product.get_mph()
    metadata = str(mph).replace(' = ', '=').split('\n')
    gdal_ds.SetMetadata(metadata, 'MPH')

    sph = product.get_sph()
    metadata = str(sph).replace(' = ', '=').split('\n')
    gdal_ds.SetMetadata(metadata, 'SPH')

    for band in product.bands():
        epr2gdal_band(band, gdal_ds)

    # @TODO: set geographic info

    return gdal_ds


if __name__ == '__main__':
    filename = 'MER_LRC_2PTGMV20000620_104318_00000104X000_00000_00000_0001.N1'
    vrtfilename = os.path.splitext(filename)[0] + '.vrt'

    gdal_ds = epr2gdal(filename, vrtfilename)

    with epr.open(filename) as product:
        band_index = product.get_band_names().index('water_vapour')
        band = product.get_band('water_vapour')
        eprdata = band.read_as_array()
        unit = band.unit
        lines_mirrored = band.lines_mirrored
        scaling_offset = band.scaling_offset
        scaling_factor = band.scaling_factor

    gdal_band = gdal_ds.GetRasterBand(band_index + 1)
    vrtdata = gdal_band.ReadAsArray()

    if lines_mirrored:
        vrtdata = vrtdata[:, ::-1]

    vrtdata = vrtdata * scaling_factor + scaling_offset

    print('Max absolute error:', abs(vrtdata - eprdata).max())

    # plot
    from matplotlib import pyplot as plt

    plt.figure()
    plt.subplot(2, 1, 1)
    plt.imshow(eprdata)
    plt.grid(True)
    cb = plt.colorbar()
    cb.set_label(unit)
    plt.title('EPR data')
    plt.subplot(2, 1, 2)
    plt.imshow(vrtdata)
    plt.grid(True)
    cb = plt.colorbar()
    cb.set_label(unit)
    plt.title('VRT data')
    plt.show()
