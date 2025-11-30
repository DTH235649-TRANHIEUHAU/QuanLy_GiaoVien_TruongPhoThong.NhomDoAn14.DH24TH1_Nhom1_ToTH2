import tkinter as tk
from tkinter import ttk, messagebox
import dbconnection

class GiaoDienPhanCong:
    def __init__(self, frame_noi_dung):
        self.frame = frame_noi_dung
        for widget in self.frame.winfo_children(): widget.destroy()

        # Tiêu đề
        tk.Label(self.frame, text="PHÂN CÔNG GIẢNG DẠY", 
                 font=("Arial", 22, "bold"), fg="#003366", bg="white").pack(pady=15)

        # =================================================================
        #                   KHUNG NHẬP LIỆU & TÌM KIẾM     
        # =================================================================
        top_frame = tk.Frame(self.frame, bg="white")
        top_frame.pack(fill="x", padx=10, pady=5)

        # --- KHUNG NHẬP ---
        nhap_frame = tk.LabelFrame(top_frame, text=" Xếp Lịch Dạy ", bg="white", font=("Arial", 10, "bold"), fg="#8B4513")
        nhap_frame.pack(side="left", fill="both", expand=True, padx=5)

        # Dòng 1
        row1 = tk.Frame(nhap_frame, bg="white"); row1.pack(fill="x", pady=5)
        tk.Label(row1, text="Giáo Viên:", bg="white").pack(side="left", padx=5)
        self.cb_gv = ttk.Combobox(row1, width=22, values=dbconnection.lay_ds_ma_gv())
        self.cb_gv.pack(side="left", padx=5)
        
        tk.Label(row1, text="Lớp Dạy:", bg="white").pack(side="left", padx=5)
        self.cb_lop = ttk.Combobox(row1, width=15, values=dbconnection.lay_ds_lop())
        self.cb_lop.pack(side="left", padx=5)

        # Dòng 2
        row2 = tk.Frame(nhap_frame, bg="white"); row2.pack(fill="x", pady=5)
        tk.Label(row2, text="Môn Học:", bg="white").pack(side="left", padx=5)
        self.txt_mon = tk.Entry(row2, width=25); self.txt_mon.pack(side="left", padx=5)
        
        tk.Label(row2, text="Số Tiết:", bg="white").pack(side="left", padx=5)
        self.sb_tiet = ttk.Spinbox(row2, from_=1, to=30, width=5); self.sb_tiet.set(4)
        self.sb_tiet.pack(side="left", padx=5)

        # --- KHUNG TÌM KIẾM & NÚT ---
        btn_frame = tk.LabelFrame(top_frame, text=" Tác Vụ ", bg="white", font=("Arial", 10, "bold"), fg="blue")
        btn_frame.pack(side="right", fill="both", padx=5)

        # Ô Tìm kiếm
        search_row = tk.Frame(btn_frame, bg="white"); search_row.pack(pady=5)
        tk.Label(search_row, text="Tìm (Tên/Lớp):", bg="white").pack(side="left")
        self.txt_tim = tk.Entry(search_row, width=20)
        self.txt_tim.pack(side="left", padx=5)
        tk.Button(search_row, text="Tìm", bg="#007bff", fg="white", width=8, command=self.cn_tim).pack(side="left")

        # Các nút chức năng
        action_row = tk.Frame(btn_frame, bg="white"); action_row.pack(pady=5)
        self.tao_nut(action_row, "Thêm", "#28a745", self.cn_them)
        self.tao_nut(action_row, "Xóa", "#dc3545", self.cn_xoa)
        self.tao_nut(action_row, "Làm Mới", "gray", self.load_data)

        # =================================================================
        #                        BẢNG DANH SÁCH 
        # =================================================================
        columns = ("ID", "TenGV", "Lop", "Mon", "SoTiet")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("ID", text="ID"); self.tree.column("ID", width=30, anchor="center")
        self.tree.heading("TenGV", text="Họ Tên Giáo Viên"); self.tree.column("TenGV", width=200)
        self.tree.heading("Lop", text="Lớp"); self.tree.column("Lop", width=80, anchor="center")
        self.tree.heading("Mon", text="Môn Giảng Dạy"); self.tree.column("Mon", width=150)
        self.tree.heading("SoTiet", text="Số Tiết/Tuần"); self.tree.column("SoTiet", width=80, anchor="center")

        sc = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=sc.set)
        sc.pack(side="right", fill="y", padx=10)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        self.load_data()

    # --- HÀM XỬ LÝ ---
    def tao_nut(self, frame, text, color, cmd):
        tk.Button(frame, text=text, bg=color, fg="white", font=("Arial", 9, "bold"), width=10, command=cmd).pack(side="left", padx=2)

    def load_data(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        data = dbconnection.lay_ds_phan_cong()
        for row in data: self.tree.insert("", "end", values=list(row))

    def cn_tim(self):
        k = self.txt_tim.get().strip()
        if k == "": return self.load_data()
        for item in self.tree.get_children(): self.tree.delete(item)
        data = dbconnection.tim_kiem_phan_cong(k)
        for row in data: self.tree.insert("", "end", values=list(row))

    def cn_them(self):
        mgv = self.cb_gv.get(); mlop = self.cb_lop.get()
        mon = self.txt_mon.get(); tiet = self.sb_tiet.get()
        if mgv=="" or mlop=="" or mon=="": return messagebox.showwarning("Thiếu", "Nhập đủ thông tin!")
        if dbconnection.them_phan_cong(mgv, mlop, mon, tiet):
            messagebox.showinfo("OK", "Đã phân công!"); self.load_data()
        else: messagebox.showerror("Lỗi", "Thất bại!")

    def cn_xoa(self):
        sel = self.tree.focus()
        if not sel: return
        val = self.tree.item(sel, 'values')
        if messagebox.askyesno("Xóa", f"Xóa phân công {val[3]} của {val[1]}?"):
            if dbconnection.xoa_phan_cong(val[0]): self.load_data(); messagebox.showinfo("OK", "Đã xóa!")