#!/usr/bin/python
# -*- coding: utf-8 -*-

# api.py: REST API for 3dmeasure
#   - receive some inputs: obj url; person infos
#   - call 3rd api, get the results.

import time
import json
from flask import request, jsonify, g
from playhouse.shortcuts import dict_to_model, update_model_from_dict

import db
import util
from client import rest_get, rest_post
from webutil import app, login_required, get_myself

import logging
log = logging.getLogger("api.measure")


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
                #2. GET. Send requestId to get final result.
                args = {"requestId" : request_id}
                s1, rsp1 = rest_get("metrics", args)
                sc = s1
                if s1 == 200:
                    m_result = rsp1['body'] 
                elif s1 == 202:
                    time.sleep(3)
                else:
                    break

            if sc != 200:
                rsp_code = 500
                result = {f"reason": "query measure result failed by request id:{request_id}."}
            else:
                # handl/parse result.
                rsp_code = 200
                result = handle_3d_measure_json(m_result)

            m.result = json.dumps(m_result)
    if not m.result:
        m.result = json.dumps(result)
    m.modified = m.created = util.utcnow()
    #m.creator = get_myself()
    m.save()

    return jsonify(result), rsp_code

def handle_3d_measure_json(m_result):
    g_required_map = {
        "Xiong": [144, 105, 106],
        "Yao": [108, 163, 1108, 1145, 1150, 107],
        "Tun": [109, 1109],
        "Tui": [141, 142, 136, 137],
        "Bi": [125, 126, 124, 122]
    }
    lp_required_map = {
        "Tou_CeWai": [212, 213],
        "Tou_QianYin": [212, 210, 213, 211],
        "Jian_GaoDi": [210, 211],
        "Body_QingXie": [204, 236],
        "Tui_XO": [226, 227, 234, 235]
    }
    try:
        girths = m_result['result']['metrics']['girths']
    except:
        girths = []
    try:
        ldmk_points = m_result['result']['metrics']['landmarkPoints']
    except:
        ldmk_points = []
    result = {"TiWei":{}, "TiTai":{}}

    g_result = result['TiWei']
    for _k, _ids in g_required_map.items():
        if g_result.get(_k, None) is None:
            g_result[_k] = []
        for girth in girths:
            if girth.get('id', 0) in _ids:
                g_result[_k].append(girth)
   
    lp_result = result['TiTai']
    for _k1, _ids1 in lp_required_map.items():
        if lp_result.get(_k1, None) is None:
            lp_result[_k1] = [] 
        for lp in ldmk_points:
            if lp.get('id', 0) in _ids1:
                lp_result[_k1].append(lp)
                
    return result
    #return m_result


@app.route('/api/movies/<id>', methods = ['PUT'])
@login_required(role='editor')
def movie_update(id):
    """Updates a movie and returns it."""

    input = request.json
    # don't update created/creator-fields
    input.pop("created", 0)
    input.pop("creator", 0)

    m = db.get_movie(id)
    update_model_from_dict(m, input)
    m.modified = util.utcnow()
    m.save()

    return jsonify(m), 200


@app.route('/api/movies/<id>', methods = ['DELETE'])
@login_required(role='editor')
def movie_delete(id):
    """Deletes a movie."""

    m = db.get_movie(id)
    m.delete_instance()

    return jsonify(m), 200

