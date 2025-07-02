# 🖼️ Meme Generator (Tenglish Edition)

This project is a Tenglish meme generator that takes a topic as input, analyzes the emotional tone, and generates a relevant meme with Tenglish dialogue overlaid on it. It uses generative AI and image processing pipelines to produce creative outputs.

## 🚀 Features

- 🔥 Generates memes based on user-provided topics
- 🧠 Uses emotion detection to select suitable meme templates
- 🖋️ Supports Tenglish text rendering using custom fonts
- 🎨 Returns images as PNG or base64
- 🌐 Exposes a FastAPI-based web API for easy integration
- ☁️ Integrates with Supabase for dynamic template fetching

## 🗂️ Project Structure

```
meme_generator/
├── artifacts/                   # Data and output folders
│   ├── memes/                  # Generated memes (optional storage)
│   └── emotion_image_urls.json # Image URL mappings from Supabase
├── fonts/
│   └── NotoSansTelugu-Regular.ttf  # Font for Tenglish rendering
├── logs/                       # Logging files
├── src/                        # Core source code
│   ├── components/             # Logic modules (emotion, meme, topic ingestion)
│   ├── constants/              # Constant definitions
│   ├── entity/                 # Pydantic entity definitions
│   ├── exceptions/             # Custom error handling
│   ├── logger/                 # Logging setup
│   ├── pipeline/               # Pipeline orchestration
│   ├── utils/                  # Utility modules (template selection, etc.)
├── template_dir/               # Stores selected image templates
├── venv/                       # Virtual environment
├── app.py                      # FastAPI app
├── requirements.txt            # Dependencies
└── README.md                   # Project documentation
```

## 🔌 API Endpoints

### 🔸 POST /generate-meme

Generates a meme and returns the image as a PNG stream.

**Request Body:**
```json
{
  "topic_name": "job interviews"
}
```

**Response Headers:**
- X-Emotion: Detected emotion (e.g., "angry")

**Response:**
Returns a streaming PNG image.

### 🔸 POST /generate-meme-base64

Generates a meme and returns it as a base64-encoded string.

**Request Body:**
```json
{
  "topic_name": "job interviews"
}
```

**Response:**
```json
{
  "status": "success",
  "emotion": "angry",
  "image_base64": "data:image/png;base64,..."
}
```

### 🔸 GET /fetch-templates

Fetches image template metadata from Supabase.

**Response:**
```json
{
  "status": "success",
  "templates": {
    "happy": ["happy1.png", "happy2.png"],
    "sad": ["sad1.png"]
  }
}
```

## ⚙️ Installation

```bash
# Clone the repo
git clone https://github.com/your-username/meme_generator.git
cd meme_generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

## ▶️ Running the App

```bash
uvicorn app:app --reload
```

API will be live at: http://127.0.0.1:8000

## 🧪 Sample Usage (cURL)

```bash
curl -X POST http://127.0.0.1:8000/generate-meme \
     -H "Content-Type: application/json" \
     -d '{"topic_name": "first salary"}' \
     --output meme.png
```

## 📌 Notes

- Font rendering is handled using NotoSansTelugu for better support of Telugu script in Tenglish.
- Templates are fetched from Supabase and stored locally in `template_dir/`.
- The project assumes pre-existing template image URLs stored in `emotion_image_urls.json`.

## 🛠️ Tech Stack

- Python
- FastAPI
- Pillow (PIL)
- Supabase
- Google Gemini (for dialogue generation)
- Logging, Exception Handling, Modular Design

## 📄 License

MIT License. Free to use, fork, and modify.# meme_generator
