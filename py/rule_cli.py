import collections
import json

Person = collections.namedtuple('figure', 'name age gender')
from rule import execute as rule_exec
from rule import reset_rule_results, current_result


def _g(g_id_map, _id):
    g = g_id_map.get(_id, None)
    return g['girth'][0] if g else 0
   
def _w(p_id_map, id0, id1):

    p0 = p_id_map.get(id0, None)
    p1 = p_id_map.get(id1, None)

    x0 = p0['position']['x'] if p0 else 0
    x1 = p1['position']['x'] if p1 else 0

    return abs(x1 - x0)

def _h(p_id_map, _id, delta=0):
    p = p_id_map.get(_id, None)
    return p['level'] - delta if p else 0
    # return p['position']['y'] - delta if p else 0

def _h_avg(p_id_map, id0, id1, delta=0):
    y0 = _h(p_id_map, id0, delta)
    y1 = _h(p_id_map, id1, delta)

    return (y0 + y1) /2

def _g_sum(g_id_map, id0, id1):
    return _g(g_id_map, id0) + _g(g_id_map, id1) 

def _g_delta(g_id_map, id0, id1):
    pass

def _s(sl_id_map, _id):
    sl = sl_id_map.get(_id, None)
    return sl['length'] if sl else 0

def _s_avg(sl_id_map, id0, id1):
    l0 = _s(sl_id_map, id0)
    l1 = _s(sl_id_map, id1)
    return (l0 + l1) / 2

def test_0():

    ff = {'height': 175,  'weight': 140.1,}
    # fw = {'TunWei_167': 111, 'ShoulderWei_104':112, 'TS_sum': (111 + 112), 'WaistWei_155': 94}

    # f21 = {'JianKuan': 63, 'TouKuan':50}
    # f22 = {'height': 100, 'Head_Height':80}
    # f23 = {'Leg_Length': 10, 'top_half_Length':50}

    # rule_exec({**ff, **fw})



    fx = {'height': 170,  'weight': 140.1, 'TunWei_167': 111, 'ShoulderWei_104':112, 'TS_sum': (111 + 112), 
        'WaistWei_155': 94, 'JianKuan': 63, 'TouKuan':50, 'LeftThigh_111': 89, 'RightThigh_112':91, 'Head_Height':80,
        'LeftArm_125': 34, 'LeftWrist_123': 22, 'RightArm_126':35, 'RightWrist_121': 23, 'Leg_Length': 10, 'top_half_Length':50,
        'top_leg_Length':10, 'Nip_Distance': 23, }

    rule_exec(fx, 'figure-body')
    rule_exec(fx, 'figure-bmi')

    for i in range(6):
        print(f"\nfigure-part-2{i+1}\n")
        rule_exec(fx, f'figure-part-2{i+1}')

    for i in range(8):
        print(f"\nfigure-detail-3{i+1}\n")
        rule_exec(fx, f'figure-detail-3{i+1}')

def new_figure(NT, f, height, weight, g_data, lmp_data, slen_data):
    # g_data = d['body']['result']['metrics']['girths']
    g_id_map = {g['id']: g for g  in g_data}
    # lmp_data = d['body']['result']['metrics']['landmarkPoints']
    p_id_map = {p['id']: p for p in lmp_data}
    # print(p_id_map.keys())
    # slen_data = d['body']['result']['metrics']['surfaceLengths']
    # print(slen_data[0])
    s_id_map = {sl['id']: sl for sl in slen_data}

    f['height'] =  height #d['others']['height']
    f['weight'] = weight
    f['height2'] = height * height
    f['g_hip_167'] = _g(g_id_map, 167)
    f['g_shoulder_104'] = _g(g_id_map, 104)
    f['g_sum_167_104'] = _g_sum(g_id_map, 167, 104)
    f['g_waist_155'] = _g(g_id_map, 155)
    f['g_neck_140'] = _g(g_id_map, 140)
    f['g_bust_144'] = _g(g_id_map, 144)
    f['g_lbiceps_125'] = _g(g_id_map, 125)
    f['g_lwrist_123'] = _g(g_id_map, 123)
    f['g_rbiceps_126'] = _g(g_id_map, 126)
    f['g_rwrist_121'] = _g(g_id_map, 121)
    f['g_lmthigh_111'] = _g(g_id_map, 111)
    f['g_rmthigh_112'] = _g(g_id_map, 112)
    f['g_lmcalf_115'] = _g(g_id_map, 115)
    f['g_rmcalf_116'] = _g(g_id_map, 116)
    f['g_lankle_117'] = _g(g_id_map, 117)
    f['g_rankle_118'] = _g(g_id_map, 118)
    f['g_abdomen_161'] = _g(g_id_map, 161)
    f['g_waist_163'] = _g(g_id_map, 163)
    f['g_upper_chest_143'] = _g(g_id_map, 143)
    f['w_shoulder_210_211'] = _w(p_id_map, 210, 211)
    f['w_busts_205_206'] = _w(p_id_map, 205, 206)
    f['w_head_212_213'] = _w(p_id_map, 212, 213)
    f['h_leg_333_334'] = _s_avg(s_id_map, 333,334)
    f['h_leg_333_334'] = f['h_leg_333_334'] / 1.25
    f['h_knee'] = _h_avg(p_id_map, 226, 227)
    f['h_upper_body'] = f['height'] - f['h_leg_333_334']
    f['h_upper_leg'] = f['h_leg_333_334'] - f['h_knee']
    f['h_chin'] = _h(p_id_map, 202)
    f['h_head_202'] = f['height'] - f['h_chin'] 

    for k, v in f.items():
        if k == 'weight':
            f[k] = v * 1
        elif k.startswith('height'):
            f[k] = round(v * 100., 2)
        else:
            f[k] = round(v * 100., 1) # meter to cm
    f['height'] = int(f['height'])
    f['weight'] = int(f['weight'])
    print(f['height'])
    f['height'] = 175 if f['height'] > 175 else f['height']
    f['weight'] = 100 if f['weight'] <= 0 else f['weight']

    nt = NT(**f)

    return nt

def main():
    figure_key_item = ( 'height', 'weight', 'height2',
                        'g_hip_167', 'g_shoulder_104', 'g_sum_167_104', 'g_waist_155', 'g_neck_140', 
                        'g_bust_144', 'g_lbiceps_125', 'g_lwrist_123', 'g_rbiceps_126', 'g_rwrist_121', 'g_lmthigh_111', 
                        'g_rmthigh_112', 'g_lmcalf_115', 'g_rmcalf_116', 'g_lankle_117', 'g_rankle_118', 
                        'w_shoulder_210_211', 'w_busts_205_206', 'w_head_212_213', 'h_head_202', 'h_upper_body', 'h_knee',
                        'h_chin', 'h_leg_333_334', 'h_upper_leg', 'g_abdomen_161', 'g_waist_163', 'g_upper_chest_143')

    mock_json_file = '../mock/3dm_api/metrics/GET_200.json'
    data = json.load(open(mock_json_file))
    # print(data['body']['result'])
    rdata = data['body']['result']
    girths_data = rdata['metrics']['girths']
    lmpoints_data = rdata['metrics']['landmarkPoints']
    slen_data = rdata['metrics']['surfaceLengths']
    height = data['others']['height']

    # M = collections.namedtuple('Metric', girths_data[0])(**girths_data[0])
    # print(M.id)
    # print(M._field_defaults)
    weight = 110
    f = dict.fromkeys(figure_key_item, -1.)
    M = collections.namedtuple('Metric', f)
    new_figure(M, f, height, weight, girths_data, lmpoints_data, slen_data)
    # print(m)

    fx = f #dict(m._asdict())

    print(fx)
    print('\n')
    rule_exec(fx)
    # print('\nbody\n')
    # rule_exec(fx, 'figure-body')
    # print('\nbmi\n')
    # rule_exec(fx, 'figure-bmi')

    # for i in range(6):
    #     print(f"\nfigure-part-2{i+1}\n")
    #     rule_exec(fx, f'figure-part-2{i+1}')

    # for i in range(8):
    #     print(f"\nfigure-detail-3{i+1}\n")
    #     rule_exec(fx, f'figure-detail-3{i+1}')

if __name__ == "__main__":
    reset_rule_results()
    main()
    print(current_result())
