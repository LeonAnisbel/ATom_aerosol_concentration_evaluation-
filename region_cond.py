reg_data = {'South Atlantic':[],
            'South Pacific':[],
            'Central Pacific':[],
            'North Pacific': [],
            'North Atlantic':[],
            'North Pole': [],}

subkeys = {'latitud': [],
           'longitud': [],
           'aer_data': [],
           'model_data': [],
           'altitude': [],
           'pressure': [],
           'time': []}

def get_cond_list(lat,lon):
    """
    Define the subregions limits
    :param lat: list of latitude values
    :param lon: list of longitudes values
    :return: list with region limits, latitude and longitude arrays from the model grid
    """
    conditions = [[[lat, -90, 0], [lon, 290, 360]],
                  [[lat, -90, -23], [lon, 130, 293]],
                  [[lat, -23, 23], [lon, 130, 293]],
                  [[lat, 23, 60], [lon, 130, 240]],
                  [[lat, 0, 60], [lon, 300, 360]],
                  [[lat, 60, 90]],
                  ]
    return conditions














































































