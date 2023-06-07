from mutation import *
import json
import os

def gen_header_frame(method, scheme, authority, path ,flags, id,header_fileds,verbose=True):
    # TODO: 对:authority、:method、:scheme修改
    # * 1. :method 目标URL模式部分(请求)
    # * 2. :scheme 目标URL模式部分(请求) 
    # * 3. :authority 目标URL认证部分(请求)
    # * 4. :path 
    # header fileds = []
    if verbose:
        path = "/?reqid=%s" %id
    head_frame =  {"<headers-frame-%s>"%id: {":method": method, ":scheme": scheme, ":authority": authority, ":path": path,"flags": flags}}
    for i in range(len(header_fileds)):
        head_frame["<headers-frame-%s>"%id][header_fileds[i][0]] = header_fileds[i][1]
    return head_frame

def gen_header_frame1(method, scheme, authority, path ,flags, id,header_fileds,verbose=True):
    # TODO: 对:authority、:method、:scheme修改
    # * 1. :method 目标URL模式部分(请求)
    # * 2. :scheme 目标URL模式部分(请求) 
    # * 3. :authority 目标URL认证部分(请求)
    # * 4. :path 
    # header fileds = []
    if verbose:
        path = "/?reqid=%s" %id
    head_frame =  {"<headers-frame-%s>"%id: {":method": method, ":scheme": scheme, ":authority": authority, ":path": path,"flags": flags}}
    
    head_frame["<headers-frame-%s>"%id][header_fileds[0]] = header_fileds[1]
    return head_frame

# ! 使用continuation frame 和直接将header fileds 放在header frame里有区别吗？

def gen_continue_frame(header_fileds,flags,id):

    continue_frame =  {"<continuation-frame-%s>"%id: {"flags": flags}}
    # TODO 这种用于多个header的情况目前暂时不需要拓展
    # TODO 发送两个Content-Length
    header_name = header_fileds[0]
    header_value = header_fileds[1]
    continue_frame["<continuation-frame-%s>"%id][header_name] = header_value
    return continue_frame

def gen_data_frame(data,flags,id):
    data_frame = {"<data-frame-%s>"%id: {"data":data,"flags": flags}}
    return data_frame

def gen_req(frames):
    req = {}
    for frame in frames:
        for frame_name, frame_value in frame.items():
            req[frame_name] = frame_value
    return req


def gen_single_header_frame_req(method,scheme,domain,path,header_fileds,verbose):
    i = 1
    req_list = []
    head_frame = gen_header_frame(method=method, scheme=scheme, authority=domain, path=path ,flags=["EH","ES"], id=i, verbose=verbose,header_fileds=header_fileds)

    req = gen_req(frames=[head_frame])
    req_list.append(req)

    return req_list

def gen_all_single_header_frame_reqs(method,scheme,domain,path,verbose):
    i = 1
    req_list = []
    header_list = gen_single_header()
    for header in header_list:
        head_frame = gen_header_frame1(method=method, scheme=scheme, authority=domain, path=path ,flags=["EH","ES"], id=i, verbose=verbose,header_fileds=header)
        req = gen_req(frames=[head_frame])
        req_list.append(req)
        i += 2
    return req_list

# save attack data to json format
def save_mutated_data(attack_type,attack_req_list):
    
    attack_req_dict = {}
    i = 0
    for req in attack_req_list:
        i += 1
        attack_req_dict['reqid_%s' %i] = req
    # * save data in attack_data
    file_name = "./" + str(attack_type) + '_attack_data.json'
    with open(file_name, 'w') as f:
        json_str = json.dumps(attack_req_dict, indent=0)
        f.write(json_str)
        f.write('\n')


def save_mutated_data1(header,attack_req_list):
    
    attack_req_dict = {}
    i = 0
    for req in attack_req_list:
        i += 1
        attack_req_dict['reqid_%s' %i] = req
    # * save data in attack_data
    file_name = "./" + "test_"+ str(header) + '_req.json'
    with open(file_name, 'w') as f:
        json_str = json.dumps(attack_req_dict, indent=0)
        f.write(json_str)
        f.write('\n')

def save_mutated_data2(attack_req_list):
    
    attack_req_dict = {}
    i = 0
    for req in attack_req_list:
        i += 1
        attack_req_dict['reqid_%s' %i] = req
    # * save data in attack_data
    file_name = "./" + "test_all_single_header_req.json"
    with open(file_name, 'w') as f:
        json_str = json.dumps(attack_req_dict, indent=0)
        f.write(json_str)
        f.write('\n')





if __name__ == "__main__":

    req_list = gen_all_single_header_frame_reqs(method="GET", scheme="https", domain="cl.lzytest.tech",path="/",verbose=True)

    print(req_list[:2])
    save_mutated_data1(header="test",attack_req_list=req_list)
