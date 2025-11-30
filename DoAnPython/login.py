import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk 
import os

import dbconnection 
from main import TrangChinh

class CuaSoDangNhap(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Đăng nhập")
        self.geometry("600x350")
        self.configure(bg="#011f26") 

        self.tao_giao_dien()

    def tao_giao_dien(self):
        # --- 2 THANH NGANG MÀU XANH ---
        tk.Frame(self, bg="#000080").place(x=0, y=0, width=600, height=20)
        tk.Frame(self, bg="#000080").place(x=0, y=330, width=600, height=20)

        # --- Ảnh bên trái ---
        try:
            img = Image.open("login.png")
            img = img.resize((200, 200))
            self.hinh_anh = ImageTk.PhotoImage(img)
            lbl_anh = tk.Label(self, image=self.hinh_anh, bg="#011f26")
            lbl_anh.place(x=20, y=70)
        except:
            lbl_anh = tk.Label(self, text="[Ảnh]", bg="white")
            lbl_anh.place(x=50, y=100)

        # --- Form nhập bên phải ---
        lbl_tieu_de = tk.Label(self, text="QUẢN LÝ GIÁO VIÊN", font=("Arial", 18, "bold"), bg="#011f26", fg="white")
        lbl_tieu_de.place(x=250, y=40) 

        # Email
        tk.Label(self, text="Email:", font=("Arial", 10), bg="#011f26", fg="white").place(x=250, y=100)
        self.txt_email = tk.Entry(self, width=30, font=("Arial", 10))
        self.txt_email.place(x=330, y=100)
        self.txt_email.insert(0,"admin")

        # Mật khẩu
        tk.Label(self, text="Mật khẩu:", font=("Arial", 10), bg="#011f26", fg="white").place(x=250, y=150)
        self.txt_pass = tk.Entry(self, width=30, font=("Arial", 10), show="*")
        self.txt_pass.place(x=330, y=150)
        self.txt_pass.insert(0,"123")

        # Nút bấm
        btn_dang_nhap = tk.Button(self, text="ĐĂNG NHẬP", bg="green", fg="white", font=("Arial", 10, "bold"), command=self.xu_ly_dang_nhap)
        btn_dang_nhap.place(x=330, y=200, width=100, height=35)

        btn_thoat = tk.Button(self, text="THOÁT", bg="red", fg="white", font=("Arial", 10, "bold"), command=self.destroy)
        btn_thoat.place(x=450, y=200, width=80, height=35)

        self.bind('<Return>', self.xu_ly_dang_nhap)

    def xu_ly_dang_nhap(self, event=None):
        email = self.txt_email.get()
        mat_khau = self.txt_pass.get()

        ket_qua = dbconnection.kiem_tra_dang_nhap(email, mat_khau)

        if ket_qua:
            ten_gv = ket_qua[0]
            quyen_gv = ket_qua[1]
            messagebox.showinfo("Thành công", f"Xin chào: {ten_gv}")
            self.withdraw() 
            app_chinh = TrangChinh(ten_gv, quyen_gv) 
            app_chinh.master = self 
        else:
            messagebox.showerror("Thất bại", "Sai email hoặc mật khẩu!")

if __name__ == "__main__":
    app = CuaSoDangNhap()
    app.mainloop()