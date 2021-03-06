from __future__ import division
from os.path import isfile
import csv, json

def read_file(file_loc):
    content = []
    try:
        with open(file_loc, mode='r') as input_data:
            content = input_data.read()
    except IOError:
        print 'File: ' + file_loc + ' not found!'
    return content

def read_csv(csv_loc):
    try:
        with open(csv_loc, 'rb') as csv_file:
            reader = csv.reader(csv_file, delimiter='|')
            return list(reader)
    except IOError:
        print 'CSV File: ' + csv_loc + ' not found!'
    return []

def read_csv_dist(csv_loc, value):
    dic = {}
    records = read_csv(csv_loc)
    if 'District' in records[0] and value in records[0]:
        key_idx = records[0].index('District')
        val_idx = records[0].index(value)
        for record in records[1:]:
            dic[record[key_idx]] = float(record[val_idx])
    return dic

def read_csv_state(csv_loc, value):
    dic = {}
    dic_perc = {}
    records = read_csv(csv_loc)
    if 'State' in records[0] and value in records[0]:
        key_idx = records[0].index('State')
        val_idx = records[0].index(value)
        for record in records[1:]:
            if record[key_idx] not in dic:
                dic[record[key_idx]] = float(record[val_idx])
            else:
                dic[record[key_idx]] += float(record[val_idx])
    total = 0
    for state in dic.keys():
        total += dic[state]
    for state in dic.keys():
        dic_perc[state] = format(round(dic[state] / total * 100, 2), '.2f')
    return dic_perc

def parse_json(data_json):
    return json.loads(data_json)

def read_geo_json(geo_json, dic, pri_key_field, field):
    num_feat = len(geo_json['features'])
    for i in range(0, num_feat):
        pri_key = geo_json['features'][i]['properties'][pri_key_field]
        if pri_key in dic:
            geo_json['features'][i]['properties'][field] = dic[pri_key]
        else:
            #print geo_json['features'][i]['properties']['NAME_1'] +': ' + pri_key
            print pri_key
            geo_json['features'][i]['properties'][field] = 0.0
    return geo_json

def get_dist_data(geo_json, state_name, dic, field):
    num_feat = len(geo_json['features'])
    for i in reversed(range(0, num_feat)):
        pri_key = geo_json['features'][i]['properties']['NAME_2']
        if geo_json['features'][i]['properties']['NAME_1'] != state_name:
            del geo_json['features'][i]
        else:
            if pri_key in dic:
                geo_json['features'][i]['properties'][field] = dic[pri_key]
            else:
                geo_json['features'][i]['properties'][field] = 0.0
    print len(geo_json['features'])
    file_name = '../data/states/' + state_name.replace(' ', '_') + '.js'
    write_state_json(geo_json, file_name)

def write_geo_json(geo_json, file_loc):
    with open(file_loc, 'a') as geo_out:
        geo_out.write('var statesData = ')
        json.dump(geo_json, geo_out)
        geo_out.write(';')

def write_state_json(geo_json, file_loc):
    with open(file_loc, 'a') as geo_out:
        geo_out.write('distData = ')
        json.dump(geo_json, geo_out)
        geo_out.write(';')

def main():
    states = ['Andaman and Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli', 'Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Orissa', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Tripura', 'Uttaranchal', 'Uttar Pradesh', 'West Bengal']
    #for state in states:
    #    print state
    #    dic = read_csv_dist('../data/out.csv', 'Proportion to Population (2011)')
    #    file_data = read_file('IND_adm2.json')
    #    geo_json = parse_json(file_data.decode('ISO-8859-1').strip())
    #    get_dist_data(geo_json, state, dic, 'POP_PROP_2011')
    #mod_geo_json = read_geo_json(geo_json, dic, 'NAME_2', 'POP_PROP_2011')
    #write_geo_json(mod_geo_json, 'new_districts.js')

    dic = read_csv_state('../data/out.csv', 'Actual Population (2011)')
    file_data = read_file('../data/geojson/IND_adm1.json')
    geo_json = parse_json(file_data.decode('ISO-8859-1').strip())
    mod_geo_json = read_geo_json(geo_json, dic, 'NAME_1', 'POP_PROP_2011')
    write_geo_json(mod_geo_json, '../data/geojson/districts.json')

if __name__ == '__main__':
    main()
