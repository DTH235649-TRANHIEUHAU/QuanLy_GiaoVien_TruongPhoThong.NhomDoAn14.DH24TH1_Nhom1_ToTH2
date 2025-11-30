import sys
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
from tkcalendar import DateEntry 
import dbconnection 

class GiaoDienGV:
    def __init__(self, frame_noi_dung):
        self.frame = frame_noi_dung
        
        # Xóa form cũ
        for widget in self.frame.winfo_children():
            widget.destroy()
            
        # =============================================================
        #                    STYLE & CẤU HÌNH
        # =============================================================
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="#003366", foreground="white", font=("Arial", 10, "bold"))
        style.configure("Treeview", font=("Arial", 10), rowheight=30)
        style.map("Treeview", background=[('selected', '#2E8B57')]) 

        # Tiêu đề
        tk.Label(self.frame, text="QUẢN LÝ HỒ SƠ GIÁO VIÊN", 
                 font=("Arial", 22, "bold"), fg="#003366", bg="white").pack(pady=(10, 5))

        # =============================================================
        #                        KHUNG TÌM KIẾM
        # =============================================================
        frame_tim = tk.Frame(self.frame, bg="white")
        frame_tim.pack(fill="x", padx=20, pady=5)
        
        container_tim = tk.Frame(frame_tim, bg="#f0f8ff", bd=1, relief="solid")
        container_tim.pack(pady=5)

        tk.Label(container_tim, text="Tìm kiếm tên GV:", bg="#f0f8ff", font=("Arial", 10, "bold")).pack(side="left", padx=10, pady=5)
        
        self.txt_tim_kiem = tk.Entry(container_tim, width=30, font=("Arial", 10))
        self.txt_tim_kiem.pack(side="left", padx=5, pady=5)
        self.txt_tim_kiem.bind('<Return>', lambda event: self.cn_tim_kiem())

        btn_tim = tk.Button(container_tim, text="Tìm Ngay", bg="#007bff", fg="white", font=("Arial", 9, "bold"), 
                            width=10, command=self.cn_tim_kiem)
        btn_tim.pack(side="left", padx=10, pady=5)

        # Nút Hủy tìm
        tk.Button(container_tim, text="Hủy tìm / Xem tất cả", bg="gray", fg="white", width=15, command=self.load_data).pack(side="left", padx=5)


        # =============================================================
        #                         FORM NHẬP LIỆU
        # =============================================================
        frame_nhap = tk.LabelFrame(self.frame, text=" Thông tin chi tiết ", bg="white", font=("Arial", 10, "bold"), fg="#555")
        frame_nhap.pack(pady=5, padx=20, ipadx=10, ipady=5)

        # Cột Trái
        tk.Label(frame_nhap, text="Mã GV:", bg="white").grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.txt_ma = tk.Entry(frame_nhap, width=30, font=("Arial", 10), bd=2, relief="groove")
        self.txt_ma.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(frame_nhap, text="Họ Tên:", bg="white").grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.txt_ten = tk.Entry(frame_nhap, width=30, font=("Arial", 10), bd=2, relief="groove")
        self.txt_ten.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(frame_nhap, text="Ngày sinh:", bg="white").grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.txt_ngaysinh = DateEntry(frame_nhap, width=28, background='darkblue', foreground='white', borderwidth=2, 
                                      date_pattern='yyyy-mm-dd', year=1990, font=("Arial", 10))
        self.txt_ngaysinh.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(frame_nhap, text="Giới tính:", bg="white").grid(row=3, column=0, sticky="e", padx=10, pady=10)
        self.cb_gioitinh = ttk.Combobox(frame_nhap, values=["Nam", "Nữ"], width=28, font=("Arial", 10))
        self.cb_gioitinh.grid(row=3, column=1, padx=10, pady=10)
        self.cb_gioitinh.current(0)

        # Cột Phải
        tk.Label(frame_nhap, text="Số ĐT:", bg="white").grid(row=0, column=2, sticky="e", padx=10, pady=10)
        self.txt_sdt = tk.Entry(frame_nhap, width=30, font=("Arial", 10), bd=2, relief="groove")
        self.txt_sdt.grid(row=0, column=3, padx=10, pady=10)

        tk.Label(frame_nhap, text="Email:", bg="white").grid(row=1, column=2, sticky="e", padx=10, pady=10)
        self.txt_email = tk.Entry(frame_nhap, width=30, font=("Arial", 10), bd=2, relief="groove")
        self.txt_email.grid(row=1, column=3, padx=10, pady=10)

        tk.Label(frame_nhap, text="Chức vụ/CM:", bg="white").grid(row=2, column=2, sticky="e", padx=10, pady=10)
        self.txt_mon = tk.Entry(frame_nhap, width=30, font=("Arial", 10), bd=2, relief="groove")
        self.txt_mon.grid(row=2, column=3, padx=10, pady=10)
        
        tk.Label(frame_nhap, text="Mật khẩu:", bg="white").grid(row=3, column=2, sticky="e", padx=10, pady=10)
        self.txt_matkhau = tk.Entry(frame_nhap, width=30, font=("Arial", 10), bd=2, relief="groove")
        self.txt_matkhau.grid(row=3, column=3, padx=10, pady=10)

        # --- KHU VỰC NÚT BẤM ---
        frame_nut = tk.Frame(self.frame, bg="white")
        frame_nut.pack(pady=15)

        self.tao_nut_xin(frame_nut, "Thêm Mới", "#28a745", self.cn_them) 
        self.tao_nut_xin(frame_nut, "Cập Nhật", "#ffc107", self.cn_sua, text_color="black") 
        self.tao_nut_xin(frame_nut, "Xóa Bỏ", "#dc3545", self.cn_xoa) 

        # --- BẢNG DANH SÁCH ---
        columns = ("Ma", "Ten", "NgaySinh", "GioiTinh", "SDT", "Email", "ChuyenMon", "MatKhau")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=10)
        
        self.tree.heading("Ma", text="Mã GV"); self.tree.heading("Ten", text="Họ Tên")
        self.tree.heading("NgaySinh", text="Ngày Sinh"); self.tree.heading("GioiTinh", text="Giới Tính")
        self.tree.heading("SDT", text="Số ĐT"); self.tree.heading("Email", text="Email")
        self.tree.heading("ChuyenMon", text="Chức Vụ"); self.tree.heading("MatKhau", text="Mật Khẩu")
        
        self.tree.column("Ma", width=60, anchor="center"); self.tree.column("Ten", width=150)
        self.tree.column("NgaySinh", width=80, anchor="center"); self.tree.column("GioiTinh", width=60, anchor="center")
        self.tree.column("SDT", width=90, anchor="center"); self.tree.column("Email", width=150)
        self.tree.column("ChuyenMon", width=100); self.tree.column("MatKhau", width=80)
        
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y", pady=(0, 20), padx=(0, 20))
        self.tree.pack(pady=(0, 20), padx=(20, 0), fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.chon_dong)
        self.load_data()

    # --- CÁC HÀM XỬ LÝ ---
    def tao_nut_xin(self, frame, text, bg_color, command, text_color="white"):
        btn = tk.Button(frame, text=text, bg=bg_color, fg=text_color, font=("Arial", 10, "bold"), width=12, height=1, bd=0, cursor="hand2", command=command)
        btn.pack(side="left", padx=10)
        def on_enter(e): btn['bg'] = "black"; btn['fg'] = "white"
        def on_leave(e): btn['bg'] = bg_color; btn['fg'] = text_color
        btn.bind("<Enter>", on_enter); btn.bind("<Leave>", on_leave)

    def load_data(self):
        self.txt_tim_kiem.delete(0, tk.END) 
        for item in self.tree.get_children(): self.tree.delete(item)
        try:
            conn = dbconnection.tao_ket_noi()
            cursor = conn.cursor()
            sql = "SELECT MaGV, HoTen, NgaySinh, GioiTinh, SDT, Email, ChucVuChuyenMon, MatKhau FROM GIAO_VIEN"
            cursor.execute(sql); rows = cursor.fetchall(); conn.close()
            for row in rows: self.tree.insert("", "end", values=list(row))
        except: pass

    def cn_tim_kiem(self):
        tu_khoa = self.txt_tim_kiem.get().strip()
        if tu_khoa == "": messagebox.showwarning("Nhắc nhở", "Vui lòng nhập tên cần tìm!"); return
        for item in self.tree.get_children(): self.tree.delete(item)
        ket_qua = dbconnection.tim_kiem_gv_theo_ten(tu_khoa)
        if len(ket_qua) == 0: messagebox.showinfo("Kết quả", "Không tìm thấy giáo viên nào!"); self.load_data()
        else:
            for row in ket_qua: self.tree.insert("", "end", values=list(row))

    def chon_dong(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, 'values')
            self.txt_ma.delete(0, tk.END); self.txt_ma.insert(0, values[0])
            self.txt_ten.delete(0, tk.END); self.txt_ten.insert(0, values[1])
            try: self.txt_ngaysinh.set_date(values[2]) 
            except: pass
            self.cb_gioitinh.set(values[3])
            self.txt_sdt.delete(0, tk.END); self.txt_sdt.insert(0, values[4])
            self.txt_email.delete(0, tk.END); self.txt_email.insert(0, values[5])
            self.txt_mon.delete(0, tk.END); self.txt_mon.insert(0, values[6])
            self.txt_matkhau.delete(0, tk.END); self.txt_matkhau.insert(0, values[7])

    def cn_them(self):
        ma = self.txt_ma.get(); ten = self.txt_ten.get()
        ngaysinh = self.txt_ngaysinh.get(); gioitinh = self.cb_gioitinh.get()
        sdt = self.txt_sdt.get(); email = self.txt_email.get()
        mon = self.txt_mon.get(); mk = self.txt_matkhau.get()
        if ma == "": return
        if dbconnection.them_giao_vien(ma, ten, ngaysinh, gioitinh, sdt, email, mon, mk):
            messagebox.showinfo("OK", "Thành công!"); self.load_data()
        else: messagebox.showerror("Lỗi", "Thất bại!")

    def cn_sua(self):
        ma = self.txt_ma.get(); ten = self.txt_ten.get()
        ngaysinh = self.txt_ngaysinh.get(); gioitinh = self.cb_gioitinh.get()
        sdt = self.txt_sdt.get(); email = self.txt_email.get()
        mon = self.txt_mon.get(); mk = self.txt_matkhau.get()
        if ma == "": return
        if messagebox.askyesno("Xác nhận", f"Cập nhật GV: {ma}?"):
            if dbconnection.cap_nhat_giao_vien(ma, ten, ngaysinh, gioitinh, sdt, email, mon, mk):
                messagebox.showinfo("OK", "Đã cập nhật!"); self.load_data()
            else: messagebox.showerror("Lỗi", "Thất bại!")

    def cn_xoa(self):
        ma = self.txt_ma.get()
        if ma == "": return
        if messagebox.askyesno("Xác nhận", f"XÓA giáo viên {ma}?"):
            if dbconnection.xoa_giao_vien(ma):
                messagebox.showinfo("OK", "Đã xóa!"); self.load_data()
                self.txt_ma.delete(0, tk.END); self.txt_ten.delete(0, tk.END)
            else: messagebox.showerror("Lỗi", "Không xóa được!")