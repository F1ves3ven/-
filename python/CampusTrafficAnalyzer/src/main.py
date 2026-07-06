# main.py
# -*- coding: utf-8 -*-
"""
四川大学《计算机通信与网络》课程设计
模块：main.py (校园网多终端流量分析与异常检测中心)
"""

import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
import socket
import struct
import time
import csv
import ipaddress

from parser import TrafficParser
from classifier import TrafficClassifier
from gui import CampusTrafficGUI


class TrafficControlCenter:
    def __init__(self):
        self.root = tk.Tk()
        self.parser = TrafficParser()
        self.classifier = TrafficClassifier()

        self.is_running = False
        self.is_paused = False

        self.terminal_database = {}
        self.selected_ip = "全网总计"

        self.stats_template = {
            "学习办公": {"count": 0, "bytes": 0, "color": "#4E73DF"},
            "网络视频": {"count": 0, "bytes": 0, "color": "#1CC88A"},
            "社交聊天": {"count": 0, "bytes": 0, "color": "#36B9CC"},
            "休闲游戏": {"count": 0, "bytes": 0, "color": "#F6C23E"},
            "系统服务": {"count": 0, "bytes": 0, "color": "#858796"},
            "购物金融": {"count": 0, "bytes": 0, "color": "#E74A3B"},
            "其他流量": {"count": 0, "bytes": 0, "color": "#6F4E37"}
        }

        self.terminal_database["全网总计"] = {cat: data.copy() for cat, data in self.stats_template.items()}
        self.terminal_database["全网总计"]["total_bytes"] = 0
        self.terminal_database["全网总计"]["inner_bytes"] = 0
        self.terminal_database["全网总计"]["outer_bytes"] = 0

        self.detail_history = {cat: [] for cat in self.stats_template.keys()}

        self.alert_history = []
        self.syn_counter = {}
        self.last_alert_time = {}
        self.ip_last_bytes = {}
        self.arp_table = {}

        self.rate_window_start = time.time()
        self.rate_window_bytes = 0

        self.tcp_connections = {}

        self.ui = CampusTrafficGUI(
            self.root,
            self.ui_click_start,
            self.ui_click_pause,
            self.ui_click_clear,
            self.ui_click_export
        )
        self.inject_ip_selector_to_ui()
        self.ui.tree.bind("<Double-1>", self.handle_main_table_double_click)
        self.sync_data_to_view_table()

    @staticmethod
    def is_private_ip(ip_str: str) -> bool:
        try:
            ip = ipaddress.ip_address(ip_str)
            return ip.is_private
        except:
            return False

    @staticmethod
    def is_broadcast_ip(ip_str: str) -> bool:
        try:
            ip = ipaddress.ip_address(ip_str)
            return ip.is_broadcast or ip.is_multicast or str(ip) == "255.255.255.255"
        except:
            return False

    def check_anomalies(self, src_ip: str, dst_ip: str, proto: str, size: int, raw_data: bytes):
        now = time.time()
        if self.is_broadcast_ip(dst_ip) and size > 500:
            self._push_alert(f"🚨 广播风暴疑似: {src_ip} -> {dst_ip} ({size}B)", "broadcast")
        if proto == "TCP" and len(raw_data) >= 40:
            tcp_flags = raw_data[33] if len(raw_data) > 33 else 0
            if tcp_flags & 0x02 and not (tcp_flags & 0x10):
                self.syn_counter[src_ip] = self.syn_counter.get(src_ip, 0) + 1
                if self.syn_counter[src_ip] > 50:
                    self._push_alert(f"⚠️ SYN Flood 疑似: {src_ip} 半开连接过多", "synflood")
                    self.syn_counter[src_ip] = 0
        current_total = self.terminal_database.get(src_ip, {}).get("total_bytes", 0)
        last_total = self.ip_last_bytes.get(src_ip, 0)
        if current_total - last_total > 5 * 1024 * 1024:
            self._push_alert(f"📈 流量突增: {src_ip} 5秒内超 5MB", "traffic_spike")
        self.ip_last_bytes[src_ip] = current_total

    def _push_alert(self, msg: str, alert_type: str):
        now = time.time()
        last = self.last_alert_time.get(alert_type, 0)
        if now - last < 5:
            return
        self.last_alert_time[alert_type] = now
        self.alert_history.append((time.strftime('%H:%M:%S'), msg))
        if len(self.alert_history) > 20:
            self.alert_history.pop(0)
        self.root.after(0, lambda: self.ui.update_alert_panel(self.alert_history))

    def get_top_talkers(self, n=3):
        candidates = []
        for ip, data in self.terminal_database.items():
            if ip == "全网总计":
                continue
            candidates.append((ip, data.get("total_bytes", 0)))
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[:n]

    def get_current_rate(self):
        elapsed = time.time() - self.rate_window_start
        if elapsed > 2:
            rate = self.rate_window_bytes / elapsed / 1024
            self.rate_window_start = time.time()
            self.rate_window_bytes = 0
            return round(rate, 2)
        return 0

    def inject_ip_selector_to_ui(self):
        """核心前端魔改：在控制面板处横向塞入一个目标审计终端下拉框及画像展示栏"""
        # ★★★ 修复：直接访问 gui.py 暴露的 control_panel，不再遍历查找 ★★★
        widget = self.ui.control_panel

        selector_frame = tk.Frame(widget, bg="#F4F6F9")
        selector_frame.pack(side=tk.LEFT, padx=15)

        tk.Label(selector_frame, text="🔍 目标审计终端:", font=("微软雅黑", 10, "bold"), bg="#F4F6F9",
                 fg="#A6192E").pack(side=tk.LEFT)

        self.ip_combobox = ttk.Combobox(selector_frame, values=["全网总计"], width=16, state="readonly")
        self.ip_combobox.current(0)
        self.ip_combobox.pack(side=tk.LEFT, padx=5)
        self.ip_combobox.bind("<<ComboboxSelected>>", self.handle_ip_switch)

        self.profile_label = tk.Label(widget, text="【终端标签】: 等待捕获流量生成用户画像...",
                                      font=("微软雅黑", 10, "italic"), bg="#F4F6F9", fg="#5A5C69")
        self.profile_label.pack(side=tk.LEFT, padx=20)

    def handle_ip_switch(self, event):
        self.selected_ip = self.ip_combobox.get()
        self.sync_data_to_view_table()

        current_dataset = self.terminal_database[self.selected_ip]
        if self.selected_ip == "全网总计":
            self.profile_label.config(text="【终端标签】: 正在监控局域网大盘态势...", fg="#5A5C69")
        else:
            profile_text = self.classifier.generate_user_profile(current_dataset)
            self.profile_label.config(text=profile_text, fg="#A6192E")

        self.ui.draw_native_pie(current_dataset, current_dataset["total_bytes"])
        self.ui.log_message(f"[审计中心] 切换控制台视图 -> 锁定监控目标: [{self.selected_ip}]")

    def init_new_ip_bucket(self, ip):
        if ip not in self.terminal_database:
            self.terminal_database[ip] = {}
            for cat, data in self.stats_template.items():
                self.terminal_database[ip][cat] = data.copy()
            self.terminal_database[ip]["total_bytes"] = 0
            self.terminal_database[ip]["inner_bytes"] = 0
            self.terminal_database[ip]["outer_bytes"] = 0

            current_values = list(self.ip_combobox['values'])
            if ip not in current_values:
                current_values.append(ip)
                self.ip_combobox['values'] = current_values

    def ui_click_start(self):
        if not self.is_running:
            self.is_running = True
            self.ui.start_btn.config(text="🛑 审计中...", bg="#DC3545", state=tk.DISABLED)
            self.ui.pause_btn.config(state=tk.NORMAL)
            self.ui.status_label.config(text="态势感知中: 校园网混杂监听已开启...", fg="#28A745")
            threading.Thread(target=self.packet_capture_loop, daemon=True).start()

    def ui_click_pause(self):
        if not self.is_running:
            return
        self.is_paused = not self.is_paused
        self.ui.pause_btn.config(
            text="▶ 恢复审计" if self.is_paused else "⏸ 暂停审计",
            bg="#007BFF" if self.is_paused else "#6C757D"
        )

    def ui_click_clear(self):
        if messagebox.askyesno("安全清空", "确认销毁全网终端的行为轨迹和审计日志吗？"):
            self.terminal_database = {
                "全网总计": {cat: data.copy() for cat, data in self.stats_template.items()}
            }
            self.terminal_database["全网总计"]["total_bytes"] = 0
            self.terminal_database["全网总计"]["inner_bytes"] = 0
            self.terminal_database["全网总计"]["outer_bytes"] = 0

            self.ip_combobox['values'] = ["全网总计"]
            self.ip_combobox.current(0)
            self.selected_ip = "全网总计"
            self.profile_label.config(text="【终端标签】: 等待捕获流量生成用户画像...", fg="#5A5C69")
            self.detail_history = {cat: [] for cat in self.stats_template.keys()}
            self.alert_history = []
            self.syn_counter = {}
            self.ip_last_bytes = {}
            self.tcp_connections = {}
            self.sync_data_to_view_table()
            self.ui.draw_native_pie(self.terminal_database["全网总计"], 0)
            self.ui.clear_log_area()
            self.ui.update_alert_panel([])
            self.ui.update_top_talkers([])

    def ui_click_export(self):
        has_data = any(len(records) > 0 for records in self.detail_history.values())
        if not has_data:
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV审计报表", "*.csv")])
        if not file_path:
            return
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(["捕获时间", "审计源IP(终端)", "目标Host", "协议类型", "端口信息",
                                 "审计分类", "内外网", "载荷大小"])
                for cat, records in self.detail_history.items():
                    for rec in records:
                        t_time, proto, host, size_str = rec["row_data"]
                        src_ip = rec.get("src_ip", "未知设备")
                        port_info = rec.get("port_info", "-")
                        net_type = rec.get("net_type", "-")
                        writer.writerow([t_time, src_ip, host, proto, port_info, cat, net_type, size_str])
            messagebox.showinfo("存盘成功", f"校园网流量审计报表已导出：\n{file_path}")
        except Exception as e:
            messagebox.showerror("导出错误", str(e))

    def packet_capture_loop(self):
        try:
            local_ip = socket.gethostbyname(socket.gethostname())
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
            s.bind((local_ip, 0))
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        except Exception as e:
            self.root.after(0, lambda: self.ui.log_message(
                f"[-] 混杂模式开启失败！必须以管理员权限运行本程序！错误: {e}"))
            self.root.after(0, lambda: self.ui.status_label.config(text="初始化失败：无权限", fg="#DC3545"))
            return

        while self.is_running:
            try:
                raw_data, addr = s.recvfrom(65565)
                if self.is_paused:
                    continue

                ip_header = raw_data[0:20]
                iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
                ihl = (iph[0] & 0xF) * 4
                protocol = iph[6]
                total_len = iph[2]
                src_ip = socket.inet_ntoa(iph[8])
                dst_ip = socket.inet_ntoa(iph[9])

                is_inner = self.is_private_ip(src_ip) and self.is_private_ip(dst_ip)
                net_type = "内网" if is_inner else "外网"

                self.check_anomalies(src_ip, dst_ip, "TCP" if protocol == 6 else "UDP", total_len, raw_data)

                res = self.parser.process_raw_packet(raw_data)
                if not res:
                    continue

                host = res["host"]
                video_hint = res["video_hint"]
                proto = res["protocol"]
                size = res["size"]
                pkt_bytes = res["raw_data"]
                dst_port = res.get("dst_port", 0)
                src_port = res.get("src_port", 0)

                category = self.classifier.classify(
                    host, proto, size,
                    dst_port=dst_port,
                    src_port=src_port,
                    video_hint=video_hint
                )

                if host:
                    display_host = host[:28]
                else:
                    port = dst_port if dst_port != 0 else src_port
                    display_host = f"{dst_ip}:{port}"

                port_info = f"{src_port}→{dst_port}" if src_port or dst_port else "-"

                self.rate_window_bytes += size

                self.root.after(0, lambda ip=src_ip: self.init_new_ip_bucket(ip))

                db_total = self.terminal_database["全网总计"]
                db_total[category]["count"] += 1
                db_total[category]["bytes"] += size
                db_total["total_bytes"] += size
                if is_inner:
                    db_total["inner_bytes"] += size
                else:
                    db_total["outer_bytes"] += size

                if src_ip in self.terminal_database:
                    db_ip = self.terminal_database[src_ip]
                    db_ip[category]["count"] += 1
                    db_ip[category]["bytes"] += size
                    db_ip["total_bytes"] += size
                    if is_inner:
                        db_ip["inner_bytes"] += size
                    else:
                        db_ip["outer_bytes"] += size

                if len(self.detail_history[category]) > 800:
                    self.detail_history[category].pop(0)
                self.detail_history[category].append({
                    "src_ip": src_ip,
                    "row_data": (time.strftime('%H:%M:%S'), proto, display_host, f"{size} B"),
                    "port_info": port_info,
                    "net_type": net_type,
                    "raw_bytes": pkt_bytes
                })

                log_msg = f"📡 [{src_ip}] ➔ {proto} | {display_host.ljust(28)} ➔ {net_type} | {category}"
                self.root.after(0, lambda m=log_msg: self.ui.log_message(m))

                self.root.after(0, self.sync_data_to_view_table)
                self.root.after(0, self.async_refresh_ui_dashboard)

                if int(time.time()) % 2 == 0:
                    top = self.get_top_talkers(3)
                    rate = self.get_current_rate()
                    self.root.after(0, lambda t=top, r=rate: self.ui.update_top_talkers(t, r))

            except Exception:
                pass

    def async_refresh_ui_dashboard(self):
        current_dataset = self.terminal_database.get(self.selected_ip, self.terminal_database["全网总计"])
        self.ui.draw_native_pie(current_dataset, current_dataset["total_bytes"])
        if self.selected_ip != "全网总计":
            profile_text = self.classifier.generate_user_profile(current_dataset)
            self.profile_label.config(text=profile_text, fg="#A6192E")

    def sync_data_to_view_table(self):
        for item in self.ui.tree.get_children():
            self.ui.tree.delete(item)

        current_dataset = self.terminal_database.get(self.selected_ip, self.terminal_database["全网总计"])
        total_b = current_dataset.get("total_bytes", 0)

        for category in ["学习办公", "网络视频", "社交聊天", "休闲游戏", "系统服务", "购物金融", "其他流量"]:
            data = current_dataset[category]
            count = data["count"]
            kb_size = round(data["bytes"] / 1024, 2)
            percentage = f"{round((data['bytes'] / total_b) * 100, 2)}%" if total_b > 0 else "0.00%"
            self.ui.tree.insert("", tk.END, values=(category, count, kb_size, percentage))

    def handle_main_table_double_click(self, event):
        selected = self.ui.tree.selection()
        if not selected:
            return
        category = self.ui.tree.item(selected[0], "values")[0]

        all_records = self.detail_history.get(category, [])
        if self.selected_ip == "全网总计":
            filtered_records = all_records
        else:
            filtered_records = [r for r in all_records if r.get("src_ip") == self.selected_ip]

        self.ui.show_category_details(category, filtered_records, self.handle_sub_table_double_click)

    def handle_sub_table_double_click(self, sub_tree_widget, item_map):
        selected = sub_tree_widget.selection()
        if not selected or selected[0] not in item_map:
            return
        raw_bytes = item_map[selected[0]]
        self.ui.show_packet_hex_view(raw_bytes)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    center = TrafficControlCenter()
    center.run()