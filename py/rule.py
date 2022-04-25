import os
import sys

from durable.lang import *


class Figure():
    height: float
    weight: float

    g_hip_167: float
    g_shoulder_104: float
    g_sum_167_104: float # 167 + 104
    g_waist_155: float
    g_neck_140: float
    g_bust_144: float
    g_lbiceps_125: float
    g_lwrist_123: float
    g_rbiceps_126: float
    g_rwrist_121: float
    g_lmthigh_111: float
    g_rmthigh_112: float
    g_lmcalf_115: float
    g_rmcalf_116: float
    g_lankle_117: float
    g_rankle_118: float

    w_shoulder_210_211: float
    w_head_212_213: float
    w_busts_205_206: float

    h_head_202: float
    h_leg_333_334: float
    h_upper_body: float # height - h_leg_333_334
    h_upper_leg: float # 


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
bw_r_1 = (m.g_hip_167 > m.g_shoulder_104 + BS_W['delta_Tun_Jian'])
bw_r_2 = (m.g_shoulder_104 > m.g_waist_155 + BS_W['delta_Jian_Yao'])
bw_r_3 = (m.g_hip_167 <= m.g_shoulder_104 + BS_W['delta_Tun_Jian'])
bw_r_4 = (m.g_shoulder_104 <= m.g_waist_155 + BS_W['delta_Jian_Yao'])
bw_r_5 = (m.g_sum_167_104 <= (m.g_waist_155  + BS_W['delta_TJ_Yao']) * 2 )
bw_r_6 = (m.g_sum_167_104 >  (m.g_waist_155 + BS_W['delta_TJ_Yao']) * 2 )
#- m.g_shoulder_104
rule_121 = bw_r_1 & bw_r_2
rule_122 = bw_r_1 & bw_r_4
rule_123 = bw_r_3 & bw_r_5
rule_124 = bw_r_3 & bw_r_6

BS_P = Body_Standards['part']
r211_a = m.w_shoulder_210_211 <= m.w_head_212_213 * (BS_P['ratio_Jian_Tou'] + BS_P['range_Jian_Tou_down'])
r211_b = m.w_shoulder_210_211 >= m.w_head_212_213 * (BS_P['ratio_Jian_Tou'] - BS_P['range_Jian_Tou_down'])
rule_211 = r211_a & r211_b

r212_a = m.w_shoulder_210_211 >  m.w_head_212_213 * (BS_P['ratio_Jian_Tou'] + BS_P['range_Jian_Tou_down'])
r212_b = m.w_shoulder_210_211 <= m.w_head_212_213 * (BS_P['ratio_Jian_Tou'] + BS_P['range_Jian_Tou_up'])
rule_212 = r212_a & r212_b

r213_a = m.w_shoulder_210_211 > m.w_head_212_213 * (BS_P['ratio_Jian_Tou'] + BS_P['range_Jian_Tou_up'])
r213_b = m.w_shoulder_210_211 <  m.w_head_212_213 * (BS_P['ratio_Jian_Tou'] - BS_P['range_Jian_Tou_down'])
rule_213 = r213_a | r213_b

r221_a = m.height == m.h_head_202 * BS_P['ratio_Body_Head'] 
r222_a = m.height >= m.h_head_202 * (BS_P['ratio_Body_Head'] - BS_P['range_Body_Head'])
r222_b = m.height <= m.h_head_202 * (BS_P['ratio_Body_Head'] + BS_P['range_Body_Head'])
r222_c = m.height != m.h_head_202 * BS_P['ratio_Body_Head']
r223_a = m.height < m.h_head_202 * (BS_P['ratio_Body_Head'] - BS_P['range_Body_Head'])
r223_b = m.height > m.h_head_202 * (BS_P['ratio_Body_Head'] + BS_P['range_Body_Head'])
rule_221 = r221_a 
rule_222 = r222_a & r222_b & r222_c
rule_223 = r223_a | r223_b


r231_a = m.h_leg_333_334 >= m.h_upper_body * BS_P['ratio_half_top']
r232_a = m.h_leg_333_334 < m.h_upper_body * BS_P['ratio_half_top']
r232_b = m.h_leg_333_334 >= m.h_upper_body * BS_P['ratio_half_middle']
r233_a = m.h_leg_333_334 < m.h_upper_body * BS_P['ratio_half_middle']
r233_b = m.h_leg_333_334 >= m.h_upper_body * BS_P['radio_half_down']
r234_a = m.h_leg_333_334 < m.h_upper_body * BS_P['radio_half_down']
rule_231 = r231_a
rule_232 = r232_a & r232_b
rule_233 = r233_a & r233_b
rule_234 = r234_a

r241_a = m.h_upper_leg < m.h_leg_333_334 * BS_P['ratio_half_Leg']
r242_a = m.h_upper_leg >= m.h_leg_333_334 * BS_P['ratio_half_Leg']
rule_241 = r241_a
rule_242 = r242_a

r251_a = m.g_waist_155 > m.g_hip_167 * BS_P['ratio_Yao_Tun_s0'] 
r251_b = m.g_waist_155 < m.g_hip_167 * BS_P['ratio_Yao_Tun_s1']
r252_a = m.g_waist_155 > m.g_hip_167 * BS_P['ratio_Yao_Tun_top']
r253_a = m.g_waist_155 <= m.g_hip_167 * BS_P['ratio_Yao_Tun_s0']
r253_b = m.g_waist_155 >= m.g_hip_167 * BS_P['ratio_Yao_Tun_s1']
r253_c = m.g_waist_155 <= m.g_hip_167 * BS_P['ratio_Yao_Tun_top']
rule_251 = r251_a & r251_b
rule_252 = r252_a
rule_253 = r253_a | r253_b & r253_c

r261_a = m.w_busts_205_206 > m.w_shoulder_210_211 * BS_P['ratio_Nip_Shoulder']
r262_a =  m.w_busts_205_206 <= m.w_shoulder_210_211 * BS_P['ratio_Nip_Shoulder']
rule_261 = r261_a
rule_262 = r262_a

BS_D = Body_Standards['detail']
rule_311 = m.g_neck_140 <  BS_D['girth_Neck_down']
r312_a = m.g_neck_140 >= BS_D['girth_Neck_down']
r312_b = m.g_neck_140 < BS_D['girth_Neck_top']
rule_312 = r312_a & r312_b
rule_313 = m.g_neck_140 > BS_D['girth_Neck_top']

rule_321 = m.g_waist_155 <= m.height * BS_D['ratio_YaoW_height_down']
r322_a = m.g_waist_155 > m.height * BS_D['ratio_YaoW_height_down']
r322_b = m.g_waist_155 <= m.height * BS_D['ratio_YaoW_height_top']
rule_322 = r322_a & r322_b
rule_323 = m.g_waist_155 > m.height * BS_D['ratio_YaoW_height_top']

rule_331 = m.g_bust_144 >= m.height * BS_D['ratio_XiongW_height_top']
r_332_a = m.g_bust_144 < m.height * BS_D['ratio_XiongW_height_top']
r_332_b = m.g_bust_144 >= m.height * BS_D['ratio_XiongW_height_down']
rule_332 = r_332_a & r_332_b
rule_333 = m.g_bust_144 < m.height * BS_D['ratio_XiongW_height_down']

rule_341 = m.g_hip_167 == m.height * BS_D['radio_TunW_height_perfect']
r342_a = m.g_hip_167 >= m.height * BS_D['radio_TunW_height_down']
r342_b = m.g_hip_167 <= m.height * BS_D['radio_TunW_height_top']
r342_c = m.g_hip_167 != m.height * BS_D['radio_TunW_height_perfect']
rule_342 = r342_a & r342_b & r342_c
rule_343 = m.g_hip_167 > m.height * BS_D['radio_TunW_height_top']
rule_344 = m.g_hip_167 < m.height * BS_D['radio_TunW_height_down']

r351_a = m.g_lbiceps_125 == m.g_lwrist_123 * BS_D['radio_ArmW_Wrist_perfect']
r351_b = m.g_rbiceps_126 == m.g_rwrist_121 * BS_D['radio_ArmW_Wrist_perfect']
rule_351 = r351_a & r351_b
r352_a = m.g_lbiceps_125 >= m.g_lwrist_123 * BS_D['radio_ArmW_Wrist_down']
r352_b = m.g_rbiceps_126 >= m.g_rwrist_121 * BS_D['radio_ArmW_Wrist_down']
r352_c = m.g_lbiceps_125 <= m.g_lwrist_123 * BS_D['radio_ArmW_Wrist_top']
r352_d = m.g_rbiceps_126 <= m.g_rwrist_121 * BS_D['radio_ArmW_Wrist_top']
rule_352 = r352_a & r352_c | r352_b & r352_d
r353_a = m.g_lbiceps_125 > m.g_lwrist_123 * BS_D['radio_ArmW_Wrist_top']
r353_b = m.g_rbiceps_126 > m.g_rwrist_121 * BS_D['radio_ArmW_Wrist_top']
rule_353 = r353_a | r353_b
r354_a = m.g_lbiceps_125 < m.g_lwrist_123 * BS_D['radio_ArmW_Wrist_down']
r354_b = m.g_rbiceps_126 < m.g_rwrist_121 * BS_D['radio_ArmW_Wrist_down']
rule_354 = r354_a | r354_b

r361_a = m.g_lmthigh_111 == m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_perfect']
r361_b = m.g_rmthigh_112 == m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_perfect']
rule_361 = r361_a & r361_b
r362_a = m.g_lmthigh_111 >= m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_down']
r362_b = m.g_rmthigh_112 >= m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_down']
r362_c = m.g_lmthigh_111 <= m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_top']
r362_d = m.g_rmthigh_112 <= m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_top']
rule_362 = r362_a & r362_c | r362_b & r362_d
r363_a = m.g_lmthigh_111 > m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_top']
r363_b = m.g_rmthigh_112 > m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_top']
rule_363 = r363_a | r363_b
r364_a = m.g_lmthigh_111 < m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_down']
r364_b = m.g_rmthigh_112 < m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_down']
rule_364 = r364_a | r364_b

r371_a = m.g_lmcalf_115 == m.height * BS_D['radio_ShankW_height_perfect']
r371_b = m.g_rmcalf_116 == m.height * BS_D['radio_ShankW_height_perfect']
rule_371 = r371_a & r371_b
r372_a = m.g_lmcalf_115 >= m.height * BS_D['radio_ShankW_height_down']
r372_b = m.g_rmcalf_116 >= m.height * BS_D['radio_ShankW_height_down']
r372_c = m.g_lmcalf_115 <= m.height * BS_D['radio_ShankW_height_top']
r372_d = m.g_rmcalf_116 <= m.height * BS_D['radio_ShankW_height_top']
rule_372 = r372_a & r372_c | r372_b & r372_d
r373_a = m.g_lmcalf_115 > m.height * BS_D['radio_ShankW_height_top'] 
r373_b = m.g_rmcalf_116 > m.height * BS_D['radio_ShankW_height_top']
rule_373 = r373_a | r373_b
r374_a = m.g_lmcalf_115 < m.height * BS_D['radio_ShankW_height_down']
r374_b = m.g_rmcalf_116 < m.height * BS_D['radio_ShankW_height_down']
rule_374 = r374_a | r374_b

r381_a = m.g_lankle_117 == m.height * BS_D['radio_AnkleW_ShankW_perfect']
r381_b = m.g_rankle_118 == m.height * BS_D['radio_AnkleW_ShankW_perfect']
rule_381 = r381_a & r381_b
r382_a = m.g_lankle_117 >= m.height * BS_D['radio_AnkleW_ShankW_down']
r382_b = m.g_rankle_118 >= m.height * BS_D['radio_AnkleW_ShankW_down']
r382_c = m.g_lankle_117 <= m.height * BS_D['radio_AnkleW_ShankW_top']
r382_d = m.g_rankle_118 <= m.height * BS_D['radio_AnkleW_ShankW_top']
rule_382 = r382_a & r382_c | r382_b & r382_d
r383_a = m.g_lankle_117 > m.height * BS_D['radio_AnkleW_ShankW_top'] 
r383_b = m.g_rankle_118 > m.height * BS_D['radio_AnkleW_ShankW_top']
rule_383 = r383_a | r383_b
r384_a = m.g_lankle_117 < m.height * BS_D['radio_AnkleW_ShankW_down']
r384_b = m.g_rankle_118 < m.height * BS_D['radio_AnkleW_ShankW_down']
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

def reset_rule_results():
    execute.results = {}

def current_result():
    return execute.results

def execute(facts, rule_str=None):
    # global rule_result
    if rule_str:
        assert_fact(rule_str, facts)
    else:
        post('figure-bmi', facts)
        post('figure-body',facts)

        for i in range(6):
            post(f'figure-part-2{i+1}', facts)

        for i in range(8):
            post(f"figure-detail-3{i+1}", facts)

    # print(f"result is {execute.results}")
    # print(get_facts(rule_str))
    return execute.results

execute.results = {}

def register_rules():

    with ruleset('figure-detail-31'):
        @when_all(rule_311)
        def r_3(c):
            execute.results['颈围31'] = '修长'

        @when_all(rule_312)
        def r_3(c):
            execute.results['颈围31'] = '标准脖'

        @when_all(rule_313)
        def r_3(c):
            execute.results['颈围31'] = '粗脖'

    with ruleset('figure-detail-32'):
        @when_all(rule_321)
        def r_3(c):
            execute.results['腰围32'] = '纤细'

        @when_all(rule_322)
        def r_3(c):
            execute.results['腰围32'] = '标准'

        @when_all(rule_323)
        def r_3(c):
            execute.results['腰围32'] = '偏胖'

    with ruleset('figure-detail-33'):
        @when_all(rule_331)
        def r_3(c):
            execute.results['胸围33'] = '完美'

        @when_all(rule_332)
        def r_3(c):
            execute.results['胸围33'] = '标准'

        @when_all(rule_333)
        def r_3(c):
            execute.results['胸围33'] = '偏小'

    with ruleset('figure-detail-34'):
        @when_all(rule_341)
        def r_3(c):
            execute.results['臀围34'] = '完美'

        @when_all(rule_342)
        def r_3(c):
            execute.results['臀围34'] = '标准'

        @when_all(rule_343)
        def r_3(c):
            execute.results['臀围34'] = '偏大'

        @when_all(rule_344)
        def r_3(c):
            execute.results['臀围34'] = '偏小'

    with ruleset('figure-detail-35'):
        @when_all(rule_351)
        def r_3(c):
            execute.results['手臂围35'] = '完美'

        @when_all(rule_352)
        def r_3(c):
            execute.results['手臂围35'] = '标准'

        @when_all(rule_353)
        def r_3(c):
            execute.results['手臂围35'] = '偏粗'

        @when_all(rule_354)
        def r_3(c):
            execute.results['手臂围35'] = '偏细'

    with ruleset('figure-detail-36'):
        @when_all(rule_361)
        def r_3(c):
            execute.results['大腿围36'] = '完美'

        @when_all(rule_362)
        def r_3(c):
            execute.results['大腿围36'] = '标准'

        @when_all(rule_363)
        def r_3(c):
            execute.results['大腿围36'] = '偏粗'

        @when_all(rule_364)
        def r_3(c):
            execute.results['大腿围36'] = '偏细'

    with ruleset('figure-detail-37'):
        @when_all(rule_371)
        def r_3(c):
            execute.results['小腿围37'] = '完美'

        @when_all(rule_372)
        def r_3(c):
            execute.results['小腿围37'] = '标准'

        @when_all(rule_373)
        def r_3(c):
            execute.results['小腿围37'] = '偏粗'

        @when_all(rule_374)
        def r_3(c):
            execute.results['小腿围37'] = '偏细'

    with ruleset('figure-detail-38'):
        @when_all(rule_381)
        def r_3(c):
            execute.results['脚踝38'] = '完美'

        @when_all(rule_382)
        def r_3(c):
            execute.results['脚踝38'] = '标准'

        @when_all(rule_383)
        def r_3(c):
            execute.results['脚踝38'] = '偏粗'

        @when_all(rule_384)
        def r_3(c):
            execute.results['脚踝38'] = '偏细'

    with ruleset('figure-part-21'):
        # part of body
        @when_all(rule_211)
        def r_211(c):
            execute.results['头肩比21'] = '完美'

        @when_all(rule_212)
        def r_212(c):
            execute.results['头肩比21'] = '标准'

        @when_all(rule_213)
        def r_213(c):
            execute.results['头肩比21'] = '有待改善'

    with ruleset('figure-part-22'):
        @when_all(rule_221)
        def r_221(c):
            execute.results['头身比22'] = '八头身'

        @when_all(rule_222)
        def r_222(c):
            execute.results['头身比22'] = '标准'

        @when_all(rule_223)
        def r_223(c):
            execute.results['头身比22'] = '有待改善'

    with ruleset('figure-part-23'):
        @when_all(rule_231)
        def r_231(c):
            execute.results['腿身比23'] = '超长腿'
        
        @when_all(rule_232)
        def r_232(c):
            execute.results['腿身比23'] = '长腿'

        @when_all(rule_233)
        def r_233(c):
            execute.results['腿身比23'] = '标准腿'

        @when_all(rule_234)
        def r_234(c):
            execute.results['腿身比23'] = '短腿'

    with ruleset('figure-part-24'):
        @when_all(rule_241)
        def r_241(c):
            execute.results['大小腿长比24'] = '黄金比例'

        @when_all(rule_242)
        def r_242(c):
            execute.results['大小腿长比24'] = '正常标准'

    with ruleset('figure-part-25'):
        @when_all(rule_251)
        def r_251(c):
            execute.results['腰臀比25'] = '黄金比例'

        @when_all(rule_252)
        def r_252(c):
            execute.results['腰臀比25'] = '肥胖'

        @when_all(rule_253)
        def r_253(c):
            execute.results['腰臀比25'] = '标准'

    with ruleset('figure-part-26'):
        @when_all(rule_261)
        def r_261(c):
            execute.results['胸型26'] = '胸外扩'

        @when_all(rule_262)
        def r_262(c):
            execute.results['胸型26'] = '标准胸型'

    with ruleset('figure-body'):
        # whole body
        @when_all(rule_121)
        def r_121(c):
            execute.results['身型12'] = '梨型身材'
        
        @when_all(rule_122)
        def r_122(c):
            execute.results['身型12'] = '苹果型身材'

        @when_all(rule_123)
        def r_123(c):
            execute.results['身型12'] = '直筒型身材'

        @when_all(rule_124)
        def r_124(c):
            execute.results['身型12'] = '沙漏型身材'

    with ruleset('figure-bmi'):
        # thin bmi
        @when_all(trule_half0)
        def thin(c):
            execute.results['BMI11'] = '偏瘦'

        @when_all(trule_half1)
        def thin_a(c):
            execute.results['BMI11'] = '偏瘦'
        # fat bmi

        @when_all(frule_half0)
        def fat(c):
            execute.results['BMI11'] = '偏胖'

        @when_all(frule_half1)
        def fat_a(c):
            execute.results['BMI11'] = '偏胖'
        # standard bmi

        @when_all(srule_half0)
        def normal(c):
            execute.results['BMI11'] = '标准'

        @when_all(srule_half1)
        def normal_a(c):
            execute.results['BMI11'] = '标准'
        # perfect bmi

        @when_all(prule_half0)
        def perfect(c):
            execute.results['BMI11'] = '完美'

        @when_all(prule_half1)
        def perfect_a(c):
            execute.results['BMI11'] = '完美'

register_rules()

