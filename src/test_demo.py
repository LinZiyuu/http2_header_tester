from gen_req import check_file, save_mutated_data, gen_header_size_multi_req, gen_header_size_multi_req1
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
from helper_functions import _print_exception

verboselogs.install()
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', logger=logger)

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
    



    
def test_single_req(dn, port, attack_file_name,tls, verbose=False):

    h2client = H2Client(tls, verbose=verbose)
    frames = h2client.gen_all_frames(file_name=attack_file_name)
    h2client.send(dn=dn, port=port, frames=frames)
    h2client.recv_response2()


def test_stream_timeout(dn, port, attack_file_name,tls, verbose=False):

    h2client = H2Client(tls, verbose=verbose)
    frames = h2client.gen_all_frames(file_name=attack_file_name)
    # print(len(frames))
    # send header frame
    # 2 streams 24 frames
    # 0 12
    # 1
    try:
        h2client.send(dn=dn, port=port, frames=frames[0])
        # h2client.send_sequence2(frames=frames[12])
        # send continuation frame
        for i in range(10):
            time.sleep(5)
            h2client.send_sequence2(frames=frames[i+1])
            # h2client.send_sequence2(frames=frames[i+13])
        h2client.send_sequence2(frames=frames[11])
        valid = h2client.recv_response2()
        h2client.send_sequence2(frames=frames[12])
        for i in range(10):
            time.sleep(5)
            h2client.send_sequence2(frames=frames[i+13])
        # h2client.send_sequence2(frames=frames[10])
        # send data frame
        # h2client.send_sequence2(frames=frames[11])
        h2client.send_sequence2(frames=frames[23])
        valid = h2client.recv_response2()
    except Exception as e:
        # _print_exception()
        logger.warning(repr(e))
        print(False)
        return False
    
def check_if_cache_size_out_multi100(dn, port, tls, header_size, total_time, verbose=False):

    try:
        h2client = H2Client(tls, verbose=verbose)
        # cache_size = 
        req_list = gen_header_size_multi_req(domain=dn, num_stream=100)

        save_mutated_data(attack_type=f"{header_size}B",attack_req_list=req_list)
        frames = h2client.gen_all_frames(file_name=f"{header_size}B_attack_data.json")
        print(len(frames)) 
     
        sleep_time = float(total_time / len(frames) / 100)
        h2client.send(dn=dn, port=port, frames=frames[0])
        h2client.send_sequence2(frames=frames[1])
        # send other streams header
        for i in range(1,100):
            # time.sleep(0.1)
            h2client.send_sequence2(frames=frames[i*3])
            h2client.send_sequence2(frames=frames[i*3 + 1])
        # send data frame es
        for i in range(1, 100):
            # time.sleep(0.1)
            h2client.send_sequence2(frames=frames[i*3 + 2])


        valid = h2client.recv_response2()
        # valid = h2client.recv_response2()
        # valid = h2client.recv_response2()
        if valid:
            logger.success("the response is a valid http response")
        else:
            logger.warning("the response is not a valid http response")
        return valid
    except Exception as e:
        # _print_exception()
        logger.warning(repr(e))
        return False
    
def check_if_header_buffer_size_out_multi_stream(dn, port, tls, header_size, total_time, num_stream,verbose=False):
    '''
    # 只有一个header 一个continue 一个data
    '''
    try:
        h2client = H2Client(tls, verbose=verbose)

        req_list = gen_header_size_multi_req1(domain=dn, num_stream=num_stream,header_size=header_size)

        save_mutated_data(attack_type=f"{header_size}B",attack_req_list=req_list)
        frames = h2client.gen_all_frames(file_name=f"{header_size}B_attack_data.json")
        print(len(frames)) 

        # 空的时间比超时时间略小一点

        sleep_time = float(total_time / (num_stream+1))
        h2client.send(dn=dn, port=port, frames=frames[0])
        h2client.send_sequence2(frames=frames[1])

        # send other streams header
        for i in range(1,num_stream):
            time.sleep(sleep_time)
            h2client.send_sequence2(frames=frames[i*3])
            h2client.send_sequence2(frames=frames[i*3 + 1])
        
        # send  all data frame es
        for i in range(1, num_stream):
            h2client.send_sequence2(frames=frames[i*3 + 2])


        valid = h2client.recv_response2()
        # valid = h2client.recv_response2()
        # valid = h2client.recv_response2()
        if valid:
            logger.success("the response is a valid http response")
        else:
            logger.warning("the response is not a valid http response")
        return valid
    except Exception as e:
        # _print_exception()
        logger.warning(repr(e))
        return False

def check_if_timeout_by_send_header_and_continuation_frame(dn, port,attack_file_name, tls, time_sleep, verbose):

    h2client = H2Client(tls, verbose=verbose)
    frames = h2client.gen_all_frames(file_name=attack_file_name)
    # send header frame
    h2client.send(dn=dn, port=port, frames=frames[0])
    # send continuation frame
    for i in range(10):
        time.sleep(time_sleep)
        h2client.send_sequence2(frames=frames[i+1])

    # send data frame
    h2client.send_sequence2(frames=frames[11])
    valid = h2client.recv_response2()
    return valid

def detect_timeout_range_roughly(dn, port,attack_file_name, tls, verbose=False,lo=0, hi=1):
    while lo < hi:
        logger.info(f"checking if the timeout lays in [{lo}, {hi}]")
        if check_if_timeout_by_send_header_and_continuation_frame(dn, port,attack_file_name, tls, float(hi/10), verbose):
            logger.debug(f"the timeout is greater than {hi}")
            lo = hi
            hi *= 2
        else:
            logger.debug(f"the timeout is smaller than {hi}")
            break
    return lo, hi

if __name__ == '__main__':

    # test(dn='tencent.lzytest.tech', port=80, tls=False, attack_file_name='cl_attack_data.json',verbose=True)
    # test_timeout(dn='lzybunny2.b-cdn.net', port=443, tls=True, attack_file_name='cl_attack_data.json',verbose=True)
    # test_single_req(dn='lzybunny2.b-cdn.net', port=443, tls=True, attack_file_name='cl_attack_data3.json',verbose=True)
    # test_stream_timeout4(dn='lzybunny2.b-cdn.net', port=443, tls=True, attack_file_name='cl_attack_data3.json',verbose=True)
    # test_stream_timeout4(dn='127.0.0.1', port=85, tls=False, attack_file_name='2stream_attack_data.json',verbose=True)
    # check_if_cache_size_out_multi100(dn='127.0.0.1', port=85, tls=False, header_size=1, total_time=10, verbose=True)
    # check_if_cache_size_out_multi100(dn='lzybunny2.b-cdn.net', port=443, tls=True, header_size=1, total_time=10, verbose=True)
    check_if_header_buffer_size_out_multi_stream(dn='lzybunny2.b-cdn.net', port=443, tls=True, header_size=1024, total_time=10, num_stream=128,verbose=True)
    # test_single_req(dn='lzybunny2.b-cdn.net', port=443, tls=True, attack_file_name='cl_attack_data2.json',verbose=True)
    # test(dn='127.0.0.1', port=443, attack_file_name='te_attack_data.json')
    # test_multi_req(dn='127.0.0.1', port=85, tls=False, attack_file_name='hpack_attack2.json',verbose=True)
    # test_multi_req(dn='cl.lzytest.tech', port=443, tls=True, attack_file_name='hpack_attack2.json',verbose=True)
    # test_multi_req(dn='tencent.lzytest.tech', port=80, tls=False, attack_file_name='hpack_attack2.json',verbose=True)
    # test_multi_req(dn='127.0.0.1', port=80, tls=False, attack_file_name='hpack_attack_data.json',verbose=True)
    # test_multi_req(dn='linziyu-lzy-production.edgio.link', port=443, tls=True, attack_file_name='hpack_attack2.json',verbose=True)
    # test_multi_req(dn='lzy.freetls.fastly.net', port=443, tls=True, attack_file_name='hpack_attack2.json',verbose=True)


