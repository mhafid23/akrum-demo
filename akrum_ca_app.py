
import streamlit as st
import base64
from pathlib import Path
from PIL import Image
import os
import uuid
from akrum_ca_engine import rule30_ca_key_stream

# --- Custom CSS for Modern Styling ---
st.markdown("""
    <style>
        .main {
            background-color: #0a1f44;
            color: #f5f5f5;
        }
        h1, h2, h3 {
            color: #f5f5f5;
        }
        .stButton>button {
            background-color: #1f77b4;
            color: white;
            border-radius: 8px;
            padding: 0.5em 1em;
            border: none;
        }
        .stFileUploader>div>div>div>button {
            background-color: #1f77b4;
            color: white;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Display AKRUM Logo ---
logo_path = "akrum_logo.png"
if Path(logo_path).exists():
    logo = Image.open(logo_path)
    st.image(logo, width=220)

# --- Title ---
st.markdown("<h1 style='text-align: center;'>AKRUM Secure Encryption Demo</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔐 Encrypt", "🔓 Decrypt"])

# --- CA Key Generator ---
def generate_ca_key(seed: str, length: int = 256):
    bitstream = rule30_ca_key_stream(seed, length)
    key_bytes = bytes(int(bitstream[i:i+8], 2) for i in range(0, length, 8))
    return base64.urlsafe_b64encode(key_bytes).decode()

def encrypt_file(data, filename, key):
    encrypted = base64.b64encode(data[::-1])
    filename_encoded = base64.urlsafe_b64encode(filename.encode()).decode()
    combined = f"{filename_encoded}||".encode() + encrypted
    return combined

def decrypt_file(data, key):
    parts = data.split(b'||', 1)
    if len(parts) != 2:
        raise ValueError("Invalid file format.")
    filename = base64.urlsafe_b64decode(parts[0]).decode()
    decrypted = base64.b64decode(parts[1])[::-1]
    return decrypted, filename

with tab1:
    st.subheader("Upload your file to encrypt")
    upload_file = st.file_uploader("📂 Drag and drop or browse your file", key="enc")
    seed = st.text_input("Enter 10-bit binary seed (e.g., 1011001101)", "1011001101")
    if upload_file is not None and seed:
        if st.button("🔐 Encrypt File"):
            try:
                key = generate_ca_key(seed)
                encrypted_data = encrypt_file(upload_file.read(), upload_file.name, key)
                st.success("✅ File encrypted successfully!")
                st.download_button("⬇️ Download Encrypted File", encrypted_data, file_name="encrypted.akrum")
                st.code(key, language="text")
                st.info("🔑 Save this encryption key securely for decryption.")
            except Exception as e:
                st.error(f"Encryption error: {e}")

with tab2:
    st.subheader("Upload the encrypted file and enter the key")
    decrypt_file_up = st.file_uploader("📂 Drag and drop the encrypted file", key="dec")
    decrypt_key = st.text_input("🔑 Enter the encryption key")
    if decrypt_file_up and decrypt_key:
        try:
            decrypted_data, original_filename = decrypt_file(decrypt_file_up.read(), decrypt_key)
            st.success("✅ File decrypted successfully!")
            st.download_button("⬇️ Download Decrypted File", decrypted_data, file_name=original_filename)
        except Exception as e:
            st.error(f"Decryption failed: {e}")

st.markdown("""
<hr style='margin-top: 50px;'>
<p style='text-align: center; color: grey;'>© 2025 AKRUM Technologies. All rights reserved.</p>
""", unsafe_allow_html=True)
