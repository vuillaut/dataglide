import time
from numpy import nan




class igc_trace():
    def __init__(self):
        self.file = ''
        self.pilot = ''
        self.trace={
            'times' : [],
            'latitudes' : [],
            'longitudes': [],
            'altitudes_p' : [],
            'altitudes_gps' : [],
        }
    def read_igc_file(self, filename):
        self.file = filename
        f = open(filename, "r", errors='ignore')
        data = f.read().splitlines()
        f.close()
        if len(data[3].split(':')) > 1:
            self.pilot = data[3].split(':')[1]
        for d in data:
            if d[0] == 'B':
                igc_B = read_igc_B(d)
                self.trace['times'].append(igc_B['time'])
                self.trace['latitudes'].append(igc_B['lat'])
                self.trace['longitudes'].append(igc_B['long'])
                self.trace['altitudes_p'].append(igc_B['alt_p'])
                self.trace['altitudes_gps'].append(igc_B['alt_gps'])
                
                
                
def read_igc_B(line):
    lat = line[7:15]
    long = line[15:24]
    dic = {'time': time.strptime(line[1:7], '%H%M%S'), 
           'lat': (-1*(lat[-1]=='S') + 1*(lat[-1]=='N')) * (int(lat[:2]) + (float(lat[2:4])+float(lat[4:-1])/1000.)/60), 
           'long': (-1*(long[-1]=='W') + 1*(long[-1]=='E')) * (int(long[:3]) + (float(long[3:5])+float(long[5:-1])/1000.)/60)
          }
    if 'A' in line:
        dic['alt_p'] = float(line[25:30])
        dic['alt_gps'] = float(line[30:35])
    else:
        dic['alt_p'] = nan
        dic['alt_gps'] = nan
    return dic
