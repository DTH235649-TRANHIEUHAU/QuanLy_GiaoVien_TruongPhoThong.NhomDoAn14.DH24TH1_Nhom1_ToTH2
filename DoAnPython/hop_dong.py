import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import dbconnection

class GiaoDienHopDong:
    def __init__(self, frame_noi_dung):
        self.frame = frame_noi_dung
        
        # Xóa cái cũ
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Tiêu đề
        tk.Label(self.frame, text="QUẢN LÝ HỢP ĐỒNG LAO ĐỘNG", 
                 font=("Arial", 22, "bold"), fg="#003366", bg="white").pack(pady=15)

        # --- KHUNG NHẬP LIỆU ---
        frame_nhap = tk.LabelFrame(self.frame, text=" Thông tin hợp đồng ", bg="white", font=("Arial", 10, "bold"), fg="green")
        frame_nhap.pack(fill="x", padx=20, pady=5)

        # Dòng 1: Mã HĐ (Ẩn/Readonly) - Chọn GV - Loại HĐ
        row1 = tk.Frame(frame_nhap, bg="white")
        row1.pack(fill="x", pady=5, padx=10)

        tk.Label(row1, text="Mã HĐ:", bg="white").pack(side="left")
        self.txt_ma_hd = tk.Entry(row1, width=10, state="readonly") # Không cho sửa mã
        self.txt_ma_hd.pack(side="left", padx=5)

        tk.Label(row1, text="Giáo Viên:", bg="white").pack(side="left", padx=(15, 0))
        # Lấy danh sách Mã GV từ file dbconnection
        self.cb_gv = ttk.Combobox(row1, width=25, values=dbconnection.lay_ds_ma_gv())
        self.cb_gv.pack(side="left", padx=5)

        tk.Label(row1, text="Loại HĐ:", bg="white").pack(side="left", padx=(15, 0))
        self.cb_loai = ttk.Combobox(row1, width=20, values=["Thử việc (2 tháng)", "Có thời hạn 1 năm", "Có thời hạn 3 năm", "Vô thời hạn"])
        self.cb_loai.current(1)
        self.cb_loai.pack(side="left", padx=5)

        # Dòng 2: Ngày bắt đầu - Ngày kết thúc - Trạng thái
        row2 = tk.Frame(frame_nhap, bg="white")
        row2.pack(fill="x", pady=10, padx=10)

        tk.Label(row2, text="Ngày Bắt Đầu:", bg="white").pack(side="left")
        self.de_ngay_bd = DateEntry(row2, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.de_ngay_bd.pack(side="left", padx=5)

        tk.Label(row2, text="Ngày Kết Thúc:", bg="white").pack(side="left", padx=(15, 0))
        self.de_ngay_kt = DateEntry(row2, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.de_ngay_kt.pack(side="left", padx=5)
        # Nút xóa ngày kết thúc (cho HĐ vô thời hạn)
        tk.Button(row2, text="X", bg="#ddd", command=lambda: self.de_ngay_kt.delete(0, "end"), width=2).pack(side="left")

        tk.Label(row2, text="Trạng Thái:", bg="white").pack(side="left", padx=(15, 0))
        self.cb_trang_thai = ttk.Combobox(row2, width=15, values=["Đang hiệu lực", "Đã hết hạn", "Đã thanh lý"])
        self.cb_trang_thai.current(0)
        self.cb_trang_thai.pack(side="left", padx=5)

        # --- KHUNG NÚT BẤM ---
        frame_nut = tk.Frame(self.frame, bg="white")
        frame_nut.pack(pady=10)

        self.tao_nut(frame_nut, "Thêm Mới", "#28a745", self.cn_them)
        self.tao_nut(frame_nut, "Cập Nhật", "#ffc107", self.cn_sua, text_color="black")
        self.tao_nut(frame_nut, "Xóa HĐ", "#dc3545", self.cn_xoa)
        self.tao_nut(frame_nut, "Làm Mới", "#6c757d", self.load_data)

        # --- BẢNG DANH SÁCH ---
        columns = ("MaHD", "MaGV", "TenGV", "LoaiHD", "NgayBD", "NgayKT", "TrangThai")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=12)
        
        self.tree.heading("MaHD", text="ID")
        self.tree.heading("MaGV", text="Mã GV")
        self.tree.heading("TenGV", text="Họ Tên")
        self.tree.heading("LoaiHD", text="Loại Hợp Đồng")
        self.tree.heading("NgayBD", text="Ngày Bắt Đầu")
        self.tree.heading("NgayKT", text="Ngày Kết Thúc")
        self.tree.heading("TrangThai", text="Trạng Thái")
        
        # Chỉnh cột
        self.tree.column("MaHD", width=40, anchor="center")
        self.tree.column("MaGV", width=60, anchor="center")
        self.tree.column("TenGV", width=150)
        self.tree.column("LoaiHD", width=120)
        self.tree.column("NgayBD", width=90, anchor="center")
        self.tree.column("NgayKT", width=90, anchor="center")
        self.tree.column("TrangThai", width=100, anchor="center")

        self.tree.pack(padx=20, pady=5, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.chon_dong)
        
        self.load_data()

    # --- CÁC HÀM XỬ LÝ ---
    def tao_nut(self, frame, text, color, cmd, text_color="white"):
        btn = tk.Button(frame, text=text, bg=color, fg=text_color, font=("Arial", 10, "bold"), width=12, command=cmd)
        btn.pack(side="left", padx=10)

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        data = dbconnection.lay_ds_hop_dong()
        for row in data:
            r = list(row)
            # Xử lý nếu ngày kết thúc là None
            if r[5] is None: r[5] = "---"
            self.tree.insert("", "end", values=r)
            
        # Dọn form nhập
        self.txt_ma_hd.config(state="normal"); self.txt_ma_hd.delete(0, "end"); self.txt_ma_hd.config(state="readonly")

    def chon_dong(self, event):
        sel = self.tree.focus()
        if sel:
            val = self.tree.item(sel, 'values')
            # Điền ngược lại form
            self.txt_ma_hd.config(state="normal"); self.txt_ma_hd.delete(0, "end"); self.txt_ma_hd.insert(0, val[0]); self.txt_ma_hd.config(state="readonly")
            self.cb_gv.set(val[1])
            self.cb_loai.set(val[3])
            try: self.de_ngay_bd.set_date(val[4])
            except: pass
            
            if val[5] != "---":
                try: self.de_ngay_kt.set_date(val[5])
                except: pass
            else:
                self.de_ngay_kt.delete(0, "end")
                
            self.cb_trang_thai.set(val[6])

    def cn_them(self):
        mgv = self.cb_gv.get()
        if mgv == "": return messagebox.showwarning("Thiếu", "Chưa chọn Giáo viên!")
        
        loai = self.cb_loai.get()
        bd = self.de_ngay_bd.get()
        kt = self.de_ngay_kt.get()
        tt = self.cb_trang_thai.get()
        
        if dbconnection.them_hop_dong(mgv, loai, bd, kt, tt):
            messagebox.showinfo("OK", "Đã thêm hợp đồng!")
            self.load_data()
        else: messagebox.showerror("Lỗi", "Thêm thất bại!")

    def cn_sua(self):
        mhd = self.txt_ma_hd.get()
        if mhd == "": return messagebox.showwarning("Lỗi", "Chưa chọn hợp đồng để sửa!")
        
        loai = self.cb_loai.get()
        bd = self.de_ngay_bd.get()
        kt = self.de_ngay_kt.get()
        tt = self.cb_trang_thai.get()
        
        if dbconnection.sua_hop_dong(mhd, loai, bd, kt, tt):
            messagebox.showinfo("OK", "Đã cập nhật!")
            self.load_data()
        else: messagebox.showerror("Lỗi", "Sửa thất bại!")

    def cn_xoa(self):
        mhd = self.txt_ma_hd.get()
        if mhd == "": return
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa hợp đồng này?"):
            if dbconnection.xoa_hop_dong(mhd):
                self.load_data()
                messagebox.showinfo("OK", "Đã xóa!")