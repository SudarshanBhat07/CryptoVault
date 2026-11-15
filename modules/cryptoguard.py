import streamlit as st
import os
import matplotlib.pyplot as plt

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag


# ==========================================
# 1. SMART ALGORITHM ADVISOR
# ==========================================

def algorithm_advisor():

    st.subheader("🧠 Smart Algorithm Advisor")

    st.write(
        "Select your requirement to get an educational "
        "cryptography recommendation."
    )

    task = st.selectbox(
        "What do you want to protect?",
        [
            "A file or document",
            "A password",
            "A message that needs authentication",
            "Secure key exchange between two users",
            "Learning classical encryption"
        ]
    )

    if st.button("Get Recommendation", key="advisor_btn"):

        recommendations = {
            "A file or document": (
                "AES-256-GCM",
                "Provides confidentiality and authentication. "
                "It is suitable for protecting files when used "
                "with secure key management."
            ),
            "A password": (
                "Scrypt or PBKDF2",
                "These password-based key derivation functions "
                "are designed to derive cryptographic keys "
                "from passwords."
            ),
            "A message that needs authentication": (
                "HMAC-SHA-256",
                "HMAC checks message integrity and verifies "
                "that the sender possesses the shared secret."
            ),
            "Secure key exchange between two users": (
                "ECDH",
                "Elliptic Curve Diffie-Hellman allows two parties "
                "to derive a shared secret over a communication "
                "channel. Authentication is also needed."
            ),
            "Learning classical encryption": (
                "Hill Cipher",
                "Useful for understanding matrix-based "
                "classical encryption, but not suitable "
                "for protecting real information."
            )
        }

        method, explanation = recommendations[task]

        st.success(f"Recommended method: {method}")
        st.info(explanation)


# ==========================================
# 2. ENCRYPTION VISUALIZER
# ==========================================

def encryption_visualizer():

    st.subheader("📊 Encryption Visualizer")

    st.write(
        "Understand how a message passes through "
        "the encryption process."
    )

    message = st.text_input(
        "Enter a sample message",
        value="HELLO"
    )

    if st.button("Visualize Encryption", key="visualizer_btn"):

        if not message.strip():

            st.warning("Please enter a message.")

        else:

            st.markdown("### Encryption Process")

            steps = [
                ("1. Plaintext", message),
                (
                    "2. Key Generation",
                    "A cryptographic key is generated or derived."
                ),
                (
                    "3. Encryption",
                    "AES-256-GCM encrypts the plaintext using "
                    "the key and a unique nonce."
                ),
                (
                    "4. Authentication",
                    "An authentication tag is generated to "
                    "help detect unauthorized modifications."
                ),
                (
                    "5. Encrypted Output",
                    "Ciphertext and authentication data are ready "
                    "to be stored or transmitted."
                )
            ]

            for title, description in steps:

                with st.container(border=True):

                    st.markdown(f"**{title}**")
                    st.write(description)

            st.success(
                "Visualization completed! "
                "This is a conceptual explanation of AES-256-GCM."
            )

    st.divider()

    st.markdown("### Encryption Flow")

    st.code(
        """
Plaintext
    |
    v
Key Generation / Derivation
    |
    v
AES-256-GCM Encryption
    |
    v
Ciphertext + Authentication Tag
    |
    v
Protected Encrypted File
        """,
        language="text"
    )


# ==========================================
# 3. TAMPER DETECTION DEMONSTRATION
# ==========================================

def tamper_detection():

    st.subheader("🛡️ Tamper Detection Lab")

    st.write(
        "Demonstrate how AES-256-GCM detects changes "
        "to encrypted data."
    )

    st.info(
        "This is a separate demonstration using temporary "
        "data. It does not modify your original project files."
    )

    if st.button("Run Tamper Detection Test", key="tamper_btn"):

        # Sample plaintext
        plaintext = b"CryptoGuard Security Test"

        # Generate a temporary key and nonce
        key = AESGCM.generate_key(bit_length=256)
        nonce = os.urandom(12)

        # Create AES-GCM object
        aesgcm = AESGCM(key)

        # Encrypt the sample message
        encrypted_data = aesgcm.encrypt(
            nonce,
            plaintext,
            None
        )

        st.success("Step 1: Original message encrypted.")

        st.write("**Original message:**")
        st.code(plaintext.decode())

        st.write("**Encrypted data:**")
        st.code(encrypted_data.hex()[:100] + "...")

        # Verify original encrypted data
        try:

            recovered = aesgcm.decrypt(
                nonce,
                encrypted_data,
                None
            )

            st.success(
                "Step 2: Original data authenticated successfully."
            )

        except InvalidTag:

            st.error("Original data authentication failed.")
            return

        # Create a modified copy for the demonstration
        modified_data = bytearray(encrypted_data)

        modified_data[-1] ^= 1

        st.warning(
            "Step 3: A temporary copy of the encrypted data "
            "has been modified."
        )

        # Try decrypting modified data
        try:

            aesgcm.decrypt(
                nonce,
                bytes(modified_data),
                None
            )

            st.error(
                "Unexpected result: modified data was accepted."
            )

        except InvalidTag:

            st.error(
                "TAMPERING DETECTED! "
                "AES-256-GCM rejected the modified data."
            )

            st.write(
                "The authentication check failed, so the "
                "modified encrypted data was not accepted."
            )

        st.success(
            "CryptoGuard test completed successfully."
        )


# ==========================================
# MAIN CRYPTOGUARD MODULE
# ==========================================

def render_cryptoguard():

    st.title("🛡️ CryptoGuard")

    st.markdown(
        "An intelligent cryptography learning and "
        "security demonstration module."
    )

    st.divider()

    tab1, tab2, tab3 = st.tabs(
        [
            "🧠 Algorithm Advisor",
            "📊 Encryption Visualizer",
            "🛡️ Tamper Detection"
        ]
    )

    with tab1:
        algorithm_advisor()

    with tab2:
        encryption_visualizer()

    with tab3:
        tamper_detection()
