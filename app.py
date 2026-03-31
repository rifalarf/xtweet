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
st.write("generate, edit, dan post ke x secara otomatis & random.")

# --- 2. KONFIGURASI API (VIA SIDEBAR) ---
with st.sidebar:
    st.header("🔑 konfigurasi api")
    X_CONSUMER_KEY = st.text_input("X Consumer Key", type="password")
    X_CONSUMER_SECRET = st.text_input("X Consumer Secret", type="password")
    X_ACCESS_TOKEN = st.text_input("X Access Token", type="password")
    X_ACCESS_TOKEN_SECRET = st.text_input("X Access Token Secret", type="password")
    GOOGLE_API_KEY = st.text_input("Google AI API Key", type="password")
    st.info("pastikan semua key sudah diisi agar bisa posting.")

    st.divider()
    st.header("pengaturan konten")
    topic = st.text_input("topik cuitan:", "mingyu")
    mood = st.selectbox("pilih mood:", ["sambat", "receh", "halu", "kangen wamil", "update konser"])
    num_posts = st.slider("jumlah tweet:", 1, 6, 3)


# --- 3. FUNGSI GENERATOR AI (BAHASA INDONESIA) ---
def generate_carat_tweet(topic, mood):
    if not GOOGLE_API_KEY:
        return "error: google ai api key belum diisi di sidebar."

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


# --- 4. TOMBOL GENERATE ---
if st.button("generate draf cuitan ✨"):
    if not GOOGLE_API_KEY:
        st.error("isi dulu Google AI API Key di sidebar kiri!")
    else:
        with st.spinner("lagi mikir ala carat..."):
            st.session_state.drafts = [generate_carat_tweet(topic, mood) for _ in range(num_posts)]

# --- 5. REVIEW & POSTING ---
if "drafts" in st.session_state:
    st.subheader("review & edit draf")
    final_tweets = []
    for i, draft in enumerate(st.session_state.drafts):
        final_tweets.append(st.text_area(f"post {i+1}", draft, key=f"edit_{i}"))

    if st.button("🚀 post semua dengan jeda waktu random"):
        if not X_CONSUMER_KEY or not X_CONSUMER_SECRET or not X_ACCESS_TOKEN or not X_ACCESS_TOKEN_SECRET:
            st.error("isi dulu semua X API Key & Token di sidebar kiri!")
        else:
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
