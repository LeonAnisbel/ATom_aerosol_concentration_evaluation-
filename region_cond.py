# reg_data = {'N. Pole': [],
#             'S. Pole': [],
#             'S. Pacific': [],
#             'N. Pacific': [],
#             'S. Atlantic': [],
#             'N. Atlantic': [],
#             'Sub. Pacific': [],
#             'Sub. Atlantic': [], }

reg_data = {'N. Pole': [],
            'N. Pacific': [],
            'N. Atlantic':[],
           'S. Pacific':[],
           'S. Atlantic':[],
           'C. Pacific':[]}

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
    conditions = [[[lat, 63, 90]],
                  [[lat, 23, 63], [lon, 130, 240]],
                  [[lat, 0, 63], [lon, 300, 360]],
                  [[lat, -85, -23], [lon, 130, 290]],
                  [[lat, -85, 0], [lon, 290, 360]],
                  [[lat, -23, 23], [lon, 130, 290]]]
    return conditions
