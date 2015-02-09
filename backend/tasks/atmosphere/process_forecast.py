from pygrib import open as grib
import numpy as np


def process_forecast(input_name):
    """Strip irrelevant records and return the compressed filename."""
    # Open grib file
    grib_file = grib(input_name)
    # Select records from grib file
    u_sel = grib_file.select(shortName='u', typeOfLevel='isobaricInhPa')
    v_sel = grib_file.select(shortName='v', typeOfLevel='isobaricInhPa')
    t_sel = grib_file.select(shortName='t', typeOfLevel='isobaricInhPa')
    h_sel = grib_file.select(shortName='gh', typeOfLevel='isobaricInhPa')
    # Extract values from records
    vals = lambda x: x.values
    u_val = map(vals, u_sel)
    v_val = map(vals, v_sel)
    t_val = map(vals, t_sel)
    h_val = map(vals, h_sel)
    p_val = map(lambda x: x.level * 100, u_sel)
    lats = u_sel[0].distinctLatitudes
    lons = u_sel[0].distinctLongitudes
    # Close input file
    grib_file.close()

    # Determine output file name
    output_name = input_name.split('.')[0] + '.npz'
    # Save values to output file
    np.savez_compressed(
        output_name,
        h=h_val,
        p=p_val,
        t=t_val,
        u=u_val,
        v=v_val,
        lat=lats,
        lon=lons
    )

    # Return output file name
    return output_name
