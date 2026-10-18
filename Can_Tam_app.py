import streamlit as st

# Thiết lập cấu hình trang
st.set_page_config(
    page_title="Phần mềm Căn chỉnh Đồng tâm Trục - Rim & Face",
    layout="centered",
)

st.title("🔧 Căn chỉnh Đồng tâm Trục (Rim & Face)")
st.write(
    "Ứng dụng tính toán hiệu chỉnh tâm máy cho kỹ thuật viên bảo trì trực tiếp"
    " trên điện thoại/web."
)

# --- 0. Chọn cách gá ---
st.subheader("0. Chọn cách gá đồng hồ so")
setup_type = st.radio(
    "Chọn phương án gá đặt:",
    options=[1, 2],
    format_func=lambda x: (
        "Cách gá 1: Đồng hồ B đo mặt đầu bích phía đối diện"
        if x == 1
        else "Cách gá 2: Đồng hồ B đo mặt đầu bích cùng bên trục động"
    ),
)

# === CHÈN HÌNH CẢNH SƠ ĐỒ VÀO ĐÂY ===
try:
  st.image(
      "So_do.png",
      caption="Sơ đồ mô tả gá đặt đồng hồ so (Rim & Face)",
      use_container_width=True,
  )
except Exception:
  st.info("💡 (Thêm file so_do.png vào GitHub để hiển thị sơ đồ minh họa)")
# ===================================

# --- 1. Thông số hình học ---
st.subheader("1. Thông số hình học (mm)")
col1, col2, col3 = st.columns(3)
with col1:
  L1_str = st.text_input("L1 (Từ khớp tới chân trước):", value="100")
with col2:
  L2_str = st.text_input("L2 (Từ khớp tới chân sau):", value="300")
with col3:
  D_str = st.text_input("D (Đường kính vòng quay / Khớp):", value="200")

# --- 2. Đồng hồ Rim (Hướng kính) ---
st.subheader("2. Đồng hồ Hướng kính (RIM - a) (mm)")
r_col1, r_col2 = st.columns(2)
with r_col1:
  a1_str = st.text_input("a1 (12h):", value="0")
  a3_str = st.text_input("a3 (6h):", value="0")
with r_col2:
  a2_str = st.text_input("a2 (3h):", value="0")
  a4_str = st.text_input("a4 (9h):", value="0")

# --- 3. Đồng hồ Face (Mặt bích) ---
st.subheader("3. Đồng hồ Mặt bích (FACE - b) (mm)")
f_col1, f_col2 = st.columns(2)
with f_col1:
  b1_str = st.text_input("b1 (12h):", value="0")
  b3_str = st.text_input("b3 (6h):", value="0")
with f_col2:
  b2_str = st.text_input("b2 (3h):", value="0")
  b4_str = st.text_input("b4 (9h):", value="0")


# Hàm chuyển đổi dữ liệu an toàn (hỗ trợ dấu phẩy và dấu chấm)
def parse_val(val):
  return float(val.strip().replace(",", "."))


# --- 4. Nút Tính toán & Xử lý kết quả ---
if st.button("🚀 TÍNH TOÁN KẾT QUẢ", type="primary", use_container_width=True):
  try:
    L1 = parse_val(L1_str)
    L2 = parse_val(L2_str)
    D = parse_val(D_str)

    a1 = parse_val(a1_str)
    a2 = parse_val(a2_str)
    a3 = parse_val(a3_str)
    a4 = parse_val(a4_str)

    b1 = parse_val(b1_str)
    b2 = parse_val(b2_str)
    b3 = parse_val(b3_str)
    b4 = parse_val(b4_str)

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

    st.success(f"Đã tính toán thành công (Cách gá {setup_type})!")

    # Hiển thị kết quả chi tiết
    st.markdown("### 📊 Kết quả hiệu chỉnh chi tiết")

    st.markdown("#### 1. Phương đứng (VERTICAL - Căn đệm Shim):")
    st.code(
        f"• Chân trước (L1): {yb1:+.3f} mm\n"
        f"  ➔ {'Thêm lá căn dày ' + f'{abs(yb1):.3f}' if yb1 >= 0 else 'Rút bớt lá căn ' + f'{abs(yb1):.3f}'} mm\n\n"
        f"• Chân sau (L2):   {yb2:+.3f} mm\n"
        f"  ➔ {'Thêm lá căn dày ' + f'{abs(yb2):.3f}' if yb2 >= 0 else 'Rút bớt lá căn ' + f'{abs(yb2):.3f}'} mm"
    )

    st.markdown("#### 2. Phương ngang (HORIZONTAL - Dịch chuyển):")
    st.code(
        f"• Chân trước (L1): {xb1:+.3f} mm\n"
        f"  ➔ {'Dịch chuyển sang phải ' + f'{abs(xb1):.3f}' if xb1 >= 0 else 'Dịch chuyển sang trái ' + f'{abs(xb1):.3f}'} mm\n\n"
        f"• Chân sau (L2):   {xb2:+.3f} mm\n"
        f"  ➔ {'Dịch chuyển sang phải ' + f'{abs(xb2):.3f}' if xb2 >= 0 else 'Dịch chuyển sang trái ' + f'{abs(xb2):.3f}'} mm"
    )

  except ValueError:
    st.error(
        "⚠️ Vui lòng kiểm tra lại dữ liệu đầu vào! Đảm bảo tất cả các ô đều"
        " là số hợp lệ."
    )
