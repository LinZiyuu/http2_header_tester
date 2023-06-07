import sys
import linecache
import configargparse
import random
import re
import copy

def _parse_url(url):
    """ This function extracts 
        components from a given URL.
        解析url 并提取host port authority uri
    """
    # 主体
    authority = url.split('/')[2]
    # 请求的东西
    uri = '/'.join(url.split('/')[3:])
    # scheme 协议
    scheme = url.split('/')[0]
    # 有：就是指定端口的情况 http 端口是80 https端口是 443
    if ':' not in authority:
        host = authority
        if scheme == 'https:':
            port = 443
        else:
            port = 80
    else:
        # 指定端口的情况
        host, port = authority.split(':')

    return host, port, authority, uri

def _print_exception(extra_details=[]):
    """ This function prints exception details
        including the line number where the exception
        is raised, which is helpful in most cases.
    """
    # exc_info找到执行except 字句的堆栈
    # (type, value, traceback)
    exc_type, exc_obj, tb = sys.exc_info()
    # tb_frame 指向当前层级的执行帧
    f = tb.tb_frame
    # tb_lineno 给出发生异常所在的行号
    lineno = tb.tb_lineno
    # 获得filename
    filename = f.f_code.co_filename
    # 检查缓存中的文件在磁盘中是否发生了改变
    linecache.checkcache(filename)
    # 获得报错的这行
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}, {}'.format(filename, lineno, line.strip(), exc_obj, extra_details), file=sys.stderr)

def _parse_args(): 
    """ This function is for parsing the command
        line arguments fed into the script.
    """
    parser = configargparse.ArgParser(description='Frameshifter: Grammar-based HTTP/2 fuzzer with mutation ability')

    parser.add('-c', dest="config", required=True, help='config file path')
    parser.add('-i', action="store_true", dest="individual_mode", help="Turns the individual mode on where the fuzzer is run only for specified seeds.")
    parser.add('-s', dest="seed", type=int, help="Only needed for individual mode. Seed parameter for random number generator.")
    parser.add('-v', action="store_true", dest="verbose", help="Only needed for individual mode. Adds verbosity.")
    parser.add('-o', dest="outfilename", help = "Only needed for individual mode. File to write output.")
    parser.add('-f', dest="seedfile", help = "Only needed for individual mode. Input file containing seeds.")
    # testing mode just generate mutation but not deliver them
    parser.add('-t', action="store_true", dest="testing_mode", help="Turns the testing mode on where the fuzzer generates and mutates inputs, but not delivers them.")

    args = parser.parse_args()
    #print(type(args))
    #print(args)

    return args

# 这个函数的作用就是根据权重选一个扩展 应该是插入一个帧
def random_choose_with_options(possible_expansions):
    # possible_expansions可选的扩展
    possible_expansions_copy = copy.deepcopy(possible_expansions)
    #  probabilities = [0, 0] 0的个数为len
    probabilities = [0]*len(possible_expansions_copy)
    for index, expansion in enumerate(possible_expansions_copy):
        # 取出prob
        if "prob=" in expansion:
            probability = re.findall('(?<=prob=)[0-9.]+',expansion)[0]
            probabilities[index] = float(probability)
    # (如果probalities全是0的话)就让选到每个的概率平均
    probabilities = [(1-sum(probabilities))/probabilities.count(0) if elem == 0 else elem for elem in probabilities]
    # 选一个扩展
    chosen_expansion = random.choices(possible_expansions_copy, weights=probabilities)[0]
    # '(<headers-frame-1><data-frame-1>, opts(prob=0.9))'
    # for cases where symbol looks like above, trimming is needed
    if ', opts' in chosen_expansion:
        chosen_expansion = chosen_expansion.split(', opts')[0][1:]
    #
    return chosen_expansion
