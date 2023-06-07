
import time 
import datetime

from gen_req import save_mutated_data,save_mutated_data1,gen_single_header_frame_req,gen_all_single_header_frame_reqs,save_mutated_data2
from h2client import H2Client
import time 
import os
import datetime
import argparse
import coloredlogs
import logging
import verboselogs
import math
import socket
import uuid
import random
import string

verboselogs.install()
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', logger=logger)



def Send_single_header_frame(dn, port, tls, method,scheme,path,header_fileds,verbose=True):
    '''
    # 只有一个header z
    '''

    h2client = H2Client(tls, verbose=verbose)
    
    req_list = gen_single_header_frame_req(method=method,scheme=scheme,domain=dn, path=path,header_fileds=header_fileds,verbose=verbose)
    save_mutated_data1(header=header_fileds[0][0],attack_req_list=req_list)
    frames1 = h2client.gen_all_frames(file_name=f"test_{header_fileds[0][0]}_req.json")

    # 空的时间比超时时间略小一点
    # 第一个请求
    
    h2client.send(dn=dn,port=port,frames=frames1)
 

def test_all_single_header(dn, port, tls, method,scheme,path,verbose=True):
    '''
    # 只有一个header frame
    '''
    gen_all_single_header_frame_reqs(method="GET", scheme="https", domain="cl.lzytest.tech",path="/",verbose=True)

    h2client = H2Client(tls, verbose=verbose)
    
    req_list = gen_all_single_header_frame_reqs(method=method,scheme=scheme,domain=dn, path=path,verbose=verbose)
    save_mutated_data2(attack_req_list=req_list)
    frames = h2client.gen_all_frames(file_name="test_all_single_header_req.json")
    print(len(frames))
    # 空的时间比超时时间略小一点
    # 第一个请求
    
    # h2client.tls_setup_exchange(dn=dn,port=port)
    # h2client.initial_h2_exchange()
    for i in range(len(frames)):
        # 不等待响应
        time.sleep(0.1)
        # h2client.send_sequence2(frames=frames[i])
        h2client.send(dn=dn,port=port, frames=frames[i])




if __name__ == '__main__':


    # parser = argparse.ArgumentParser(description='Test HTTP/2')  # 2、创建参数对象
    # parser.add_argument('-dn', '--domain', default="127.0.0.1", type=str, help='IP of reverse proxy or domain')
    # parser.add_argument('-p', '--port', default=80, type=int, help='Port of reverse proxy')
    # parser.add_argument('--tls', default=False, type=bool, help='use https')
    # parser.add_argument('--method', default="GET", type=str, help='HTTP METHOD')
    # parser.add_argument('--path', default="/", type=str, help='url path')
    # parser.add_argument('--header_name',  help='header name')  
    # parser.add_argument('--header_value',  help='header value')  
    # parser.add_argument('-v', '--verbose', default=False , help='print')
    # args = parser.parse_args()  # 4、解析参数对象获得解析对象
    # dn, port, tls, = args.domain, args.port, args.tls
    # method,path ,verbose = args.method, args.path,args.verbose
    # header_name , header_value = args.header_name, args.header_value
    # header_fileds = [[header_name, header_value]]
    # print(header_fileds)
    # if tls:
    #     scheme ="https"
    # else:
    #     scheme = 'http'
    # Send_single_header_frame(dn, port, tls, method,scheme,path,header_fileds,verbose)
   
    # python3 main.py -dn "127.0.0.1" -p 80 --method "GET" --path "/" --header_name "accept" --header_value "*/*" -v True
    # Send_single_header_frame(dn="127.0.0.1", port=80, tls=False, method="GET",scheme="http",path="/",header_fileds=[["accept","*/*"]],verbose=True)
    test_all_single_header(dn="127.0.0.1", port=81, tls=False, method="GET",scheme="http",path="/",verbose=True)