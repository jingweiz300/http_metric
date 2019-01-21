from bottle import Bottle,run,route,template,post,request
import json
import os
import logging
logging.basicConfig(filename='http_metric.log',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y/%m/%d %I:%M:%S ',
                    level=logging.DEBUG)

#配置路径，key为具体的类别，value为具体的路径
__PATHCONFIG__ = {
    "NBA":"/Users/zhoujingwei/PycharmProjects/job3/http_metric/NBA",
    "FIFA": "/Users/zhoujingwei/PycharmProjects/job3/http_metric/FIFA/",
    "CBA" : "/Users/zhoujingwei/PycharmProjects/job3/http_metric/CBA/"
}
#获取当日
def get_today():
    import time
    return time.strftime('%Y%m%d',time.localtime(time.time()))
#实例bottle
app = Bottle()
#路由/sharlook/<classone>/<classtwo>
#例如：访问127.0.0.1:9001/sharlook/network/cisco
#例如：访问127.0.0.1:9001/sharlook/network/hw
@app.post('/sharlook/:classone/:classtwo')
def sharlook(classone,classtwo):
    #获取常用请求信息打印
    req_info = {"Content-Type":request.get_header('Content-Type'),"Request":request.environ['bottle.request'],"Body_String":request._get_body_string()}
    logging.debug('RECEIVE ONE REQ:{}'.format(str(req_info)))
    try:
        if classone in __PATHCONFIG__.keys():
            #拼接目标文件路径
            locale_file = __PATHCONFIG__[classone] + '/' + 'metric_' + classone + '_' + classtwo + '_' + get_today()
            #转换字典，如果请求非json，此处会直接raise异常，建议该接口全部送json串，
            post_data = request.json
            #转换字符串
            str_data = json.dumps(post_data)
            #判断文件
            if not os.path.exists(locale_file):
                os.mkdir(os.path.dirname(locale_file))
            #落地文件
            with open(locale_file,'a')as f:
                f.write(str_data + '\n')
            logging.debug("File Has Been Writen Succeed In the {} :{}".format(locale_file,str_data))
            return 'Succeed'
        else:
            logging.warning('RECEIVE ONE ERROR PATH:{}'.format(request.url))
            return 'Path error!'
    except Exception as e:
        #返回异常
        logging.error(e)
        return 'Exception Error'
    finally:
        pass
#启动server
run(app,host='127.0.0.1',port='1234')
#测试
#curl -H "Content-Type:application-XPOST 127.0.0.1:1234/sharlook/CBA/nbalog -d '{"a":1,"b":9,"c":[1,2,"test"],"d":{"e":1}}'
