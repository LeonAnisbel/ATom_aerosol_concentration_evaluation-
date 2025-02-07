# reg_data = {'N. Pole': [],
#             'S. Pole': [],
#             'S. Pacific': [],
#             'N. Pacific': [],
#             'S. Atlantic': [],
#             'N. Atlantic': [],
#             'Sub. Pacific': [],
#             'Sub. Atlantic': [], }

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
    # conditions = [[[lat, 55, 90]],
    #               [[lat, -80, -55]],
    #               [[lat, -55, -23], [lon, 130, 290]],
    #               [[lat, 23, 55], [lon, 130, 240]],
    #               [[lat, -55, -23], [lon, 290, 360]],
    #               [[lat, 23, 55], [lon, 300, 360]],
    #               [[lat, -23, 23], [lon, 130, 290]],
    #               [[lat, -23, 23], [lon, 300, 360]]]
    conditions = [[[lat, -90, 0], [lon, 290, 360]],
                  [[lat, -90, -23], [lon, 130, 293]],
                  [[lat, -23, 23], [lon, 130, 293]],
                  [[lat, 23, 60], [lon, 130, 240]],
                  [[lat, 0, 60], [lon, 300, 360]],
                  [[lat, 60, 90]],
                  ]
    return conditions














































































