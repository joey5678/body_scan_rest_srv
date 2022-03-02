import os
import sys
import math


def get_xyz(points):
    xyz = points['position']
    return xyz['x'], xyz['y'], xyz['z']

#calculate the distance_Z of (ltp-lsp) and (rtp-rsp)
def cal_head_qianyin(ls_points, rs_points, lt_points, rt_points):
    pass

def cal_head_cewai(lt_points, rt_points):
    x0, y0, z0 = get_xyz(lt_points)
    x1, y1, z1 = get_xyz(rt_points)
    d_x = abs(x0 - x1)
    d_y = y1 - y0
    return math.atan2((d_y), d_x)/math.pi * 180


def cal_shoulder_gaodi(ls_points, rs_points):
    h_ls = ls_points['level']
    h_rs = rs_points['level']
    return (h_ls - h_rs) * 100


def cal_body_qingxie(cc_points, crotch_points):
    x0, y0, z0 = get_xyz(cc_points) 
    x1, y1, z1 = get_xyz(crotch_points)
    d_x = x0 - x1
    d_y = abs(y0 - y1)
    return math.atan2((d_x), d_y)/math.pi * 180


def cal_leg_xo(lff_points, rff_points, lkc_points, rkc_points):
    pass


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

