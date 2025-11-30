import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime

import quan_ly_gv 
import tinh_luong
import bao_hiem
import hop_dong 
import phan_cong

class TrangChinh(tk.Toplevel):
    def __init__(self, ten_gv, quyen_gv):
        super().__init__()
        self.title("Hệ thống Quản lý Giáo Viên")
        self.state('zoomed') 
        
        self.ten_gv = ten_gv
        self.quyen_gv = quyen_gv # Lưu cái quyền này để lát kiểm tra
        
        self.tao_giao_dien()
        self.hien_thi_trang_chu() 
        self.cap_nhat_gio()

    def tao_giao_dien(self):
        # 1. HEADER
        header_frame = tk.Frame(self, bg="#66ff33", height=50)
        header_frame.pack(side="top", fill="x")
        tk.Label(header_frame, text="QUẢN LÝ GIÁO VIÊN", bg="#66ff33", font=("Arial", 14, "bold")).place(x=20, y=10)
        self.lbl_dong_ho = tk.Label(header_frame, text="...", bg="#66ff33", font=("Arial", 14, "bold"), fg="#003366")
        self.lbl_dong_ho.place(relx=0.5, y=25, anchor="center") 

        try:
            original_img = Image.open("icon_user.png")
            resized_img = original_img.resize((30, 30), Image.LANCZOS)
            self.icon_img = ImageTk.PhotoImage(resized_img, master=self)
            # Hiện thêm cái Chức vụ bên cạnh tên cho ngầu
            tk.Label(header_frame, text=f"  {self.ten_gv} ({self.quyen_gv})", 
                     image=self.icon_img, compound="left", bg="#66ff33", font=("Arial", 10, "italic")).place(relx=0.98, y=25, anchor="e")
        except:
            tk.Label(header_frame, text=f"{self.ten_gv} ({self.quyen_gv})", bg="#66ff33", font=("Arial", 10, "italic")).place(relx=0.98, y=15, anchor="e")

        # 2. MENU BÊN TRÁI
        menu_frame = tk.Frame(self, bg="white", width=200)
        menu_frame.pack(side="left", fill="y"); menu_frame.pack_propagate(False) 

        # --- XỬ LÝ PHÂN QUYỀN ---
        
        # Danh sách các Sếp được full quyền
        phan_quyen = ['HoiDongTruong', 'HieuTruong']
        
        # Kiểm tra xem người đang đăng nhập có phải là Hội Đồng Trường hoặc Hiệu Trưởng không?
        is_admin = self.quyen_gv in phan_quyen

        # Biến y dùng để đặt vị trí nút (tự động tăng dần)
        y_pos = 80
        khoang_cach = 50

        # 1. Trang chủ (Ai cũng được xem)
        self.tao_nut_menu(menu_frame, "Trang chủ", y_pos, self.hien_thi_trang_chu)
        y_pos += khoang_cach

        # 2. Hồ sơ giáo viên (Chỉ HDT và HT mới được )
        if is_admin:
            self.tao_nut_menu(menu_frame, "Hồ sơ giáo viên", y_pos, self.hien_thi_ho_so)
            y_pos += khoang_cach

        # 3. Tính lương (Chỉ HDT và HT xem)
        if is_admin:
            self.tao_nut_menu(menu_frame, "Tính lương", y_pos, self.hien_thi_tinh_luong)
            y_pos += khoang_cach

        # 4. Bảo hiểm (Chỉ HDT và HT xem)
        if is_admin:
            self.tao_nut_menu(menu_frame, "Bảo hiểm xã hội", y_pos, self.hien_thi_bao_hiem)
            y_pos += khoang_cach

        # 5. Hợp đồng (Chỉ HDT và HT xem)
        if is_admin:
            self.tao_nut_menu(menu_frame, "Hợp đồng lao động", y_pos, self.hien_thi_hop_dong)
            y_pos += khoang_cach

        # 6. Phân công (Ai cũng xem được để biết lịch dạy)
        self.tao_nut_menu(menu_frame, "Phân công giảng dạy", y_pos, self.hien_thi_phan_cong)
        y_pos += khoang_cach

        # Nút Đăng xuất
        tk.Button(menu_frame, text="Đăng xuất", bg="#f0f0f0", command=self.dang_xuat).place(x=10, y=550, width=180, height=40)

        # CONTENT
        self.content_frame = tk.Frame(self, bg="white")
        self.content_frame.pack(side="right", fill="both", expand=True)

    def cap_nhat_gio(self):
        gio_hien_tai = datetime.now().strftime("%H:%M:%S  -  %d/%m/%Y")
        self.lbl_dong_ho.config(text=gio_hien_tai)
        self.after(1000, self.cap_nhat_gio)

    def tao_nut_menu(self, frame_cha, ten_nut, vi_tri_y, lenh_thuc_hien):
        btn = tk.Button(frame_cha, text=ten_nut, bg="white", fg="#003366", font=("Arial", 11, "bold"), bd=0, highlightthickness=0, anchor="w", padx=20, cursor="hand2", command=lenh_thuc_hien)
        btn.place(x=0, y=vi_tri_y, width=200, height=45)
        def on_enter(e): btn['bg'] = "#e6f7ff"; btn['fg'] = "#0056b3"
        def on_leave(e): btn['bg'] = "white"; btn['fg'] = "#003366"
        btn.bind("<Enter>", on_enter); btn.bind("<Leave>", on_leave)

    def xoa_form_cu(self):
        if hasattr(self, 'content_frame'): self.content_frame.destroy()
        self.content_frame = tk.Frame(self, bg="white")
        self.content_frame.pack(side="right", fill="both", expand=True)

    def hien_thi_trang_chu(self):
        self.xoa_form_cu()
        try:
            load = Image.open("trangchu.jpg")
            load = load.resize((1100, 650), Image.LANCZOS)
            self.render_bg = ImageTk.PhotoImage(load, master=self)
            img_bg = tk.Label(self.content_frame, image=self.render_bg)
            img_bg.place(x=0, y=0, relwidth=1, relheight=1)
        except: pass

        tk.Label(self.content_frame, text="HỆ THỐNG QUẢN LÝ GIÁO VIÊN", font=("Arial", 24, "bold"), fg="#003366", bg="white").pack(pady=40)
        frame_thong_ke = tk.Frame(self.content_frame); frame_thong_ke.pack(pady=10)
        try:
            import dbconnection
            so_gv = dbconnection.lay_so_luong_gv()
            so_lop = dbconnection.dem_so_lop()
            so_pc = dbconnection.dem_so_phan_cong()
        except: so_gv=0; so_lop=0; so_pc=0

        self.tao_card_xin(frame_thong_ke, "GIÁO VIÊN", f"{so_gv}", "#2196F3", "👤")
        self.tao_card_xin(frame_thong_ke, "LỚP HỌC", f"{so_lop}", "#FF9800", "🏫")
        self.tao_card_xin(frame_thong_ke, "PHÂN CÔNG", f"{so_pc}", "#4CAF50", "📅")

        frame_bottom = tk.Frame(self.content_frame); frame_bottom.pack(fill="both", expand=True, padx=40, pady=20)
        frame_info = tk.LabelFrame(frame_bottom, text=" Thông tin đơn vị ", bg="white", font=("Arial", 11, "bold"), fg="#003366")
        frame_info.pack(side="left", fill="both", expand=True, padx=10)
        info_text = """
        🏫  TRƯỜNG TRUNG HỌC PHỔ THÔNG AN GIANG
        📍   Địa chỉ: 123 Đường Học Vấn, Quận Kiến Thức
        📞  Hotline: 0832.644.945 (Phòng Giáo Vụ)
        📧  Email: hau_dth235649@student.agu.edu.vn
        📅  Năm học hiện tại: 2025 - 2026
        """
        tk.Label(frame_info, text=info_text, bg="white", font=("Arial", 11), justify="left").pack(padx=20, pady=10, anchor="w")

        frame_note = tk.LabelFrame(frame_bottom, text=" Ghi chú nhanh ", bg="white", font=("Arial", 11, "bold"), fg="#8B4513")
        frame_note.pack(side="right", fill="both", expand=True, padx=10)
        txt_note = tk.Text(frame_note, height=8, width=40, font=("Arial", 10), bg="#fff9c4")
        txt_note.pack(padx=10, pady=10, fill="both", expand=True)
        txt_note.insert("1.0", "- Chiều thứ 2 ngày 01/12/2025 Báo cáo đồ án python.\n- Sau khi báo cáo, tối thi thử kỹ năng nghe nói tiếng Anh.\n- Sáng thứ 3 kiểm tra toán rời rạc.\n- Báo cáo lại Quản Trị Mạng chưa biết ngày cụ thể. ")

    def hien_thi_ho_so(self): self.xoa_form_cu(); quan_ly_gv.GiaoDienGV(self.content_frame)
    def hien_thi_tinh_luong(self): self.xoa_form_cu(); tinh_luong.GiaoDienTinhLuong(self.content_frame)
    def hien_thi_bao_hiem(self): self.xoa_form_cu(); bao_hiem.GiaoDienBaoHiem(self.content_frame)
    def hien_thi_hop_dong(self): self.xoa_form_cu(); hop_dong.GiaoDienHopDong(self.content_frame)
    def hien_thi_phan_cong(self): self.xoa_form_cu(); phan_cong.GiaoDienPhanCong(self.content_frame)

    def tao_card_xin(self, frame_cha, tieu_de, so_lieu, mau_nen, icon):
        card = tk.Frame(frame_cha, bg=mau_nen, bd=2, relief="raised", width=280, height=150)
        card.pack(side="left", padx=20); card.pack_propagate(False)
        content = tk.Frame(card, bg=mau_nen); content.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(content, text=icon, font=("Arial", 40), bg=mau_nen, fg="white").pack()
        tk.Label(content, text=so_lieu, font=("Arial", 28, "bold"), bg=mau_nen, fg="white").pack()
        tk.Label(content, text=tieu_de, font=("Arial", 12, "bold"), bg=mau_nen, fg="white").pack(pady=5)

    def dang_xuat(self):
        if messagebox.askyesno("Đăng xuất", "Bạn có chắc muốn đăng xuất?"):
            self.destroy(); self.master.deiconify()

if __name__ == "__main__":
    root = tk.Tk(); root.withdraw()
    app = TrangChinh("Test", "Admin"); root.mainloop()