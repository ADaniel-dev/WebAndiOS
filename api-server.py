#coding=utf-8
defaultencoding = 'utf-8'
import os
import hashlib
import flask
from flask import request,jsonify
from flask import abort
import time
import json
from flask import Flask, redirect, url_for

app={100002:{'dev':'@cdappkey#','sit':'rhappkey124!','uat':'!CDappkey#'},100008:{'dev':'@dhy123appkey#','sit':'@dhy123appkey#','uat':'@dhy123appkey#'}}   #集中存放appid和appkey

class local_exp(Exception):
    def __init__(self):
        pass
    @classmethod
    def no_appid(cls):
        return {"code":9001,"msg":"failed","result":{"unRegState":"","reason":"appid is a required parameter, parameter missing"}}
    @classmethod
    def no_timestamp(cls):
        return {"code":9002,"msg":"failed","result":{"unRegState":"","reason":"timestamp is a required parameter, parameter missing"}}
    @classmethod
    def no_sig(cls):
        return {"code":9003,"msg":"failed","result":{"unRegState":"","reason":"signature is a required parameter, parameter missing"}}
    @classmethod
    def sig_error(cls):
        return {"code":9004,"msg":"failed","result":{"unRegState":"","reason":"signature is error"}}
    @classmethod
    def no_uid(cls):
        return {"code":9005,"msg":"failed","result":{"unRegState":"","reason":"union_id is a required parameter, parameter missing"}}
    @classmethod
    def no_silent_time(cls):
        return {"code":9006,"msg":"failed","result":{"unRegState":"","reason":"silent_time is a required parameter, parameter missing"}}

api_s=flask.Flask(__name__)

def sig_chk(appid,appkey,timestamp,sig):
    tmp_sig="appid=%s&appkey=%s&timestamp=%s"%(appid,appkey,timestamp)
    s=hashlib.md5(tmp_sig.encode()).hexdigest().upper()
    if s == sig:
        return s
    else:
        return
    #return sig

@api_s.route('/query_unreg',methods=['get','post'])
def query_unreg():
    if not request.args:
        abort(400)
    for i in dict(request.args):
        dd=json.loads(i)
    if not 'appId' in dd:
        return jsonify(local_exp.no_appid())
    elif not 'timestamp' in dd:
        return jsonify(local_exp.no_timestamp())
    elif not 'sign' in dd:
        return jsonify(local_exp.no_sig())
    elif not 'union_id' in dd:
        return jsonify(local_exp.no_uid())
    if not sig_chk(dd['appId'],app[dd['appId']]['sit'],dd['timestamp'],dd['sign']):
        return jsonify(local_exp.sig_error())
    if dd['appId'] == 100002:
        return jsonify({"code":0,"msg":"success","result":{"unRegState":0,"reason":""}})
    elif dd['appId'] == 100008:
        return jsonify({"code":0,"msg":"success","result":{"unRegState":0,"reason":"allow to unregister"}})
        # return jsonify({"code":0,"msg":"success","result":{"unRegState":1,"reason":"Transaction in progress,pls try again later"}})


@api_s.route('/do_unreg',methods=['get','post'])
def do_unreg():
    if not request.args :
        abort(400)
    for i in dict(request.args):
        dd = json.loads(i)
    if not 'appId' in dd:
        return jsonify(local_exp.no_appid())
    elif not 'timestamp' in dd:
        return jsonify(local_exp.no_timestamp())
    elif not 'sign' in dd:
        return jsonify(local_exp.no_sig())
    elif not 'union_id' in dd:
        return jsonify(local_exp.no_uid())
    elif not 'silent_time' in dd:
        return jsonify(local_exp.no_silent_time())
    if not sig_chk(dd['appId'],app[dd['appId']]['sit'],dd['timestamp'],dd['sign']):
        return jsonify(local_exp.sig_error())
    return jsonify({"code":0,"msg":"success"})

@api_s.route('/undo_unreg',methods=['get','post'])
def undo_unreg():
    if not request.args :
        abort(400)
    for i in dict(request.args):
        dd = json.loads(i)
    if not 'appId' in dd:
        return jsonify(local_exp.no_appid())
    elif not 'timestamp' in dd:
        return jsonify(local_exp.no_timestamp())
    elif not 'sign' in dd:
        return jsonify(local_exp.no_sig())
    elif not 'union_id' in dd:
        return jsonify(local_exp.no_uid())
    if not sig_chk(dd['appId'],app[dd['appId']]['sit'],dd['timestamp'],dd['sign']):
        return jsonify(local_exp.sig_error())
    return jsonify({"code":0,"msg":"success"})

@api_s.route('/test/<int:appid>',methods=['GET','POST'])
def test(appid):
    test_d=[{"appid":100002,"timestamp":int(time.time())},{"appid":100003,"timestamp":int(time.time())}]
    td=list(filter(lambda t: t["appid"] == appid, test_d))
    if len(td) == 0:
        abort(404)
    return jsonify({"aa":td[0]})

@api_s.route('/test1',methods=['POST','GET'])
def test1():
    # data=request.json
    # data=request.form
    #data=request.args.get("reason")
    data = request.args
    data = dict(data)
    print data,type(data)
    for i in data:
        print i,type(i)
        dd=json.loads(i)
        print dd,type(dd)
        # d_d=dict(i)
    # print d_d,type(d_d)
    # data=json.loads(data)
    # return jsonify({"bb":data})
    return jsonify(dd)

@api_s.route('/get_code_url/<string:phoneNum>/<string:type>')
def get_code(phoneNum,type):
    # redis-cli -c -h 10.101.72.69 -p 7000 -a hdiot HGET USERCENTER:Phone:code_18219205522_8 code
    Temp_Str = os.popen('redis-cli -c -h 10.101.72.69 -p 7000 -a hdiot HGET USERCENTER:Phone:code_"%s"_"%s" code"' % phoneNum % type).read()
    return jsonify({"code":Temp_Str})

@api_s.route('/clear_code_limit/<string:phone>')
def clear_code_limit(phone):
    Temp_Str = os.popen(('redis-cli -c -h 10.101.72.69 -p 7000 -a hdiot del USERCENTER:Phone:sum_"%s"_num')%phone).read()
    return jsonify({"status":Temp_Str})

#  ####新增静态页面
@api_s.route('/success/<name>')
def success(name):
    return 'send =====> %s' % name

@api_s.route('/send',methods = ['POST', 'GET'])
def send():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name = user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name = user))


if __name__== '__main__':
    api_s.run(debug=True)