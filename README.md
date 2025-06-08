# 中国省份照片评分 Flask 应用

这是一个基于 Flask 的网页应用，允许用户上传照片并关联到特定中国省份，然后让其他用户对这些照片进行评分并尝试猜测原始省份。

## 项目结构

```
.
├── app/
│   ├── main.py         # Flask 主程序逻辑
│   └── templates/
│       ├── index.html  # 相册和上传表单的 HTML 模板
│       └── rate.html   # 照片评分和省份猜测的 HTML 模板
├── data/
│   └── metadata.json   # 存储图像元数据（ID、文件名、原始省份、评分、猜测）- 自动生成
├── uploads/
│                       # 存储上传的图像文件（使用 UUID 前缀命名）- 自动生成
├── requirements.txt    # Python 依赖项
└── README.md           # 本文档
```

## 设置与安装

1.  **克隆仓库（或按上述结构创建文件）**

2.  **创建虚拟环境（推荐）：**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Windows 系统使用 `venv\Scripts\activate`
    ```

3.  **安装依赖：**
    ```bash
    pip install -r requirements.txt
    ```

4.  **确保必要目录存在：**
    当运行 `app/main.py` 时，如果项目根目录下 `/app/data` 和 `/app/uploads` 目录不存在，应用程序会自动创建它们。

## 运行应用

1.  **进入主应用目录 (`/app`)：**
    ```bash
    cd /app
    ```
    （如果已在 `/app` 目录则无需再次切换）

2.  **运行 Flask 应用：**
    ```bash
    python app/main.py
    ```
    应用通常会在 `http://127.0.0.1:5000/` 启动。

3.  **打开浏览器**访问终端显示的地址即可使用应用。

## 工作原理

-   **`app/main.py`**:
    -   初始化 Flask 应用并设置用于 flash 消息的密钥
    -   定义上传目录 (`/app/uploads/`) 和允许的图像扩展名
    -   将图像元数据存储在 `/app/data/metadata.json`
    -   使用预定义的 `PROVINCES` 省份列表保持表单下拉选项一致性
    -   使用 UUID 作为唯一图像标识符 (`id`) 并创建唯一文件名（如 `uuid.jpg`）防止冲突
    -   **路由功能：**
        -   `/`: 显示主页面 (`index.html`)，包含相册和上传表单。相册中的图片显示原始省份和评分摘要（平均分）
        -   `/upload` (POST): 处理图片上传。将上传图片与选定原始省份关联，使用 UUID 前缀保存文件
        -   `/uploads/<filename>`: 提供上传的图片文件
        -   `/rate_image` (GET): 从元数据中随机选择图片并在 `rate.html` 显示供用户评分和猜测省份
            -   `/submit_rating/<image_id>` (POST): 接收评分(1-10)、猜测省份和评分者所在省份，更新 `metadata.json` 中对应图片的评分信息

-   **`app/templates/index.html`**:
    -   显示 flash 消息的 Jinja2 模板
    -   提供前往相册和评分页面的导航链接
    -   包含上传新图片的表单，带有所属中国省份的下拉选择（从 `PROVINCES` 列表生成）
    -   显示已上传图片的相册，每项包含图片、原始省份和评分摘要（次数和平均分）

-   **`app/templates/rate.html`**:
    -   用于图片评分的 Jinja2 模板
    -   显示 flash 消息
    -   展示随机选择的图片
    -   提供提交表单：数字评分(1-10)、选择猜测省份和评分者所在省份（所有下拉选项均来自 `PROVINCES` 列表）

-   **`data/metadata.json`**:
    -   存储图片对象列表的 JSON 文件，每个对象结构如下：
        ```json
        {
          "id": "唯一图片ID字符串 (UUID)",
          "filename": "带UUID前缀的实际文件名.jpg",
          "original_province": "选定的省份字符串",
          "ratings": [
            {
              "score": "1-10的整数评分",
              "guessed_province": "用户猜测的省份字符串",
              "rater_province": "评分者所在省份字符串"
            }
            // ... 更多评分记录
          ]
        }
        ```

-   **`uploads/`**:
    -   存储所有上传图片文件的目录，文件名使用 UUID 前缀确保唯一性

## 待办事项 / 潜在改进

-   添加图片删除功能
-   实现用户认证以跟踪上传者和评分者
-   为大型相册添加分页功能
-   更智能的评分图片选择（如：选择评分次数少的图片，当前用户未评分的图片）
-   显示更详细的评分统计（如：猜测省份的分布情况）
-   使用更高级的 CSS/JavaScript 改进用户界面
-   编写单元测试和集成测试
-   添加编辑图片详情（如原始省份）的选项

# Chinese Province Photo Rater Flask App

This Flask web application allows users to upload images, associate them with a specific Chinese province, and then have other users rate these photos and try to guess the original province.

## Project Structure

```
.
├── app/
│   ├── main.py         # Main Flask application logic
│   └── templates/
│       ├── index.html  # HTML template for the gallery and upload form
│       └── rate.html   # HTML template for rating an image and guessing its province
├── data/
│   └── metadata.json   # Stores image metadata (ID, filename, original province, ratings, guesses) - auto-generated
├── uploads/
│                       # Stores uploaded image files (with UUID-prefixed names) - auto-generated
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Setup and Installation

1.  **Clone the repository (or create the files as listed above).**

2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ensure necessary directories exist:**
    The application is designed to create `data/` and `uploads/` directories (located at the project root `/app/data` and `/app/uploads`) if they don't exist when `app/main.py` is run.

## Running the Application

1.  **Navigate to the main application directory (`/app`):**
    *(This is the directory where the `app` sub-directory and `requirements.txt` are located)*
    ```bash
    cd /app
    ```
    *(If you are already in `/app`, you don't need to `cd` again)*

2.  **Run the Flask application:**
    ```bash
    python app/main.py
    ```
    The application will typically start on `http://127.0.0.1:5000/`.

3.  **Open your web browser** and go to the address shown in the terminal to use the application.

## How it Works

-   **`app/main.py`**:
    -   Initializes a Flask app with a secret key for flash messages.
    -   Defines the upload folder (`/app/uploads/`) and allowed image extensions.
    -   Stores image metadata in `/app/data/metadata.json`.
    -   Manages a predefined list of `PROVINCES` for consistent dropdowns in forms.
    -   Uses UUIDs for unique image identifiers (`id`) and for creating unique filenames (e.g., `uuid.jpg`) to prevent collisions.
    -   **Routes:**
        -   `/`: Displays the main page (`index.html`) with the image gallery and upload form. Images in the gallery show their original province and a summary of any ratings (average score).
        -   `/upload` (POST): Handles image uploads. Associates the uploaded image with a selected original province. Saves the file with a UUID-prefixed name.
        -   `/uploads/<filename>`: Serves uploaded image files.
        -   `/rate_image` (GET): Selects a random image from the metadata and displays it on `rate.html` for users to rate and guess its province.
            -   `/submit_rating/<image_id>` (POST): Receives the rating score (1-10), the guessed province, and the rater's own province for the specified image. Updates the image's entry in `metadata.json` with this new rating information.
-   **`app/templates/index.html`**:
    -   A Jinja2 template that displays flash messages.
    -   Provides navigation links to the gallery and the image rating page.
    -   Contains a form to upload new images, including a dropdown to select the image's original Chinese province (populated from the `PROVINCES` list).
    -   Displays a gallery of uploaded images. Each item shows the image, its original province, and a summary of its ratings (count and average score).
-   **`app/templates/rate.html`**:
    -   A Jinja2 template for rating an image.
    -   Displays flash messages.
    -   Shows a randomly selected image.
    -   Provides a form where users can submit a numerical rating (1-10), select a guessed province, and select their own province (all from dropdowns populated with the `PROVINCES` list).
-   **`data/metadata.json`**:
    -   A JSON file storing a list of image objects. Each object has the following structure:
        ```json
        {
          "id": "unique_image_id_string (UUID)",
          "filename": "uuid_prefixed_actual_filename.jpg",
          "original_province": "selected_province_string",
          "ratings": [
            {
              "score": integer_rating_from_1_to_10,
              "guessed_province": "user_guessed_province_string",
              "rater_province": "user_rater_province_string"
            }
            // ... more ratings
          ]
        }
        ```
-   **`uploads/`**:
    -   This directory stores all uploaded image files. Filenames are prefixed with a UUID to ensure uniqueness.

## To Do / Potential Improvements

-   Add image deletion functionality.
-   Implement user authentication to track who uploaded and rated images.
-   Add pagination for large galleries.
-   More sophisticated image selection for rating (e.g., images with fewer ratings, images not yet rated by the current user).
-   Display more detailed rating statistics (e.g., distribution of guessed provinces).
-   Improve UI/UX with more advanced CSS/JavaScript.
-   Write unit and integration tests.
-   Option to edit image details (e.g., original province).
```
