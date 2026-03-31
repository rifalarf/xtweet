import streamlit as st
import tweepy
from google import genai
import random
import time

MIN_DELAY_SECONDS = 120  # 2 minutes
MAX_DELAY_SECONDS = 600  # 10 minutes

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="SVT Tweet Gen", page_icon="💎")
st.title("💎 svt-tweet auto generator")
st.write("generate, edit, dan post ke X secara otomatis & random.")

# --- 2. KONFIGURASI API (DARI secrets.toml) ---
try:
    X_CONSUMER_KEY = st.secrets["X_CONSUMER_KEY"]
    X_CONSUMER_SECRET = st.secrets["X_CONSUMER_SECRET"]
    X_ACCESS_TOKEN = st.secrets["X_ACCESS_TOKEN"]
    X_ACCESS_TOKEN_SECRET = st.secrets["X_ACCESS_TOKEN_SECRET"]
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except KeyError as e:
    st.error(
        f"secret {e} tidak ditemukan. "
        "salin .streamlit/secrets.toml.example ke .streamlit/secrets.toml "
        "dan isi dengan nilai yang sebenarnya."
    )
    st.stop()

# --- 3. PENGATURAN KONTEN (SIDEBAR) ---
with st.sidebar:
    st.header("pengaturan konten")
    topic = st.text_input("topik cuitan:", "mingyu")
    mood = st.selectbox("pilih mood:", ["sambat", "receh", "halu", "kangen wamil", "update konser"])
    num_posts = st.slider("jumlah tweet:", 1, 6, 3)


# --- 4. FUNGSI GENERATOR AI (BAHASA INDONESIA) ---
def generate_carat_tweet(topic, mood):
    prompt = (
        f"buatkan tweet twitter pendek dalam BAHASA INDONESIA tentang {topic} dengan mood {mood}. "
        "persona: fans berat seventeen (carat), bias mingyu. "
        "aturan: gunakan huruf kecil semua (lowercase), gaya santai anak kpop, "
        "sedikit sambat, receh, atau halu tapi tetap keren/estetik. "
        "gunakan istilah lokal seperti 'sebong', 'menangis', 'cawe-cawe', atau 'capek bgt'. "
        "jangan gunakan banyak hashtag."
    )

    try:
        client = genai.Client(api_key=GOOGLE_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        return response.text.lower()
    except Exception as e:
        return f"error generate: {e}"


# --- 5. TOMBOL GENERATE ---
if st.button("generate draf cuitan ✨"):
    with st.spinner("lagi mikir ala carat..."):
        st.session_state.drafts = [generate_carat_tweet(topic, mood) for _ in range(num_posts)]

# --- 6. REVIEW & POSTING ---
if "drafts" in st.session_state:
    st.subheader("review & edit draf")
    final_tweets = []
    for i, draft in enumerate(st.session_state.drafts):
        final_tweets.append(st.text_area(f"post {i+1}", draft, key=f"edit_{i}"))

    if st.button("🚀 post semua dengan jeda waktu random"):
        try:
            client = tweepy.Client(
                consumer_key=X_CONSUMER_KEY,
                consumer_secret=X_CONSUMER_SECRET,
                access_token=X_ACCESS_TOKEN,
                access_token_secret=X_ACCESS_TOKEN_SECRET,
            )

            st.divider()
            for i, tweet in enumerate(final_tweets):
                client.create_tweet(text=tweet)
                st.success(f"✅ berhasil post: {tweet[:40]}...")

                if i < len(final_tweets) - 1:
                    wait_time = random.randint(MIN_DELAY_SECONDS, MAX_DELAY_SECONDS)
                    st.info(f"⏳ nunggu {wait_time / 60:.1f} menit sebelum post berikutnya...")
                    time.sleep(wait_time)

            st.balloons()
            st.success("semua draf sudah ter-post! cek akun x kamu ya 💎")
        except Exception as e:
            st.error(f"ada masalah pas posting: {e}")
