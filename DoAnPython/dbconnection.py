import pyodbc

# --- 1. TẠO KẾT NỐI ---
def tao_ket_noi():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DESKTOP-33RD74C\\SQLEXPRESS;' 
            'DATABASE=QuanLyGiaoVien;' 
            'Trusted_Connection=yes;'
        )
        return conn
    except Exception as e:
        print("Lỗi kết nối SQL:", e)
        return None

# --- 2. ĐĂNG NHẬP ---
def kiem_tra_dang_nhap(email, mat_khau):
    try:
        conn = tao_ket_noi()
        if conn is None: return None
        cursor = conn.cursor()
        sql = "SELECT HoTen, VaiTroHeThong FROM GIAO_VIEN WHERE Email=? AND MatKhau=?"
        cursor.execute(sql, (email, mat_khau))
        ket_qua = cursor.fetchone()
        conn.close() 
        return ket_qua 
    except Exception as e:
        print("Lỗi đăng nhập:", e)
        return None

# --- 3. ĐẾM SỐ LƯỢNG ---
def lay_so_luong_gv():
    try:
        conn = tao_ket_noi()
        if conn is None: return 0
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM GIAO_VIEN")
        ket_qua = cursor.fetchone() 
        conn.close()
        return ket_qua[0] if ket_qua else 0
    except Exception as e:
        print("Lỗi đếm GV:", e) # In lỗi ra để biết đường sửa
        return 0

# --- 4. DANH SÁCH GV ---
def lay_danh_sach_gv():
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        sql = "SELECT MaGV, HoTen, NgaySinh, GioiTinh, SDT, Email, ChucVuChuyenMon, MatKhau FROM GIAO_VIEN"
        cursor.execute(sql)
        ds = cursor.fetchall()
        conn.close()
        return ds
    except Exception as e:
        return []

# --- 5. THÊM GV ---
def them_giao_vien(ma, ten, ngaysinh, gioitinh, sdt, email, chuyenmon, mat_khau):
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        sql = """INSERT INTO GIAO_VIEN (MaGV, HoTen, NgaySinh, GioiTinh, SDT, Email, ChucVuChuyenMon, MatKhau, VaiTroHeThong, MaMucLuong) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'GiaoVienBoMon', 1)"""
        val = (ma, ten, ngaysinh, gioitinh, sdt, email, chuyenmon, mat_khau)
        cursor.execute(sql, val)
        conn.commit()
        conn.close()
        return True 
    except Exception as e:
        print("Lỗi thêm:", e)
        return False

# --- 6. CẬP NHẬT GV ---
def cap_nhat_giao_vien(ma, ten, ngaysinh, gioitinh, sdt, email, chuyenmon, mat_khau):
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        sql = """UPDATE GIAO_VIEN SET HoTen=?, NgaySinh=?, GioiTinh=?, SDT=?, Email=?, ChucVuChuyenMon=?, MatKhau=? WHERE MaGV=?"""
        val = (ten, ngaysinh, gioitinh, sdt, email, chuyenmon, mat_khau, ma)
        cursor.execute(sql, val)
        conn.commit()
        conn.close()
        return True
    except: return False

# --- 7. XÓA GV ---
def xoa_giao_vien(ma):
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM GIAO_VIEN WHERE MaGV=?", (ma,))
        conn.commit()
        conn.close()
        return True
    except: return False

# --- 8. LẤY LIST MÃ GV ---
def lay_ds_ma_gv():
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        cursor.execute("SELECT MaGV FROM GIAO_VIEN ORDER BY MaGV ASC")
        ds = [row[0] for row in cursor.fetchall()]
        conn.close()
        return ds
    except: return []

# --- 9. LƯƠNG CƠ BẢN ---
def lay_luong_co_ban(ma_gv):
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        sql = "SELECT L.LuongCoDinh FROM GIAO_VIEN G JOIN LUONG_CO_BAN L ON G.MaMucLuong = L.MaMucLuong WHERE G.MaGV = ?"
        cursor.execute(sql, (ma_gv,))
        row = cursor.fetchone()
        conn.close()
        return float(row[0]) if row else 0
    except: return 0

# --- 10. LƯU LƯƠNG ---
def luu_bang_luong(ma, thang, nam, luong_cb, phu_cap, bao_hiem, thuc_linh):
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        cursor.execute("SELECT MaLuong FROM THONG_KE_LUONG WHERE MaGV=? AND Thang=? AND Nam=?", (ma, thang, nam))
        row = cursor.fetchone()
        
        if row: # Update
            sql = "UPDATE THONG_KE_LUONG SET LuongCoDinh=?, PhuCapKhac=?, TongTienBaoHiem=?, ThucLinh=? WHERE MaLuong=?"
            cursor.execute(sql, (luong_cb, phu_cap, bao_hiem, thuc_linh, row[0]))
        else: # Insert
            sql = "INSERT INTO THONG_KE_LUONG (MaGV, Thang, Nam, LuongCoDinh, PhuCapKhac, TongTienBaoHiem, ThucLinh) VALUES (?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(sql, (ma, thang, nam, luong_cb, phu_cap, bao_hiem, thuc_linh))
        conn.commit(); conn.close()
        return True
    except Exception as e:
        print("Lỗi lưu lương:", e)
        return False

# --- 11. LỊCH SỬ LƯƠNG ---
def lay_lich_su_luong():
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        sql = """SELECT T.MaLuong, T.Thang, T.Nam, G.HoTen, T.LuongCoDinh, T.PhuCapKhac, T.TongTienBaoHiem, T.ThucLinh 
                 FROM THONG_KE_LUONG T JOIN GIAO_VIEN G ON T.MaGV = G.MaGV ORDER BY T.Nam DESC, T.Thang DESC, G.HoTen ASC"""
        cursor.execute(sql)
        ds = cursor.fetchall()
        conn.close()
        return ds
    except: return []

# --- 12. TÌM KIẾM LƯƠNG ---
def tim_kiem_luong(thang, nam):
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        sql = """SELECT T.MaLuong, T.Thang, T.Nam, G.HoTen, T.LuongCoDinh, T.PhuCapKhac, T.TongTienBaoHiem, T.ThucLinh 
                 FROM THONG_KE_LUONG T JOIN GIAO_VIEN G ON T.MaGV = G.MaGV WHERE T.Thang=? AND T.Nam=? ORDER BY G.HoTen ASC"""
        cursor.execute(sql, (thang, nam))
        ds = cursor.fetchall()
        conn.close()
        return ds
    except: return []

# --- 13. HỢP ĐỒNG ---
def lay_danh_sach_hop_dong():
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        sql = "SELECT MaGV, HoTen, NgayVaoLam, ChucVuChuyenMon FROM GIAO_VIEN"
        cursor.execute(sql)
        ds = cursor.fetchall()
        conn.close()
        return ds
    except: return []

# --- 14. LẤY DANH SÁCH HỢP ĐỒNG ĐẦY ĐỦ ---
def lay_ds_hop_dong():
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        # Kết nối với bảng GIAO_VIEN để lấy tên giáo viên
        sql = """SELECT H.MaHD, H.MaGV, G.HoTen, H.LoaiHD, H.NgayBatDau, H.NgayKetThuc, H.TrangThai 
                 FROM HOP_DONG H 
                 JOIN GIAO_VIEN G ON H.MaGV = G.MaGV
                 ORDER BY H.MaHD ASC"""
        cursor.execute(sql)
        ds = cursor.fetchall()
        conn.close()
        return ds
    except: return []

# --- 15. THÊM HỢP ĐỒNG MỚI ---
def them_hop_dong(ma_gv, loai_hd, ngay_bd, ngay_kt, trang_thai):
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        # Nếu ngày kết thúc rỗng (Vô thời hạn) thì lưu là NULL
        if ngay_kt == "": 
            sql = "INSERT INTO HOP_DONG (MaGV, LoaiHD, NgayBatDau, TrangThai) VALUES (?, ?, ?, ?)"
            val = (ma_gv, loai_hd, ngay_bd, trang_thai)
        else:
            sql = "INSERT INTO HOP_DONG (MaGV, LoaiHD, NgayBatDau, NgayKetThuc, TrangThai) VALUES (?, ?, ?, ?, ?)"
            val = (ma_gv, loai_hd, ngay_bd, ngay_kt, trang_thai)
            
        cursor.execute(sql, val)
        conn.commit(); conn.close()
        return True
    except Exception as e:
        print(e)
        return False

# --- 16. CẬP NHẬT HỢP ĐỒNG ---
def sua_hop_dong(ma_hd, loai_hd, ngay_bd, ngay_kt, trang_thai):
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        
        if ngay_kt == "":
            sql = "UPDATE HOP_DONG SET LoaiHD=?, NgayBatDau=?, NgayKetThuc=NULL, TrangThai=? WHERE MaHD=?"
            val = (loai_hd, ngay_bd, trang_thai, ma_hd)
        else:
            sql = "UPDATE HOP_DONG SET LoaiHD=?, NgayBatDau=?, NgayKetThuc=?, TrangThai=? WHERE MaHD=?"
            val = (loai_hd, ngay_bd, ngay_kt, trang_thai, ma_hd)
            
        cursor.execute(sql, val)
        conn.commit(); conn.close()
        return True
    except: return False

# --- 17. XÓA HỢP ĐỒNG ---
def xoa_hop_dong(ma_hd):
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM HOP_DONG WHERE MaHD=?", (ma_hd,))
        conn.commit(); conn.close()
        return True
    except: return False

# --- 18. TÌM KIẾM GIÁO VIÊN THEO TÊN ---
def tim_kiem_gv_theo_ten(tu_khoa):
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        sql = """SELECT MaGV, HoTen, NgaySinh, GioiTinh, SDT, Email, ChucVuChuyenMon, MatKhau 
                 FROM GIAO_VIEN 
                 WHERE HoTen LIKE ? 
                 ORDER BY HoTen ASC"""
        
        # Thêm dấu % vào trước và sau để tìm kiếm: chứa từ khóa
        val = (f"%{tu_khoa}%", ) 
        
        cursor.execute(sql, val)
        ds = cursor.fetchall()
        conn.close()
        return ds
    except Exception as e:
        print("Lỗi tìm kiếm GV:", e)
        return []

# --- 19. LẤY BẢNG TỶ LỆ BẢO HIỂM ---
def lay_ty_le_bao_hiem():
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        sql = "SELECT LoaiBaoHiem, TyLeNguoiLaoDong, TyLeDonVi FROM BAO_HIEM"
        cursor.execute(sql)
        ds = cursor.fetchall()
        conn.close()
        return ds
    except: return []

# --- 20. LẤY DANH SÁCH ĐÓNG BẢO HIỂM ---
def lay_lich_su_bao_hiem():
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        sql = """SELECT T.MaGV, G.HoTen, T.Thang, T.Nam, T.LuongCoDinh, T.TongTienBaoHiem 
                 FROM THONG_KE_LUONG T
                 JOIN GIAO_VIEN G ON T.MaGV = G.MaGV
                 ORDER BY T.Nam DESC, T.Thang DESC, G.HoTen ASC""" 
                 
        cursor.execute(sql)
        ds = cursor.fetchall()
        conn.close()
        return ds
    except: return []

# --- 21. TÌM KIẾM BẢO HIỂM ---
def tim_kiem_bao_hiem(ten):
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        sql = """SELECT T.MaGV, G.HoTen, T.Thang, T.Nam, T.LuongCoDinh, T.TongTienBaoHiem 
                 FROM THONG_KE_LUONG T
                 JOIN GIAO_VIEN G ON T.MaGV = G.MaGV
                 WHERE G.HoTen LIKE ?
                 ORDER BY T.Nam DESC, T.Thang DESC, G.HoTen ASC"""
                 
        cursor.execute(sql, (f"%{ten}%",))
        ds = cursor.fetchall()
        conn.close()
        return ds
    except: return []

# --- 22. LẤY DANH SÁCH MÃ LỚP (Để đổ vào Combobox) ---
def lay_ds_lop():
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        # Sắp xếp tên lớp tăng dần cho dễ tìm (10A1 -> 12C5)
        sql = "SELECT MaLop FROM LOP_HOC ORDER BY MaLop ASC"
        cursor.execute(sql)
        ds = [row[0] for row in cursor.fetchall()]
        conn.close()
        return ds
    except: return []

# --- 23. LẤY DANH SÁCH PHÂN CÔNG HIỆN TẠI ---
def lay_ds_phan_cong():
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        # Lấy thêm Tên GV và Tên Lớp để hiển thị cho rõ
        sql = """SELECT P.MaPhanCong, G.HoTen, L.TenLop, P.TenMonHoc, P.SoTietTuan
                 FROM PHAN_CONG_GIANG_DAY P
                 JOIN GIAO_VIEN G ON P.MaGV = G.MaGV
                 JOIN LOP_HOC L ON P.MaLop = L.MaLop
                 ORDER BY L.TenLop ASC, G.HoTen ASC"""
        cursor.execute(sql)
        ds = cursor.fetchall()
        conn.close()
        return ds
    except: return []

# --- 24. THÊM PHÂN CÔNG MỚI ---
def them_phan_cong(magv, malop, mon, sotiet):
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        sql = "INSERT INTO PHAN_CONG_GIANG_DAY (MaGV, MaLop, TenMonHoc, SoTietTuan) VALUES (?, ?, ?, ?)"
        cursor.execute(sql, (magv, malop, mon, sotiet))
        conn.commit(); conn.close()
        return True
    except Exception as e:
        print("Lỗi thêm phân công:", e)
        return False

# --- 25. XÓA PHÂN CÔNG ---
def xoa_phan_cong(ma_pc):
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PHAN_CONG_GIANG_DAY WHERE MaPhanCong=?", (ma_pc,))
        conn.commit(); conn.close()
        return True
    except: return False

# --- 26. LẤY DANH SÁCH CHỈ GIÁO VIÊN ĐI DẠY (Loại bỏ Sếp) ---
def lay_ds_gv_giang_day():
    try:
        conn = tao_ket_noi()
        cursor = conn.cursor()
        
        # Chỉ lấy những người có vai trò là GV
        sql = """SELECT MaGV FROM GIAO_VIEN 
                 WHERE VaiTroHeThong IN ('GiaoVienBoMon', 'GiaoVienChuNhiem') 
                 ORDER BY MaGV ASC"""
                 
        cursor.execute(sql)
        ds = [row[0] for row in cursor.fetchall()]
        conn.close()
        return ds
    except: return []

# --- 27. ĐẾM SỐ LƯỢNG LỚP HỌC (Cho Trang chủ) ---
def dem_so_lop():
    try:
        conn = tao_ket_noi(); cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM LOP_HOC")
        kq = cursor.fetchone()
        conn.close()
        return kq[0] if kq else 0
    except: return 0

# --- 28. ĐẾM SỐ LƯỢNG PHÂN CÔNG (Cho Trang chủ) ---
def dem_so_phan_cong():
    try:
        conn = tao_ket_noi(); cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM PHAN_CONG_GIANG_DAY")
        kq = cursor.fetchone()
        conn.close()
        return kq[0] if kq else 0
    except: return 0

# --- 29. TÌM KIẾM PHÂN CÔNG (Theo tên GV hoặc tên Lớp) ---
def tim_kiem_phan_cong(tu_khoa):
    try:
        conn = tao_ket_noi(); cursor = conn.cursor()
        sql = """SELECT P.MaPhanCong, G.HoTen, L.TenLop, P.TenMonHoc, P.SoTietTuan
                 FROM PHAN_CONG_GIANG_DAY P
                 JOIN GIAO_VIEN G ON P.MaGV = G.MaGV
                 JOIN LOP_HOC L ON P.MaLop = L.MaLop
                 WHERE G.HoTen LIKE ? OR L.TenLop LIKE ?
                 ORDER BY L.TenLop ASC"""
        val = (f"%{tu_khoa}%", f"%{tu_khoa}%")
        cursor.execute(sql, val)
        ds = cursor.fetchall()
        conn.close()
        return ds
    except: return []