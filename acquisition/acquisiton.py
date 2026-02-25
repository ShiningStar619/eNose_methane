import pandas as pd
import numpy as np
from pathlib import Path
import os
from datetime import datetime

# --- Configuration ---
# Path settings
CURRENT_DIR = Path(__file__).parent
READING_DATA_DIR = CURRENT_DIR.parent / "reading" / "data"
OUTPUT_DIR = CURRENT_DIR / "processed_data"

# Filter settings (SAMPLE_RATE จะอ่านจากไฟล์ NPZ)
CUTOFF_FREQ = 50           # Hz (Cutoff frequency for Low-pass)
MOVING_AVG_WINDOW = 1000       # Window size for Moving Average


def get_latest_npz_file(directory):
    """Finds the latest NPZ file in the specified directory."""
    if not directory.exists():
        print(f"Directory not found: {directory}")
        return None
    
    # Get list of npz files
    npz_files = list(directory.glob("*.npz"))
    if not npz_files:
        print(f"No NPZ files found in {directory}")
        return None
    
    # Sort by modification time, latest first
    latest_file = max(npz_files, key=os.path.getmtime)
    return latest_file


def load_npz_to_dataframe(npz_path):
    """
    Load NPZ file and convert to DataFrame
    
    NPZ format from reading/main.py:
    - data: shape (n_samples, 1 + num_channels) = [elapsed_time, sensor_1, sensor_2, ...]
    - columns: ['elapsed_time_sec', 'sensor_1', 'sensor_2', ...]
    - sample_rate: float (Hz)
    - num_channels: int
    
    Returns:
    --------
    df : DataFrame
        ข้อมูลในรูปแบบ DataFrame
    sample_rate : float
        Sample rate (Hz) จากไฟล์
    """
    npz_data = np.load(npz_path, allow_pickle=True)
    
    data = npz_data['data']
    columns = npz_data['columns']
    sample_rate = float(npz_data['sample_rate'])
    
    # Convert to DataFrame
    df = pd.DataFrame(data, columns=columns)
    
    print(f"  Loaded {len(df)} samples at {sample_rate} Hz")
    print(f"  Columns: {list(columns)}")
    
    return df, sample_rate


def lowpass_filter(data, cutoff_freq, sample_rate):
    """
    Simple first-order IIR Low-pass Filter (Exponential Smoothing)
    
    สูตร: y[n] = alpha * x[n] + (1 - alpha) * y[n-1]
    โดย alpha = dt / (RC + dt), RC = 1 / (2 * pi * cutoff_freq)
    
    Parameters:
    -----------
    data : array-like
        ข้อมูลดิบจากเซ็นเซอร์
    cutoff_freq : float
        ความถี่ตัด (Hz) - ความถี่ที่สูงกว่านี้จะถูกกรองออก
    sample_rate : float
        Sample rate (Hz)
    
    Returns:
    --------
    filtered : array
        ข้อมูลที่ผ่าน low-pass filter แล้ว
    """
    data = np.array(data)
    
    # คำนวณ alpha สำหรับ first-order low-pass
    dt = 1.0 / sample_rate                    # ช่วงเวลาระหว่าง sample
    rc = 1.0 / (2 * np.pi * cutoff_freq)      # Time constant
    alpha = dt / (rc + dt)                     # Smoothing factor (0-1)
    
    # Apply filter
    filtered = np.zeros_like(data, dtype=float)
    filtered[0] = data[0]
    
    for i in range(1, len(data)):
        filtered[i] = alpha * data[i] + (1 - alpha) * filtered[i-1]
    
    return filtered


def process_data():
    # 1. Setup output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 2. Get the latest input file (NPZ)
    input_file = get_latest_npz_file(READING_DATA_DIR)
    if input_file is None:
        return

    print(f"Processing file: {input_file.name}")
    
    # 3. Load NPZ data
    try:
        df, sample_rate = load_npz_to_dataframe(input_file)
    except Exception as e:
        print(f"Error reading NPZ: {e}")
        return

    # Identify sensor columns (sensor_1, sensor_2, sensor_3, sensor_4)
    channel_cols = [col for col in df.columns if col.startswith('sensor_')]
    
    if not channel_cols:
        print("No sensor data columns found.")
        return

    # Create a copy for processed data
    df_processed = df.copy()

    # 4. Apply Filters: Low-pass -> Moving Average
    print(f"\n--- Applying Filters (Low-pass {CUTOFF_FREQ}Hz -> Moving Avg window={MOVING_AVG_WINDOW}) ---")
    for col in channel_cols:
        # Fill NaNs if any (forward fill then backward fill) to avoid filter errors
        clean_data = df[col].ffill().bfill() 
        
        # Debug: ตรวจสอบข้อมูลดิบ
        print(f"  {col}: Original data - min={clean_data.min():.4f}, max={clean_data.max():.4f}, mean={clean_data.mean():.4f}, NaN count={clean_data.isna().sum()}")
        
        # Check if we have enough data points for filtering
        if len(clean_data) > 15:
            # Step 1: Low-pass Filter (ใช้ sample_rate จากไฟล์ NPZ)
            df_processed[f'{col}_lp'] = lowpass_filter(clean_data.values, CUTOFF_FREQ, sample_rate)
            
            # Step 2: Moving Average (on top of Low-pass)
            # ใช้ min_periods=1 เพื่อให้ใช้ข้อมูลที่มีได้แม้ไม่ครบ window (ลด NaN)
            df_processed[f'{col}_lp_ma'] = df_processed[f'{col}_lp'].rolling(
                window=MOVING_AVG_WINDOW, 
                center=True, 
                min_periods=1
            ).mean()
            
            # Debug: ตรวจสอบข้อมูลหลัง filter
            lp_ma_col = f'{col}_lp_ma'
            if lp_ma_col in df_processed.columns:
                lp_ma_data = df_processed[lp_ma_col]
                valid_count = lp_ma_data.notna().sum()
                print(f"  {col}: After filtering - valid samples={valid_count}/{len(lp_ma_data)}, min={lp_ma_data.min():.4f}, max={lp_ma_data.max():.4f}, mean={lp_ma_data.mean():.4f}")
        else:
            print(f"  {col}: Not enough data points to filter (only {len(clean_data)} samples)")

    # 5. Save to CSV - ใช้รูปแบบ adc1263_date_time
    # ดึง date_time จากชื่อไฟล์ input (รองรับทั้งรูปแบบเก่าและใหม่)
    input_stem = input_file.stem  # เช่น "adc1263_20251217_150155" หรือ "ads1263_voltage_20251217_150155"
    
    # แยกด้วย underscore และหาส่วนที่เป็น date_time (รูปแบบ YYYYMMDD_HHMMSS)
    parts = input_stem.split('_')
    date_time = None
    
    # หาส่วนที่มีรูปแบบ YYYYMMDD_HHMMSS (8 หลัก_6 หลัก)
    for i in range(len(parts) - 1):
        if len(parts[i]) == 8 and parts[i].isdigit() and len(parts[i+1]) == 6 and parts[i+1].isdigit():
            date_time = f"{parts[i]}_{parts[i+1]}"
            break
    
    if date_time:
        output_filename = f"adc1263_{date_time}.csv"
    else:
        # ถ้าไม่พบ date_time ให้ใช้ timestamp ใหม่
        date_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"adc1263_{date_time}.csv"
    
    output_path = OUTPUT_DIR / output_filename
    cols_to_keep = ['elapsed_time_sec'] + [col for col in df_processed.columns if col.endswith('_lp_ma')]
    df_final = df_processed[cols_to_keep]
    
    # บันทึกไฟล์ - เพิ่ม error handling สำหรับ permission issues
    try:
        # ตรวจสอบว่าไฟล์มีอยู่แล้วและถูก lock หรือไม่
        if output_path.exists():
            # ถ้าไฟล์มีอยู่แล้ว ให้เพิ่ม timestamp เพื่อหลีกเลี่ยง conflict
            timestamp = datetime.now().strftime('%H%M%S_%f')[:-3]  # เพิ่ม milliseconds
            output_filename = f"adc1263_{date_time}_{timestamp}.csv"
            output_path = OUTPUT_DIR / output_filename
            print(f"  Warning: Original filename exists, using: {output_filename}")
        
        # ตรวจสอบสิทธิ์การเขียนใน directory
        if not os.access(OUTPUT_DIR, os.W_OK):
            raise PermissionError(f"No write permission for directory: {OUTPUT_DIR}")
        
        # บันทึกไฟล์
        df_final.to_csv(output_path, index=False)
        print(f"\nSaved processed data to: {output_path}")
        
    except PermissionError as e:
        print(f"\n✗ Permission Error: {e}")
        print(f"  Please check file permissions for: {output_path}")
        print(f"  Try running: sudo chmod 755 {OUTPUT_DIR}")
        return
    except Exception as e:
        print(f"\n✗ Error saving file: {e}")
        print(f"  File path: {output_path}")
        return

    print("-" * 30)
    # แสดงผลตัวอย่างจาก df_final
    print(df_final.head())


if __name__ == "__main__":
    process_data()
