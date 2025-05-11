from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image
import io
from werkzeug.utils import secure_filename
import os
from bone import process_video

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'processed_videos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/reco')
def reco():
    return render_template('reco.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/extract')
def extract():
    return render_template('extract.html')

@app.route('/stat')
def stat():
    return render_template('stat.html')

# 上传视频的路由
@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # 保存上传的视频文件
    video_filename = secure_filename(file.filename)
    video_path = os.path.join(UPLOAD_FOLDER, video_filename)
    file.save(video_path)

    # 处理视频 (这里可以进行视频处理，下面是一个简单的示例)
    processed_video_path = os.path.join(OUTPUT_FOLDER, 'processed_' + video_filename)
    process_video(video_path, processed_video_path)  # 调用你的处理视频的函数

    # 返回处理后的视频 URL
    video_url = f"/processed_videos/{processed_video_path.split('/')[-1]}"
    return jsonify({"video_url": video_url})

# 提供处理后的视频文件
@app.route('/processed_videos/<filename>')
def serve_processed_video(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)


# 检测
existing_names = ['张三', '李四']
@app.route('/check_name', methods=['POST'])
def check_name():
    data = request.get_json()
    name = data['name']
    exists = name in existing_names

    return jsonify({'exists': exists})

if __name__ == '__main__':
    app.run(debug=True, port=5001)