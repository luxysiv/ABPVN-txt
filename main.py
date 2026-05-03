import hashlib
from datetime import datetime

def generate_adblock_list(file_path):
    # 1. Đọc và lọc các quy tắc cũ (bỏ qua comment cũ và dòng trống)
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_lines = [line.strip() for line in f if line.strip() and not line.startswith('!')]
    
    # Loại bỏ trùng lặp bằng set
    rules = list(set(raw_lines))

    # 2. Phân loại quy tắc
    categorized = {
        'BLOCK RULES': [],
        'HIDE RULES': [],
        'SCRIPT RULES': [],
        'MEDIA RULES': [],
        'IMAGE RULES': [],
        'OTHER RULES': []
    }

    for rule in rules:
        if rule.startswith('||'):
            categorized['BLOCK RULES'].append(rule)
        elif '##' in rule or '#?#' in rule:
            categorized['HIDE RULES'].append(rule)
        elif '$script' in rule.lower():
            categorized['SCRIPT RULES'].append(rule)
        elif '$media' in rule.lower():
            categorized['MEDIA RULES'].append(rule)
        elif '$image' in rule.lower():
            categorized['IMAGE RULES'].append(rule)
        else:
            categorized['OTHER RULES'].append(rule)

    # 3. Sắp xếp các quy tắc trong từng nhóm
    content_body = ""
    for category in sorted(categorized.keys()):
        if categorized[category]:
            content_body += f"! --- {category} ---\n"
            content_body += "\n".join(sorted(categorized[category])) + "\n\n"

    # 4. Tính toán Checksum (Dựa trên nội dung body, bỏ qua các dòng comment)
    # Lưu ý: Các trình chặn thường tính checksum trên dữ liệu thô đã lọc comment
    hash_md5 = hashlib.md5(content_body.encode('utf-8')).hexdigest()

    # 5. Tạo Header chuẩn Adblock
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"""[Adblock Plus 2.0]
! Title: My Custom Adblock List
! Last Modified: {now}
! Expires: 4 days (update interval)
! Checksum: {hash_md5}
! Version: {datetime.now().strftime("%Y%m%d%H%M")}
!
"""

    # 6. Ghi file hoàn thiện
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(header + content_body)
    
    print(f"Đã cập nhật danh sách thành công với Checksum: {hash_md5}")

# Thực thi
file_path = 'adblock.txt'
generate_adblock_list(file_path)
