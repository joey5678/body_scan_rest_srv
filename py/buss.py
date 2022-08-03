import os
import sys
import math
import random

from sklearn import datasets, linear_model


DEG = '°'
DESCS = [
    '你的头部处在一个非常标准的位置哦～',
    '你的头部有侧歪的倾向，长期会造成肌肉代偿，且影响美观哦',
    '你的头部处在非常健康美观的位置哦～',
    '你的头部有前引倾向，长期会导致颈椎突出，且严重影响你的气质哦',
    '你是非常健康标准的平肩，请保持哦～' ,
    '你有高低肩的倾向，左边肩高相较于右肩要高' ,
    '你有高低肩的倾向，右边肩高相较于左肩要高' ,
    '你的身体重心非常健康标准，请保持哦～' ,
    '你的身体重心有向左边倾斜的倾向' ,
    '你的身体重心有向右边倾斜的倾向' ,
    '你的腿型非常健康标准，请保持哦～' ,
    '你的腿型有O型腿倾向',
    '你的腿型有X型腿倾向'
]

desc_map = {
    411: {
        'name': '头侧歪',
        'result':'正常',
        'tag_str': '健康状态，请继续保持哦',
        'symptom_desc': "头弯向一侧是斜颈的现象，斜颈根据它的原因，主要是采取非手术治疗和手术治疗。如果是肌性的斜颈一般都是采用非手术治疗，以促进局部肿块的消散，包括局部热敷、按摩推拿，每天局部轻柔的推拿，适度的向健侧牵引头部，每天数次，睡觉时可以用沙袋固定头部于矫正位",
        'tip': ''
    },
    412: {
        'name': '头侧歪',
        'result':'侧歪',
        'tag_str': '头侧歪，有待改善',
        'symptom_desc': "头弯向一侧是斜颈的现象，斜颈根据它的原因，主要是采取非手术治疗和手术治疗。如果是肌性的斜颈一般都是采用非手术治疗，以促进局部肿块的消散，包括局部热敷、按摩推拿，每天局部轻柔的推拿，适度的向健侧牵引头部，每天数次，睡觉时可以用沙袋固定头部于矫正位",
        'tip': '如果是生活习惯引起，平时请端正坐姿,坐的时候抬头挺胸、头放正,避免不良的看书习惯,才可以纠正头倾斜'
    },

    421: {
        'name': '头前引',
        'result':'正常',
        'tag_str': '健康状态，请继续保持哦',
        'symptom_desc': "头前伸也叫头部前引，通常表现为头部相对肩膀往前移动，经常出现于面对电脑工作者、坐姿不正确久坐者、经常使用手机者、不良体态的人群中。",
        'tip': ''
    },
    422: {
        'name': '头前引',
        'result':'前引',
        'tag_str': '头前引，有待改善',
        'symptom_desc': "头前伸也叫头部前引，通常表现为头部相对肩膀往前移动，经常出现于面对电脑工作者、坐姿不正确久坐者、经常使用手机者、不良体态的人群中。",
        'tip': '首先需要纠正不良的姿势，行走的时候要挺胸抬头，夜晚睡眠时要保持仰卧位姿势。每天坚持做靠墙站立的动作，站立时头肩部后仰，尽量靠在墙壁上，每次20-30分钟，每天做2次。'
    },

    431: {
        'name': '高低肩',
        'result':'正常',
        'tag_str': '健康状态，请继续保持哦',
        'symptom_desc': "高低肩，就是由于不正确的背包姿势，或者长期背单肩包导致人体两肩不一样高的现象。",
        'tip': ''
    },
    432: {
        'name': '高低肩',
        'result':'左高',
        'tag_str': '高低肩（左高），有待改善',
        'symptom_desc': "高低肩，就是由于不正确的背包姿势，或者长期背单肩包导致人体两肩不一样高的现象。",
        'tip': '提肩练习者配合呼吸做提肩胛骨及放松的动作，先双肩向上提，吸气，持续一分钟，然后放松，呼气，如是者做二十次，每天一次。'
    },
    433: {
        'name': '高低肩',
        'result':'右高',
        'tag_str': '高低肩（右高），有待改善',
        'symptom_desc': "高低肩，就是由于不正确的背包姿势，或者长期背单肩包导致人体两肩不一样高的现象。",
        'tip': '提肩练习者配合呼吸做提肩胛骨及放松的动作，先双肩向上提，吸气，持续一分钟，然后放松，呼气，如是者做二十次，每天一次。'
    },

    441: {
        'name': '身体倾斜',
         'result':'正常',
        'tag_str': '健康状态，请继续保持哦',
        'symptom_desc': "脊椎侧弯这种情况通常和坐姿有很大的关系，脊柱侧弯会对生活造成很大的影响。严重者会感到腰部分酸疼",
        'tip': ''
    },
    442: {
        'name': '身体倾斜',
        'result':'左倾斜',
        'tag_str': '身体向左倾斜，有待改善',
        'symptom_desc': "脊椎侧弯这种情况通常和坐姿有很大的关系，脊柱侧弯会对生活造成很大的影响。严重者会感到腰部分酸疼",
        'tip': '可以尝试做引体向上的锻炼，如果是侧弯比较严重的，需要及时进行手术的治疗，纠正患者脊椎的异常情况'
    },
    443: {
        'name': '身体倾斜',
        'result':'右倾斜',
        'tag_str': '身体向右倾斜，有待改善',
        'symptom_desc': "脊椎侧弯这种情况通常和坐姿有很大的关系，脊柱侧弯会对生活造成很大的影响。严重者会感到腰部分酸疼",
        'tip': '可以尝试做引体向上的锻炼，如果是侧弯比较严重的，需要及时进行手术的治疗，纠正患者脊椎的异常情况'
    },

    451: {
        'name': '异形腿',
         'result':'正常',
        'tag_str': '健康状态，请继续保持哦',
        'symptom_desc': "因为长期不科学的生活姿势和不合理发力习惯，会导致人体肌肉力量的不对称或者代偿，从而易导致体态出现诸多问题，轻者影响美观，重者会影响生活及健康状况。",
        'tip': ''
    },
    452: {
        'name': '异形腿',
        'result':'O型腿',
        'tag_str': 'O型腿，有待改善',
        'symptom_desc': "因为长期不科学的生活姿势和不合理发力习惯，会导致人体肌肉力量的不对称或者代偿，从而易导致体态出现诸多问题，轻者影响美观，重者会影响生活及健康状况。",
        'tip': '日常生活中不要翘二郎腿、盘坐、跪坐等 调整站姿 调整走路姿势'
    },
    453: {
        'name': '异形腿',
        'result':'X型腿',
        'tag_str': 'X型腿，有待改善',
        'symptom_desc': "因为长期不科学的生活姿势和不合理发力习惯，会导致人体肌肉力量的不对称或者代偿，从而易导致体态出现诸多问题，轻者影响美观，重者会影响生活及健康状况。",
        'tip': '日常生活中不要翘二郎腿、盘坐、跪坐等 调整站姿 调整走路姿势'
    },
    461: {
        'result':'胸外扩',
        'tag_str': '胸外扩，有待改善',
        'symptom_desc': "胸型外扩是指乳房向两边长，形不成乳沟，影响美观。",
        'tip': '建议穿具有调整胸型的内衣，多做胸部运动或者多做健美操让胸部坚挺，需要长时间坚持锻炼。'
    },
    462: {
        'result':'标准胸型',
        'tag_str': '标准胸型，有待改善',
        'symptom_desc': "胸型外扩是指乳房向两边长，形不成乳沟，影响美观。",
        'tip': ''
    },

}

def get_xyz(points):
    xyz = points['position']
    return xyz['x'], xyz['y'], xyz['z']

#calculate the distance_Z of (ltp-lsp) and (rtp-rsp)
def cal_head_qianyin(ls_points, rs_points, lt_points, rt_points, coef=1.):
    _desc = DESCS[2]
    if not all((ls_points, rs_points, lt_points, rt_points)):
        dis = round(random.uniform(2, 5), 1)
        return desc_map[421]
    _, _, ltz = get_xyz(lt_points)
    _, _, lsz = get_xyz(ls_points)
    _, _, rtz = get_xyz(rt_points)
    _, _, rsz = get_xyz(rs_points)
    #print(lsz, rsz, ltz, rtz)
    dis = round((ltz - lsz + rtz - rsz) * coef * 100 /2, 1)
    cls_num = 421 if dis < 6. else 422
    return desc_map[cls_num]

    # rst_str = "正常" if dis < 6. else "前引"
    # _desc = DESCS[2] if dis < 6. else DESCS[3]
    # return {"name":"头前引", "value": dis, "unit": "cm", "result": rst_str, "description": _desc}

def cal_head_cewai(lt_points, rt_points):
    _desc = DESCS[0]
    if not all((lt_points, rt_points)):
        degree = round(random.uniform(-4, 4), 1)
        return desc_map[411]
    x0, y0, z0 = get_xyz(lt_points)
    x1, y1, z1 = get_xyz(rt_points)
    d_x = abs(x0 - x1)
    d_y = y1 - y0
    degree =  round(math.atan2((d_y), d_x)/math.pi * 180, 1)
    cls_num = 411 if abs(degree) < 5. else 412
    return desc_map[cls_num]

    # rst_str = "正常" if abs(degree) < 5. else "侧歪" 
    # _desc = DESCS[0] if abs(degree) < 5. else DESCS[1]
    # if degree > 0:
    #     description = f"head {abs(degree)} degree to the left."
    # elif degree < 0:
    #     description = f"head {abs(degree)} degree to the right."
    # else:
    #     description = "head no left no right."
    # return {"name":"头侧歪", "value": degree, "unit": DEG, "result": rst_str, "description": _desc }


def cal_shoulder_gaodi(ls_points, rs_points):
    _desc = DESCS[4]
    if not all((ls_points, rs_points)):
       d_h = round(random.uniform(-1, 1), 1) 
       return desc_map[431]
    h_ls = ls_points['level']
    h_rs = rs_points['level']
    d_h = round((h_ls - h_rs) * 100, 1)
    cls_num = 431 if abs(d_h) < 2. else (432 if d_h > 2. else 433)
    return desc_map[cls_num]

    # rst_str = "正常" if abs(d_h) < 2. else ("左高" if d_h > 2. else "右高")
    # _desc =  DESCS[4] if abs(d_h) < 2. else (DESCS[5] if d_h > 2. else DESCS[6])
    # if d_h > 0:
    #     description = f"left shoulder {abs(d_h)} cm higher than right. "
    # elif d_h < 0:
    #     description = f"right shoulder {abs(d_h)} cm higher than left. "
    # else:
    #     description = "shoulders are same height. "
    # return {"name":"高低肩", "value": d_h, "unit":"cm", "result": rst_str,  "description": _desc}


def cal_body_qingxie(cc_points, crotch_points):
    _desc = DESCS[7]
    if not all((cc_points, crotch_points)):
        degree = round(random.uniform(-2, 2), 1)
        return desc_map[441]
    x0, y0, z0 = get_xyz(cc_points) 
    x1, y1, z1 = get_xyz(crotch_points)
    d_x = x0 - x1
    d_y = abs(y0 - y1)
    degree =  round(math.atan2((d_x), d_y)/math.pi * 180, 1)
    cls_num =  441 if abs(degree) < 3. else (442 if degree > 3 else 443)
    return desc_map[cls_num]

    # rst_str =  "正常" if abs(degree) < 3. else ("左倾斜" if degree > 3 else "右倾斜")
    # _desc = DESCS[7] if abs(degree) < 3. else (DESCS[8] if degree > 3 else DESCS[9])
    # if degree > 0:
    #     description = f"body {abs(degree)} degrees to left."
    # elif degree < 0:
    #     description = f"body {abs(degree)} degrees to right."
    # else:
    #     description = f"body no tilt."
    # return {"name":"身体倾斜", "value": degree, "unit":DEG, "result": rst_str, "description": _desc}


def cal_leg_xo(rof_points, lof_points, lkc_points, rkc_points):
    _desc = DESCS[10]
    if not all((rof_points, lof_points, lkc_points, rkc_points)):
       degree = round(random.uniform(170, 195), 1) 
       return desc_map[451]
    x0, y0, _ = get_xyz(lof_points)
    x1, y1, _ = get_xyz(rof_points)
    x2, y2, _ = get_xyz(lkc_points)
    x3, y3, _ = get_xyz(rkc_points)
    print(f"[lk, lo, ro, rk]: [{x2}, {x0}, {x1}, {x3}]") 
    d_ly = y0 - y2
    d_lx = x2 - x0
    d_ry = y1 - y3
    d_rx = x1 - x3
    print(f"[d_lx, d_rx]: [{d_lx}, {d_rx}]")
    degree_l = math.atan2((d_ly), d_lx)/math.pi * 180
    degree_r = math.atan2((d_ry), d_rx)/math.pi * 180
    print(f"d_l, d_r: {degree_l}, {degree_r}")
    degree = round(degree_l + degree_r, 1)
    cls_num =  451 if 160 < degree < 200 else (452 if degree > 200 else 453) 
    return desc_map[cls_num]

    # rst_str =  "正常" if 160 < degree < 200 else ("O型腿" if degree > 200 else "X型腿") 
    # _desc = DESCS[10] if 160 < degree < 200 else (DESCS[11] if degree > 200 else DESCS[12]) 
    # return {"name":"异形腿", "value": degree, "unit":DEG, "result": rst_str, "description": _desc}   


def fit_scale(points):
    if not points:
        return [1.]
    y_list = []
    meter_list = []
    for pdata in points:
        y_list.append([float(pdata['position']['y'])])
        meter_list.append([float(pdata['level'])])
    
    regr = linear_model.LinearRegression()
    regr.fit(y_list, meter_list)    
    
    return regr.coef_[0]

if __name__ == "__main__":
    data = {
        "TiTai": {
            "Body_QingXie": [
                {
                    "id": 204,
                    "label": "Centre Chest Point",
                    "level": 1.4652716114087618,
                    "position": {
                        "x": 0.018759065077848615,
                        "y": 1.4525876177376724,
                        "z": 0.0717124540087434
                    },
                    "refid": "Iso-8559-1-3-1-12"
                },
                {
                    "id": 236,
                    "label": "Crotch Point",
                    "level": 0.8663249306612397,
                    "position": {
                        "x": 0.019983360462025042,
                        "y": 0.8536409369901503,
                        "z": 0.012029498815536499
                    },
                    "refid": "Iso-8559-CrotchPoint"
                }
            ],
            "Jian_GaoDi": [
                {
                    "id": 210,
                    "label": "Left Shoulder Point",
                    "level": 1.5367750124741382,
                    "position": {
                        "x": 0.2603774980878077,
                        "y": 1.5240910188030488,
                        "z": -0.05960560766564105
                    },
                    "refid": "Iso-8559-1-3-1-1l"
                },
                {
                    "id": 211,
                    "label": "Right Shoulder Point",
                    "level": 1.5415120925485117,
                    "position": {
                        "x": -0.19292285717025537,
                        "y": 1.5288280988774223,
                        "z": -0.04777749858613678
                    },
                    "refid": "Iso-8559-1-3-1-1r"
                }
            ],
            "Tou_CeWai": [
                {
                    "id": 212,
                    "label": "Left Tragion Point",
                    "level": 1.7157443656922005,
                    "position": {
                        "x": 0.11062127796449905,
                        "y": 1.703060372021111,
                        "z": -0.01595818074320373
                    },
                    "refid": "Iso-8559-1-3-1-3l"
                },
                {
                    "id": 213,
                    "label": "Right Tragion Point",
                    "level": 1.7019171548014433,
                    "position": {
                        "x": -0.05411577119808418,
                        "y": 1.689233161130354,
                        "z": -0.020456207481247782
                    },
                    "refid": "Iso-8559-1-3-1-3rl"
                }
            ],
            "Tou_QianYin": [
                {
                    "id": 210,
                    "label": "Left Shoulder Point",
                    "level": 1.5367750124741382,
                    "position": {
                        "x": 0.2603774980878077,
                        "y": 1.5240910188030488,
                        "z": -0.05960560766564105
                    },
                    "refid": "Iso-8559-1-3-1-1l"
                },
                {
                    "id": 211,
                    "label": "Right Shoulder Point",
                    "level": 1.5415120925485117,
                    "position": {
                        "x": -0.19292285717025537,
                        "y": 1.5288280988774223,
                        "z": -0.04777749858613678
                    },
                    "refid": "Iso-8559-1-3-1-1r"
                },
                {
                    "id": 212,
                    "label": "Left Tragion Point",
                    "level": 1.7157443656922005,
                    "position": {
                        "x": 0.11062127796449905,
                        "y": 1.703060372021111,
                        "z": -0.01595818074320373
                    },
                    "refid": "Iso-8559-1-3-1-3l"
                },
                {
                    "id": 213,
                    "label": "Right Tragion Point",
                    "level": 1.7019171548014433,
                    "position": {
                        "x": -0.05411577119808418,
                        "y": 1.689233161130354,
                        "z": -0.020456207481247782
                    },
                    "refid": "Iso-8559-1-3-1-3rl"
                }
            ],
            "Tui_XO": [
                {
                    "id": 234,
                    "label": "Left Front Foot Point",
                    "level": 0.012681469455305794,
                    "position": {
                        "x": 0.0125049931262858,
                        "y": -2.5242157836169454e-06,
                        "z": 0.3441069260193653
                    },
                    "refid": "Iso-8559-LeftFrontFootPoint"
                },
                {
                    "id": 235,
                    "label": "Right Front Foot Point",
                    "level": 0.012681042842272117,
                    "position": {
                        "x": 0.019962502850974558,
                        "y": -2.9508288172941377e-06,
                        "z": 0.344151465952938
                    },
                    "refid": "Iso-8559-RightFrontFootPoint"
                }
            ]
        }
    }
    tt1 = data['TiTai']['Tou_CeWai']
    print(cal_head_cewai(tt1[0], tt1[1]))

    tt2 = data['TiTai']['Jian_GaoDi']
    print(cal_shoulder_gaodi(tt2[0], tt2[1]))

    tt3 = data['TiTai']['Body_QingXie']
    print(cal_body_qingxie(tt3[0], tt3[1]))
    
    tt4 = data['TiTai']['Tou_QianYin']
    print(cal_head_qianyin(tt4[0], tt4[1], tt4[2], tt4[3]))
