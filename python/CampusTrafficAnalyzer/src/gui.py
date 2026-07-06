# gui.py
# -*- coding: utf-8 -*-
"""
四川大学《计算机通信与网络》课程设计
模块：gui.py (校园网专用版：告警面板 + Top Talkers + 实时速率)
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import math


class CampusTrafficGUI:
    def __init__(self, root, start_cb, pause_cb, clear_cb, export_cb):
        self.root = root
        self.root.title("SCU 校园网多终端流量审计与异常检测系统")
        self.root.geometry("1280x800")
        self.root.configure(bg="#F4F6F9")

        self.start_cb = start_cb
        self.pause_cb = pause_cb
        self.clear_cb = clear_cb
        self.export_cb = export_cb

        # 1. 顶部标题
        title_frame = tk.Frame(self.root, bg="#A6192E", height=55)
        title_frame.pack(fill=tk.X, side=tk.TOP)
        tk.Label(title_frame, text="SCU CAMPUS NETWORK TRAFFIC ANALYSIS & ANOMALY DETECTION",
                 font=("Century Gothic", 14, "bold"), fg="#FFFFFF", bg="#A6192E").pack(pady=12)

        # 2. 底部控制面板 (暴露为实例属性，供 main.py 直接访问)
        self.control_panel = tk.Frame(self.root, bg="#F4F6F9", bd=1, relief=tk.GROOVE)
        self.control_panel.pack(fill=tk.X, side=tk.BOTTOM, padx=15, pady=10)

        self.start_btn = tk.Button(self.control_panel, text="▶ 启动审计", font=("微软雅黑", 10, "bold"),
                                   bg="#28A745", fg="#FFFFFF", width=14, command=self.start_cb)
        self.start_btn.pack(side=tk.LEFT, padx=10, pady=8)

        self.pause_btn = tk.Button(self.control_panel, text="⏸ 暂停", font=("微软雅黑", 10, "bold"),
                                   bg="#6C757D", fg="#FFFFFF", width=10, state=tk.DISABLED, command=self.pause_cb)
        self.pause_btn.pack(side=tk.LEFT, padx=5, pady=8)

        self.clear_btn = tk.Button(self.control_panel, text="🔄 安全重置", font=("微软雅黑", 10),
                                   bg="#F8F9FA", fg="#212529", width=12, command=self.clear_cb)
        self.clear_btn.pack(side=tk.LEFT, padx=5, pady=8)

        self.export_btn = tk.Button(self.control_panel, text="📥 导出报表", font=("微软雅黑", 10),
                                    bg="#17A2B8", fg="#FFFFFF", width=14, command=self.export_cb)
        self.export_btn.pack(side=tk.RIGHT, padx=10, pady=8)

        self.status_label = tk.Label(self.control_panel, text="系统就绪: 等待启动校园网混杂监听...",
                                     font=("微软雅黑", 10), fg="#6C757D", bg="#F4F6F9")
        self.status_label.pack(side=tk.RIGHT, padx=20)

        # 3. 中部工作区
        main_work_frame = tk.Frame(self.root, bg="#F4F6F9")
        main_work_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=2)

        # ================= 左半部分：饼图 + 分类表 =================
        left_panel = tk.Frame(main_work_frame, bg="#F4F6F9")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_frame = tk.LabelFrame(left_panel, text="📊 终端上网行为应用动态占比统计",
                                          font=("微软雅黑", 10, "bold"), bg="#FFFFFF", fg="#A6192E", bd=2)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, pady=4)
        self.pie_canvas = tk.Canvas(self.canvas_frame, bg="#FFFFFF", highlightthickness=0, height=260)
        self.pie_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        table_frame = tk.LabelFrame(left_panel, text="📋 数据链路分类行为矩阵 (双击下钻)",
                                    font=("微软雅黑", 10, "bold"), bg="#FFFFFF", fg="#A6192E", bd=2)
        table_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=4)

        columns = ("category", "count", "size", "percentage")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)
        self.tree.heading("category", text="上网行为大类")
        self.tree.heading("count", text="报文计数")
        self.tree.heading("size", text="数据量 (KB)")
        self.tree.heading("percentage", text="带宽占比")
        self.tree.column("category", width=110, anchor=tk.CENTER)
        self.tree.column("count", width=90, anchor=tk.E)
        self.tree.column("size", width=100, anchor=tk.E)
        self.tree.column("percentage", width=90, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # ================= 右半部分：三层堆叠 =================
        right_panel = tk.Frame(main_work_frame, bg="#F4F6F9", width=480)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(15, 0))
        right_panel.pack_propagate(False)

        # A. Top Talkers + 实时速率
        top_frame = tk.LabelFrame(right_panel, text="🏆 校园网 Top Talkers & 实时速率",
                                  font=("微软雅黑", 10, "bold"), bg="#FFFFFF", fg="#1CC88A", bd=2, height=120)
        top_frame.pack(fill=tk.X, pady=4)
        top_frame.pack_propagate(False)

        self.rate_label = tk.Label(top_frame, text="⚡ 实时速率: 0.00 KB/s", font=("微软雅黑", 10, "bold"),
                                   bg="#FFFFFF", fg="#E74A3B")
        self.rate_label.pack(anchor=tk.W, padx=10, pady=(5, 0))

        self.top_tree = ttk.Treeview(top_frame, columns=("rank", "ip", "traffic"), show="headings", height=3)
        self.top_tree.heading("rank", text="排名")
        self.top_tree.heading("ip", text="终端 IP")
        self.top_tree.heading("traffic", text="累计流量")
        self.top_tree.column("rank", width=50, anchor=tk.CENTER)
        self.top_tree.column("ip", width=140, anchor=tk.CENTER)
        self.top_tree.column("traffic", width=100, anchor=tk.E)
        self.top_tree.pack(fill=tk.X, padx=10, pady=5)

        # B. 异常告警面板
        alert_frame = tk.LabelFrame(right_panel, text="🚨 校园网异常行为告警",
                                    font=("微软雅黑", 10, "bold"), bg="#FFF3CD", fg="#856404", bd=2, height=140)
        alert_frame.pack(fill=tk.X, pady=4)
        alert_frame.pack_propagate(False)

        self.alert_list = tk.Listbox(alert_frame, font=("微软雅黑", 9), bg="#FFF3CD", fg="#856404",
                                     selectmode=tk.SINGLE, height=5)
        self.alert_list.pack(fill=tk.BOTH, expand=True, padx=8, pady=5)

        # C. 日志台
        log_frame = tk.LabelFrame(right_panel, text="👁️ 局域网态势感知实时流水",
                                  font=("微软雅黑", 10, "bold"), bg="#FFFFFF", fg="#343A40", bd=2)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=4)

        self.log_area = scrolledtext.ScrolledText(log_frame, font=("Consolas", 9), bg="#1E1E1E", fg="#00FF00",
                                                  insertbackground="white")
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def log_message(self, text):
        self.log_area.insert(tk.END, text + "\n")
        self.log_area.see(tk.END)

    def clear_log_area(self):
        self.log_area.delete('1.0', tk.END)

    def update_alert_panel(self, alert_history):
        self.alert_list.delete(0, tk.END)
        for t, msg in reversed(alert_history[-6:]):
            self.alert_list.insert(tk.END, f"[{t}] {msg}")

    def update_top_talkers(self, top_list, rate=0):
        self.rate_label.config(text=f"⚡ 实时速率: {rate:.2f} KB/s")
        for item in self.top_tree.get_children():
            self.top_tree.delete(item)
        for i, (ip, byte_count) in enumerate(top_list, 1):
            val = f"{round(byte_count / 1024, 1)} KB" if byte_count < 1024 * 1024 else f"{round(byte_count / (1024 * 1024), 2)} MB"
            self.top_tree.insert("", tk.END, values=(f"#{i}", ip, val))

    def draw_native_pie(self, current_dataset, total_bytes):
        self.pie_canvas.delete("all")
        w = self.pie_canvas.winfo_width()
        h = self.pie_canvas.winfo_height()
        if w < 10 or h < 10:
            w, h = 420, 260

        cx, cy = w * 0.35, h * 0.5
        r = min(w, h) * 0.38

        if total_bytes == 0:
            self.pie_canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="#E9ECEF", outline="#CED4DA", width=2)
            self.pie_canvas.create_text(cx, cy, text="局域网静默中\n暂无流载荷", font=("微软雅黑", 11, "bold"),
                                        fill="#6C757D", justify=tk.CENTER)
            return

        start_angle = 0.0
        legend_x = w * 0.72
        legend_y_start = h * 0.12

        categories = ["学习办公", "网络视频", "社交聊天", "休闲游戏", "系统服务", "购物金融", "其他流量"]
        valid_index = 0

        for category in categories:
            data = current_dataset[category]
            b_size = data["bytes"]
            color = data["color"]
            if b_size == 0:
                continue

            extent = (b_size / total_bytes) * 360.0
            self.pie_canvas.create_arc(cx - r, cy - r, cx + r, cy + r, start=start_angle, extent=extent,
                                       fill=color, outline="#FFFFFF", width=1.5)

            mid_angle = math.radians(start_angle + extent / 2.0)
            tx = cx + (r * 0.65) * math.cos(mid_angle)
            ty = cy - (r * 0.65) * math.sin(mid_angle)
            pct = (b_size / total_bytes) * 100
            if pct > 4.5:
                self.pie_canvas.create_text(tx, ty, text=f"{round(pct, 1)}%", font=("Calibri", 9, "bold"),
                                            fill="#FFFFFF")

            ly_pos = legend_y_start + valid_index * 26
            self.pie_canvas.create_rectangle(legend_x, ly_pos, legend_x + 16, ly_pos + 14, fill=color, outline="")

            kb_str = f"{round(b_size / 1024, 1)} KB" if b_size < 1024 * 1024 else f"{round(b_size / (1024 * 1024), 2)} MB"
            self.pie_canvas.create_text(legend_x + 25, ly_pos + 7, text=f"{category} ({kb_str})", font=("微软雅黑", 9),
                                        anchor=tk.W, fill="#333333")

            start_angle += extent
            valid_index += 1

    def show_category_details(self, category, filtered_records, sub_table_double_click_cb):
        sub_win = tk.Toplevel(self.root)
        sub_win.title(f"🔍 深度审计下钻明细 - 【{category}】")
        sub_win.geometry("960x500")
        sub_win.configure(bg="#F4F6F9")

        top_bar = tk.Frame(sub_win, bg="#343A40", height=40)
        top_bar.pack(fill=tk.X)
        tk.Label(top_bar, text=f"当前大类【{category}】底层网络层捕获流水 (双击查看十六进制载荷)",
                 font=("微软雅黑", 10), fg="#FFC107", bg="#343A40").pack(pady=8)

        sub_frame = tk.Frame(sub_win, bg="#FFFFFF")
        sub_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        cols = ("time", "src_ip", "host", "protocol", "port", "net", "size")
        sub_tree = ttk.Treeview(sub_frame, columns=cols, show="headings", height=15)
        sub_tree.heading("time", text="时间")
        sub_tree.heading("src_ip", text="源IP")
        sub_tree.heading("host", text="目标主机")
        sub_tree.heading("protocol", text="协议")
        sub_tree.heading("port", text="端口")
        sub_tree.heading("net", text="内外网")
        sub_tree.heading("size", text="包长")

        sub_tree.column("time", width=80, anchor=tk.CENTER)
        sub_tree.column("src_ip", width=110, anchor=tk.CENTER)
        sub_tree.column("host", width=240, anchor=tk.W)
        sub_tree.column("protocol", width=70, anchor=tk.CENTER)
        sub_tree.column("port", width=80, anchor=tk.CENTER)
        sub_tree.column("net", width=60, anchor=tk.CENTER)
        sub_tree.column("size", width=70, anchor=tk.E)

        vsb = ttk.Scrollbar(sub_frame, orient="vertical", command=sub_tree.yview)
        sub_tree.configure(yscrollcommand=vsb.set)
        sub_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        item_map = {}
        for rec in reversed(filtered_records):
            t_time, proto, host, size_str = rec["row_data"]
            src_ip = rec.get("src_ip", "未知设备")
            port_info = rec.get("port_info", "-")
            net_type = rec.get("net_type", "-")
            node_id = sub_tree.insert("", tk.END, values=(t_time, src_ip, host, proto, port_info, net_type, size_str))
            item_map[node_id] = rec["raw_bytes"]

        sub_tree.bind("<Double-1>", lambda e: sub_table_double_click_cb(sub_tree, item_map))

    def show_packet_hex_view(self, raw_bytes):
        hex_win = tk.Toplevel(self.root)
        hex_win.title("💾 原始链路层报文十六进制结构载荷还原")
        hex_win.geometry("720x450")

        container = tk.Frame(hex_win, bg="#F8F9FA")
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        v_scroll = tk.Scrollbar(container, orient=tk.VERTICAL)
        h_scroll = tk.Scrollbar(hex_win, orient=tk.HORIZONTAL)

        txt_area = tk.Text(container, font=("Consolas", 10), bg="#F8F9FA", fg="#212529",
                           wrap=tk.NONE, yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        v_scroll.config(command=txt_area.yview)
        h_scroll.config(command=txt_area.xview)

        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        txt_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        if not raw_bytes:
            txt_area.insert(tk.END, "当前报文为空或无应用层可导出载荷。")
            txt_area.configure(state=tk.DISABLED)
            return

        lines = []
        for offset in range(0, len(raw_bytes), 16):
            chunk = raw_bytes[offset:offset + 16]
            hex_str = " ".join(f"{b:02X}" for b in chunk)
            if len(chunk) < 16:
                hex_str = hex_str.ljust(47)
            ascii_str = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
            lines.append(f"{offset:04X}  {hex_str}  | {ascii_str} |")

        txt_area.insert(tk.END, "\n".join(lines))
        txt_area.configure(state=tk.DISABLED)