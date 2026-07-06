# parser.py
# -*- coding: utf-8 -*-
"""
四川大学《计算机通信与网络》课程设计
模块：parser.py (增强版：支持 TCP/UDP/DNS/QUIC + HTTP 视频路径嗅探)
"""

import struct
import socket
import re


class TrafficParser:
    def __init__(self):
        self.port_hints = {
            53: "DNS", 123: "NTP", 161: "SNMP",
            443: "HTTPS", 80: "HTTP", 8080: "HTTP",
            22: "SSH", 23: "TELNET", 21: "FTP",
            1935: "RTMP", 3478: "STUN", 5349: "STUN-TLS",
            8801: "ZOOM", 8802: "ZOOM",
            4000: "QQ", 4010: "WeGame", 10000: "WeChat",
            27015: "Steam", 27016: "Steam", 27017: "Steam",
            5060: "SIP", 5061: "SIPS",
        }

    def process_raw_packet(self, raw_data: bytes):
        if len(raw_data) < 20:
            return None

        ip_header = raw_data[0:20]
        iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
        version_ihl = iph[0]
        ihl = version_ihl & 0xF
        ip_header_len = ihl * 4
        protocol = iph[6]
        total_len = iph[2]
        src_ip = socket.inet_ntoa(iph[8])
        dst_ip = socket.inet_ntoa(iph[9])

        trans_data = raw_data[ip_header_len:]
        if len(trans_data) < 8:
            return None

        host_found = None
        video_hint = False
        proto_type = "TCP"
        src_port = dst_port = 0

        if protocol == 6 and len(trans_data) >= 20:
            tcph = struct.unpack('!HHLLBBHHH', trans_data[:20])
            src_port = tcph[0]
            dst_port = tcph[1]
            tcp_header_len = (tcph[4] >> 4) * 4
            app_payload = trans_data[tcp_header_len:]

            if dst_port in self.port_hints:
                proto_type = self.port_hints[dst_port]
            elif src_port in self.port_hints:
                proto_type = self.port_hints[src_port]

            sni = self._extract_sni(app_payload)
            if sni:
                host_found = sni
                proto_type = "HTTPS"
            elif app_payload:
                host_found, video_hint = self._extract_http_info(app_payload)

        elif protocol == 17 and len(trans_data) >= 8:
            udph = struct.unpack('!HHHH', trans_data[:8])
            src_port = udph[0]
            dst_port = udph[1]
            udp_payload = trans_data[8:]

            if dst_port in self.port_hints:
                proto_type = self.port_hints[dst_port]
            elif src_port in self.port_hints:
                proto_type = self.port_hints[src_port]
            else:
                proto_type = "UDP"

            if dst_port == 53 or src_port == 53:
                dns_host = self._extract_dns_query(udp_payload)
                if dns_host:
                    host_found = dns_host
                    proto_type = "DNS"

            if not host_found and (dst_port in [443, 784, 8801] or src_port in [443, 784]):
                quic_host = self._extract_quic_sni(udp_payload)
                if quic_host:
                    host_found = quic_host
                    proto_type = "QUIC"

        return {
            "host": host_found,
            "video_hint": video_hint,
            "protocol": proto_type,
            "size": total_len,
            "raw_data": raw_data,
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "src_port": src_port,
            "dst_port": dst_port
        }

    def _extract_sni(self, app_payload: bytes) -> str:
        if not app_payload or len(app_payload) < 43 or app_payload[0] != 0x16:
            return None
        try:
            pos = 5
            pos += 4
            pos += 34
            if pos >= len(app_payload):
                return None
            sess_id_len = app_payload[pos]
            pos += 1 + sess_id_len
            if pos + 2 > len(app_payload):
                return None
            cipher_len = struct.unpack('!H', app_payload[pos:pos + 2])[0]
            pos += 2 + cipher_len
            if pos >= len(app_payload):
                return None
            comp_len = app_payload[pos]
            pos += 1 + comp_len
            if pos + 2 > len(app_payload):
                return None
            ext_len = struct.unpack('!H', app_payload[pos:pos + 2])[0]
            pos += 2
            end = pos + ext_len
            while pos + 4 <= len(app_payload) and pos < end:
                ext_type, ext_len = struct.unpack('!HH', app_payload[pos:pos + 4])
                pos += 4
                if ext_type == 0:
                    if pos + 5 > len(app_payload):
                        return None
                    name_type = app_payload[pos + 2]
                    if name_type != 0:
                        return None
                    name_len = struct.unpack('!H', app_payload[pos + 3:pos + 5])[0]
                    if pos + 5 + name_len <= len(app_payload):
                        return app_payload[pos + 5:pos + 5 + name_len].decode('utf-8', errors='ignore')
                    return None
                pos += ext_len
        except Exception:
            pass
        return None

    def _extract_http_info(self, app_payload: bytes):
        host_found = None
        video_hint = False
        try:
            payload_str = app_payload[:2000].decode('utf-8', errors='ignore')
            lines = payload_str.split("\r\n")
            if not lines:
                return None, False

            req_line = lines[0]
            video_exts = r'\.(m4s|ts|mp4|flv|f4v|m3u8|mpd|dash|mov|avi|wmv|rmvb|mkv|webm|3gp)(\?|$|/)'
            if re.search(video_exts, req_line, re.IGNORECASE):
                video_hint = True

            for line in lines[1:]:
                if line.startswith("Host:"):
                    host_found = line.split("Host:")[1].strip().split(':')[0]
                    break
        except Exception:
            pass
        return host_found, video_hint

    def _extract_dns_query(self, udp_payload: bytes) -> str:
        if len(udp_payload) < 12:
            return None
        try:
            flags = struct.unpack('!H', udp_payload[2:4])[0]
            if (flags >> 15) & 0x1 != 0:
                return None
            qdcount = struct.unpack('!H', udp_payload[4:6])[0]
            if qdcount == 0:
                return None
            offset = 12
            labels = []
            while offset < len(udp_payload):
                length = udp_payload[offset]
                if length == 0:
                    break
                if length > 63:
                    break
                offset += 1
                labels.append(udp_payload[offset:offset + length].decode('utf-8', errors='ignore'))
                offset += length
            if labels:
                return ".".join(labels)
        except Exception:
            pass
        return None

    def _extract_quic_sni(self, udp_payload: bytes) -> str:
        if len(udp_payload) < 20:
            return None
        try:
            first_byte = udp_payload[0]
            if not (first_byte & 0x80):
                return None
            pos = 5
            dcid_len = udp_payload[4]
            pos += dcid_len
            if pos >= len(udp_payload):
                return None
            scid_len = udp_payload[pos]
            pos += 1 + scid_len
            if pos >= len(udp_payload):
                return None
            token_len_byte = udp_payload[pos]
            if token_len_byte & 0x80:
                token_len = struct.unpack('!H', bytes([token_len_byte & 0x7F, udp_payload[pos + 1]]))[0]
                pos += 2
            else:
                token_len = token_len_byte
                pos += 1
            pos += token_len
            if pos >= len(udp_payload):
                return None
            len_byte = udp_payload[pos]
            if len_byte & 0x80:
                length = struct.unpack('!H', bytes([len_byte & 0x7F, udp_payload[pos + 1]]))[0]
                pos += 2
            else:
                length = len_byte
                pos += 1
            payload = udp_payload[pos:pos + length]
            if b"sn" in payload[:10]:
                text = payload.decode('utf-8', errors='ignore')
                match = re.search(r'([a-zA-Z0-9-]+\.[a-zA-Z0-9-]+\.[a-zA-Z]{2,})', text)
                if match:
                    return match.group(1)
        except Exception:
            pass
        return None