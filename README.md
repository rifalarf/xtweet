# xtweet

Streamlit app untuk generate dan auto-post tweet ke X (Twitter) menggunakan Google Gemini AI.

## Cara Setup

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/rifalarf/xtweet.git
cd xtweet
pip install -r requirements.txt
```

### 2. Konfigurasi Secrets

App ini membutuhkan beberapa API key. Cara mengisinya tergantung environment:

#### Pengembangan Lokal

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Buka `.streamlit/secrets.toml` dan isi dengan nilai yang sebenarnya:

```toml
X_CONSUMER_KEY        = "consumer_key_dari_twitter_developer_portal"
X_CONSUMER_SECRET     = "consumer_secret_dari_twitter_developer_portal"
X_ACCESS_TOKEN        = "access_token_dari_twitter_developer_portal"
X_ACCESS_TOKEN_SECRET = "access_token_secret_dari_twitter_developer_portal"
GOOGLE_API_KEY        = "api_key_dari_google_ai_studio"
```

> **Catatan:** File `secrets.toml` sudah ada di `.gitignore` sehingga tidak akan ter-commit ke repository.

#### Streamlit Community Cloud

1. Deploy app dari GitHub ke [share.streamlit.io](https://share.streamlit.io)
2. Buka **App Settings → Secrets**
3. Tambahkan semua variabel berikut beserta nilainya:

```toml
X_CONSUMER_KEY        = "consumer_key_dari_twitter_developer_portal"
X_CONSUMER_SECRET     = "consumer_secret_dari_twitter_developer_portal"
X_ACCESS_TOKEN        = "access_token_dari_twitter_developer_portal"
X_ACCESS_TOKEN_SECRET = "access_token_secret_dari_twitter_developer_portal"
GOOGLE_API_KEY        = "api_key_dari_google_ai_studio"
```

Lihat dokumentasi resmi: [Streamlit Secrets Management](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)

### 3. Mendapatkan API Keys

- **X (Twitter) API Keys:** Daftar di [developer.x.com](https://developer.x.com) dan buat project/app baru. Pastikan app memiliki permission **Read and Write**.
- **Google API Key:** Buka [Google AI Studio](https://aistudio.google.com/app/apikey) dan buat API key baru.

### 4. Jalankan App

```bash
streamlit run app.py
```
