import hashlib
import base64
import re
from datetime import datetime

def generate_standard_adblock(file_path):
    # 1. Đọc dữ liệu thô và lọc bỏ các dòng Header/Checksum cũ
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    clean_rules = []
    for line in lines:
        l = line.strip()
        # Bỏ qua dòng trống và các dòng thuộc Header cũ
        if l and not l.startswith(('[Adblock', '! Title', '! Last', '! Expires', '! Checksum', '! Version')):
            clean_rules.append(l)

    # 2. Tạo phần nội dung quy tắc (Body)
    # Lưu ý: Không để dòng trống ở cuối để tránh sai lệch checksum
    body_content = "\n".join(clean_rules) + "\n"

    # 3. Tạo Header mẫu (Không có dòng Checksum) để lấy dữ liệu băm
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    version = datetime.now().strftime("%Y%m%d%H%M")
    
    # Cấu trúc Header cố định
    header_part1 = "[Adblock Plus 2.0]\n"
    header_part2 = f"! Title: My Custom Adblock List\n! Last Modified: {now}\n! Expires: 4 days\n! Version: {version}\n!\n"
    
    # Dữ liệu dùng để băm = Header (không checksum) + Body
    data_to_hash = header_part1 + header_part2 + body_content
    
    # 4. Tính toán Checksum (MD5 -> Base64)
    md5_obj = hashlib.md5(data_to_hash.encode('utf-8'))
    checksum_value = base64.b64encode(md5_obj.digest()).decode('utf-8').rstrip('=')

    # 5. Ráp lại file hoàn chỉnh với Checksum nằm ở trên
    final_file_content = (
        f"{header_part1}"
        f"! Checksum: {checksum_value}\n"
        f"{header_part2}"
        f"{body_content}"
    )

    # 6. Ghi file với Encoding UTF-8 chuẩn
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(final_file_content)

    print(f"--- Đã tạo file thành công ---")
    print(f"Checksum: {checksum_value}")

# Thực thi
generate_standard_adblock('adblock.txt')
