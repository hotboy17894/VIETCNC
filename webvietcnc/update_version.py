#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script đơn giản để cập nhật version trong update.json
Không cần Git, chỉ cập nhật file local
Sau đó bạn upload thủ công lên GitHub
"""

import json
from datetime import datetime

UPDATE_JSON = "update.json"

def increment_version(version):
    """Tăng version tự động (3.2.5 -> 3.2.6)"""
    parts = version.split('.')
    parts[-1] = str(int(parts[-1]) + 1)
    return '.'.join(parts)

def main():
    print("=" * 60)
    print("CẬP NHẬT VERSION - VIETCNC")
    print("=" * 60)
    
    # Đọc file hiện tại
    try:
        with open(UPDATE_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file {UPDATE_JSON}")
        return
    
    # Hiển thị thông tin hiện tại
    current_version = data['version']
    print(f"\nVersion hiện tại: {current_version}")
    print(f"Ngày cập nhật: {data['release_date']}")
    
    # Hỏi version mới
    suggested_version = increment_version(current_version)
    print(f"\nVersion đề xuất: {suggested_version}")
    new_version = input(f"Nhập version mới (Enter để dùng {suggested_version}): ").strip()
    
    if not new_version:
        new_version = suggested_version
    
    # Hỏi changelog
    print("\nNhập các thay đổi (mỗi dòng 1 thay đổi, Enter 2 lần để kết thúc):")
    changelog = []
    while True:
        line = input("- ").strip()
        if not line:
            break
        changelog.append(line)
    
    if not changelog:
        print("⚠ Không có changelog mới, giữ nguyên changelog cũ")
        changelog = data.get('changelog', [])
    
    # Cập nhật data
    data['version'] = new_version
    data['release_date'] = datetime.now().strftime('%Y-%m-%d')
    data['changelog'] = changelog
    
    # Ghi file
    with open(UPDATE_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Hiển thị kết quả
    print("\n" + "=" * 60)
    print("✓ ĐÃ CẬP NHẬT FILE update.json")
    print("=" * 60)
    print(f"Version: {new_version}")
    print(f"Ngày: {data['release_date']}")
    print("\nCác thay đổi:")
    for change in changelog:
        print(f"  • {change}")
    print("=" * 60)
    
    # Hướng dẫn tiếp theo
    print("\n📋 BƯỚC TIẾP THEO:")
    print("1. Đổi tên file RBZ thành: vietcnc_latest.rbz")
    print("2. Vào: https://github.com/hotboy17894/VIETCNC/upload/main")
    print("3. Kéo thả 2 files:")
    print("   - vietcnc_latest.rbz")
    print("   - update.json")
    print("4. Commit message: Release v" + new_version)
    print("5. Click 'Commit changes'")
    print("\n✓ Xong! User có thể update ngay!")

if __name__ == '__main__':
    main()
