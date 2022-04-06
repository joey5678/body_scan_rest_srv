import collections
import json

Person = collections.namedtuple('figure', 'name age gender')
from rule import execute as rule_exec


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
    return p['position']['y'] - delta if p else 0

def _h_avg(p_id_map, id0, id1, delta=0):
    y0 = _h(p_id_map, id0, delta)
    y1 = _h(p_id_map, id1, delta)

    return (y0 + y1) /2

def _g_sum(g_id_map, id0, id1):
    return _g(g_id_map, id0) + _g(g_id_map, id1) 

def _g_delta(g_id_map, id0, id1):
    pass


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

def new_figure(NT, f, d):
    g_data = d['body']['result']['metrics']['girths']
    g_id_map = {g['id']: g for g  in g_data}
    lmp_data = d['body']['result']['metrics']['landmarkPoints']
    p_id_map = {p['id']: p for p in lmp_data}
    print(p_id_map.keys())
    
    f['height'] =  d['others']['height']
    f['weight'] = 0.0
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
    f['w_shoulder_210_211'] = _w(p_id_map, 210, 211)
    f['w_busts_205_206'] = _w(p_id_map, 205, 206)
    f['w_head_212_213'] = _w(p_id_map, 212, 213)
    f['h_leg_333_334'] = _h_avg(p_id_map, 333,334)

    nt = NT(**f)

    return nt

def test_1():
    figure_key_item = ( 'height', 'weight', 
                        'g_hip_167', 'g_shoulder_104', 'g_sum_167_104', 'g_waist_155', 'g_neck_140', 
                        'g_bust_144', 'g_lbiceps_125', 'g_lwrist_123', 'g_rbiceps_126', 'g_rwrist_121', 'g_lmthigh_111', 
                        'g_rmthigh_112', 'g_lmcalf_115', 'g_rmcalf_116', 'g_lankle_117', 'g_rankle_118', 
                        'w_shoulder_210_211', 'w_busts_205_206', 'w_head_212_213', 'h_head_202', 'h_upper_body', 'h_leg_333_334', 'h_upper_leg', )

    mock_json_file = '../mock/3dm_api/metrics/GET_200.json'
    data = json.load(open(mock_json_file))
    # print(data['body']['result'])
    print(data['others'])
    rdata = data['body']['result']
    print(rdata['metrics'].keys())
    girths_data = rdata['metrics']['girths']
    lmpoints_data = rdata['metrics']['landmarkPoints']
    print(girths_data[0])
    print(lmpoints_data[0])

    # M = collections.namedtuple('Metric', girths_data[0])(**girths_data[0])
    # print(M.id)
    # print(M._field_defaults)

    f = dict.fromkeys(figure_key_item, -1.)
    M = collections.namedtuple('Metric', f)
    m = new_figure(M, f, data)
    print(m)


test_1()
