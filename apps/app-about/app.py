import socket
from flask import Flask

app = Flask(__name__)

@app.route("/")
@app.route("/about")
def about():
    pod_name = socket.gethostname()
    pod_ip = socket.gethostbyname(pod_name)
    return f"""
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <title>About - ID 039</title>
        <style>
            body {{ font-family: sans-serif; max-width: 720px; margin: 40px auto; padding: 20px; background: #f4f6f9; }}
            .card {{ background: #fff; padding: 28px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
            .badge {{ display: inline-block; background: #0d6efd; color: #fff; padding: 4px 10px; border-radius: 6px; font-size: 0.9em; }}
            .meta {{ margin-top: 20px; padding: 12px; background: #e9ecef; border-radius: 6px; font-family: monospace; }}
            a {{ color: #0d6efd; text-decoration: none; margin-right: 15px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <span class="badge">Service: app-about</span>
            <h1>ข้อมูลผู้จัดทำโครงงาน (About)</h1>
            <p><strong>ชื่อ-นามสกุล:</strong> Padegh Sangbusarakum</p>
            <p><strong>รหัสนักศึกษา (3 ตัวท้าย):</strong> 039</p>
            <p><strong>โดเมนระบบ:</strong> id-039.com</p>
            <div class="meta">
                <strong>Served by Pod:</strong> {pod_name} ({pod_ip})
            </div>
            <p style="margin-top: 20px;">
                <a href="/">← กลับหน้าหลัก (Research)</a>
                <a href="/api/raw" target="_blank">ดูไฟล์ Text ดิบ (/api/raw) →</a>
            </p>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)