import os
import streamlit as st

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.exceptions import InvalidTag


# ==========================================
# AES-256-GCM CONFIGURATION
# ==========================================

MAGIC = b"HCP1"

SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32
TAG_SIZE = 16

SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1


# ==========================================
# PASSWORD-BASED KEY DERIVATION
# ==========================================

def derive_key(password, salt):

    if not password:
        raise ValueError("Password cannot be empty.")

    kdf = Scrypt(
        salt=salt,
        length=KEY_SIZE,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P
    )

    return kdf.derive(password.encode("utf-8"))


# ==========================================
# AES-256-GCM ENCRYPTION
# ==========================================

def encrypt_file(file_data, password):

    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)

    key = derive_key(password, salt)

    aesgcm = AESGCM(key)

    encrypted_data = aesgcm.encrypt(
        nonce,
        file_data,
        MAGIC
    )

    # File format:
    # MAGIC + SALT + NONCE + CIPHERTEXT + AUTHENTICATION TAG

    encrypted_file = (
        MAGIC +
        salt +
        nonce +
        encrypted_data
    )

    return encrypted_file


# ==========================================
# AES-256-GCM DECRYPTION
# ==========================================

def decrypt_file(encrypted_file, password):

    minimum_size = (
        len(MAGIC) +
        SALT_SIZE +
        NONCE_SIZE +
        TAG_SIZE
    )

    if len(encrypted_file) < minimum_size:
        raise ValueError("Invalid or corrupted encrypted file.")

    if encrypted_file[:len(MAGIC)] != MAGIC:
        raise ValueError(
            "This is not a HILL CIPHER PRO encrypted file."
        )

    position = len(MAGIC)

    salt = encrypted_file[
        position:position + SALT_SIZE
    ]

    position += SALT_SIZE

    nonce = encrypted_file[
        position:position + NONCE_SIZE
    ]

    position += NONCE_SIZE

    ciphertext = encrypted_file[position:]

    key = derive_key(password, salt)

    aesgcm = AESGCM(key)

    # AES-GCM automatically verifies authentication.
    # Incorrect password or modified data raises InvalidTag.

    decrypted_data = aesgcm.decrypt(
        nonce,
        ciphertext,
        MAGIC
    )

    return decrypted_data


# ==========================================
# STREAMLIT USER INTERFACE
# ==========================================

def render_aes_encryption():

    st.title("🛡️ AES-256-GCM File Encryption")

    st.write(
        "Protect your files using authenticated encryption "
        "and password-based key derivation."
    )

    st.info(
        "AES-256-GCM provides confidentiality and integrity. "
        "Scrypt derives a 256-bit encryption key from your password."
    )

    st.divider()

    # ======================================
    # ENCRYPTION AND DECRYPTION TABS
    # ======================================

    encrypt_tab, decrypt_tab = st.tabs(
        ["🔒 Encrypt File", "🔓 Decrypt File"]
    )

    # ======================================
    # ENCRYPTION TAB
    # ======================================

    with encrypt_tab:

        st.subheader("Encrypt Your File")

        uploaded_file = st.file_uploader(
            "Choose a file to encrypt",
            key="aes_encrypt_upload"
        )

        password = st.text_input(
            "Create Encryption Password",
            type="password",
            key="aes_encrypt_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="aes_confirm_password"
        )

        if st.button(
            "🔒 Encrypt File",
            use_container_width=True,
            key="aes_encrypt_button"
        ):

            if uploaded_file is None:

                st.error("Please upload a file.")

            elif not password:

                st.error("Please enter a password.")

            elif password != confirm_password:

                st.error("Passwords do not match.")

            else:

                try:

                    file_data = uploaded_file.getvalue()

                    with st.spinner("Encrypting your file..."):

                        encrypted_data = encrypt_file(
                            file_data,
                            password
                        )

                    st.success("File encrypted successfully!")

                    st.write(
                        "**Original filename:**",
                        uploaded_file.name
                    )

                    st.write(
                        "**Original file size:**",
                        f"{len(file_data):,} bytes"
                    )

                    st.write(
                        "**Encrypted file size:**",
                        f"{len(encrypted_data):,} bytes"
                    )

                    st.download_button(
                        "📥 Download Encrypted File",
                        data=encrypted_data,
                        file_name=uploaded_file.name + ".hcp",
                        mime="application/octet-stream",
                        key="aes_download_encrypted"
                    )

                    st.warning(
                        "Keep your password safe. It is not stored "
                        "by this application and cannot be recovered "
                        "if lost."
                    )

                except Exception as error:

                    st.error(
                        f"Encryption failed: {error}"
                    )

    # ======================================
    # DECRYPTION TAB
    # ======================================

    with decrypt_tab:

        st.subheader("Decrypt Your File")

        encrypted_upload = st.file_uploader(
            "Upload your encrypted .hcp file",
            key="aes_decrypt_upload"
        )

        decrypt_password = st.text_input(
            "Enter Decryption Password",
            type="password",
            key="aes_decrypt_password"
        )

        if st.button(
            "🔓 Decrypt File",
            use_container_width=True,
            key="aes_decrypt_button"
        ):

            if encrypted_upload is None:

                st.error("Please upload an encrypted file.")

            elif not decrypt_password:

                st.error("Please enter your password.")

            else:

                try:

                    encrypted_data = encrypted_upload.getvalue()

                    with st.spinner("Decrypting your file..."):

                        decrypted_data = decrypt_file(
                            encrypted_data,
                            decrypt_password
                        )

                    original_name = encrypted_upload.name

                    if original_name.lower().endswith(".hcp"):

                        original_name = original_name[:-4]

                    else:

                        original_name += ".decrypted"

                    st.success(
                        "Decryption successful! "
                        "File authentication passed."
                    )

                    st.write(
                        "**Recovered filename:**",
                        original_name
                    )

                    st.write(
                        "**Decrypted file size:**",
                        f"{len(decrypted_data):,} bytes"
                    )

                    st.download_button(
                        "📥 Download Decrypted File",
                        data=decrypted_data,
                        file_name=original_name,
                        mime="application/octet-stream",
                        key="aes_download_decrypted"
                    )

                except InvalidTag:

                    st.error(
                        "Authentication failed! The password is "
                        "incorrect or the encrypted file has been "
                        "modified."
                    )

                except ValueError as error:

                    st.error(str(error))

                except Exception:

                    st.error(
                        "Decryption failed due to an unexpected error."
                    )

    # ======================================
    # TAMPER DETECTION LAB
    # ======================================

    st.divider()

    st.title("🛡️ AES-GCM Tamper Detection Lab")

    st.write(
        "Demonstrate how AES-256-GCM detects modifications "
        "to encrypted files."
    )

    st.info(
        "This test uses a temporary copy of the encrypted file. "
        "Your original file will not be modified."
    )

    tamper_file = st.file_uploader(
        "Upload an encrypted .hcp file for testing",
        key="tamper_test_upload"
    )

    tamper_password = st.text_input(
        "Enter the original encryption password",
        type="password",
        key="tamper_test_password"
    )

    if st.button(
        "🧪 Run Tamper Detection Test",
        use_container_width=True,
        key="run_tamper_test"
    ):

        if tamper_file is None:

            st.error("Please upload an encrypted .hcp file.")

        elif not tamper_password:

            st.error("Please enter the original password.")

        else:

            try:

                original_data = tamper_file.getvalue()

                with st.spinner("Verifying original encrypted file..."):

                    # First verify that the original file
                    # and password are valid.

                    decrypt_file(
                        original_data,
                        tamper_password
                    )

                st.success(
                    "Original encrypted file authentication passed."
                )

                # Create a temporary copy.
                # The uploaded original remains unchanged.

                modified_data = bytearray(original_data)

                # Change one bit in the authentication tag.
                modified_data[-1] ^= 1

                st.write(
                    "A temporary copy has been modified for testing."
                )

                try:

                    decrypt_file(
                        bytes(modified_data),
                        tamper_password
                    )

                    st.error(
                        "Unexpected result: Modified data was accepted."
                    )

                except InvalidTag:

                    st.success(
                        "TAMPERING DETECTED! "
                        "AES-256-GCM rejected the modified file."
                    )

                    st.markdown("""
                    **Security verification**

                    - Original file remains unchanged.
                    - Modified authentication tag was rejected.
                    - Decryption was not accepted.
                    - AES-GCM integrity protection is working.
                    """)

            except InvalidTag:

                st.error(
                    "The original file could not be authenticated. "
                    "Check your password or encrypted file."
                )

            except ValueError as error:

                st.error(str(error))

            except Exception:

                st.error(
                    "The tamper detection test could not be completed."
                )
