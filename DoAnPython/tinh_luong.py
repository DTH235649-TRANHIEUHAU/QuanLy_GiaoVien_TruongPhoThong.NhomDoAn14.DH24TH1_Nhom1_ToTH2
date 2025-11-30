import tkinter as tk
from tkinter import ttk, messagebox
import dbconnection

class GiaoDienTinhLuong:
    def __init__(self, frame_noi_dung):
        self.frame = frame_noi_dung
        
        # Xóa form cũ
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Tiêu đề
        tk.Label(self.frame, text="QUẢN LÝ VÀ TÍNH LƯƠNG", 
                 font=("Arial", 20, "bold"), fg="#003366", bg="white").pack(pady=10)

        # =================================================================
        #                     KHUNG NHẬP LIỆU & TÌM KIẾM 
        # =================================================================
        top_frame = tk.Frame(self.frame, bg="white")
        top_frame.pack(fill="x", padx=10, pady=5)

        # --- TÍNH LƯƠNG MỚI ---
        nhap_frame = tk.LabelFrame(top_frame, text=" Lập Phiếu Lương ", bg="white", font=("Arial", 10, "bold"), fg="green")
        nhap_frame.pack(side="left", fill="both", expand=True, padx=5)

        # Dòng 1: Chọn GV + Phụ cấp
        row1 = tk.Frame(nhap_frame, bg="white")
        row1.pack(fill="x", pady=5)
        
        tk.Label(row1, text="Giáo viên:", bg="white").pack(side="left", padx=5)
        self.cb_magv = ttk.Combobox(row1, width=15, values=dbconnection.lay_ds_ma_gv())
        self.cb_magv.pack(side="left", padx=5)

        tk.Label(row1, text="Phụ cấp (VNĐ):", bg="white").pack(side="left", padx=(20, 5))
        self.txt_phucap = tk.Entry(row1, width=15)
        self.txt_phucap.insert(0, "0")
        self.txt_phucap.pack(side="left", padx=5)

        # Dòng 2: Thời gian tính lương + Nút Tính
        row2 = tk.Frame(nhap_frame, bg="white")
        row2.pack(fill="x", pady=5)

        tk.Label(row2, text="Tháng:", bg="white").pack(side="left", padx=5)
        self.sb_thang_nhap = ttk.Spinbox(row2, from_=1, to=12, width=3)
        self.sb_thang_nhap.set(11)
        self.sb_thang_nhap.pack(side="left", padx=5)

        tk.Label(row2, text="Năm:", bg="white").pack(side="left", padx=5)
        self.sb_nam_nhap = ttk.Spinbox(row2, from_=2020, to=2030, width=5)
        self.sb_nam_nhap.set(2025)
        self.sb_nam_nhap.pack(side="left", padx=5)

        # Nút Tính lương
        tk.Button(row2, text="TÍNH & LƯU", bg="#FF8C00", fg="white", font=("Arial", 9, "bold"), 
                  command=self.xu_ly_tinh_luong).pack(side="left", padx=30)


        # --- TÌM KIẾM ---
        tim_frame = tk.LabelFrame(top_frame, text=" Tìm Kiếm / Lọc ", bg="white", font=("Arial", 10, "bold"), fg="blue")
        tim_frame.pack(side="right", fill="both", expand=True, padx=5)

        tk.Label(tim_frame, text="Xem lương tháng:", bg="white").pack(pady=5)
        
        search_row = tk.Frame(tim_frame, bg="white")
        search_row.pack()

        self.sb_thang_tim = ttk.Spinbox(search_row, from_=1, to=12, width=3)
        self.sb_thang_tim.set(11)
        self.sb_thang_tim.pack(side="left", padx=5)

        tk.Label(search_row, text="/", bg="white").pack(side="left")

        self.sb_nam_tim = ttk.Spinbox(search_row, from_=2020, to=2030, width=5)
        self.sb_nam_tim.set(2025)
        self.sb_nam_tim.pack(side="left", padx=5)

        # Nút tìm kiếm
        tk.Button(search_row, text="Xem", bg="blue", fg="white", width=8, 
                  command=self.xu_ly_tim_kiem).pack(side="left", padx=10)
        
        # Nút xem tất cả
        tk.Button(tim_frame, text="Xem tất cả lịch sử", bg="gray", fg="white", borderwidth=0,
                  command=self.load_lich_su).pack(pady=5)


        # =================================================================
        #                       BẢNG DANH SÁCH 
        # =================================================================
        table_frame = tk.Frame(self.frame, bg="white")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("Thang", "Nam", "TenGV", "LuongCung", "BaoHiem", "PhuCap", "ThucLinh")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        self.tree.heading("Thang", text="Tháng")
        self.tree.heading("Nam", text="Năm")
        self.tree.heading("TenGV", text="Họ Tên GV")
        self.tree.heading("LuongCung", text="Lương Cứng")
        self.tree.heading("BaoHiem", text="Trừ BH (10.5%)")
        self.tree.heading("PhuCap", text="Phụ Cấp")
        self.tree.heading("ThucLinh", text="THỰC LĨNH")
        
        # Căn chỉnh cột
        self.tree.column("Thang", width=50, anchor="center")
        self.tree.column("Nam", width=60, anchor="center")
        self.tree.column("TenGV", width=200)
        self.tree.column("LuongCung", width=120, anchor="e")
        self.tree.column("BaoHiem", width=120, anchor="e")
        self.tree.column("PhuCap", width=100, anchor="e")
        self.tree.column("ThucLinh", width=150, anchor="e")

        # Thanh cuộn
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        
        self.load_lich_su()

    # --- HÀM XỬ LÝ ---
    def hien_thi_len_bang(self, data):
        # Hàm dùng chung để đổ dữ liệu lên bảng
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for row in data:
            r = list(row)
            # Format tiền
            r[4] = "{:,.0f}".format(r[4])
            r[5] = "{:,.0f}".format(r[5])
            r[6] = "{:,.0f}".format(r[6])
            r[7] = "{:,.0f}".format(r[7])
            
            # Hiển thị đúng cột
            hien_thi = (r[1], r[2], r[3], r[4], r[6], r[5], r[7])
            self.tree.insert("", "end", values=hien_thi)

    def load_lich_su(self):
        data = dbconnection.lay_lich_su_luong()
        self.hien_thi_len_bang(data)

    def xu_ly_tim_kiem(self):
        # Load theo tháng năm
        t = self.sb_thang_tim.get()
        n = self.sb_nam_tim.get()
        data = dbconnection.tim_kiem_luong(t, n)
        
        if not data:
            messagebox.showinfo("Thông báo", f"Không tìm thấy bảng lương nào của tháng {t}/{n}")
        
        self.hien_thi_len_bang(data)

    def xu_ly_tinh_luong(self):
        magv = self.cb_magv.get()
        thang = self.sb_thang_nhap.get()
        nam = self.sb_nam_nhap.get()
        phucap = self.txt_phucap.get()

        if magv == "":
            messagebox.showwarning("Thiếu", "Vui lòng chọn Mã GV!")
            return

        luong_cb_goc = dbconnection.lay_luong_co_ban(magv)
        if luong_cb_goc == 0:
            messagebox.showerror("Lỗi", "GV chưa có lương cơ bản!")
            return

        luong_cb = float(luong_cb_goc) 
        tong_bao_hiem = luong_cb * 0.105 
        try: pc = float(phucap)
        except: pc = 0
            
        thuc_linh = luong_cb + pc - tong_bao_hiem

        kq = dbconnection.luu_bang_luong(magv, thang, nam, luong_cb, pc, tong_bao_hiem, thuc_linh)
        
        if kq:
            messagebox.showinfo("Thành công", f"Đã tính lương xong cho {magv}")
            # Tính xong thì tự động Tìm kiếm hiển thị tháng vừa tính
            self.sb_thang_tim.set(thang)
            self.sb_nam_tim.set(nam)
            self.xu_ly_tim_kiem()
        else:
            messagebox.showerror("Lỗi", "Không lưu được!")