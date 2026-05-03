import hashlib
import base64
from datetime import datetime

def fix_adblock_list(input_file):
    # 1. Đọc dữ liệu và phân loại (bỏ qua các dòng comment cũ/header cũ)
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith(('[Adblock', '! Title', '! Last', '! Expires', '! Checksum', '! Version'))]

    # Phân loại rule dựa trên keyword
    categories = {
        'BLOCK RULES': [],
        'HIDE RULES': [],
        'IMAGE RULES': [],
        'OTHER RULES': [],
        'SCRIPT RULES': []
    }

    for line in lines:
        if line.startswith('!'): continue # Bỏ qua các comment tự do
        
        if line.startswith('||'):
            categories['BLOCK RULES'].append(line)
        elif '##' in line:
            categories['HIDE RULES'].append(line)
        elif '$image' in line or '/ads/*.gif' in line:
            categories['IMAGE RULES'].append(line)
        elif '$script' in line:
            categories['SCRIPT RULES'].append(line)
        else:
            categories['OTHER RULES'].append(line)

    # 2. Xây dựng nội dung Body (Phần quy tắc)
    body_content = ""
    for cat in sorted(categories.keys()):
        if categories[cat]:
            body_content += f"! --- {cat} ---\n"
            body_content += "\n".join(sorted(categories[cat])) + "\n\n"

    # 3. Tạo Header (Tạm thời không có dòng Checksum để tính toán)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    version = datetime.now().strftime("%Y%m%d%H%M")
    
    header_template = f"[Adblock Plus 2.0]\n"
    header_template += f"! Title: My Custom Adblock List\n"
    header_template += f"! Last Modified: {now}\n"
    header_template += f"! Expires: 4 days\n"
    header_template += f"! Version: {version}\n"
    
    # Để tính checksum đúng, ta tính trên Header (không có checksum) + Body
    full_content_for_hash = header_template + "!\n" + body_content
    
    # 4. Thuật toán Checksum chuẩn: MD5 -> Base64 -> Remove '='
    md5_raw = hashlib.md5(full_content_for_hash.encode('utf-8')).digest()
    checksum = base64.b64encode(md5_raw).decode('utf-8').rstrip('=')

    # 5. Ghi file hoàn thiện (Chèn dòng Checksum vào giữa)
    final_output = (
        f"[Adblock Plus 2.0]\n"
        f"! Title: My Custom Adblock List\n"
        f"! Last Modified: {now}\n"
        f"! Expires: 4 days\n"
        f"! Checksum: {checksum}\n"
        f"! Version: {version}\n"
        f"!\n"
        f"{body_content}"
    )

    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(final_output)

    print(f"Hoàn tất! Checksum mới: {checksum}")

# Thực hiện với file của bạn
fix_adblock_list('adblock.txt')
