import streamlit as st
import time
import os
import pandas as pd
import matplotlib.pyplot as plt

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


# ==========================================
# 1. HILL CIPHER
# ==========================================

def hill_encrypt(text):

    text = "".join(
        char for char in text.upper()
        if char.isalpha()
    )

    if len(text) % 2 != 0:
        text += "X"

    key = [[3, 3], [2, 5]]

    result = ""

    for i in range(0, len(text), 2):

        a = ord(text[i]) - 65
        b = ord(text[i + 1]) - 65

        x = (key[0][0] * a + key[0][1] * b) % 26
        y = (key[1][0] * a + key[1][1] * b) % 26

        result += chr(x + 65)
        result += chr(y + 65)

    return result


# ==========================================
# 2. AES-256-GCM
# ==========================================


def aes_encrypt(data):

    # Generate a random 256-bit AES key
    key = os.urandom(32)

    # Generate a random 12-byte nonce
    nonce = os.urandom(12)

    cipher = AES.new(
        key,
        AES.MODE_GCM,
        nonce=nonce
    )

    ciphertext, tag = cipher.encrypt_and_digest(data)

    return ciphertext, tag



# ==========================================
# 3. SCRYPT
# ==========================================

def scrypt_derive(password, salt):

    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1
    )

    return kdf.derive(password)


# ==========================================
# 4. PBKDF2
# ==========================================

def pbkdf2_derive(password, salt):

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000
    )

    return kdf.derive(password)


# ==========================================
# PERFORMANCE TEST
# ==========================================

def measure_time(function, *args):

    start = time.perf_counter()

    function(*args)

    end = time.perf_counter()

    return (end - start) * 1000


# ==========================================
# MAIN MODULE
# ==========================================

def render_performance():

    st.title("📈 Performance Analysis")

    st.markdown(
        "Compare the execution time of different "
        "cryptographic algorithms."
    )

    st.info(
        "This benchmark measures local execution time. "
        "Results depend on your computer and system load."
    )

    if st.button(
        "Run Performance Benchmark",
        use_container_width=True
    ):

        sample_text = (
            b"Cryptography protects information "
            b"using mathematical algorithms."
        )

        hill_text = sample_text.decode("utf-8")

        password = b"CryptoGuardDemoPassword"
        salt = os.urandom(16)

        results = []

        with st.spinner("Running performance tests..."):

            # Hill Cipher
            hill_time = measure_time(
                hill_encrypt,
                hill_text
            )

            results.append({
                "Algorithm": "Hill Cipher",
                "Time (ms)": hill_time
            })

            # AES-256-GCM
            aes_time = measure_time(
                aes_encrypt,
                sample_text
            )

            results.append({
                "Algorithm": "AES-256-GCM",
                "Time (ms)": aes_time
            })

            # Scrypt
            scrypt_time = measure_time(
                scrypt_derive,
                password,
                salt
            )

            results.append({
                "Algorithm": "Scrypt",
                "Time (ms)": scrypt_time
            })

            # PBKDF2
            pbkdf2_time = measure_time(
                pbkdf2_derive,
                password,
                salt
            )

            results.append({
                "Algorithm": "PBKDF2",
                "Time (ms)": pbkdf2_time
            })

        df = pd.DataFrame(results)

        st.session_state["performance_results"] = df

        st.success("Performance benchmark completed!")

    if "performance_results" in st.session_state:

        df = st.session_state["performance_results"]

        st.divider()

        st.subheader("📊 Benchmark Results")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        # Bar chart
        st.subheader("1. Execution Time Comparison")

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.bar(
            df["Algorithm"],
            df["Time (ms)"]
        )

        ax.set_ylabel("Execution Time (milliseconds)")
        ax.set_xlabel("Algorithm")
        ax.set_title("Cryptographic Algorithm Performance")

        ax.grid(axis="y", alpha=0.3)

        plt.xticks(rotation=15)

        st.pyplot(fig)

        plt.close(fig)

        # Fastest algorithm
        fastest = df.loc[
            df["Time (ms)"].idxmin()
        ]

        st.metric(
            "Fastest in this test",
            fastest["Algorithm"],
            f"{fastest['Time (ms)']:.4f} ms"
        )

        st.divider()

        st.subheader("2. Algorithm Observations")

        st.write(
            f"**Hill Cipher:** {hill_time if 'hill_time' in locals() else df.loc[df['Algorithm'] == 'Hill Cipher', 'Time (ms)'].iloc[0]:.4f} ms"
        )

        st.write(
            "**AES-256-GCM:** Provides modern authenticated "
            "encryption and is suitable for protecting data."
        )

        st.write(
            "**Scrypt:** A memory-hard password-based key "
            "derivation function."
        )

        st.write(
            "**PBKDF2:** Uses repeated cryptographic hashing "
            "to derive a key from a password."
        )

        st.warning(
            "Important: A shorter execution time does not mean "
            "an algorithm is more secure. These algorithms "
            "perform different tasks, so this is an educational "
            "timing comparison, not a direct security ranking."
        )

    st.divider()

    with st.expander("📘 Understanding Performance Analysis"):

        st.write(
            "Performance analysis measures how long an "
            "algorithm takes to complete a particular operation."
        )

        st.write(
            "**Execution Time:** The time taken to perform "
            "an operation, measured here in milliseconds."
        )

        st.write(
            "**Benchmark:** A controlled test used to compare "
            "the execution time of different operations."
        )

        st.write(
            "For more reliable results, run multiple trials "
            "and compare average execution times."
        )
