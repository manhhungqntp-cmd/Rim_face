import tkinter as tk
from tkinter import messagebox


class RimFaceApp:

  def __init__(self, root):
    self.root = root
    self.root.title(
        "Phần mềm Căn chỉnh Đồng tâm Trục - Rim & Face (Professional)"
    )
    self.root.geometry("1020x780")
    self.root.resizable(False, False)

    self.blink_target = []
    self.blink_state = True

    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    left_frame = tk.Frame(main_frame)
    left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

    right_frame = tk.Frame(main_frame, width=420)
    right_frame.pack(side="right", fill="both", padx=(0, 0))
    right_frame.pack_propagate(False)

    # 0. Chọn cách gá
    frame_setup = tk.LabelFrame(
        left_frame, text=" 0. Chọn cách gá đồng hồ so ", font=("Arial", 9, "bold")
    )
    frame_setup.pack(fill="x", pady=2)

    self.setup_var = tk.IntVar(value=1)
    tk.Radiobutton(
        frame_setup,
        text="Cách gá 1: Đồng hồ B đo mặt đầu bích phía đối diện",
        variable=self.setup_var,
        value=1,
        font=("Arial", 8),
        command=self.on_setup_change,
    ).pack(anchor="w", padx=5, pady=2)
    tk.Radiobutton(
        frame_setup,
        text="Cách gá 2: Đồng hồ B đo mặt đầu bích cùng bên trục động",
        variable=self.setup_var,
        value=2,
        font=("Arial", 8),
        command=self.on_setup_change,
    ).pack(anchor="w", padx=5, pady=2)

    # 1. Thông số hình học
    frame_geo = tk.LabelFrame(
        left_frame, text=" 1. Thông số hình học (mm) ", font=("Arial", 9, "bold")
    )
    frame_geo.pack(fill="x", pady=2)

    self.entries = {}
    labels_geo = [
        ("L1", "L1 (Từ khớp tới cặp chân trước):"),
        ("L2", "L2 (Từ khớp tới cặp chân sau):"),
        ("D", "D (Đường kính vòng quay / Khớp):"),
    ]
    for i, (k, text) in enumerate(labels_geo):
      tk.Label(frame_geo, text=text, font=("Arial", 9)).grid(
          row=i, column=0, sticky="w", padx=5, pady=2
      )
      entry = tk.Entry(frame_geo, width=10)
      entry.grid(row=i, column=1, padx=5, pady=2)
      entry.bind("<FocusIn>", lambda e, key=k: self.on_entry_focus(key))
      self.entries[k] = entry

    # 2. Đồng hồ Rim
    frame_rim = tk.LabelFrame(
        left_frame,
        text=" 2. Đồng hồ Hướng kính (RIM - a) (mm) ",
        font=("Arial", 9, "bold"),
    )
    frame_rim.pack(fill="x", pady=2)
    rim_keys = [
        ("a1", "a1 (12h):", 0, 0),
        ("a2", "a2 (3h):", 0, 2),
        ("a3", "a3 (6h):", 1, 0),
        ("a4", "a4 (9h):", 1, 2),
    ]
    for k, text, r, c in rim_keys:
      tk.Label(frame_rim, text=text).grid(
          row=r, column=c, sticky="w", padx=5, pady=1
      )
      entry = tk.Entry(frame_rim, width=8)
      entry.grid(row=r, column=c + 1, padx=3, pady=1)
      entry.bind("<FocusIn>", lambda e, key=k: self.on_entry_focus(key))
      self.entries[k] = entry

    # 3. Đồng hồ Face
    frame_face = tk.LabelFrame(
        left_frame,
        text=" 3. Đồng hồ Mặt bích (FACE - b) (mm) ",
        font=("Arial", 9, "bold"),
    )
    frame_face.pack(fill="x", pady=2)
    face_keys = [
        ("b1", "b1 (12h):", 0, 0),
        ("b2", "b2 (3h):", 0, 2),
        ("b3", "b3 (6h):", 1, 0),
        ("b4", "b4 (9h):", 1, 2),
    ]
    for k, text, r, c in face_keys:
      tk.Label(frame_face, text=text).grid(
          row=r, column=c, sticky="w", padx=5, pady=1
      )
      entry = tk.Entry(frame_face, width=8)
      entry.grid(row=r, column=c + 1, padx=3, pady=1)
      entry.bind("<FocusIn>", lambda e, key=k: self.on_entry_focus(key))
      self.entries[k] = entry

    btn_calc = tk.Button(
        left_frame,
        text="TÍNH TOÁN KẾT QUẢ",
        bg="#28a745",
        fg="white",
        font=("Arial", 10, "bold"),
        command=self.calculate,
    )
    btn_calc.pack(fill="x", pady=4)

    # 4. Kết quả
    frame_res = tk.LabelFrame(
        left_frame, text=" Kết quả hiệu chỉnh chi tiết ", font=("Arial", 9, "bold")
    )
    frame_res.pack(fill="both", expand=True, pady=2)

    self.text_result = tk.Text(frame_res, height=7, font=("Courier New", 9))
    self.text_result.pack(fill="both", expand=True, padx=3, pady=3)
    self.text_result.config(state=tk.DISABLED)

    # Canvas bên phải
    frame_canvas = tk.LabelFrame(
        right_frame,
        text=" Sơ đồ mô tả trực quan ",
        font=("Arial", 9, "bold"),
    )
    frame_canvas.pack(fill="both", expand=True)

    self.canvas = tk.Canvas(frame_canvas, bg="white", width=400, height=730)
    self.canvas.pack(fill="both", expand=True, padx=2, pady=2)

    self.draw_diagram()
    self.start_blink_animation()

  def draw_diagram(self):
    self.canvas.delete("all")

    # --- CÁCH GÁ 1 (C1) ---
    self.canvas.create_text(
        25, 20, text="C1", font=("Arial", 10, "bold"), fill="black"
    )
    self.canvas.create_line(45, 45, 345, 45, width=2, fill="black")
    self.canvas.create_rectangle(
        175, 20, 195, 70, fill="#bdc3c7", outline="black"
    )
    self.canvas.create_rectangle(
        265, 20, 285, 70, fill="#bdc3c7", outline="black"
    )

    self.canvas.create_line(275, 20, 275, 8, width=2, fill="black")
    self.canvas.create_line(185, 8, 275, 8, width=2, fill="black")
    self.canvas.create_line(185, 8, 185, 20, width=2, fill="black")

    self.tag_gauge_a1 = self.canvas.create_oval(
        175, 10, 195, 30, outline="blue", width=2, fill="white"
    )
    self.canvas.create_line(185, 30, 185, 45, width=2, fill="red")

    self.tag_gauge_b1 = self.canvas.create_oval(
        220, 35, 240, 55, outline="green", width=2, fill="white"
    )
    self.canvas.create_line(240, 45, 265, 45, width=2, fill="red")

    # --- CÁCH GÁ 2 (C2) ---
    self.canvas.create_text(
        25, 95, text="C2", font=("Arial", 10, "bold"), fill="black"
    )
    self.canvas.create_line(45, 120, 345, 120, width=2, fill="black")
    self.canvas.create_rectangle(
        175, 95, 195, 145, fill="#bdc3c7", outline="black"
    )
    self.canvas.create_rectangle(
        265, 95, 285, 145, fill="#bdc3c7", outline="black"
    )

    self.canvas.create_line(275, 95, 275, 83, width=2, fill="black")
    self.canvas.create_line(185, 83, 275, 83, width=2, fill="black")
    self.canvas.create_line(185, 83, 185, 95, width=2, fill="black")

    self.tag_gauge_a2 = self.canvas.create_oval(
        175, 85, 195, 105, outline="blue", width=2, fill="white"
    )
    self.canvas.create_line(185, 105, 185, 120, width=2, fill="red")

    self.canvas.create_line(125, 120, 125, 135, width=2, fill="black")
    self.tag_gauge_b2 = self.canvas.create_oval(
        115, 135, 135, 155, outline="green", width=2, fill="white"
    )
    self.canvas.create_line(135, 145, 175, 145, width=2, fill="red")

    # --- MÁY CỐ ĐỊNH VÀ MÁY ĐỘNG ---
    self.canvas.create_rectangle(
        35, 190, 175, 255, fill="#dcdcdc", outline="black", width=2
    )
    self.canvas.create_text(
        105, 222, text="MÁY CỐ ĐỊNH", font=("Arial", 8, "bold")
    )
    self.canvas.create_rectangle(
        175, 205, 190, 240, fill="#343a40", outline="black"
    )

    self.canvas.create_rectangle(
        215, 190, 355, 255, fill="#d1ecf1", outline="black", width=2
    )
    self.canvas.create_text(
        285, 222, text="MÁY ĐỘNG", font=("Arial", 8, "bold")
    )
    self.canvas.create_line(20, 222, 370, 222, width=3, fill="gray")

    self.canvas.create_rectangle(
        235, 255, 255, 280, fill="#adb5bd", outline="black"
    )
    self.canvas.create_rectangle(
        315, 255, 335, 280, fill="#adb5bd", outline="black"
    )

    self.tag_d = self.canvas.create_line(
        202, 185, 202, 258, arrow=tk.BOTH, fill="orange", width=2
    )
    self.tag_d_text = self.canvas.create_text(
        225, 222, text="D", fill="orange", font=("Arial", 10, "bold")
    )

    self.canvas.create_line(190, 298, 245, 298, arrow=tk.LAST, fill="blue")
    self.canvas.create_line(245, 298, 190, 298, arrow=tk.FIRST, fill="blue")
    self.tag_l1 = self.canvas.create_text(
        217, 288, text="L1", fill="blue", font=("Arial", 9, "bold")
    )

    self.canvas.create_line(190, 318, 325, 318, arrow=tk.LAST, fill="blue")
    self.canvas.create_line(325, 318, 190, 318, arrow=tk.FIRST, fill="blue")
    self.tag_l2 = self.canvas.create_text(
        257, 328, text="L2", fill="blue", font=("Arial", 9, "bold")
    )

    # --- MẶT ĐỒNG HÒ ĐO (RIM & FACE) ---
    cx1, cy1, r1 = 95, 415, 55
    self.canvas.create_oval(
        cx1 - r1,
        cy1 - r1,
        cx1 + r1,
        cy1 + r1,
        fill="#f8f9fa",
        outline="black",
        width=2,
    )
    self.canvas.create_text(
        cx1,
        cy1 - r1 - 10,
        text="Mặt đồng hồ RIM (a)",
        font=("Arial", 8, "bold"),
        fill="green",
    )

    self.tag_a1 = self.canvas.create_oval(
        cx1 - 4, cy1 - r1 - 4, cx1 + 4, cy1 - r1 + 4, fill="black"
    )
    self.canvas.create_text(
        cx1, cy1 - r1 + 10, text="12h (a1)", font=("Arial", 6)
    )

    self.tag_a2 = self.canvas.create_oval(
        cx1 + r1 - 4, cy1 - 4, cx1 + r1 + 4, cy1 + 4, fill="black"
    )
    self.canvas.create_text(
        cx1 + r1 - 12, cy1 + 8, text="3h (a2)", font=("Arial", 6)
    )

    self.tag_a3 = self.canvas.create_oval(
        cx1 - 4, cy1 + r1 - 4, cx1 + 4, cy1 + r1 + 4, fill="black"
    )
    self.canvas.create_text(
        cx1, cy1 + r1 - 10, text="6h (a3)", font=("Arial", 6)
    )

    self.tag_a4 = self.canvas.create_oval(
        cx1 - r1 - 4, cy1 - 4, cx1 - r1 + 4, cy1 + 4, fill="black"
    )
    self.canvas.create_text(
        cx1 - r1 + 12, cy1 + 8, text="9h (a4)", font=("Arial", 6)
    )

    cx2, cy2, r2 = 255, 415, 55
    self.canvas.create_oval(
        cx2 - r2,
        cy2 - r2,
        cx2 + r2,
        cy2 + r2,
        fill="#f8f9fa",
        outline="black",
        width=2,
    )
    self.canvas.create_text(
        cx2,
        cy2 - r2 - 10,
        text="Mặt đồng hồ FACE (b)",
        font=("Arial", 8, "bold"),
        fill="purple",
    )

    self.tag_b1 = self.canvas.create_oval(
        cx2 - 4, cy2 - r2 - 4, cx2 + 4, cy2 - r2 + 4, fill="black"
    )
    self.canvas.create_text(
        cx2, cy2 - r2 + 10, text="12h (b1)", font=("Arial", 6)
    )

    self.tag_b2 = self.canvas.create_oval(
        cx2 + r2 - 4, cy2 - 4, cx2 + r2 + 4, cy2 + 4, fill="black"
    )
    self.canvas.create_text(
        cx2 + r2 - 12, cy2 + 8, text="3h (b2)", font=("Arial", 6)
    )

    self.tag_b3 = self.canvas.create_oval(
        cx2 - 4, cy2 + r2 - 4, cx2 + 4, cy2 + r2 + 4, fill="black"
    )
    self.canvas.create_text(
        cx2, cy2 + r2 - 10, text="6h (b3)", font=("Arial", 6)
    )

    self.tag_b4 = self.canvas.create_oval(
        cx2 - r2 - 4, cy2 - 4, cx2 - r2 + 4, cy2 + 4, fill="black"
    )
    self.canvas.create_text(
        cx2 - r2 + 12, cy2 + 8, text="9h (b4)", font=("Arial", 6)
    )

    note_msg = (
        "Lưu ý: Cách gá 2 (Hình 14 tài liệu):\nTrị số đồng hồ B ngược lại"
        " khi tính toán lấy (b3-b1)."
    )
    self.canvas.create_text(
        175,
        490,
        text=note_msg,
        font=("Arial", 8, "italic"),
        fill="red",
        justify=tk.CENTER,
    )

  def on_setup_change(self):
    setup_val = self.setup_var.get()
    if setup_val == 1:
      self.blink_target = [self.tag_gauge_a1, self.tag_gauge_b1]
    else:
      self.blink_target = [self.tag_gauge_a2, self.tag_gauge_b2]

  def on_entry_focus(self, key):
    mapping = {
        "L1": [self.tag_l1],
        "L2": [self.tag_l2],
        "D": [self.tag_d, self.tag_d_text],
        "a1": [self.tag_a1],
        "a2": [self.tag_a2],
        "a3": [self.tag_a3],
        "a4": [self.tag_a4],
        "b1": [self.tag_b1],
        "b2": [self.tag_b2],
        "b3": [self.tag_b3],
        "b4": [self.tag_b4],
    }
    self.blink_target = mapping.get(key, [])

  def start_blink_animation(self):
    def animate():
      if self.blink_target:
        color = "red" if self.blink_state else "black"
        for item in self.blink_target:
          try:
            self.canvas.itemconfig(item, outline=color, fill=color)
          except:
            pass
        self.blink_state = not self.blink_state
      else:
        try:
          self.canvas.itemconfig(self.tag_l1, fill="blue")
          self.canvas.itemconfig(self.tag_l2, fill="blue")
          self.canvas.itemconfig(self.tag_d, fill="orange", outline="orange")
          for tag in [
              self.tag_a1,
              self.tag_a2,
              self.tag_a3,
              self.tag_a4,
              self.tag_b1,
              self.tag_b2,
              self.tag_b3,
              self.tag_b4,
          ]:
            self.canvas.itemconfig(tag, fill="black", outline="black")
        except:
          pass
      self.root.after(400, animate)

    animate()

  def parse_float(self, key):
    return float(self.entries[key].get().strip().replace(",", "."))

  def calculate(self):
    try:
      setup_type = self.setup_var.get()
      L1 = self.parse_float("L1")
      L2 = self.parse_float("L2")
      D = self.parse_float("D")

      a1 = self.parse_float("a1")
      a2 = self.parse_float("a2")
      a3 = self.parse_float("a3")
      a4 = self.parse_float("a4")

      b1 = self.parse_float("b1")
      b2 = self.parse_float("b2")
      b3 = self.parse_float("b3")
      b4 = self.parse_float("b4")

      if setup_type == 1:
        diff_b_vert = b3 - b1
        diff_b_horiz = b4 - b2
      else:
        diff_b_vert = b1 - b3
        diff_b_horiz = b2 - b4

      ya = (a3 - a1) / 2
      yb1 = ya + (diff_b_vert / D) * L1
      yb2 = ya + (diff_b_vert / D) * L2

      xa = (a2 - a4) / 2
      xb1 = xa + (diff_b_horiz / D) * L1
      xb2 = xa + (diff_b_horiz / D) * L2

      res_text = f"======= KẾT QUẢ HIỆU CHỈNH (CÁCH GÁ {setup_type}) =======\n\n"

      res_text += "1. PHƯƠNG ĐỨNG (VERTICAL - Căn đệm Shim):\n"
      res_text += f"   - Chân trước (L1): {yb1:+.3f} mm\n"
      if yb1 >= 0:
        res_text += f"     ➔ (+) Thêm lá căn dày {abs(yb1):.3f} mm\n"
      else:
        res_text += f"     ➔ (-) Rút bớt lá căn {abs(yb1):.3f} mm\n"

      res_text += f"   - Chân sau (L2):   {yb2:+.3f} mm\n"
      if yb2 >= 0:
        res_text += f"     ➔ (+) Thêm lá căn dày {abs(yb2):.3f} mm\n"
      else:
        res_text += f"     ➔ (-) Rút bớt lá căn {abs(yb2):.3f} mm\n\n"

      res_text += "2. PHƯƠNG NGANG (HORIZONTAL - Dịch chuyển):\n"
      res_text += f"   - Chân trước (L1): {xb1:+.3f} mm\n"
      if xb1 >= 0:
        res_text += f"     ➔ (+) Dịch chuyển sang phải {abs(xb1):.3f} mm\n"
      else:
        res_text += f"     ➔ (-) Dịch chuyển sang trái {abs(xb1):.3f} mm\n"

      res_text += f"   - Chân sau (L2):   {xb2:+.3f} mm\n"
      if xb2 >= 0:
        res_text += f"     ➔ (+) Dịch chuyển sang phải {abs(xb2):.3f} mm\n"
      else:
        res_text += f"     ➔ (-) Dịch chuyển sang trái {abs(xb2):.3f} mm\n"

      self.text_result.config(state=tk.NORMAL)
      self.text_result.delete("1.0", tk.END)
      self.text_result.insert(tk.END, res_text)
      self.text_result.config(state=tk.DISABLED)

    except ValueError:
      messagebox.showerror(
          "Lỗi dữ liệu",
          "Vui lòng kiểm tra lại! Đảm bảo tất cả các ô đều là số hợp lệ.",
      )


if __name__ == "__main__":
  root = tk.Tk()
  app = RimFaceApp(root)
  root.mainloop()