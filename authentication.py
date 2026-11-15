import streamlit as st
import os
import hmac
import hashlib

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


# ==========================================
# 1. HMAC FUNCTIONS
# ==========================================

def generate_hmac(message, secret_key):

    message_bytes = message.encode("utf-8")
    key_bytes = secret_key.encode("utf-8")

    authentication_code = hmac.new(
        key_bytes,
        message_bytes,
        hashlib.sha256
    ).hexdigest()

    return authentication_code


def verify_hmac(message, secret_key, received_hmac):

    expected_hmac = generate_hmac(
        message,
        secret_key
    )

    return hmac.compare_digest(
        expected_hmac,
        received_hmac
    )


# ==========================================
# 2. ECDH FUNCTIONS
# ==========================================

def generate_ecdh_key_pair():

    private_key = ec.generate_private_key(
        ec.SECP256R1()
    )

    public_key = private_key.public_key()

    return private_key, public_key


def derive_shared_secret(private_key, peer_public_key):

    shared_secret = private_key.exchange(
        ec.ECDH(),
        peer_public_key
    )

    return shared_secret


def derive_session_key(shared_secret):

    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"hill-cipher-pro-ecdh-demo"
    )

    return hkdf.derive(shared_secret)


# ==========================================
# 3. MAIN AUTHENTICATION INTERFACE
# ==========================================

def render_authentication():

    st.title("🛡️ Authentication Lab")

    st.markdown(
        "Explore message authentication using HMAC "
        "and secure key exchange using ECDH."
    )

    tab1, tab2 = st.tabs([
        "HMAC Authentication",
        "ECDH Key Exchange"
    ])

    # ======================================
    # TAB 1: HMAC
    # ======================================

    with tab1:

        st.subheader("HMAC - Message Authentication")

        st.write(
            "HMAC uses a shared secret key to generate "
            "an authentication code for a message."
        )

        st.info(
            "Both sender and receiver must possess the same "
            "secret key to generate and verify the HMAC."
        )

        message = st.text_area(
            "Enter your message",
            value="Hello, this is a secure message!",
            key="hmac_message"
        )

        secret_key = st.text_input(
            "Enter shared secret key",
            type="password",
            key="hmac_secret"
        )

        if st.button("Generate HMAC"):

            if not message:
                st.warning("Please enter a message.")

            elif not secret_key:
                st.warning("Please enter a secret key.")

            else:

                generated_hmac = generate_hmac(
                    message,
                    secret_key
                )

                st.success("HMAC generated successfully!")

                st.write("### Authentication Code")

                st.code(generated_hmac)

                st.session_state["generated_hmac"] = generated_hmac

        st.markdown("---")

        st.subheader("Verify Message Integrity")

        st.write(
            "Enter a message and the same secret key "
            "to check its authentication code."
        )

        verify_message = st.text_area(
            "Message to verify",
            key="verify_message"
        )

        verify_secret = st.text_input(
            "Shared secret key for verification",
            type="password",
            key="verify_secret"
        )

        generated_code = st.session_state.get(
            "generated_hmac",
            ""
        )

        received_code = st.text_input(
            "Authentication code",
            value=generated_code,
            key="received_hmac"
        )

        if st.button("Verify HMAC"):

            if not verify_message or not verify_secret:
                st.warning(
                    "Please enter the message and secret key."
                )

            elif not received_code:
                st.warning(
                    "Please enter the authentication code."
                )

            else:

                is_valid = verify_hmac(
                    verify_message,
                    verify_secret,
                    received_code
                )

                if is_valid:

                    st.success(
                        "AUTHENTICATION SUCCESSFUL! "
                        "The message matches the supplied HMAC."
                    )

                else:

                    st.error(
                        "AUTHENTICATION FAILED! "
                        "The message, key or HMAC does not match."
                    )

        st.caption(
            "HMAC verifies message authentication and integrity. "
            "It does not encrypt or hide the message."
        )

    # ======================================
    # TAB 2: ECDH
    # ======================================

    with tab2:

        st.subheader("ECDH - Elliptic Curve Diffie-Hellman")

        st.write(
            "ECDH allows two parties to establish "
            "the same shared secret using their private "
            "and public keys."
        )

        st.info(
            "The private keys stay with their owners. "
            "Only public keys are exchanged."
        )

        if st.button("Generate ECDH Key Exchange"):

            # Generate Alice's key pair

            alice_private, alice_public = (
                generate_ecdh_key_pair()
            )

            # Generate Bob's key pair

            bob_private, bob_public = (
                generate_ecdh_key_pair()
            )

            # Alice calculates shared secret

            alice_secret = derive_shared_secret(
                alice_private,
                bob_public
            )

            # Bob calculates shared secret

            bob_secret = derive_shared_secret(
                bob_private,
                alice_public
            )

            # Derive session keys using HKDF

            alice_session_key = derive_session_key(
                alice_secret
            )

            bob_session_key = derive_session_key(
                bob_secret
            )

            st.success(
                "ECDH key exchange completed!"
            )

            st.write("### Alice")

            st.write("Alice generated her private and public keys.")

            st.write("### Bob")

            st.write("Bob generated his private and public keys.")

            st.write("### Shared Secret Verification")

            if hmac.compare_digest(
                alice_secret,
                bob_secret
            ):

                st.success(
                    "SUCCESS! Alice and Bob generated "
                    "the same shared secret."
                )

            else:

                st.error(
                    "Shared secret verification failed."
                )

            st.write("### Session Key Verification")

            if hmac.compare_digest(
                alice_session_key,
                bob_session_key
            ):

                st.success(
                    "SUCCESS! Both parties derived "
                    "the same 256-bit session key."
                )

            else:

                st.error(
                    "Session key verification failed."
                )

            st.write("### Key Information")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Alice Session Key",
                    f"{len(alice_session_key) * 8} bits"
                )

            with col2:

                st.metric(
                    "Bob Session Key",
                    f"{len(bob_session_key) * 8} bits"
                )

            st.caption(
                "For safety, private keys and shared secrets "
                "are not displayed. This is a demonstration "
                "of ECDH key agreement, not a complete "
                "authenticated communication protocol."
            )


    # ======================================
    # MODULE INFORMATION
    # ======================================

    st.markdown("---")

    st.subheader("What did we demonstrate?")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### HMAC")

        st.write(
            "- Message authentication"
        )

        st.write(
            "- Integrity verification"
        )

        st.write(
            "- Shared secret key"
        )

    with col2:

        st.markdown("### ECDH")

        st.write(
            "- Public and private key pairs"
        )

        st.write(
            "- Shared secret generation"
        )

        st.write(
            "- Session key derivation using HKDF"
        )

    st.success(
        "Authentication Lab demonstration completed."
    )
