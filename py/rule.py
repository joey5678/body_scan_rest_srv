import os
import sys

from durable.lang import *


class Figure():
    height: float
    weight: float

    TunWei_167: float
    ShoulderWei_104: float
    TS_sum: float # 167 + 104
    WaistWei_155: float
    NeckWei_140: float
    BustWei_144: float
    LeftArm_125: float
    LeftWrist_123: float
    RightArm_126: float
    RightWrist_121: float
    LeftThigh_111: float
    RightThigh_112: float
    LeftShank_115: float
    RightShank_116: float
    LeftAnkle_117: float
    RightAnkle_118: float

    JianKuan: float
    TouKuan: float

    Head_Height: float
    top_half_Length: float # height - Leg_Length
    top_leg_Length: float # 
    # down_leg_Length: float #
    Leg_Length: float
    BigLeg_Height: float
    Knee_Height: float
    Nip_Distance: float


BMI_Standards = {
    150: {
        'top_w': 105,
        'down_w': 81,
        'perfect_w': 90,
    },
    151: {
        'top_w': 106,
        'down_w': 82,
        'perfect_w': 91.2,
    },
    152: {
        'top_w': 107,
        'down_w': 83.2,
        'perfect_w': 92.4,
    },
    153: {
        'top_w': 108,
        'down_w': 84.2,
        'perfect_w': 93.6,
    },
    154: {
        'top_w': 109,
        'down_w': 85.4,
        'perfect_w': 94.8,
    },
    155: {
        'top_w': 110,
        'down_w': 86.4,
        'perfect_w': 96.2,
    },
    156: {
        'top_w': 111,
        'down_w': 87.6,
        'perfect_w': 97.4,
    },
    157: {
        'top_w': 112,
        'down_w': 88.8,
        'perfect_w': 98.6,
    },
    158: {
        'top_w': 113,
        'down_w': 89.8,
        'perfect_w': 99.8,
    },
    159: {
        'top_w': 114,
        'down_w': 91,
        'perfect_w': 101.2,
    },
    160: {
        'top_w': 115,
        'down_w': 92.2,
        'perfect_w': 102.4,
    },
    161: {
        'top_w': 116,
        'down_w': 93.4,
        'perfect_w': 103.6,
    },
    162: {
        'top_w': 117,
        'down_w': 94.4,
        'perfect_w': 105,
    },
    163: {
        'top_w': 118,
        'down_w': 95.6,
        'perfect_w': 106.2,
    },
    164: {
        'top_w': 119,
        'down_w': 96.8,
        'perfect_w': 107.6,
    },
    165: {
        'top_w': 120,
        'down_w': 98,
        'perfect_w': 109,
    },
    166: {
        'top_w': 121,
        'down_w': 99.2,
        'perfect_w': 110.2,
    },
    167: {
        'top_w': 122,
        'down_w': 100.4,
        'perfect_w': 111.6,
    },
    168: {
        'top_w': 123,
        'down_w': 101.6,
        'perfect_w': 112.8,
    },
    169: {
        'top_w': 124,
        'down_w': 102.8,
        'perfect_w': 114.2,
    },
    170: {
        'top_w': 125,
        'down_w': 104,
        'perfect_w': 115.6,
    },
    171: {
        'top_w': 126,
        'down_w': 105.2,
        'perfect_w': 117,
    },
    172: {
        'top_w': 127,
        'down_w': 106.6,
        'perfect_w': 118.4,
    },
    173: {
        'top_w': 128,
        'down_w': 107.8,
        'perfect_w': 119.8,
    },
    174: {
        'top_w': 129,
        'down_w': 109,
        'perfect_w': 121.2,
    },
    175: {
        'top_w': 130,
        'down_w': 110.2,
        'perfect_w': 122.6,
    },

}

Body_Standards = {
    'whole': {
        # 1.2
        'delta_Tun_Jian': 2,
        'delta_Jian_Yao': 2,
        'delta_TJ_Yao': 20,
    },
    'part': {
        # 2.1
        'ratio_Jian_Tou': 1.25,
        'range_Jian_Tou_up': 0.4,
        'range_Jian_Tou_down': 0.2,
        # 2.2
        'ratio_Body_Head': 1.75,
        'range_Body_Head': 0.05,
        # 2.3
        'ratio_half_top': 1.0,
        'ratio_half_middle': 0.9,
        'radio_half_down': 0.85,
        # 2.4
        'ratio_half_Leg': 0.48,
        # 2.5
        'ratio_Yao_Tun_top': 0.85,
        'ratio_Yao_Tun_s0': 0.67,
        'ratio_Yao_Tun_s1': 0.7,
        # 2.6
        'ratio_Nip_Shoulder': 0.5,

    },
    'detail': {
        # 3.1
        'girth_Neck_top': 45,
        'girth_Neck_down': 35,
        # 3.2
        'ratio_YaoW_height_top': 0.49,
        'ratio_YaoW_height_down': 0.37,
        # 3.3
        'ratio_XiongW_height_top': 0.53,
        'ratio_XiongW_height_down': 0.39,
        # 3.4
        'radio_TunW_height_top': 0.62,
        'radio_TunW_height_down': 0.49,
        'radio_TunW_height_perfect': 0.54,
        # 3.5
        'radio_ArmW_Wrist_top': 2,
        'radio_ArmW_Wrist_down': 1.4,
        'radio_ArmW_Wrist_perfect': 1.7,
        # 3.6
        'radio_ThighW_height': 0.26,
        'plus_ThighW_height_top': 8.6,
        'plus_ThighW_height_down': 7,
        'plus_ThighW_height_perfect': 7.8,
        # 3.7
        'radio_ShankW_height_top': 0.22,
        'radio_ShankW_height_down': 0.15,
        'radio_ShankW_height_perfect': 0.18,
        # 3.8
        'radio_AnkleW_ShankW_top': 0.7,
        'radio_AnkleW_ShankW_down': 0.5,
        'radio_AnkleW_ShankW_perfect': 0.59,

    },
}

bmi_thin_rules = []
bmi_perfect_rules = []
bmi_normal_rules = []
bmi_fat_rules = []

for h_k, w_vals in BMI_Standards.items():
    down_w = w_vals['down_w']
    top_w = w_vals['top_w']
    perfect_w = w_vals['perfect_w']

    t_rule = (m.height == h_k) & (m.weight < down_w)
    f_rule = (m.height == h_k) & (m.weight > top_w)
    s_rule = (m.height == h_k) & (m.weight >= down_w) & (m.weight <= top_w)
    p_rule = (m.height == h_k) & (m.weight == perfect_w)

    bmi_thin_rules.append(t_rule)
    bmi_fat_rules.append(f_rule)
    bmi_normal_rules.append(s_rule)
    bmi_perfect_rules.append(p_rule)

BS_W = Body_Standards['whole']
bw_r_1 = (m.TunWei_167 > m.ShoulderWei_104 + BS_W['delta_Tun_Jian'])
bw_r_2 = (m.ShoulderWei_104 > m.WaistWei_155 + BS_W['delta_Jian_Yao'])
bw_r_3 = (m.TunWei_167 <= m.ShoulderWei_104 + BS_W['delta_Tun_Jian'])
bw_r_4 = (m.ShoulderWei_104 <= m.WaistWei_155 + BS_W['delta_Jian_Yao'])
bw_r_5 = (m.TS_sum <= (m.WaistWei_155  + BS_W['delta_TJ_Yao']) * 2 )
bw_r_6 = (m.TS_sum >  (m.WaistWei_155 + BS_W['delta_TJ_Yao']) * 2 )
#- m.ShoulderWei_104
rule_121 = bw_r_1 & bw_r_2
rule_122 = bw_r_1 & bw_r_4
rule_123 = bw_r_3 & bw_r_5
rule_124 = bw_r_3 & bw_r_6

BS_P = Body_Standards['part']
r211_a = m.JianKuan <= m.TouKuan * (BS_P['ratio_Jian_Tou'] + BS_P['range_Jian_Tou_down'])
r211_b = m.JianKuan >= m.TouKuan * (BS_P['ratio_Jian_Tou'] - BS_P['range_Jian_Tou_down'])
rule_211 = r211_a & r211_b

r212_a = m.JianKuan >  m.TouKuan * (BS_P['ratio_Jian_Tou'] + BS_P['range_Jian_Tou_down'])
r212_b = m.JianKuan <= m.TouKuan * (BS_P['ratio_Jian_Tou'] + BS_P['range_Jian_Tou_up'])
rule_212 = r212_a & r212_b

r213_a = m.JianKuan > m.TouKuan * (BS_P['ratio_Jian_Tou'] + BS_P['range_Jian_Tou_up'])
r213_b = m.JianKuan <  m.TouKuan * (BS_P['ratio_Jian_Tou'] - BS_P['range_Jian_Tou_down'])
rule_213 = r213_a | r213_b

r221_a = m.height == m.Head_Height * BS_P['ratio_Body_Head'] 
r222_a = m.height >= m.Head_Height * (BS_P['ratio_Body_Head'] - BS_P['range_Body_Head'])
r222_b = m.height <= m.Head_Height * (BS_P['ratio_Body_Head'] + BS_P['range_Body_Head'])
r222_c = m.height != m.Head_Height * BS_P['ratio_Body_Head']
r223_a = m.height < m.Head_Height * (BS_P['ratio_Body_Head'] - BS_P['range_Body_Head'])
r223_b = m.height > m.Head_Height * (BS_P['ratio_Body_Head'] + BS_P['range_Body_Head'])
rule_221 = r221_a 
rule_222 = r222_a & r222_b & r222_c
rule_223 = r223_a | r223_b


r231_a = m.Leg_Length >= m.top_half_Length * BS_P['ratio_half_top']
r232_a = m.Leg_Length < m.top_half_Length * BS_P['ratio_half_top']
r232_b = m.Leg_Length >= m.top_half_Length * BS_P['ratio_half_middle']
r233_a = m.Leg_Length < m.top_half_Length * BS_P['ratio_half_middle']
r233_b = m.Leg_Length >= m.top_half_Length * BS_P['radio_half_down']
r234_a = m.Leg_Length < m.top_half_Length * BS_P['radio_half_down']
rule_231 = r231_a
rule_232 = r232_a & r232_b
rule_233 = r233_a & r233_b
rule_234 = r234_a

r241_a = m.top_leg_Length < m.Leg_Length * BS_P['ratio_half_Leg']
r242_a = m.top_leg_Length >= m.Leg_Length * BS_P['ratio_half_Leg']
rule_241 = r241_a
rule_242 = r242_a

r251_a = m.WaistWei_155 / m.TunWei_167 > BS_P['ratio_Yao_Tun_s0']
r251_b = m.WaistWei_155 / m.TunWei_167 < BS_P['ratio_Yao_Tun_s1']
r252_a = m.WaistWei_155 / m.TunWei_167 > BS_P['ratio_Yao_Tun_top']
r253_a = m.WaistWei_155 / m.TunWei_167 <= BS_P['ratio_Yao_Tun_s0']
r253_b = m.WaistWei_155 / m.TunWei_167 >= BS_P['ratio_Yao_Tun_s1']
r253_c = m.WaistWei_155 / m.TunWei_167 <= BS_P['ratio_Yao_Tun_top']
rule_251 = r251_a & r251_b
rule_252 = r252_a
rule_253 = r253_a | r253_b & r253_c

r261_a = m.Nip_Distance > m.JianKuan * BS_P['ratio_Nip_Shoulder']
r262_a =  m.Nip_Distance <= m.JianKuan * BS_P['ratio_Nip_Shoulder']
rule_261 = r261_a
rule_262 = r262_a

BS_D = Body_Standards['detail']
rule_311 = m.NeckWei_140 <  BS_D['girth_Neck_down']
rule_312 = m.NeckWei_140 >= BS_D['girth_Neck_down'] & m.NeckWei_140 < BS_D['girth_Neck_top']
rule_313 = m.NeckWei_140 > BS_D['girth_Neck_top']

rule_321 = m.WaistWei_155 <= m.height * BS_D['ratio_YaoW_height_down']
r322_a = m.WaistWei_155 > m.height * BS_D['ratio_YaoW_height_down']
r322_b = m.WaistWei_155 <= m.height * BS_D['ratio_YaoW_height_top']
rule_322 = r322_a & r322_b
rule_323 = m.WaistWei_155 > m.height * BS_D['ratio_YaoW_height_top']

rule_331 = m.BustWei_144 >= m.height * BS_D['ratio_XiongW_height_top']
r_332_a = m.BustWei_144 < m.height * BS_D['ratio_XiongW_height_top']
r_332_b = m.BustWei_144 >= m.height * BS_D['ratio_XiongW_height_down']
rule_332 = r_332_a & r_332_b
rule_333 = m.BustWei_144 < m.height * BS_D['ratio_XiongW_height_down']

rule_341 = m.TunWei_167 == m.height * BS_D['radio_TunW_height_perfect']
r342_a = m.TunWei_167 >= m.height * BS_D['radio_TunW_height_down']
r342_b = m.TunWei_167 <= m.height * BS_D['radio_TunW_height_top']
r342_c = m.TunWei_167 != m.height * BS_D['radio_TunW_height_perfect']
rule_342 = r342_a & r342_b & r342_c
rule_343 = m.TunWei_167 > m.height * BS_D['radio_TunW_height_top']
rule_344 = m.TunWei_167 < m.height * BS_D['radio_TunW_height_down']

r351_a = m.LeftArm_125 == m.LeftWrist_123 * BS_D['radio_ArmW_Wrist_perfect']
r351_b = m.RightArm_126 == m.RightWrist_121 , * BS_D['radio_ArmW_Wrist_perfect']
rule_351 = r351_a & r351_b
r352_a = m.LeftArm_125 >= m.LeftWrist_123 * BS_D['radio_ArmW_Wrist_down']
r352_b = m.RightArm_126 >= m.RightWrist_121 * BS_D['radio_ArmW_Wrist_down']
r352_c = m.LeftArm_125 <= m.LeftWrist_123 * BS_D['radio_ArmW_Wrist_top']
r352_d = m.RightArm_126 <= m.RightWrist_121 * BS_D['radio_ArmW_Wrist_top']
rule_352 = r352_a & r352_c | r352_b & r352_d
r353_a = m.LeftArm_125 > m.LeftWrist_123 * BS_D['radio_ArmW_Wrist_top']
r353_b = m.RightArm_126 > m.RightWrist_121 * BS_D['radio_ArmW_Wrist_top']
rule_353 = r353_a | r353_b
r354_a = m.LeftArm_125 < m.LeftWrist_123 * BS_D['radio_ArmW_Wrist_down']
r354_b = m.RightArm_126 < m.RightWrist_121 * BS_D['radio_ArmW_Wrist_down']
rule_354 = r354_a | r354_b

r361_a = m.LeftThigh_111 == m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_perfect']
r361_b = m.RightThigh_112 == m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_perfect']
rule_361 = r361_a & r361_b
r362_a = m.LeftThigh_111 >= m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_down']
r362_b = m.RightThigh_112 >= m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_down']
r362_c = m.LeftThigh_111 <= m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_top']
r362_d = m.RightThigh_112 <= m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_top']
rule_361 = r362_a & r362_c | r362_b & r362_d
r363_a = m.LeftThigh_111 > m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_top']
r363_b = m.RightThigh_112 > m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_top']
rule_362 = r363_a | r363_b
r364_a = m.LeftThigh_111 < m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_down']
r364_b = m.RightThigh_112 < m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_down']
rule_364 = r364_a | r364_b

r371_a = m.LeftShank_115 == m.height * BS_D['radio_ShankW_height_perfect']
r371_b = m.RightShank_116 == m.height * BS_D['radio_ShankW_height_perfect']
rule_371 = r371_a & r371_b
r372_a = m.LeftShank_115 >= m.height * BS_D['radio_ShankW_height_down']
r372_b = m.RightShank_116 >= m.height * BS_D['radio_ShankW_height_down']
r372_c = m.LeftShank_115 <= m.height * BS_D['radio_ShankW_height_top']
r372_d = m.RightShank_116 <= m.height * BS_D['radio_ShankW_height_top']
rule_371 = r372_a & r372_c | r372_b & r372_d
r373_a = m.LeftShank_115 > m.height * BS_D['radio_ShankW_height_top'] 
r373_b = m.RightShank_116 > m.height * BS_D['radio_ShankW_height_top']
rule_372 = r373_a | r373_b
r374_a = m.LeftShank_115 < m.height * BS_D['radio_ShankW_height_down']
r374_b = m.RightShank_116 < m.height * BS_D['radio_ShankW_height_down']
rule_374 = r374_a | r374_b

r381_a = m.LeftAnkle_117 == m.height * BS_D['radio_AnkleW_ShankW_perfect']
r381_b = m.RightAnkle_118 == m.height * BS_D['radio_AnkleW_ShankW_perfect']
rule_381 = r381_a & r381_b
r382_a = m.LeftAnkle_117 >= m.height * BS_D['radio_AnkleW_ShankW_down']
r382_b = m.RightAnkle_118 >= m.height * BS_D['radio_AnkleW_ShankW_down']
r382_c = m.LeftAnkle_117 <= m.height * BS_D['radio_AnkleW_ShankW_top']
r382_d = m.RightAnkle_118 <= m.height * BS_D['radio_AnkleW_ShankW_top']
rule_381 = r382_a & r382_c | r382_b & r382_d
r383_a = m.LeftAnkle_117 > m.height * BS_D['radio_AnkleW_ShankW_top'] 
r383_b = m.RightAnkle_118 > m.height * BS_D['radio_AnkleW_ShankW_top']
rule_382 = r383_a | r383_b
r384_a = m.LeftAnkle_117 < m.height * BS_D['radio_AnkleW_ShankW_down']
r384_b = m.RightAnkle_118 < m.height * BS_D['radio_AnkleW_ShankW_down']
rule_384 = r384_a | r384_b


def get2bmi_rules(bmi_rules):
    _half0 = None
    _half1 = None
    for r in bmi_rules[:13]:
        _half0 = r if not _half0 else (_half0 | r)

    for r in bmi_rules[13:]:
        _half1 = r if not _half1 else (_half1 | r)

    return _half0, _half1


trule_half0, trule_half1 = get2bmi_rules(bmi_thin_rules)
frule_half0, frule_half1 = get2bmi_rules(bmi_fat_rules)
srule_half0, srule_half1 = get2bmi_rules(bmi_normal_rules)
prule_half0, prule_half1 = get2bmi_rules(bmi_perfect_rules)

# global rule_result

def execute(facts, rule_str=None):
    # global rule_result
    execute.results = {}
    if rule_str:
        post(rule_str, facts)
    else:
        post('figure-bmi', facts)
        post('figure-body',facts)
    print(f"result is {execute.results}")
    return execute.results

execute.results = {}

def do_121(c_item):
    print(c_item.m)
    execute.results['body'] = 1

def do_122(c_item):
    print(c_item.m)
    execute.results['body'] = 2

def do_123(c_item):
    print(c_item.m)
    execute.results['body'] = 3

def do_124(c_item):
    print(c_item.m)
    execute.results['body'] = 4

def do_thin(c_item):
    print(c_item.m)
    execute.results['bmi'] = 0

def do_fat(c_item):
    print(c_item.m)
    execute.results['bmi'] = 2

def do_normal(c_item):
    print(c_item.m)
    execute.results['bmi'] = 1

def do_perfect(c_item):
    print(c_item.m)
    execute.results['bmi'] = 3

def register_rules():
    with ruleset('figure-part'):
        # part of body
        @when_all(rule_211)
        def r_211(c):
            print('rule 211')

        @when_all(rule_212)
        def r_212(c):
            print('rule 212')

        @when_all(rule_213)
        def r_213(c):
            print('rule 213')

        @when_all(rule_221)
        def r_221(c):
            print('rule 221'),

        @when_all(rule_222)
        def r_222(c):
            print('rule 222')

        @when_all(rule_223)
        def r_223(c):
            print('rule 223')

        @when_all(rule_231)
        def r_231(c):
            print('rule 231')
        
        @when_all(rule_232)
        def r_232(c):
            print('rule 232')

        @when_all(rule_233)
        def r_233(c):
            print('rule 233')

        @when_all(rule_234)
        def r_234(c):
            print('rule 234')

    with ruleset('figure-body'):
        # whole body
        @when_all(rule_121)
        def r_121(c):
            do_121(c)
        
        @when_all(rule_122)
        def r_122(c):
            do_122(c)

        @when_all(rule_123)
        def r_123(c):
            do_123(c)

        @when_all(rule_124)
        def r_124(c):
            do_124(c)

    with ruleset('figure-bmi'):
        # thin bmi
        @when_all(trule_half0)
        def thin(c):
            do_thin(c)

        @when_all(trule_half1)
        def thin_a(c):
            do_thin(c)
        # fat bmi

        @when_all(frule_half0)
        def fat(c):
            do_fat(c)

        @when_all(frule_half1)
        def fat_a(c):
            do_fat(c)
        # standard bmi

        @when_all(srule_half0)
        def normal(c):
            do_normal(c)

        @when_all(srule_half1)
        def normal_a(c):
            do_normal(c)
        # perfect bmi

        @when_all(prule_half0)
        def perfect(c):
            do_perfect(c)

        @when_all(prule_half1)
        def perfect_a(c):
            do_perfect(c)

register_rules()

