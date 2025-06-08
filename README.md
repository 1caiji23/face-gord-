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
