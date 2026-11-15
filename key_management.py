import streamlit as st
import time
import os
import pandas as pd
import matplotlib.pyplot as plt

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes


# ==========================================
# 1. KEY DERIVATION FUNCTIONS
# ==========================================

def derive_scrypt_key(password, salt):
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1
    )
    return kdf.derive(password.encode("utf-8"))


def derive_pbkdf2_key(password, salt, iterations=600000):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations
    )
    return kdf.derive(password.encode("utf-8"))


def derive_hkdf_keys(input_key):
    hkdf_encryption = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"encryption-key"
    )

    hkdf_authentication = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"authentication-key"
    )

    encryption_key = hkdf_encryption.derive(input_key)
    authentication_key = hkdf_authentication.derive(input_key)

    return encryption_key, authentication_key


# ==========================================
# 2. MAIN USER INTERFACE
# ==========================================

def render_key_management():

    st.title("🔑 Key Management Center")

    st.markdown(
        "Explore password-based key derivation, "
        "key generation and secure key management."
    )

    tab1, tab2, tab3 = st.tabs([
        "Scrypt vs PBKDF2",
        "HKDF Key Derivation",
        "Key Management Concepts"
    ])

    # ======================================
    # TAB 1: SCRYPT VS PBKDF2
    # ======================================

    with tab1:

        st.subheader("Password-Based Key Derivation")

        st.write(
            "Both Scrypt and PBKDF2 convert a password "
            "into a cryptographic key."
        )

        password = st.text_input(
            "Enter a demonstration password",
            type="password",
            key="km_password"
        )

        if st.button("Compare Algorithms"):

            if len(password) < 8:
                st.warning("Please enter at least 8 characters.")
            else:

                salt = os.urandom(16)

                start = time.perf_counter()
                scrypt_key = derive_scrypt_key(password, salt)
                scrypt_time = time.perf_counter() - start

                start = time.perf_counter()
                pbkdf2_key = derive_pbkdf2_key(password, salt)
                pbkdf2_time = time.perf_counter() - start

                st.success("Both keys generated successfully!")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Scrypt Time",
                        f"{scrypt_time:.5f} seconds"
                    )

                with col2:
                    st.metric(
                        "PBKDF2 Time",
                        f"{pbkdf2_time:.5f} seconds"
                    )

                st.write("### Key Properties")

                st.write("Scrypt key length: 256 bits")
                st.write("PBKDF2 key length: 256 bits")
                st.write("Salt length: 128 bits")

                st.info(
                    "The keys are different because each algorithm "
                    "uses a different derivation process."
                )

                comparison = pd.DataFrame({
                    "Algorithm": ["Scrypt", "PBKDF2"],
                    "Execution Time (seconds)": [
                        scrypt_time,
                        pbkdf2_time
                    ]
                })

                st.write("### Performance Comparison")

                fig, ax = plt.subplots()
                ax.bar(
                    comparison["Algorithm"],
                    comparison["Execution Time (seconds)"]
                )
                ax.set_ylabel("Execution Time (seconds)")
                ax.set_title("Scrypt vs PBKDF2")
                st.pyplot(fig)
                plt.close(fig)

                st.caption(
                    "Execution times vary depending on your computer "
                    "and system load. This is a demonstration, not "
                    "a universal security ranking."
                )

    # ======================================
    # TAB 2: HKDF
    # ======================================

    with tab2:

        st.subheader("HKDF – Key Expansion")

        st.write(
            "HKDF derives multiple purpose-specific keys "
            "from existing key material."
        )

        st.info(
            "HKDF is a key derivation function. It is not designed "
            "to turn a human password directly into a secure key."
        )

        if st.button("Generate HKDF Demonstration"):

            input_key = os.urandom(32)

            encryption_key, authentication_key = (
                derive_hkdf_keys(input_key)
            )

            st.success("Two purpose-specific keys generated!")

            st.write("### Generated Key Information")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Encryption Key**")
                st.code(encryption_key.hex()[:32] + "...")

            with col2:
                st.write("**Authentication Key**")
                st.code(authentication_key.hex()[:32] + "...")

            st.write("Encryption key length: 256 bits")
            st.write("Authentication key length: 256 bits")

            st.write(
                "The two keys are independently derived for "
                "different purposes."
            )

            st.caption(
                "These are temporary demonstration keys. "
                "Do not use them as permanent application secrets."
            )

    # ======================================
    # TAB 3: KEY MANAGEMENT CONCEPTS
    # ======================================

    with tab3:

        st.subheader("Important Key Management Concepts")

        with st.expander("1. What is a Cryptographic Key?"):
            st.write(
                "A cryptographic key is a value used by an "
                "encryption algorithm to protect or recover data."
            )

        with st.expander("2. What is a Salt?"):
            st.write(
                "A salt is random data added during key derivation. "
                "It helps prevent identical passwords from producing "
                "identical derived keys."
            )

        with st.expander("3. What is Scrypt?"):
            st.write(
                "Scrypt is a password-based key derivation function "
                "designed to require significant memory and computation."
            )

        with st.expander("4. What is PBKDF2?"):
            st.write(
                "PBKDF2 repeatedly applies a pseudorandom function "
                "to derive a cryptographic key from a password."
            )

        with st.expander("5. What is HKDF?"):
            st.write(
                "HKDF expands existing key material into multiple "
                "keys for different cryptographic purposes."
            )

        with st.expander("6. Why is Key Management Important?"):
            st.write(
                "Secure key management helps protect keys throughout "
                "their lifecycle, including generation, storage, use "
                "and replacement."
            )

        st.success(
            "Key Management module demonstration completed."
        )
