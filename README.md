# ระบบจัดการงานลูกค้า (Order Management System)

ระบบจัดการงานลูกค้าแบบครบวงจรด้วย Flask และ Jinja2 Templates

## 📁 โครงสร้างโปรเจค

```
project/
├── app.py                      # Flask Application
├── requirements.txt            # Dependencies
├── templates/                  # HTML Templates
│   ├── login.html             # หน้า Login Admin
│   ├── order_form.html        # หน้าสั่งงาน (Public)
│   ├── tracking.html          # หน้าตรวจสอบออเดอร์ (Public)
│   └── admin_dashboard.html   # หน้า Dashboard Admin
├── tasks.json                 # ไฟล์เก็บข้อมูลงาน (สร้างอัตโนมัติ)
└── users.json                 # ไฟล์เก็บข้อมูล Admin (สร้างอัตโนมัติ)
```

## 🚀 วิธีติดตั้งและรัน

### 1. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 2. รัน Flask Server

```bash
python app.py
```

Server จะรันที่: `http://localhost:5000`

## 📱 หน้าต่างๆ ในระบบ

### หน้า Public (ไม่ต้อง Login)

1. **หน้าสั่งงาน** - `/`
   - ลูกค้าสามารถกรอกฟอร์มสั่งงานได้เอง
   - กรอกข้อมูล: ชื่อ, เบอร์โทร, อีเมล, รายละเอียดงาน
   - เลือกความเร่งด่วนและวันที่ต้องการจัดส่ง

2. **หน้าตรวจสอบออเดอร์** - `/tracking`
   - ค้นหาออเดอร์ด้วยชื่อหรือวันที่จัดส่ง
   - ดูสถานะงานแบบเรียลไทม์

### หน้า Admin (ต้อง Login)

3. **หน้า Login** - `/login`
   - Login เข้าสู่ระบบ Admin
   - บัญชีเริ่มต้น: `admin` / `admin123`

4. **หน้า Dashboard** - `/admin`
   - แสดงสถิติงานทั้งหมด
   - จัดการงานทั้งหมด (เปลี่ยนสถานะ/ลบ)
   - กรองงานตามสถานะ

## 🎯 ฟีเจอร์หลัก

### สำหรับลูกค้า (Public)
- ✅ สั่งงานผ่านฟอร์ม
- ✅ ตรวจสอบสถานะออเดอร์
- ✅ ค้นหาด้วยชื่อและวันที่
- ✅ ไม่ต้อง Login

### สำหรับ Admin
- ✅ Login ระบบ
- ✅ Dashboard แสดงสถิติ
- ✅ จัดการงานทั้งหมด
- ✅ เปลี่ยนสถานะงาน (รอดำเนินการ → กำลังทำ → เสร็จสิ้น → ยกเลิก)
- ✅ ลบงาน
- ✅ กรองงานตามสถานะ
- ✅ Logout

## 💾 ข้อมูลที่บันทึก

### tasks.json
เก็บข้อมูลงานทั้งหมด:
- ข้อมูลลูกค้า (ชื่อ, เบอร์โทร, อีเมล)
- รายละเอียดงาน
- สถานะงาน
- ความเร่งด่วน
- วันที่สร้างและวันที่จัดส่ง
- ผู้สร้าง/แก้ไข

### users.json
เก็บข้อมูล Admin:
- Username และ Password
- บัญชีเริ่มต้น: `admin:admin123`

## 🔐 ระบบ Authentication

- ใช้ Flask Session
- Admin ต้อง Login ก่อนเข้า Dashboard
- Auto redirect ถ้ายังไม่ได้ Login
- Logout ได้ทุกเมื่อ

## 🌐 การ Deploy

### Deploy บน PythonAnywhere

1. Upload ไฟล์ทั้งหมดไป PythonAnywhere
2. สร้าง Virtual Environment:
```bash
mkvirtualenv myenv --python=python3.10
pip install -r requirements.txt
```

3. ตั้งค่า WSGI:
```python
import sys
path = '/home/yourusername/myproject'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

4. Reload web app

### Deploy บน Heroku

1. สร้างไฟล์ `Procfile`:
```
web: python app.py
```

2. แก้ไข `app.py` บรรทัดสุดท้าย:
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

3. Deploy:
```bash
git init
heroku create your-app-name
git add .
git commit -m "Initial commit"
git push heroku master
```

### Deploy บน Railway/Render

1. เชื่อมต่อ GitHub repository
2. ระบุ Start Command: `python app.py`
3. Deploy อัตโนมัติ

## ⚙️ Configuration

### เปลี่ยน Secret Key

แก้ไขใน `app.py`:
```python
app.secret_key = 'your-new-secret-key-here'
```

### เพิ่ม Admin Account

แก้ไขไฟล์ `users.json`:
```json
{
  "admin": "admin123",
  "manager": "password456"
}
```

หรือใช้หน้า `/login` ครั้งแรก (ถ้ายังไม่มี admin)

## 📊 สถานะงาน

- **pending** (รอดำเนินการ) - สีเหลือง
- **inprogress** (กำลังดำเนินการ) - สีน้ำเงิน
- **completed** (เสร็จสิ้น) - สีเขียว
- **cancelled** (ยกเลิก) - สีแดง

## 🎨 ความเร่งด่วน

- **low** (ไม่เร่งด่วน) - สีเขียว
- **medium** (ปานกลาง) - สีเหลือง
- **high** (เร่งด่วน) - สีแดง

## 🐛 Troubleshooting

### ไฟล์ไม่บันทึก
ตรวจสอบว่ามีสิทธิ์เขียนไฟล์ใน directory

### Session หมดอายุ
เปลี่ยน Secret Key ใหม่จะทำให้ session เก่าหมดอายุ

### Port already in use
เปลี่ยน port ใน `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 📝 License

MIT License - ใช้งานได้อย่างอิสระ

## 💡 Tips

- ระบบใช้ JSON file แทน Database เพื่อความง่าย
- เหมาะกับงานขนาดเล็ก-กลาง
- หากต้องการ scalability ให้เปลี่ยนเป็น SQLite/PostgreSQL
- ข้อมูลถูกเก็บในไฟล์ `.json` สามารถ backup ได้ง่าย

## 🔄 การ Backup

สำรอง 2 ไฟล์นี้เป็นประจำ:
- `tasks.json` - ข้อมูลงานทั้งหมด
- `users.json` - ข้อมูล Admin
