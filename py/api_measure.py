#!/usr/bin/python
# -*- coding: utf-8 -*-

# api.py: REST API for 3dmeasure
#   - receive some inputs: obj url; person infos
#   - call 3rd api, get the results.

import collections
import time
import json
import random
from pathlib import Path
from flask import request, jsonify, g
from playhouse.shortcuts import dict_to_model, update_model_from_dict

import db
import util
import red
from client import rest_get, rest_post
from webutil import app, login_required, get_myself

from buss import *

#from rule import execute as rule_exec_f
#from rule_m import execute_m as rule_exec_m
#from rule import reset_rule_results, current_result, get_eval_collection

from rule import execute as rule_exec_f
from rule import reset_rule_results as reset_rule_results_f
from rule import current_result as current_result_f
from rule import get_eval_collection as get_eval_collection_f

from rule_m import execute_m as rule_exec_m
from rule_m import reset_rule_results as reset_rule_results_m
from rule_m import current_result as current_result_m
from rule_m import get_eval_collection as get_eval_collection_m

from rule_cli import new_figure
import logging
log = logging.getLogger("api.measure")

# connect ws server:
from websocket import create_connection
ws = create_connection("ws://127.0.0.1:9001")
print("Receiving after creating conn...")
print(ws.recv())

ws.send('{"type": "connect", "data": {"websrv":"1"}}')
print("Receiving after sending connect msg")
result =  ws.recv()
print("Received '%s'" % result)


W_Dict = {
    144: "胸围",
    105: "(上)胸围",
    106: "(下)胸围",
    108: "腰围",
    107: "腹围",
    109: "臀围",
    141: "腿围(左大腿)",
    142: "腿围(右大腿)",
    125: "臂围(左上臂)",
    126: "臂围(右上臂)"
}

def safe_div(x, y):
    x = float(x)
    y = float(y)
    return x / y if y != 0. else 0

def to_zh(num, en=""):
    return W_Dict.get(num, en)

def rest_post_with_try(body_json, try_times=4):
    s = 501
    rsp = None
    if try_times <= 0:
        try_times = 3
    for ttime in range(try_times):
        try:
            s, rsp = rest_post("measure", body=body_json)
        except:
            log.error(f"\nCall 3th POST method error, tried {ttime +1} times.\n")
            time.sleep(4)#4
        else:
            break
    if rsp is None:
        rsp = {"statusCode": s, "data":""}
    return s, rsp

@app.route('/api/measures/', methods = ['GET'])
def measure_query():
    """Not Implementation"""

    #input = request.args

    return jsonify([]), 200


@app.route('/api/measure/<id>', methods = ['GET'])
def measure_get(id):
    """Returns a single measure, or 404."""

    m = db.get_measure(id)
    return jsonify(m), 200

@app.route('/api/scan', methods = ['POST'], strict_slashes=False)
def scan3d():
    in_json = request.json

    print(in_json)
    dev_id = in_json['dev_id']
    ts = in_json['time_stamp']
    _ws_key = f"{dev_id}:{ts}"

    print(f"-------------wskey: {_ws_key}")

    _res = red.get_keyval(_ws_key)
    if _res is not None: 
        if _res.get('data', None) is not None:
            return jsonify(_res), 200
        else:
            return jsonify(_res), 500
    else:
        red.set_keyval(_ws_key, {'result': 'None'})

    global ws

    print("Sending launch request message")
    ws.send('{"type": "request_launch", "data": {"dev_id":"%s"}}' % dev_id)
    print("Receiving...")
    result =  ws.recv()
    print("Received '%s'" % result)
    tout = 300
    tcount = 0
    while True:
        if tcount > tout:
            print("------------waiting timeout----------------.")
            return jsonify({'result': 'timeout to wait scan result'}), 200
        print("waiting launch result message")
        result =  ws.recv()
        print("Received '%s'" % result)
        json_msg = json.loads(result)
        if json_msg['type'] == 'return_launch':
            print("received launch result, request finished.")
            print(json_msg)
            red.set_keyval(_ws_key, json_msg)
            break
        time.sleep(10)
        tcount += 10

    return jsonify(json_msg), 200

@app.route('/api/scan/', methods = ['GET'])
def scan_query():
    args = request.args
    print(args)
    dev_id = args.get('dev_id', 0)
    ts = args.get('ts', 0)

    _key = f"{dev_id}:{ts}"
    _val = red.get_keyval(_key) 
    if _val is not None and _val.get('data', None) is not None:
        return jsonify(_val), 200
    
    return jsonify({'result':"no result"}), 201


@app.route('/api/measure', methods = ['POST'], strict_slashes=False)
#@login_required(role='editor')
def measure_me():
    cos_path = 'https://fitshike.oss-cn-hangzhou.aliyuncs.com/'
    """Creates a measure and returns measure result."""
    input_check = True
    rsp_code = 200
    result = {}
    log.warn("\n------Request Received and Start handling ----- \n")
    log.debug(f"[debug]...headers....{request.headers}")
    log.debug(f"[debug]...data....{request.data}")
    log.debug(f"[debug]...cookies ....{request.cookies  }")
    input = request.json
    input.pop("id", 0) # ignore id if given, is set by db

    m = dict_to_model(db.Measure, input, ignore_unknown=True)
    _weight =  input.get('weight', 0) 
    log.info(f"input of post: {m}")

    # Update: receive dev_id, the call websocket to notify device to execute scan
    # device will scan and upload the obj file to cloud and return the obj path
    # m_dev_id = m.dev_id
    # if not m_dev_id:
    #     input_check = False
    #     rsp_code = 403
    #     result = {"reason": "Not get the device id(dev_id) in request."}
    #     return jsonify(result), rsp_code
    # global ws
    # print("Sending launch request message")
    # ws.send('{"type": "request_launch", "data": {"dev_id":"%s"}}' % m_dev_id)
    # print("Receiving...")
    # result =  ws.recv()
    # print("Received '%s'" % result)

    # while True:
    #     print("waiting launch result message")
    #     result =  ws.recv()
    #     print("Received '%s'" % result)
    #     json_msg = json.loads(result)
    #     if json_msg['type'] == 'return_launch':
    #         print("received launch result, request finished.")
    #         print(json_msg)
    #         break
    #     time.sleep(10)

    #get measure result.
    # m_url = json_msg['data'].get('obj_file_path', None)
    m_url = m.file_path
    if not m_url:
        input_check = False
        rsp_code = 403
        result = {"reason": "Not get the obj file."}
    elif _weight <=0:
        _weight = 100
        rsp_code = 403
        result = {"reason": "Wrong Weight value."}
    elif not m_url.endswith("obj"):
        input_check = False
        rsp_code = 403
        result = {"reason": "the obj file url not end with obj."}
    else:
        #1.POST 
        # full_m_url = os.path.join(cos_path, m_url)
        # print(f"-------------full_m_url: {full_m_url}")
        body_json = {
            "type": "all",
            "fileurl": m_url,
            "orientation_matrix": "1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1",
            "filesource": "url",
            "filetype": "obj",
            "output": "json"
        }
        log.warn("Sending POST to measure method ....")
        #for ptime in range(ptry_times):
        #try:
        #s, rsp = rest_post("measure", body=body_json)
        s, rsp = rest_post_with_try(body_json)
        if s != 200 or rsp['statusCode'] != 200 or rsp.get('requestId', None) is None:
            rsp_code = 502
            result = {"reason": f"the 3th API invoke failed, received response: {rsp}"} 
            log.error("\n[Error] Submit POST to 3th API failed, EXIT Abnormal.\n")
        else:
            sc = 0
            m_result = None
            while sc != 200:
                try_times = 5
                request_id = rsp['requestId']
                if not m.request_id:
                    m.request_id = request_id
                log.warn(f"[Debug] request id: {request_id}")
                #2. GET. Send requestId to get final result.
                time.sleep(15)#15
                args = {"requestId" : request_id}
                for ttime in range(try_times):
                    try:
                        s1, rsp1 = rest_get("metrics", args)
                        sc = s1
                    except:
                        log.error(f"\nCall 3th Get method error, tried {ttime +1} times.\n")
                        time.sleep(4)#4
                    else:
                        break
                    
                if s1 == 200:
                    m_result = rsp1['body'] 
                    _height = rsp1['others']['height'] #this height is evaluated by 3d measure up
                    m_result['3mu_height'] = _height
                    m_result['height'] = _height * 100 or m.height
                    m_result['weight'] = _weight
                    m_result['gender'] = m.gender or 0
                    log.warn("Get the final result of measure data.")
                elif s1 == 202:
                    log.warn("Got 202 code when request the measure data, sleep a while...")
                    time.sleep(5)#5
                else:
                    log.error(f"[Error] not get the expected resp: {rsp1['body']} ")
                    break

            if sc != 200:
                rsp_code = 500
                log.debug(f"[Error] query measure result failed by request id:{request_id}.")
                result = {f"reason": f"query measure result failed by request id:{request_id}."}
            else:
                log.warn("Start to handling the measure data.....")
                # handl/parse result.
                rsp_code = 200
                #save to json file
                if True:
                    Path("results").mkdir(parents=True, exist_ok=True)
                    sv_json_name = Path(m_url).stem 
                    sv_json_path = Path("results") / f"{sv_json_name}.json"
                    with open(sv_json_path, 'w') as jf:
                       json.dump(m_result, jf)
                log.warn("[Info] Handling result from 3th.")
                rsp_code, result = handle_3d_measure_json(m_result)
                log.warn("[Debug] Handled result from 3th.")
            
            extra_dict = {}
            gender_str = m.gender
            if gender_str == 0:
                default_h5 = 'http://122.51.149.232:8088/wireframe.html?gender=0'
                std_weight_kg = (m.height - 70) * 0.6
            else:
                default_h5 = 'http://122.51.149.232:8088/wireframe.html?gender=1'
                std_weight_kg = (m.height -80) * 0.7

            delta_weight = round((m.weight/2 - std_weight_kg), 0)
            bmi_val = round(safe_div((m.weight * 50 * 100), (m.height * m.height)), 2)
            if bmi_val > 28:
                star_num = 1
            elif bmi_val >= 24:
                star_num = 2
            elif bmi_val >= 18.5:
                star_num = 4
            elif bmi_val < 18.5:
                star_num = 3
            elif delta_weight == 0:
                star_num = 5
            
            s_m_url = m_url[m_url.index('obj/')+4:]
            h5_link = f'http://122.51.149.232:8088/wireframe.html?gender={gender_str}&model_url={s_m_url}'

            result['EXTRA'] = {
                'star': star_num,
                'bmi': bmi_val,
                'delta_weight': delta_weight,
                'h5_default': default_h5,
                'h5': h5_link,
            }

            add_extra_info(result)
            m.result = json.dumps(m_result)
    if not m.result:
        m.result = json.dumps(result)
    m.modified = m.created = util.utcnow()
    #m.creator = get_myself()
    log.info(f"[Debug] Final result : {result}")
    m.save()
    log.warn("\n=================Request Processed.\n")

    return jsonify(result), rsp_code

def add_extra_info(result):
    pass


def new_tt_calculate(height, weight, gender, girths_data, lmpoints_data, slen_data):
    # titai 
    print("--------------------------GENDER ------------------------------------------------------------")
    print(gender)
    print("--------------------------GENDER .------------------------------------------------------------")
    figure_key_item = ('height', 'weight', 'height2',
                       'g_hip_167', 'g_shoulder_104', 'g_sum_167_104', 'g_waist_155', 'g_neck_140',
                       'g_bust_144', 'g_lbiceps_125', 'g_lwrist_123', 'g_rbiceps_126', 'g_rwrist_121', 'g_lmthigh_111',
                       'g_rmthigh_112', 'g_lmcalf_115', 'g_rmcalf_116', 'g_lankle_117', 'g_rankle_118',
                       'w_shoulder_210_211', 'w_busts_205_206', 'w_head_212_213', 'h_head_202', 'h_upper_body', 'h_knee',
                       'h_chin', 'h_leg_333_334', 'h_upper_leg', 'g_abdomen_161', 'g_waist_163', 'g_upper_chest_143')
    if gender == 0:
        reset_rule_results_f()
        #reset_rule_results_f() if gender ==0 else reset_rule_results_m()
        f = dict.fromkeys(figure_key_item, -1.)
        #print(f)
        print(f"================ height: {height}, weight: {weight}")
        M = collections.namedtuple('Metric', f)
        new_figure(M, f, height, weight, girths_data, lmpoints_data, slen_data)
        rule_exec_f(f)
        return current_result_f()
    else:
        reset_rule_results_m()
        f = dict.fromkeys(figure_key_item, -1.)
        #print(f)
        print(f"================ height: {height}, weight: {weight}")
        M = collections.namedtuple('Metric', f)
        new_figure(M, f, height, weight, girths_data, lmpoints_data, slen_data)
        rule_exec_m(f)
        return current_result_m()
    #rule_exec = rule_exec_f if gender == 0 else rule_exec_m
    #f_test = {'height': 173, 'weight': 60, 'height2': 300.15, 'g_hip_167': 105.7, 'g_shoulder_104': 105.7, 'g_sum_167_104': 211.4, 'g_waist_155': 90.0, 'g_neck_140': 44.8, 'g_bust_144': 111.7, 'g_lbiceps_125': 33.7, 'g_lwrist_123': 19.9, 'g_rbiceps_126': 34.3, 'g_rwrist_121': 20.4, 'g_lmthigh_111': 49.7, 'g_rmthigh_112': 51.3, 'g_lmcalf_115': 36.6, 'g_rmcalf_116': 36.0, 'g_lankle_117': 27.4, 'g_rankle_118': 34.5, 'w_shoulder_210_211': 43.7, 'w_busts_205_206': 22.9, 'w_head_212_213': 17.4, 'h_head_202': 25.0, 'h_upper_body': 95.7, 'h_knee': 50.6, 'h_chin': 148.2, 'h_leg_333_334': 77.5, 'h_upper_leg': 27.0, 'g_abdomen_161': 89.9, 'g_waist_163': 91.9, 'g_upper_chest_143': 111.3}

    #rule_exec(f_test)
    #rule_exec(f)
    #return current_result_f() if gender == 0 else current_result_m()

RC4_dict = {
    "TouCeWai": get_eval_collection_f(41) ,
    "TouQianYin": get_eval_collection_f(42),
    "GaoDiJian": get_eval_collection_f(43),
    "ShenTiQingXie":  get_eval_collection_f(44),
    "YiXingTui":  get_eval_collection_f(45),
}

TT_KEYS = [
    "TouCeWai",
    "TouQianYin",
    "GaoDiJian",
    "ShenTiQingXie",
    "YiXingTui",
]

Summary_dict = {
    "Head": [1, 2],
    "Shoulder": [3],
    "Leg": [5],
    "Other": [4]
}

def find_summary_key(item_id):
    # res = []
    for _k, _v in Summary_dict.items():
        if item_id in _v:
            return _k
    return None
    # return res

def merge_result(res_1, res_2):
    tt_v1 = res_1['TiTai']
    tw_v1 = res_1['TiWei']

    res_2['YiTai'] = {}  #加入之前计算的体态数据

    for _k, _v in tt_v1.items():
        rc = RC4_dict.get(_k, [])
        _v['result_collection'] = rc
        _v['type'] = TT_KEYS.index(_k) + 1
        res_2['YiTai'][_k] = _v
    
    # 将体围的值加进去
    wd_section = res_2['WeiDu']
    wd_keys = wd_section.keys()

    for _k, _list in tw_v1.items():
        if _k in wd_keys:
            _g = []
            for _v in _list:
                _g.append(_v['girth'])
            if len(_g) > 0:
                wd_section[_k]['girth'] = round((sum(_g) / len(_g)), 1)

    # dict to list
    result = {}
    for _k, cls_res in res_2.items():
        if _k == 'Summary':
            result[_k] = res_2[_k].copy()
            # add YiTai exception results to summary.
            for _, _v in res_2['YiTai'].items():
                if _v['result'] != '正常':
                    _vtype = _v['type']
                    sm_key = find_summary_key(_vtype)
                    if result[_k].get(sm_key, None) is None:
                        result[_k][sm_key] = []
                    result[_k][sm_key].append(_v.copy())
        else:
            if result.get(_k, None) is None:
                result[_k] = []
            if not isinstance(cls_res, dict):
                continue
            for _sk, cls_v in cls_res.items():
                if isinstance(cls_v, dict):
                    result[_k].append(cls_v)
                else:
                    result[_k].append({_sk: cls_v})

    return result

def handle_3d_measure_json(m_result):
    g_required_map = {
        "JingWei": [140],
        "YaoWei" : [155],
        "TunWei" : [167],
        "XiongWei": [144],
        "ShouBiWei": [125, 126],
        "DaTuiWei": [111, 112],
        "XiaoTuiWei": [115, 116],
        "JiaoHuai": [117, 118],
        # 'Bi': [125, 126],
        # "Xiong": [144, 105, 106],
        # "Yao": [108, 107],
        # "Tun": [109],
        # "Tui": [141, 142],
    }
    # list order is important
    lp_required_map = {
        "TouCeWai": [212, 213],
        "TouQianYin": [212, 210, 213, 211],
        "GaoDiJian": [210, 211],
        "ShenTiQingXie": [204, 236],
        "YiXingTui": [243, 244, 234, 235]
    }

    required_points = [] # [210, 211, 212, 213, 204, 236, ] #234, 235, 243, 244 ]
    required_gs = [] #[167, 104, 155, 144, 115, ]
    skipped_list = m_result.get("skippedMeasurements", [])
    skipped_ids = [ int(x.split(':')[0].strip()[1:-1]) for x in skipped_list]

    try:
        girths = m_result['result']['metrics']['girths']
    except:
        girths = []
    
    measured_gids = [g['id'] for g in girths]
    missed_gids = list(set(required_gs).difference(set(measured_gids)))
    if len(missed_gids) > 0:
        rsp_code = 406
        result = {
            "reason": f"Key Body Girths: {missed_gids} not measured, pls measure again."
        }
        return rsp_code, result

    coef = 1.
    try:
        ldmk_points = m_result['result']['metrics']['landmarkPoints']
    except:
        ldmk_points = []

    measured_pids = [p['id'] for p in ldmk_points]
    missed_pids = list(set(required_points).difference(set(measured_pids)))
    if len(missed_pids) > 0:
        rsp_code = 406
        result = {
            "reason": f"Key Body Points: {missed_pids} not measured, pls measure again."
        }
        return rsp_code, result

    try:
        slen_data = m_result['result']['metrics']['surfaceLengths']
    except:
        slen_data = []
    eval_height = m_result['height']

    try:
        coef = fit_scale(ldmk_points)
    except:
        coef = 1.
    log.info(f"got the coef : {coef}.")
    if isinstance(coef, list):
        coef = coef[0]

    result_v1 = {"TiWei":{}, "TiTai":{}}
    log.warn("[Debug] Handling TiWei .....\n")
    g_result = result_v1['TiWei']
    for _k, _ids in g_required_map.items():
        if g_result.get(_k, None) is None:
            g_result[_k] = []
        for girth in girths:
            if girth.get('id', 0) in _ids:
                g_result[_k].append({"id": girth['id'], "label": to_zh(girth['id'], girth['label']), "girth": round(girth['girth'][0] * 100, 1), "unit": "cm"})
    # handle exception case
    tui_tws = g_result.get('Tui', [])
    if len(tui_tws) == 1:
        got_id = tui_tws[0]['id']
        got_girth = tui_tws[0]['girth']
        missed_id = 142 if got_id == 141 else 141
        tui_tws.append({"id": missed_id, "label": to_zh(missed_id, "leg"), "girth": round(got_girth + random.uniform(0.1, 1), 1), "unit": "cm"})
    bi_tws = g_result.get('Bi', []) 
    if len(bi_tws) == 1:
        got_id = bi_tws[0]['id']
        got_girth = bi_tws[0]['girth']
        missed_id = 126 if got_id == 125 else 125
        bi_tws.append({"id": missed_id, "label": to_zh(missed_id, "arm"), "girth": round(got_girth + random.uniform(0.1, 1), 1), "unit": "cm"})
    xiong_tws = g_result.get('Xiong', [])
    for xog_item in xiong_tws:
        if xog_item['id'] == 105:
            xog_item['girth'] = round((xog_item['girth'] - random.uniform(2, 3)), 1)
        elif xog_item['id'] == 106:
            xog_item['girth'] = round((xog_item['girth'] - random.uniform(5, 8)), 1)
        else:
            xog_item['girth'] = round((xog_item['girth'] - random.uniform(4, 5)), 1)
        
    
    log.warn("[Debug] Handled TiWei.\n")
    lp_original_result = {}

    log.warn("[Debug] Handling TiTai .....\n")
    for _k1, _ids1 in lp_required_map.items():
        if lp_original_result.get(_k1, None) is None:
            lp_original_result[_k1] = [] 
        for lp in ldmk_points:
            if lp.get('id', 0) in _ids1:
                lp_original_result[_k1].append(lp)
    lp_result = result_v1['TiTai']
    log.info("[Debug] Evaling TiTai .....\n")
    eval_titai(lp_original_result, lp_result)  

    log.warn("[Debug] Extra: calculate new TiTai.\n")
    input_weight = m_result['weight']
    _gender = m_result.get('gender', 0)
    result_v2 = new_tt_calculate(eval_height/100, input_weight/2, _gender, girths, ldmk_points, slen_data)
    # result_v1['TiTai']['v2'] = new_tt_calculate(eval_height, input_weight, girths, ldmk_points, slen_data) 
    # 
    result = merge_result(result_v1, result_v2)          

    log.warn("[Debug] Handled TiTai .\n")
    return 200, result
    #return m_result

def eval_titai(titai_data, titai_result):
    cw_rst, qy_rst, gd_rst, qx_rst, xo_rst = None, None, None, None, None
    log.info(f"\n[Debug] TT Data:\n {titai_data}\n")
    for tt_k, tt_items in titai_data.items():
        tt_item_dict = {item['id']: item for item in tt_items}
        if tt_k == "TouCeWai":
            log.info("[Debug] Cal Ce Wai ...")
            cw_rst = cal_head_cewai(tt_item_dict.get(212, None), tt_item_dict.get(213, None))
            titai_result[f'{tt_k}'] = cw_rst
        elif tt_k == "TouQianYin":
            log.info("[Debug] Cal QianYin ...")
            qy_rst = cal_head_qianyin(tt_item_dict.get(210, None), tt_item_dict.get(211, None), tt_item_dict.get(212, None), tt_item_dict.get(213, None))
            titai_result[f'{tt_k}'] = qy_rst
        elif tt_k == "GaoDiJian":
            log.info("[Debug] Cal GaoDi ...")
            gd_rst = cal_shoulder_gaodi(tt_item_dict.get(210, None), tt_item_dict.get(211, None))
            titai_result[f'{tt_k}'] = gd_rst
        elif tt_k == "ShenTiQingXie":
            log.info("[Debug] Cal QingXie ...")
            qx_rst = cal_body_qingxie(tt_item_dict.get(204, None), tt_item_dict.get(236, None))
            titai_result[f'{tt_k}'] = qx_rst
        elif tt_k == "YiXingTui":
            log.info("[Debug] Cal XO ...")
            xo_rst = cal_leg_xo(tt_item_dict.get(243, None), tt_item_dict.get(244, None), tt_item_dict.get(234, None), tt_item_dict.get(235, None))
            titai_result[f'{tt_k}'] = xo_rst
