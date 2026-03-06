# Django Shop Management System

นี่คือโปรเจกต์ระบบจัดการร้านค้า (Shop Management System) ที่พัฒนาด้วย **Django (Python)** 

## 📦 โครงสร้างของระบบ (Apps)
โปรเจกต์นี้ถูกแบ่งการทำงานออกเป็น App ย่อยๆ ดังนี้:
- `login`: จัดการระบบล็อกอินและการยืนยันตัวตนของผู้ใช้งาน
- `category`: จัดการหมวดหมู่ของสินค้า
- `product`: จัดการข้อมูลสินค้าหลัก (ชื่อ, หมวดหมู่)
- `lot`: จัดการสต็อกสินค้า การนำเข้าสินค้า (ล็อต) ตามวันหมดอายุและวันที่นำเข้า
- `payment`: จัดการระบบการขาย การนำสินค้าลงตะกร้า และการชำระเงินตัดสต็อก

## 🛠️ เครื่องมือและไลบรารีที่ใช้
- **Python** (version 3.x)
- **Django** (version 5.1.1)
- **PostgreSQL** หรือ **SQLite** (สำหรับฐานข้อมูล)
- `humanize` (แสดงผลตัวเลขให้อ่านง่าย)
- `django-extensions`

---

## 🚀 วิธีการรันโปรเจกต์ในเครื่อง (Local Setup)

### 1. การเตรียม Environment
เข้าไปที่โฟลเดอร์โปรเจกต์และสร้าง Virtual Environment:
```bash
cd my_project
python -m venv venv
```

เปิดใช้งาน Virtual Environment:
- **Windows:**
  ```bash
  .\venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 2. ติดตั้ง Dependencies
ติดตั้งแพ็กเกจที่จำเป็นจากไฟล์ `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. การตั้งค่า Database
โปรเจกต์นี้ตั้งค่าพื้นฐานเชื่อมต่อกับ **PostgreSQL** (ดูที่ `my_project/myshop/myshop/settings.py`) 
หากต้องการทดสอบด้วย **SQLite** สามารถเข้าไปเปิดคอมเมนต์ส่วน `sqlite3` และปิด `postgresql` ในบรรทัดที่เกี่ยวกับ `DATABASES` ได้

จากนั้นสร้างตารางฐานข้อมูล:
```bash
cd myshop
python manage.py migrate
```

### 4. สร้างบัญชีผู้ดูแลระบบ (Admin)
สร้างผู้ใช้สำหรับการล็อกอินจัดการระบบ (Superuser):
```bash
python manage.py createsuperuser
```
(จากนั้นกรอก Username, Email, และ Password ตามต้องการ)

### 5. รันเซิร์ฟเวอร์
เริ่มต้นการทำงานของแอปพลิเคชัน:
```bash
python manage.py runserver
```
จากนั้นเปิดเว็บเบราว์เซอร์ไปที่ `http://127.0.0.1:8000/`

---

## 📌 หมายเหตุ
- ไฟล์ `requirements.txt` ถูกสร้างขึ้นเพิ่มเติมเพื่อรวมแพ็กเกจที่จำเป็นทั้งหมดไว้ให้แล้ว
- หากพบปัญหา "This field is required" ในฟอร์ม Lot ระบบได้มีการอัปเดตวิวให้ส่งค่า `initial={'product': product}` เข้าไปแก้ไขปัญหานี้แล้ว
