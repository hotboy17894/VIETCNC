#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tự động deploy phiên bản mới lên GitHub
Cách dùng: python deploy.py
"""

import os
import json
import subprocess
import sys
from datetime import datetime
import glob

# ===== CẤU HÌNH =====
GITHUB_REPO = "hotboy17894/VIETCNC"
GITHUB_BRANCH = "main"
RBZ_FILENAME = "vietcnc_latest.rbz"
UPDATE_JSON = "update.json"
# ====================

def get_latest_rbz():
    """Tìm file RBZ mới nhất trong thư mục"""
    rbz_files = glob.glob("*.rbz")
    if not rbz_files:
        print("❌ Không tìm thấy file .rbz nào trong thư mục!")
        return None
    
    # Lấy file mới nhất
    latest = max(rbz_files, key=os.path.getmtime)
    print(f"✓ Tìm thấy file: {latest}")
    return latest

def read_update_json():
    """Đọc file update.json"""
    if not os.path.exists(UPDATE_JSON):
        print(f"❌ Không tìm thấy file {UPDATE_JSON}")
        return None
    
    with open(UPDATE_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_update_json(data):
    """Ghi file update.json"""
    with open(UPDATE_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✓ Đã cập nhật {UPDATE_JSON}")

def increment_version(version):
    """Tăng version tự động (3.2.5 -> 3.2.6)"""
    parts = version.split('.')
    parts[-1] = str(int(parts[-1]) + 1)
    return '.'.join(parts)

def git_push():
    """Push lên GitHub"""
    try:
        # Kiểm tra git đã init chưa
        if not os.path.exists('.git'):
            print("⚙ Khởi tạo git repository...")
            subprocess.run(['git', 'init'], check=True)
            subprocess.run(['git', 'remote', 'add', 'origin', f'https://github.com/{GITHUB_REPO}.git'], check=True)
        
        # Add files
        print("⚙ Đang thêm files...")
        subprocess.run(['git', 'add', RBZ_FILENAME, UPDATE_JSON], check=True)
        
        # Commit
        data = read_update_json()
        commit_msg = f"Release v{data['version']} - {datetime.now().strftime('%Y-%m-%d')}"
        print(f"⚙ Commit: {commit_msg}")
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        
        # Push
        print("⚙ Đang push lên GitHub...")
        subprocess.run(['git', 'push', '-u', 'origin', GITHUB_BRANCH], check=True)
        
        print("✓ Push thành công!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi git: {e}")
        return False

def main():
    print("=" * 60)
    print("VIETCNC AUTO DEPLOY TOOL")
    print("=" * 60)
    
    # 1. Tìm file RBZ
    rbz_file = get_latest_rbz()
    if not rbz_file:
        sys.exit(1)
    
    # 2. Đổi tên file RBZ thành tên chuẩn
    if rbz_file != RBZ_FILENAME:
        if os.path.exists(RBZ_FILENAME):
            os.remove(RBZ_FILENAME)
        os.rename(rbz_file, RBZ_FILENAME)
        print(f"✓ Đã đổi tên: {rbz_file} -> {RBZ_FILENAME}")
    
    # 3. Đọc update.json
    data = read_update_json()
    if not data:
        sys.exit(1)
    
    # 4. Hỏi version mới
    current_version = data['version']
    suggested_version = increment_version(current_version)
    
    print(f"\nVersion hiện tại: {current_version}")
    print(f"Version đề xuất: {suggested_version}")
    new_version = input(f"Nhập version mới (Enter để dùng {suggested_version}): ").strip()
    
    if not new_version:
        new_version = suggested_version
    
    # 5. Hỏi changelog
    print("\nNhập các thay đổi (mỗi dòng 1 thay đổi, Enter 2 lần để kết thúc):")
    changelog = []
    while True:
        line = input("- ").strip()
        if not line:
            break
        changelog.append(line)
    
    if not changelog:
        changelog = data.get('changelog', [])
    
    # 6. Cập nhật update.json
    data['version'] = new_version
    data['release_date'] = datetime.now().strftime('%Y-%m-%d')
    data['download_url'] = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/webvietcnc/{RBZ_FILENAME}"
    data['changelog'] = changelog
    
    write_update_json(data)
    
    # 7. Hiển thị thông tin
    print("\n" + "=" * 60)
    print("THÔNG TIN PHIÊN BẢN MỚI")
    print("=" * 60)
    print(f"Version: {new_version}")
    print(f"Ngày: {data['release_date']}")
    print(f"File: {RBZ_FILENAME}")
    print(f"URL: {data['download_url']}")
    print("\nCác thay đổi:")
    for change in changelog:
        print(f"  • {change}")
    print("=" * 60)
    
    # 8. Xác nhận
    confirm = input("\nBạn có muốn push lên GitHub? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Đã hủy!")
        sys.exit(0)
    
    # 9. Push lên GitHub
    if git_push():
        print("\n" + "=" * 60)
        print("✓ DEPLOY THÀNH CÔNG!")
        print("=" * 60)
        print(f"\nURL tải file:")
        print(f"  {data['download_url']}")
        print(f"\nURL update.json:")
        print(f"  https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/webvietcnc/{UPDATE_JSON}")
        print("\nUser có thể cập nhật ngay bây giờ!")
    else:
        print("\n❌ Deploy thất bại!")
        sys.exit(1)

if __name__ == '__main__':
    main()
