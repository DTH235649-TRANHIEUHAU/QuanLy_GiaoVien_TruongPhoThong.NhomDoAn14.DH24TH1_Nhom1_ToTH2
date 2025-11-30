import tkinter as tk
from tkinter import ttk, messagebox
import dbconnection

class GiaoDienBaoHiem:
    def __init__(self, frame_noi_dung):
        self.frame = frame_noi_dung
        
        # Xóa Form cũ
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Tiêu đề
        tk.Label(self.frame, text="QUẢN LÝ BẢO HIỂM XÃ HỘI", 
                 font=("Arial", 22, "bold"), fg="#003366", bg="white").pack(pady=15)

        # =================================================================
        #                        QUY ĐỊNH TỶ LỆ 
        # =================================================================
        top_frame = tk.LabelFrame(self.frame, text=" Quy định tỷ lệ đóng BH hiện hành ", bg="white", font=("Arial", 10, "bold"), fg="blue")
        top_frame.pack(fill="x", padx=20, pady=5)

        # Bảng tỷ lệ nhỏ
        cols_tyle = ("Loai", "NLD", "DonVi")
        self.tree_tyle = ttk.Treeview(top_frame, columns=cols_tyle, show="headings", height=4)
        
        self.tree_tyle.heading("Loai", text="Loại Bảo Hiểm")
        self.tree_tyle.heading("NLD", text="% Người Lao Động Đóng")
        self.tree_tyle.heading("DonVi", text="% Nhà Trường Đóng")
        
        self.tree_tyle.column("Loai", anchor="center"); self.tree_tyle.column("NLD", anchor="center"); self.tree_tyle.column("DonVi", anchor="center")
        self.tree_tyle.pack(fill="x", padx=10, pady=10)
        
        # Load tỷ lệ
        self.load_ty_le()

        # =================================================================
        #                   PHẦN 2: LỊCH SỬ ĐÓNG TIỀN 
        # =================================================================
        bot_frame = tk.LabelFrame(self.frame, text=" Chi tiết đóng bảo hiểm của Giáo Viên ", bg="white", font=("Arial", 10, "bold"), fg="green")
        bot_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # --- KHUNG TÌM KIẾM ---
        search_frame = tk.Frame(bot_frame, bg="white")
        search_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(search_frame, text="Tìm tên Giáo viên:", bg="white").pack(side="left")
        self.txt_tim = tk.Entry(search_frame, width=30, bd=2, relief="groove")
        self.txt_tim.pack(side="left", padx=10)
        self.txt_tim.bind('<Return>', lambda e: self.xu_ly_tim()) # Enter là tìm

        tk.Button(search_frame, text="Tìm kiếm", bg="#2196F3", fg="white", width=10, command=self.xu_ly_tim).pack(side="left")
        tk.Button(search_frame, text="Hiện tất cả", bg="gray", fg="white", width=10, command=self.load_lich_su).pack(side="left", padx=5)

        # --- BẢNG LỊCH SỬ ---
        cols_his = ("MaGV", "Ten", "Thang", "Nam", "Luong", "TienBH")
        self.tree_his = ttk.Treeview(bot_frame, columns=cols_his, show="headings")
        
        self.tree_his.heading("MaGV", text="Mã GV")
        self.tree_his.heading("Ten", text="Họ Tên")
        self.tree_his.heading("Thang", text="Tháng")
        self.tree_his.heading("Nam", text="Năm")
        self.tree_his.heading("Luong", text="Lương Đóng BH")
        self.tree_his.heading("TienBH", text="Tiền Đã Trừ (VNĐ)")
        
        self.tree_his.column("MaGV", width=80, anchor="center")
        self.tree_his.column("Ten", width=200)
        self.tree_his.column("Thang", width=50, anchor="center")
        self.tree_his.column("Nam", width=60, anchor="center")
        self.tree_his.column("Luong", width=120, anchor="e")
        self.tree_his.column("TienBH", width=150, anchor="e") 

        # Thanh cuộn
        sc = ttk.Scrollbar(bot_frame, orient="vertical", command=self.tree_his.yview)
        self.tree_his.configure(yscroll=sc.set)
        sc.pack(side="right", fill="y")
        self.tree_his.pack(fill="both", expand=True, padx=5, pady=5)

        self.load_lich_su()

    # --- HÀM XỬ LÝ ---
    def load_ty_le(self):
        # Lấy dữ liệu tỷ lệ từ SQL
        data = dbconnection.lay_ty_le_bao_hiem()
        for row in data:
            # row = (BHXH, 0.08, 0.175) -> Đổi ra % cho dễ nhìn
            r = list(row)
            r[1] = f"{r[1]*100}%" 
            r[2] = f"{r[2]*100}%"
            self.tree_tyle.insert("", "end", values=r)

    def load_lich_su(self):
        for item in self.tree_his.get_children(): self.tree_his.delete(item)
        data = dbconnection.lay_lich_su_bao_hiem()
        self.hien_thi(data)

    def xu_ly_tim(self):
        ten = self.txt_tim.get().strip()
        if ten == "": return self.load_lich_su()
        
        # Xóa cũ, tìm mới
        for item in self.tree_his.get_children(): self.tree_his.delete(item)
        data = dbconnection.tim_kiem_bao_hiem(ten)
        self.hien_thi(data)

    def hien_thi(self, data):
        for row in data:
            r = list(row)
            r[4] = "{:,.0f}".format(r[4])
            r[5] = "{:,.0f}".format(r[5])
            self.tree_his.insert("", "end", values=r)