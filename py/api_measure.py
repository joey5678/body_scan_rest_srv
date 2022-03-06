#!/usr/bin/python
# -*- coding: utf-8 -*-

# api.py: REST API for 3dmeasure
#   - receive some inputs: obj url; person infos
#   - call 3rd api, get the results.

import time
import json
from pathlib import Path
from flask import request, jsonify, g
from playhouse.shortcuts import dict_to_model, update_model_from_dict

import db
import util
from client import rest_get, rest_post
from webutil import app, login_required, get_myself

from buss import *
import logging
log = logging.getLogger("api.measure")


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

def to_zh(num, en=""):
    return W_Dict.get(num, en)

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


@app.route('/api/measure', methods = ['POST'], strict_slashes=False)
#@login_required(role='editor')
def measure_me():
    """Creates a measure and returns measure result."""
    input_check = True
    rsp_code = 200
    result = {}
    print(f"[debug]...headers....{request.headers}")
    #print(f"[debug]...auth....{request.auth}")
    print(f"[debug]...data....{request.data}")
    #print(f"[debug]...verify....{request.verify}")
    #print(f"[debug]...cert....{request.cert }")
    print(f"[debug]...cookies ....{request.cookies  }")
    input = request.json
    input.pop("id", 0) # ignore id if given, is set by db

    m = dict_to_model(db.Measure, input, ignore_unknown=True)
    log.info(f"input of post: {m}")
    #get measure result.
    m_url = m.file_path
    if not m_url:
        input_check = False
        rsp_code = 403
        result = {"reason": "Not get the obj file."}
    elif not m_url.startswith("http"):
        input_check = False
        rsp_code = 403
        result = {"reason": "the obj file url not start with http."}
    else:
        #1.POST 
        body_json = {
            "type": "all",
            "fileurl": m_url,
            "orientation_matrix": "1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1",
            "filesource": "url",
            "filetype": "obj",
            "output": "json"
        }
        log.info("Sending POST to measure method ....")
        s, rsp = rest_post("measure", body=body_json)
        if s != 200 or rsp['statusCode'] != 200 or rsp.get('requestId', None) is None:
            rsp_code = 502
            result = {"reason": f"the 3th API invoke failed, received response: {rsp}"} 
        else:
            sc = 0
            m_result = None
            while sc != 200:

                request_id = rsp['requestId']
                if not m.request_id:
                    m.request_id = request_id
                print(f"[Debug] get request id: {request_id}")
                #2. GET. Send requestId to get final result.
                time.sleep(5)
                args = {"requestId" : request_id}
                s1, rsp1 = rest_get("metrics", args)
                sc = s1
                if s1 == 200:
                    m_result = rsp1['body'] 
                elif s1 == 202:
                    time.sleep(5)
                else:
                    print(f"not get the expected resp: {resp1['body']} ")
                    break

            if sc != 200:
                rsp_code = 500
                print(f"[Error] query measure result failed by request id:{request_id}.")
                result = {f"reason": f"query measure result failed by request id:{request_id}."}
            else:
                # handl/parse result.
                rsp_code = 200
                #save to json file
                if True:
                    Path("results").mkdir(parents=True, exist_ok=True)
                    sv_json_name = Path(m_url).stem 
                    sv_json_path = Path("results") / f"{sv_json_name}.json"
                    with open(sv_json_path, 'w') as jf:
                       json.dump(m_result, jf)
                print("[Debug] Handling result from 3th.")
                result = handle_3d_measure_json(m_result)
                print("[Debug] Handled result from 3th.")

            m.result = json.dumps(m_result)
    if not m.result:
        m.result = json.dumps(result)
    m.modified = m.created = util.utcnow()
    #m.creator = get_myself()
    print(f"[Debug] Final result : {result}")
    m.save()

    return jsonify(result), rsp_code

def handle_3d_measure_json(m_result):
    g_required_map = {
        "Xiong": [144, 105, 106],
        "Yao": [108, 107],
        "Tun": [109],
        "Tui": [141, 142],
        "Bi": [125, 126]
    }
    # list order is important
    lp_required_map = {
        "Tou_CeWai": [212, 213],
        "Tou_QianYin": [212, 210, 213, 211],
        "Jian_GaoDi": [210, 211],
        "Body_QingXie": [204, 236],
        "Tui_XO": [243, 244, 234, 235]
    }
    required_points = [210, 211, 212, 213, 204, 236, 234, 235, 243, 244 ]
    skipped_list = m_result.get("skippedMeasurements", [])
    skipped_ids = [ int(x.split(':')[0].strip()[1:-1]) for x in skipped_list]

    try:
        girths = m_result['result']['metrics']['girths']
    except:
        girths = []
    
    coef = 1.
    try:
        ldmk_points = m_result['result']['metrics']['landmarkPoints']
    except:
        ldmk_points = []

    coef = fit_scale(ldmk_points)
    log.info(f"fit the coef : {coef}.")
    if isinstance(coef, list):
        coef = coef[0]

    result = {"TiWei":{}, "TiTai":{}}
    print("[Debug] Handling TiWei .....\n")
    g_result = result['TiWei']
    for _k, _ids in g_required_map.items():
        if g_result.get(_k, None) is None:
            g_result[_k] = []
        for girth in girths:
            if girth.get('id', 0) in _ids:
                g_result[_k].append({"id": girth['id'], "label": to_zh(girth['id'], girth['label']), "girth": round(girth['girth'][0] * 100, 1), "unit": "cm"})
    print("[Debug] Handled TiWei.\n")
   
    lp_original_result = {}

    print("[Debug] Handling TiTai .....\n")
    for _k1, _ids1 in lp_required_map.items():
        if lp_original_result.get(_k1, None) is None:
            lp_original_result[_k1] = [] 
        for lp in ldmk_points:
            if lp.get('id', 0) in _ids1:
                lp_original_result[_k1].append(lp)
    #print(lp_result)
    lp_result = result['TiTai']
    print("[Debug] Evaling TiTai .....\n")
    eval_titai(lp_original_result, lp_result)                
    print("[Debug] Handled TiWei .\n")
    return result
    #return m_result

def eval_titai(titai_data, titai_result):
    cw_rst, qy_rst, gd_rst, qx_rst, xo_rst = None, None, None, None, None
    print(f"\n[Debug] TT Data:\n {titai_data}\n")
    for tt_k, tt_items in titai_data.items():
        tt_item_dict = {item['id']: item for item in tt_items}
        if tt_k == "Tou_CeWai":
            print("[Debug] Cal Ce Wai ...")
            cw_rst = cal_head_cewai(tt_item_dict.get(212, None), tt_item_dict.get(213, None))
            titai_result[f'{tt_k}_Result'] = cw_rst
        elif tt_k == "Tou_QianYin":
            print("[Debug] Cal QianYin ...")
            qy_rst = cal_head_qianyin(tt_item_dict.get(210, None), tt_item_dict.get(211, None), tt_item_dict.get(212, None), tt_item_dict.get(213, None))
            titai_result[f'{tt_k}_Result'] = qy_rst
        elif tt_k == "Jian_GaoDi":
            print("[Debug] Cal GaoDi ...")
            gd_rst = cal_shoulder_gaodi(tt_item_dict.get(210, None), tt_item_dict.get(211, None))
            titai_result[f'{tt_k}_Result'] = gd_rst
        elif tt_k == "Body_QingXie":
            print("[Debug] Cal QingXie ...")
            qx_rst = cal_body_qingxie(tt_item_dict.get(204, None), tt_item_dict.get(236, None))
            titai_result[f'{tt_k}_Result'] = qx_rst
        elif tt_k == "Tui_XO":
            print("[Debug] Cal XO ...")
            xo_rst = cal_leg_xo(tt_item_dict.get(243, None), tt_item_dict.get(244, None), tt_item_dict.get(234, None), tt_item_dict.get(235, None))
            titai_result[f'{tt_k}_Result'] = xo_rst


    


