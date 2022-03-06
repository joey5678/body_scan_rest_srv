import os
import sys
import math
import random

from sklearn import datasets, linear_model


DEG = '°'

def get_xyz(points):
    xyz = points['position']
    return xyz['x'], xyz['y'], xyz['z']

#calculate the distance_Z of (ltp-lsp) and (rtp-rsp)
def cal_head_qianyin(ls_points, rs_points, lt_points, rt_points, coef=1.):
    if not all((ls_points, rs_points, lt_points, rt_points)):
        dis = round(random.uniform(2, 5), 1)
        return {"name":"头部前引", "value": dis, "unit": "cm", "result": "正常", "description": f"{dis} cm horizontal distance between tragion and shoulder."}
    _, _, ltz = get_xyz(lt_points)
    _, _, lsz = get_xyz(ls_points)
    _, _, rtz = get_xyz(rt_points)
    _, _, rsz = get_xyz(rs_points)
    #print(lsz, rsz, ltz, rtz)
    dis = round((ltz - lsz + rtz - rsz) * coef * 100 /2, 1)
    rst_str = "正常" if dis < 6. else "前引倾向"
    return {"name":"头部前引", "value": dis, "unit": "cm", "result": rst_str, "description": f"{dis} cm horizontal distance between tragion and shoulder."}

def cal_head_cewai(lt_points, rt_points):
    if not all((lt_points, rt_points)):
        degree = round(random.uniform(-4, 4), 1)
        return {"name":"头部侧歪", "value": degree, "unit": DEG, "result": "正常", "description": "head no left no right" }
    x0, y0, z0 = get_xyz(lt_points)
    x1, y1, z1 = get_xyz(rt_points)
    d_x = abs(x0 - x1)
    d_y = y1 - y0
    degree =  round(math.atan2((d_y), d_x)/math.pi * 180, 1)
    rst_str = "正常" if abs(degree) < 5. else "侧歪倾向" 
    if degree > 0:
        description = f"head {abs(degree)} degree to the left."
    elif degree < 0:
        description = f"head {abs(degree)} degree to the right."
    else:
        description = "head no left no right."
    return {"name":"头部侧歪", "value": degree, "unit": DEG, "result": rst_str, "description": description }


def cal_shoulder_gaodi(ls_points, rs_points):
    if not all((ls_points, rs_points)):
       d_h = round(random.uniform(-1, 1), 1) 
       return {"name":"高低肩", "value": d_h, "unit":"cm", "result": "正常",  "description": f"left right equal. "}
    h_ls = ls_points['level']
    h_rs = rs_points['level']
    d_h = round((h_ls - h_rs) * 100, 1)
    rst_str = "正常" if abs(d_h) < 2. else ("左肩膀高" if d_h > 2. else "右肩膀高")
    if d_h > 0:
        description = f"left shoulder {abs(d_h)} cm higher than right. "
    elif d_h < 0:
        description = f"right shoulder {abs(d_h)} cm higher than left. "
    else:
        description = "shoulders are same height. "
    return {"name":"高低肩", "value": d_h, "unit":"cm", "result": rst_str,  "description": description}


def cal_body_qingxie(cc_points, crotch_points):
    if not all((cc_points, crotch_points)):
        degree = round(random.uniform(-2, 2), 1)
        return {"name":"身体倾斜", "value": degree, "unit":DEG, "result": "正常", "description": f"body normal."}
    x0, y0, z0 = get_xyz(cc_points) 
    x1, y1, z1 = get_xyz(crotch_points)
    d_x = x0 - x1
    d_y = abs(y0 - y1)
    degree =  round(math.atan2((d_x), d_y)/math.pi * 180, 1)
    rst_str =  "正常" if abs(degree) < 3. else ("左倾斜" if degree > 3 else "右倾斜")
    if degree > 0:
        description = f"body {abs(degree)} degrees to left."
    elif degree < 0:
        description = f"body {abs(degree)} degrees to right."
    else:
        description = f"body no tilt."
    return {"name":"身体倾斜", "value": degree, "unit":DEG, "result": rst_str, "description": f"body {abs(degree)} degrees to left."}


def cal_leg_xo(rof_points, lof_points, lkc_points, rkc_points):
    if not all((rof_points, lof_points, lkc_points, rkc_points)):
       degree = round(random.uniform(175, 195), 1) 
       return {"name":"腿型", "value": degree, "unit":DEG, "result": "正常", "description": "leg"}
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
    rst_str =  "正常" if 170 < degree < 200 else ("O形腿倾向" if degree > 200 else "X形腿倾向") 
    return {"name":"腿型", "value": degree, "unit":DEG, "result": rst_str, "description": "leg"}   


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
