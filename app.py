import os
from flask import Flask, request, render_template_string, send_file
import yt_dlp

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مُنَزِّل الوسائط</title>
    <style>
        body { font-family: sans-serif; background: #f8f9fa; display: flex; justify-content: center; padding-top: 50px; margin: 0; }
        .box { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 90%; max-width: 400px; text-align: center; }
        input { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 8px; margin-bottom: 15px; box-sizing: border-box; text-align: center; font-size: 16px; }
        button { width: 100%; padding: 12px; background: #28a745; color: white; border: none; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="box">
        <h2>مُنَزِّل الفيديو والوسائط</h2>
        <form action="/download" method="post" onsubmit="window.open('https://omg10.com/4/11811951', '_blank');">
            <input type="text" name="url" placeholder="ضع رابط الفيديو هنا..." required>
            <button type="submit">تنزيل الفيديو</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url', '').strip()
    if url.startswith('/'):
        url = url[1:]
    
    ydl_opts = {
        'outtmpl': '/tmp/%(title)s.%(ext)s',
        'format': 'best',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
