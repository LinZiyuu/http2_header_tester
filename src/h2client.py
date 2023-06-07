import socket
import ssl
import scapy.supersocket as supersocket
import scapy.contrib.http2 as h2
import scapy.config
import scapy.packet as packet
from gen_frm import extract_type, build_frame, load_data
from helper_functions import _print_exception
import time

class H2Client:

    def __init__(self, tls, verbose=False):
        self.verbose = verbose
        self.tls = tls
    def send(self, dn, port, frames):
        try:
            # self.seed = seed
            self.target_addr = dn + ":" + str(port)
            self.tls_setup_exchange(dn, port)
            self.initial_h2_exchange()
            return self.send_sequence2(frames)

        except ConnectionRefusedError:
            print("connection refused at {}:{}.".format(dn, port))
    


    # def chose_frames(self, file_name):
    #     frames_dict = load_data(file_name=file_name)
    #     frames = []
    #     for anomaly_name, frame_dict in frames_dict.items():
    #         # print(frame_dict)
    #         for frame_name, frame_fileds in frame_dict.items():
    #             frame_type = extract_type(frame_name=frame_name)
    #             frame = build_frame(fileds_dict=frame_fileds, frame_type=frame_type)
    #             frames.append(frame)
    #     return frames
    
    def gen_all_frames(self, file_name):
        frames_dict = load_data(file_name=file_name)
        req_list = []
        i = 1
        frames = []
        for anomaly_name, frame_dict in frames_dict.items():
            for frame_name, frame_fileds in frame_dict.items():
                frame_type = extract_type(frame_name=frame_name)
                frame = build_frame(fileds_dict=frame_fileds, frame_type=frame_type,stream_id=i)
                frames.append(frame)
            # req_list.append(frames)
            i += 2
        return frames
    
    def tls_setup_exchange(self, dn, port, use_insecure_ciphers=False):
        # 获取信息
        # socket.getaddrinfo(host, port, family=0, type=0, proto=0, flags=0)
        # return (family, type, proto, canonname, sockaddr)
        # INADDR_ANY用于绑定所有借口 IPPROTO_TCP 网络层是IP 传输层是TCP
        addr_info = socket.getaddrinfo(dn, port, socket.INADDR_ANY, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        # family, type, proto
        s = socket.socket(addr_info[0][0], addr_info[0][1], addr_info[0][2])
        # set socket opt and value
        # setsockopt(level, optname, value)
        # level:选项所在的协议层 SOL_SOCKET：套接字层 SOL_IP：ip层 SOL_TCP：TCP层 SOL_UDP：UDP层
        # optname SO_REUSERADDR　　　　　 允许重用本地地址和端口
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # hasattr(object, name)
        # 判断obj是否含有name属性 并返回true false
        if hasattr(socket, 'SO_REUSEPORT'):
            # 复用port
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        # sockaddr
        ip_and_port = addr_info[0][4]
        # print(f'ip_and_port{ip_and_port}')
        # ssl上下文对象
        # 选译 TLS 版本 1.2 作为通道加密协议
        if self.tls:
        
            ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            # 不验证证书有效性
            ssl_ctx.check_hostname = False
            # 证书错误也会被忽略
            ssl_ctx.verify_mode = ssl.CERT_NONE
            # 不安全的加密？
            if use_insecure_ciphers:
                ciphers = ['AES256-GCM-SHA384', 'AES128-GCM-SHA256', 'AES256-SHA256', 'AES128-SHA256', 'CAMELLIA128-SHA256']
            else:
                ciphers = ['ECDHE-ECDSA-AES256-GCM-SHA384', 'ECDHE-RSA-AES256-GCM-SHA384', 'ECDHE-ECDSA-AES128-GCM-SHA256',
                        'ECDHE-RSA-AES128-GCM-SHA256', 'ECDHE-ECDSA-AES256-SHA384', 'ECDHE-RSA-AES256-SHA384',
                        'ECDHE-ECDSA-AES128-SHA256', 'ECDHE-RSA-AES128-SHA256', 'ECDHE-ECDSA-CAMELLIA256-SHA384',
                        'ECDHE-RSA-CAMELLIA256-SHA384', 'ECDHE-ECDSA-CAMELLIA128-SHA256', 'ECDHE-RSA-CAMELLIA128-SHA256',
                        'DHE-RSA-AES256-GCM-SHA384', 'DHE-RSA-AES128-GCM-SHA256', 'DHE-RSA-AES256-SHA256',
                        'DHE-RSA-AES128-SHA256', 'AES256-GCM-SHA384', 'AES128-GCM-SHA256', 'AES256-SHA256',
                        'AES128-SHA256', 'CAMELLIA128-SHA256']

            # 添加加密部分

            ssl_ctx.set_ciphers(':'.join(ciphers))

            # 指定在 SSL/TLS 握手期间套接字应当通告的协议
            ssl_ctx.set_alpn_protocols(['h2'])  # h2 is a RFC7540-hardcoded value
            # ssl_ctx.set_alpn_protocols(['http / 1.1'])

            # 返回的 SSL 套接字会绑定上下文、设置以及证书
            ssl_sock = ssl_ctx.wrap_socket(s, server_hostname=dn)
            # 这个是建立连接
            ssl_sock.connect(ip_and_port)
            # 检查协议是不是http2
            assert ('h2' == ssl_sock.selected_alpn_protocol())
            scapy.config.conf.debug_dissector = True
            ssl_stream_sock = supersocket.SSLStreamSocket(ssl_sock, basecls=h2.H2Frame)
            self.sock = ssl_stream_sock
        else:
            s.connect(ip_and_port)
            scapy.config.conf.debug_dissector = True
            stream_sock = supersocket.StreamSocket(s, basecls=h2.H2Frame)
            self.sock = stream_sock


    # 建立http2连接
    def initial_h2_exchange(self):
        # SENDING MAGIC
        magic = packet.Raw(h2.H2_CLIENT_CONNECTION_PREFACE)
        # magic = h2.H2_CLIENT_CONNECTION_PREFACE
        if self.verbose:
            print("-" * 32 + "SENDING" + "-" * 32)
            magic.show()
        self.sock.send(magic)
        
        # RECEIVING
        srv_set = self.sock.recv()
        # srv_set.show()
        if self.verbose:
            print("-" * 32 + "RECEIVING" + "-" * 32)
            srv_set.show()
        srv_max_frm_sz = 1 << 14
        srv_hdr_tbl_sz = 4096
        srv_max_hdr_tbl_sz = 0
        srv_global_window = 1 << 14
        for setting in srv_set.payload.settings:
            if setting.id == h2.H2Setting.SETTINGS_HEADER_TABLE_SIZE:
                srv_hdr_tbl_sz = setting.value
            elif setting.id == h2.H2Setting.SETTINGS_MAX_HEADER_LIST_SIZE:
                srv_max_hdr_lst_sz = setting.value
            elif setting.id == h2.H2Setting.SETTINGS_INITIAL_WINDOW_SIZE:
                srv_global_window = setting.value

        srv_max_hdr_lst_sz = 1 << 10

        own_set = h2.H2Frame() / h2.H2SettingsFrame()
        max_frm_sz = 1 << 14
        max_hdr_tbl_sz = 4096
        win_sz = 1 << 14
        own_set.settings = [
            h2.H2Setting(id=h2.H2Setting.SETTINGS_ENABLE_PUSH, value=0),
            h2.H2Setting(id=h2.H2Setting.SETTINGS_INITIAL_WINDOW_SIZE, value=win_sz),
            h2.H2Setting(id=h2.H2Setting.SETTINGS_HEADER_TABLE_SIZE, value=max_hdr_tbl_sz),
            h2.H2Setting(id=h2.H2Setting.SETTINGS_MAX_FRAME_SIZE, value=max_frm_sz),
        ]

        winupdate = h2.H2Frame(b'\x00\x00\x04\x08\x00\x00\x00\x00\x00\x3f\xff\x00\x01')
        set_ack = h2.H2Frame(flags={'A'}) / h2.H2SettingsFrame()

        h2seq = h2.H2Seq()
        h2seq.frames = [
            own_set,
            winupdate,
            set_ack
        ]
        for frame in h2seq.frames:
            if self.verbose:
                print("-" * 32 + "SENDING" + "-" * 32)
                frame.show()
            self.sock.send(frame)

        # while loop for waiting until ack is received for client's settings
        new_frame = None
        while isinstance(new_frame, type(None)) or not (
                new_frame.type == h2.H2SettingsFrame.type_id
                and 'A' in new_frame.flags
        ):
            try:
                new_frame = self.sock.recv()
                if self.verbose:
                    print("-" * 32 + "RECEIVING" + "-" * 32)
                    new_frame.show()
            except:
                time.sleep(1)
                new_frame = None
    
    def send_sequence2(self, frames=None):
            if not frames:
                return b'no frame to send.'
            else:
                # 创建帧序列并且发送
                sequence = h2.H2Seq()
                sequence.frames = frames
                for frame in sequence.frames:
                    if self.verbose:
                        print("-" * 32 + "SENDING" + "-" * 32)
                        frame.show()
                self.sock.send(sequence)
            # import time
            # time.sleep(1)
            # new_frame = None


    def send_sequence(self, frames=None):
        if not frames:
            return b'no frame to send.'
        else:
            # 创建帧序列并且发送
            sequence = h2.H2Seq()
            sequence.frames = frames
            for frame in sequence.frames:
                if self.verbose:
                    print("-" * 32 + "SENDING" + "-" * 32)
                    frame.show()
            self.sock.send(sequence)

        new_frame = None
        response_data = b''
        status_codes = []
        error_codes = []

        while True:
            try:
                # new_frame是从server端接收到到信息
                new_frame = self.sock.recv()
                if self.verbose:
                    print("-" * 32 + "RECEIVING" + "-" * 32)
                    new_frame.show()
                # new_frame.type == h2.H2DataFrame.type_id 判断这个帧是一个数据帧 并且有数据就加进去
                if new_frame.type == h2.H2DataFrame.type_id and new_frame.payload:
                    response_data += new_frame.payload.data
                    # 'ES'代表END_STREAM结束
                    if 'ES' in new_frame.flags:
                        break
                # new_frame.type == h2.H2HeadersFrame.type_id 判断这个帧是不是头部帧
                elif new_frame.type == h2.H2HeadersFrame.type_id and new_frame.payload:
                    status_code_in_response = False
                    # 取出状态码
                    for header in new_frame.hdrs:
                        if 'index' in dir(header):
                            index = int(header.index)
                            if index >= 8 and index <= 14:
                                status_code = bytes(h2.HPackHdrTable()._static_entries[index])
                                status_codes.append(status_code)
                                print(f"Status_code:{status_code}")
                    if 'ES' in new_frame.flags:
                        break
                # 判断是不是空
                elif not isinstance(new_frame, type(None)):
                    if 'ES' in new_frame.flags or new_frame.type == h2.H2GoAwayFrame.type_id or new_frame.type == h2.H2ResetFrame.type_id:
                        # 如果是Reset或者GoAway帧则返回错误码
                        if new_frame.type == h2.H2ResetFrame.type_id or new_frame.type == h2.H2GoAwayFrame.type_id:
                            error_code = str(new_frame.error).encode()
                            error_codes.append(h2.H2ErrorCodes.literal[new_frame.getfieldval('error')].encode())
                            print(f"Error_code:{error_code.decode()}")
                        break
            except Exception as e:
                _print_exception(["host=" + str(self.target_addr)])
                # import time
                # time.sleep(1)
                # new_frame = None
                break
        # 返回响应
        return b'response-code: ' + b','.join(status_codes) + b'\r\nerror: ' + b','.join(error_codes) + b'\r\n\r\n' + response_data
    
    def recv_response(self):
        new_frame = None
        response_data = b''
        status_codes = []
        error_codes = []

        while True:
            try:
                # new_frame是从server端接收到到信息
                new_frame = self.sock.recv()
                print("new_frame:", new_frame)
                print("new_frame_payload:", new_frame.payload.data)
                if self.verbose:
                    print("-" * 32 + "RECEIVING" + "-" * 32)
                    new_frame.show()
                    print("-" * 32 + "RECEIVING" + "-" * 32)
                # new_frame.type == h2.H2DataFrame.type_id 判断这个帧是一个数据帧 并且有数据就加进去
                if new_frame.type == h2.H2DataFrame.type_id and new_frame.payload:
                    response_data += new_frame.payload.data
                    # 'ES'代表END_STREAM结束
                    if 'ES' in new_frame.flags:
                        break
                # new_frame.type == h2.H2HeadersFrame.type_id 判断这个帧是不是头部帧
                elif new_frame.type == h2.H2HeadersFrame.type_id and new_frame.payload:
                    status_code_in_response = False
                    # 取出状态码
                    for header in new_frame.hdrs:
                        if 'index' in dir(header):
                            index = int(header.index)
                            if index >= 8 and index <= 14:
                                status_code = bytes(h2.HPackHdrTable()._static_entries[index])
                                status_codes.append(status_code)

                    if 'ES' in new_frame.flags:
                        break
                # 判断是不是空
                elif not isinstance(new_frame, type(None)):
                    if 'ES' in new_frame.flags or new_frame.type == h2.H2GoAwayFrame.type_id or new_frame.type == h2.H2ResetFrame.type_id:
                        # 如果是Reset或者GoAway帧则返回错误码
                        if new_frame.type == h2.H2ResetFrame.type_id or new_frame.type == h2.H2GoAwayFrame.type_id:
                            error_code = str(new_frame.error).encode()
                            error_codes.append(h2.H2ErrorCodes.literal[new_frame.getfieldval('error')].encode())
                        break
            except Exception as e:
                _print_exception(["host=" + str(self.target_addr)])
                # import time
                # time.sleep(1)
                # new_frame = None
                break
        # 返回响应
        return b'response-code: ' + b','.join(status_codes) + b'\r\nerror: ' + b','.join(error_codes) + b'\r\n\r\n' + response_data
    





