#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
NPZ to CSV Converter
====================
สคริปต์สำหรับแปลงไฟล์ npz จาก main.py ไปเป็นไฟล์ CSV
และเก็บไฟล์ CSV ไว้ในโฟลเดอร์ที่กำหนด

Author: eNose Project
"""

import numpy as np
import pandas as pd
from pathlib import Path
import sys
import tkinter as tk
from tkinter import filedialog


def convert_npz_to_csv(npz_path, output_dir):
    """
    แปลงไฟล์ npz เป็น CSV
    
    Args:
        npz_path (Path): path ของไฟล์ npz ที่ต้องการแปลง
        output_dir (Path): path ของโฟลเดอร์ที่ต้องการเก็บไฟล์ CSV
    
    Returns:
        Path หรือ None: path ของไฟล์ CSV ที่สร้างขึ้น หรือ None ถ้าเกิดข้อผิดพลาด
    """
    try:
        # โหลดข้อมูลจากไฟล์ npz
        npz_data = np.load(npz_path)
        
        # ดึงข้อมูลออกมา
        data = npz_data['data']
        columns = npz_data['columns']
        
        # สร้าง DataFrame จากข้อมูล
        df = pd.DataFrame(data, columns=columns)
        
        # สร้างชื่อไฟล์ CSV จากชื่อไฟล์ npz (เปลี่ยนนามสกุลเป็น .csv)
        csv_filename = npz_path.stem + '.csv'
        csv_path = output_dir / csv_filename
        
        # บันทึกเป็น CSV
        df.to_csv(csv_path, index=False)
        
        print(f"✓ แปลงสำเร็จ: {npz_path.name} -> {csv_filename}")
        print(f"  จำนวนแถว: {len(df)}, จำนวนคอลัมน์: {len(df.columns)}")
        
        return csv_path
        
    except Exception as e:
        print(f"✗ เกิดข้อผิดพลาดในการแปลง {npz_path.name}: {e}")
        return None


def convert_all_npz_files(data_dir=None, output_dir=None):
    """
    แปลงไฟล์ npz ทั้งหมดในโฟลเดอร์ data เป็น CSV
    
    Args:
        data_dir (Path, optional): path ของโฟลเดอร์ที่มีไฟล์ npz 
                                   ถ้าไม่ระบุจะใช้โฟลเดอร์ data ใน directory เดียวกับไฟล์นี้
        output_dir (Path, optional): path ของโฟลเดอร์ที่ต้องการเก็บไฟล์ CSV
                                     ถ้าไม่ระบุจะใช้โฟลเดอร์ "chacking" ใน directory เดียวกับไฟล์นี้
    
    Returns:
        list: list ของ path ของไฟล์ CSV ที่สร้างขึ้น
    """
    # กำหนด path ของโฟลเดอร์ data
    if data_dir is None:
        script_dir = Path(__file__).parent
        data_dir = script_dir / "data"
    
    # ตรวจสอบว่าโฟลเดอร์ data มีอยู่หรือไม่
    if not data_dir.exists():
        print(f"✗ ไม่พบโฟลเดอร์: {data_dir}")
        return []
    
    # กำหนด path ของโฟลเดอร์ output
    if output_dir is None:
        script_dir = Path(__file__).parent
        output_dir = script_dir / "chacking"
    
    # สร้างโฟลเดอร์ output
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 โฟลเดอร์ output: {output_dir}")
    
    # หาไฟล์ npz ทั้งหมด
    npz_files = list(data_dir.glob("*.npz"))
    
    if not npz_files:
        print(f"✗ ไม่พบไฟล์ .npz ในโฟลเดอร์: {data_dir}")
        return []
    
    print(f"\nพบไฟล์ .npz ทั้งหมด {len(npz_files)} ไฟล์\n")
    
    # แปลงไฟล์ทีละไฟล์
    converted_files = []
    for npz_file in npz_files:
        csv_path = convert_npz_to_csv(npz_file, output_dir)
        if csv_path:
            converted_files.append(csv_path)
    
    print(f"\n✅ แปลงเสร็จสิ้น: {len(converted_files)}/{len(npz_files)} ไฟล์")
    print(f"📂 ไฟล์ CSV ถูกเก็บไว้ใน: {output_dir}")
    
    return converted_files


def select_file_dialog():
    """
    เปิด dialog สำหรับเลือกไฟล์ npz
    
    Returns:
        Path หรือ None: path ของไฟล์ที่เลือก หรือ None ถ้ายกเลิก
    """
    try:
        root = tk.Tk()
        root.withdraw()  # ซ่อนหน้าต่างหลัก
        
        # ทำให้ window ได้ focus และอยู่ด้านบน (สำคัญสำหรับ Windows)
        root.update_idletasks()
        root.lift()
        root.attributes('-topmost', True)
        root.focus_force()
        root.update()
        root.attributes('-topmost', False)
        
        # เรียก dialog
        file_path = filedialog.askopenfilename(
            parent=root,
            title="เลือกไฟล์ NPZ ที่ต้องการแปลง",
            filetypes=[("NPZ files", "*.npz"), ("All files", "*.*")]
        )
        
        root.destroy()
        
        if file_path:
            return Path(file_path)
        return None
    except Exception as e:
        print(f"✗ เกิดข้อผิดพลาดในการเปิด file dialog: {e}")
        print("   ลองใช้ command line arguments แทน: python covert.py <ไฟล์.npz> [โฟลเดอร์]")
        return None


def select_output_folder_dialog(initial_dir=None):
    """
    เปิด dialog สำหรับเลือกโฟลเดอร์ output
    
    Args:
        initial_dir (str, optional): โฟลเดอร์เริ่มต้น
    
    Returns:
        Path หรือ None: path ของโฟลเดอร์ที่เลือก หรือ None ถ้ายกเลิก
    """
    try:
        root = tk.Tk()
        root.withdraw()  # ซ่อนหน้าต่างหลัก
        
        # ทำให้ window ได้ focus และอยู่ด้านบน (สำคัญสำหรับ Windows)
        root.update_idletasks()
        root.lift()
        root.attributes('-topmost', True)
        root.focus_force()
        root.update()
        root.attributes('-topmost', False)
        
        # เรียก dialog
        folder_path = filedialog.askdirectory(
            parent=root,
            title="เลือกโฟลเดอร์สำหรับเก็บไฟล์ CSV",
            initialdir=initial_dir
        )
        
        root.destroy()
        
        if folder_path:
            return Path(folder_path)
        return None
    except Exception as e:
        print(f"✗ เกิดข้อผิดพลาดในการเปิด folder dialog: {e}")
        print("   ลองใช้ command line arguments แทน: python covert.py <ไฟล์.npz> [โฟลเดอร์]")
        return None


def main():
    """ฟังก์ชันหลักสำหรับรันสคริปต์"""
    print("=" * 60)
    print("NPZ to CSV Converter")
    print("=" * 60)
    
    # ตรวจสอบ command line arguments
    # รูปแบบ: python covert.py [input_file] [output_folder]
    # หรือ: python covert.py (จะเปิด GUI dialog)
    
    npz_path = None
    output_dir = None
    
    # อ่าน arguments จาก command line
    if len(sys.argv) > 1:
        # argument แรก: ไฟล์ npz หรือโฟลเดอร์ input
        input_arg = Path(sys.argv[1])
        if input_arg.is_file() and input_arg.suffix == '.npz':
            npz_path = input_arg
        elif input_arg.is_dir():
            # ถ้าเป็นโฟลเดอร์ ให้แปลงไฟล์ทั้งหมดในโฟลเดอร์นั้น
            data_dir = input_arg
            if len(sys.argv) > 2:
                output_dir = Path(sys.argv[2])
            convert_all_npz_files(data_dir=data_dir, output_dir=output_dir)
            return
        else:
            print(f"✗ ไม่พบไฟล์หรือโฟลเดอร์: {input_arg}")
            return
        
        # argument ที่สอง: โฟลเดอร์ output (ถ้ามี)
        if len(sys.argv) > 2:
            output_dir = Path(sys.argv[2])
    
    # ถ้าไม่มี arguments หรือต้องการเลือกไฟล์/โฟลเดอร์ผ่าน GUI
    if npz_path is None:
        print("\n📂 เลือกไฟล์ NPZ ที่ต้องการแปลง...")
        npz_path = select_file_dialog()
        
        if npz_path is None:
            print("✗ ไม่ได้เลือกไฟล์")
            return
        
        if not npz_path.exists():
            print(f"✗ ไม่พบไฟล์: {npz_path}")
            return
    
    # เลือกโฟลเดอร์ output (ถ้ายังไม่ได้ระบุ)
    if output_dir is None:
        print("\n📁 เลือกโฟลเดอร์สำหรับเก็บไฟล์ CSV...")
        output_dir = select_output_folder_dialog(initial_dir=str(Path(__file__).parent))
        
        if output_dir is None:
            print("✗ ไม่ได้เลือกโฟลเดอร์ output ใช้โฟลเดอร์ default: chacking")
            output_dir = Path(__file__).parent / "chacking"
    
    # สร้างโฟลเดอร์ output ถ้ายังไม่มี
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # แปลงไฟล์
    print(f"\n📂 โฟลเดอร์ output: {output_dir}")
    convert_npz_to_csv(npz_path, output_dir)


if __name__ == "__main__":
    main()
