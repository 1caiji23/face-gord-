import os
import uuid
import random # Added import
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash
from werkzeug.utils import secure_filename
import json

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'metadata.json')

PROVINCES = [
    "Beijing", "Shanghai", "Sichuan", "Guangdong", "Zhejiang", "Jiangsu",
    "Fujian", "Hunan", "Hubei", "Shandong", "Anhui", "Chongqing",
    "Gansu", "Guizhou", "Hainan", "Hebei", "Heilongjiang", "Henan",
    "Jilin", "Liaoning", "Qinghai", "Shaanxi", "Shanxi", "Tianjin",
    "Xinjiang", "Yunnan", "Guangxi", "Inner Mongolia", "Ningxia", "Tibet", "Other"
]

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key' # Needed for flash messages

# Helper functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_metadata():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content) # Use json.loads for string content
    except json.JSONDecodeError:
        return []
    except FileNotFoundError:
        return []


def save_metadata(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Routes
@app.route('/')
def index():
    images = load_metadata()
    return render_template('index.html', images=images, provinces=PROVINCES)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Prevent filename collisions by prepending UUID, but keep original extension
        base, ext = os.path.splitext(filename)
        unique_filename = f"{uuid.uuid4().hex}{ext}"

        image_id = uuid.uuid4().hex
        original_province = request.form.get('province')

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)

        new_image_metadata = {
            "id": image_id,
            "filename": unique_filename, # Save unique filename
            "original_province": original_province,
            "ratings": []
        }

        metadata_list = load_metadata()
        metadata_list.append(new_image_metadata)
        save_metadata(metadata_list)
        flash('File successfully uploaded')
        return redirect(url_for('index'))
    else:
        flash('Allowed file types are png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/rate_image')
def rate_image():
    images = load_metadata()
    if not images:
        flash('No images to rate. Upload some first!')
        return redirect(url_for('index'))

    # Optionally, filter out images that the user has already rated if you implement user tracking
    # For now, just pick any random image
    selected_image = random.choice(images)
    return render_template('rate.html', image_data=selected_image, provinces=PROVINCES)

@app.route('/submit_rating/<image_id>', methods=['POST'])
def submit_rating(image_id):
    score = request.form.get('score', type=int)
    guessed_province = request.form.get('guessed_province')
    rater_province = request.form.get('rater_province') # Get rater's province

    if score is None or guessed_province is None or rater_province is None:
        flash('Score, guessed province, and your province are required.')
        # Consider redirecting back to the rating page for the same image, if possible
        # This requires passing image_id back or re-fetching, for simplicity redirect to new rate_image
        return redirect(url_for('rate_image'))

    metadata_list = load_metadata()
    image_found = False
    for image_data in metadata_list:
        if image_data['id'] == image_id:
            new_rating = {
                'score': score,
                'guessed_province': guessed_province,
                'rater_province': rater_province # Store rater's province
                # Optionally, add user_id if tracking users, and timestamp
            }
            image_data.setdefault('ratings', []).append(new_rating) # Ensure 'ratings' key exists
            image_found = True
            break

    if image_found:
        save_metadata(metadata_list)
        flash('Rating submitted successfully!')
    else:
        flash('Image not found. Could not submit rating.')

    return redirect(url_for('rate_image')) # Redirect to rate another image


if __name__ == '__main__':
    # Ensure upload and data directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    data_dir = os.path.dirname(DATA_FILE)
    os.makedirs(data_dir, exist_ok=True)
    app.run(debug=True)
