import socket
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    pod_name = socket.gethostname()
    return f"""
    <!DOCTYPE html>
    <html lang="th">
    <head>
        <meta charset="UTF-8">
        <title>Research Portal - ID 039</title>
        <style>
            body {{ font-family: sans-serif; max-width: 820px; margin: 40px auto; padding: 20px; background: #f4f6f9; }}
            .card {{ background: #fff; padding: 28px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 20px; }}
            .badge {{ display: inline-block; background: #198754; color: #fff; padding: 4px 10px; border-radius: 6px; font-size: 0.9em; }}
            .pod-info {{ background: #e9ecef; padding: 10px 14px; border-radius: 6px; font-family: monospace; margin: 12px 0; }}
            input[type="text"] {{ width: 72%; padding: 10px; border: 1px solid #ccc; border-radius: 6px; }}
            button {{ padding: 10px 18px; background: #0d6efd; color: #fff; border: none; border-radius: 6px; cursor: pointer; }}
            button:hover {{ background: #0b5ed7; }}
            pre {{ background: #212529; color: #f8f9fa; padding: 15px; border-radius: 6px; overflow-x: auto; line-height: 1.5; }}
            nav a {{ color: #0d6efd; text-decoration: none; font-weight: bold; margin-right: 16px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <nav>
                <a href="/">หน้าหลัก (Research)</a>
                <a href="/about">ผู้จัดทำ (About)</a>
                <a href="/api/health" target="_blank">API Health</a>
                <a href="/api/raw" target="_blank">Raw Text File</a>
            </nav>
            <hr style="border: 0; border-top: 1px solid #eee; margin: 15px 0;">
            <span class="badge">Service: app-research</span>
            <h1>ระบบคลังบันทึกงานวิจัย (Microservices K8s)</h1>
            <p>พัฒนาโดย: <strong>Padegh Sangbusarakum (รหัส 039)</strong></p>
            <div class="pod-info">Frontend Pod: <strong>{pod_name}</strong></div>
        </div>

        <div class="card">
            <h2>บันทึกข้อมูลงานวิจัยลง Persistent Storage (.txt)</h2>
            <p>ข้อมูลที่บันทึกจะถูกส่งไปยัง <code>app-api</code> และเขียนลงไฟล์ <code>/data/research_records.txt</code> บน PersistentVolume</p>
            <form onsubmit="addRecord(event)">
                <input type="text" id="noteInput" placeholder="พิมพ์หัวข้อหรือบันทึกงานวิจัย..." required>
                <button type="submit">บันทึกข้อมูล</button>
            </form>
            <div id="apiMeta" class="pod-info" style="margin-top: 15px;">กำลังโหลดข้อมูลจาก API...</div>
            <pre id="recordsBox">Loading...</pre>
        </div>

        <script>
            async function loadRecords() {{
                try {{
                    const res = await fetch('/api/records');
                    const data = await res.json();
                    document.getElementById('apiMeta').innerHTML =
                        `Backend API Pod: <strong>${{data.served_by_pod}}</strong> | จำนวนบรรทัด: <strong>${{data.total_lines}}</strong>`;
                    document.getElementById('recordsBox').textContent = data.records.join('\\n');
                }} catch (err) {{
                    document.getElementById('recordsBox').textContent = 'ไม่สามารถเชื่อมต่อ /api/records ได้: ' + err;
                }}
            }}

            async function addRecord(e) {{
                e.preventDefault();
                const input = document.getElementById('noteInput');
                const text = input.value.trim();
                if (!text) return;
                await fetch('/api/records', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ text }})
                }});
                input.value = '';
                loadRecords();
            }}

            loadRecords();
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)