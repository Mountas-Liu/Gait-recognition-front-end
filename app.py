from flask import Flask, render_template, request, jsonify
from PIL import Image
import io

app = Flask(__name__)

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

@app.route('/enter-img')
def enter_img():
    if 'image' not in request.files:
        return jsonify({'message': 'No image uploaded.'}), 400

    file = request.files['image']

    # 打开图片
    image = Image.open(file.stream)

    # 处理图片（示例：将图片转为灰度图）
    processed_image = image.convert('L')

    # 将处理后的图片保存到字节流
    byte_io = io.BytesIO()
    processed_image.save(byte_io, format='PNG')
    byte_io.seek(0)

    # 返回处理后的图片
    return jsonify({
        'message': 'Image processed successfully.',
        'image': byte_io.read().hex()  # 将图片数据转为十六进制字符串
    })


@app.route('/reco-img')
def reco_img():
    if 'image' not in request.files:
        return jsonify({'message': 'No image uploaded.'}), 400

    file = request.files['image']

    # 打开图片
    image = Image.open(file.stream)

    # 处理图片（示例：将图片转为灰度图）
    processed_image = image.convert('L')

    # 将处理后的图片保存到字节流
    byte_io = io.BytesIO()
    processed_image.save(byte_io, format='PNG')
    byte_io.seek(0)

    # 返回处理后的图片
    return jsonify({
        'message': 'Image processed successfully.',
        'image': byte_io.read().hex()  # 将图片数据转为十六进制字符串
    })

existing_names = ['张三', '李四']

@app.route('/check_name', methods=['POST'])
def check_name():
    data = request.get_json()
    name = data['name']
    exists = name in existing_names

    return jsonify({'exists': exists})

if __name__ == '__main__':
    app.run(debug=True, port=5001)