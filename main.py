import hashlib
import base64
import re
from datetime import datetime

def generate_standard_adblock(file_path):
    # 1. Đọc dữ liệu thô và lọc các quy tắc hợp lệ
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Sử dụng set để loại bỏ các dòng trùng lặp ngay từ đầu
    raw_rules = set()
    for line in lines:
        l = line.strip()
        # Bỏ qua dòng trống, Header cũ và Comment
        if l and not l.startswith(('[Adblock', '! Title', '! Last', '! Expires', '! Checksum', '! Version', '!')):
            raw_rules.add(l)

    # 2. Phân loại và Sắp xếp quy tắc (Logic từ script 1)
    categorized = {
        'block_rules': set(),
        'hide_rules': set(),
        'script_rules': set(),
        'media_rules': set(),
        'image_rules': set(),
        'other_rules': set()
    }

    for rule in raw_rules:
        if rule.startswith('||'):
            categorized['block_rules'].add(rule)
        elif '##' in rule:
            categorized['hide_rules'].add(rule)
        elif '$script' in rule.lower():
            categorized['script_rules'].add(rule)
        elif '$media' in rule.lower():
            categorized['media_rules'].add(rule)
        elif '$image' in rule.lower():
            categorized['image_rules'].add(rule)
        else:
            categorized['other_rules'].add(rule)

    # 3. Tạo nội dung Body đã được phân nhóm
    body_lines = []
    for category in ['block_rules', 'hide_rules', 'script_rules', 'media_rules', 'image_rules', 'other_rules']:
        rules_in_cat = sorted(list(categorized[category]))
        if rules_in_cat:
            body_lines.append(f"! {category.upper()}")
            body_lines.extend(rules_in_cat)
            body_lines.append("") # Dòng trống phân cách giữa các nhóm

    body_content = "\n".join(body_lines)

    # 4. Tạo Header mẫu (Không có dòng Checksum)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    version = datetime.now().strftime("%Y%m%d%H%M")
    
    header_part1 = "[Adblock Plus 2.0]\n"
    header_part2 = f"! Title: My Custom Adblock List\n! Last Modified: {now}\n! Expires: 4 days\n! Version: {version}\n!\n"
    
    # Dữ liệu để tính băm (Header + Body)
    data_to_hash = header_part1 + header_part2 + body_content
    
    # 5. Tính toán Checksum
    md5_obj = hashlib.md5(data_to_hash.encode('utf-8'))
    checksum_value = base64.b64encode(md5_obj.digest()).decode('utf-8').rstrip('=')

    # 6. Ráp file hoàn chỉnh
    final_file_content = (
        f"{header_part1}"
        f"! Checksum: {checksum_value}\n"
        f"{header_part2}"
        f"{body_content}"
    )

    # 7. Ghi file
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(final_file_content)

    print(f"--- Đã sắp xếp và tạo file thành công ---")
    print(f"Checksum mới: {checksum_value}")

# Thực thi
generate_standard_adblock('adblock.txt')
