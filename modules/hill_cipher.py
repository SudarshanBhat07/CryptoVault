import streamlit as st
import math


# ==========================================
# HILL CIPHER MATHEMATICAL FUNCTIONS
# ==========================================

def clean_text(text):
    """Convert input into uppercase English letters."""
    return "".join(
        char for char in text.upper()
        if char.isascii() and char.isalpha()
    )


def matrix_inverse_mod_26(a, b, c, d):

    determinant = (a * d - b * c) % 26

    if math.gcd(determinant, 26) != 1:
        raise ValueError(
            "Invalid key! The determinant must be relatively "
            "prime to 26. Please change your key matrix."
        )

    determinant_inverse = pow(determinant, -1, 26)

    inverse = [
        [
            (d * determinant_inverse) % 26,
            (-b * determinant_inverse) % 26
        ],
        [
            (-c * determinant_inverse) % 26,
            (a * determinant_inverse) % 26
        ]
    ]

    return inverse, determinant


def process_hill(text, matrix):

    result = []
    calculations = []

    for i in range(0, len(text), 2):

        block = text[i:i + 2]

        x = ord(block[0]) - 65
        y = ord(block[1]) - 65

        first_raw = matrix[0][0] * x + matrix[0][1] * y
        second_raw = matrix[1][0] * x + matrix[1][1] * y

        first = first_raw % 26
        second = second_raw % 26

        output = chr(first + 65) + chr(second + 65)

        result.append(output)

        calculations.append({
            "input": block,
            "numbers": [x, y],
            "first_raw": first_raw,
            "second_raw": second_raw,
            "output_numbers": [first, second],
            "output": output,
            "matrix": matrix
        })

    return "".join(result), calculations


# ==========================================
# HILL CIPHER USER INTERFACE
# ==========================================

def render_hill_cipher():

    st.title("🔢 Hill Cipher Encryption & Decryption")

    st.write(
        "Encrypt and decrypt messages using matrix-based "
        "classical cryptography."
    )

    st.info(
        "Educational demonstration only. Hill Cipher is not "
        "secure for protecting real-world files."
    )

    st.divider()

    # ======================================
    # MESSAGE INPUT
    # ======================================

    st.subheader("1. Enter Your Message")

    message = st.text_area(
        "Plaintext / Ciphertext",
        placeholder="Enter your message here...",
        height=110
    )

    # ======================================
    # KEY MATRIX
    # ======================================

    st.subheader("2. Configure Your 2 × 2 Key Matrix")

    col1, col2 = st.columns(2)

    with col1:
        a = st.number_input(
            "K11",
            value=3,
            step=1
        )

        c = st.number_input(
            "K21",
            value=2,
            step=1
        )

    with col2:
        b = st.number_input(
            "K12",
            value=3,
            step=1
        )

        d = st.number_input(
            "K22",
            value=5,
            step=1
        )

    matrix = [
        [int(a) % 26, int(b) % 26],
        [int(c) % 26, int(d) % 26]
    ]

    st.markdown("**Your Key Matrix:**")

    st.code(
        f"| {matrix[0][0]}  {matrix[0][1]} |\n"
        f"| {matrix[1][0]}  {matrix[1][1]} |"
    )

    determinant = (
        matrix[0][0] * matrix[1][1]
        - matrix[0][1] * matrix[1][0]
    ) % 26

    st.write(f"Determinant (mod 26): **{determinant}**")

    if math.gcd(determinant, 26) == 1:
        st.success("Valid key matrix")
    else:
        st.error(
            "Invalid key matrix. Choose values that produce "
            "a determinant relatively prime to 26."
        )

    st.divider()

    # ======================================
    # ENCRYPT / DECRYPT
    # ======================================

    st.subheader("3. Choose Operation")

    col1, col2 = st.columns(2)

    with col1:
        encrypt_button = st.button(
            "🔒 Encrypt Message",
            use_container_width=True
        )

    with col2:
        decrypt_button = st.button(
            "🔓 Decrypt Message",
            use_container_width=True
        )

    if encrypt_button or decrypt_button:

        text = clean_text(message)

        if not text:
            st.error("Please enter a valid English message.")
            return

        try:

            inverse_matrix, determinant = matrix_inverse_mod_26(
                matrix[0][0],
                matrix[0][1],
                matrix[1][0],
                matrix[1][1]
            )

            # ==================================
            # ENCRYPTION
            # ==================================

            if encrypt_button:

                if len(text) % 2 != 0:
                    text += "X"

                    st.warning(
                        "An X was added at the end to make "
                        "the message length even."
                    )

                active_matrix = matrix

                result, calculations = process_hill(
                    text,
                    active_matrix
                )

                heading = "Encrypted Ciphertext"

            # ==================================
            # DECRYPTION
            # ==================================

            else:

                if len(text) % 2 != 0:
                    st.error(
                        "Ciphertext length must be even."
                    )
                    return

                active_matrix = inverse_matrix

                result, calculations = process_hill(
                    text,
                    active_matrix
                )

                heading = "Decrypted Plaintext"

            # ==================================
            # RESULT
            # ==================================

            st.divider()

            st.subheader("4. Result")

            st.success(
                f"{heading}: **{result}**"
            )

            st.code(result)

            st.download_button(
                "📥 Download Result",
                data=result,
                file_name="hill_cipher_result.txt",
                mime="text/plain"
            )

            # ==================================
            # MATHEMATICAL VISUALIZATION
            # ==================================

            st.divider()

            st.subheader(
                "5. Step-by-Step Mathematical Visualization"
            )

            st.write(
                "Expand each block to understand how the "
                "Hill Cipher performs matrix multiplication."
            )

            st.markdown("**Matrix used in this operation:**")

            st.code(
                f"| {active_matrix[0][0]}  "
                f"{active_matrix[0][1]} |\n"
                f"| {active_matrix[1][0]}  "
                f"{active_matrix[1][1]} |"
            )

            for index, calc in enumerate(
                calculations,
                start=1
            ):

                with st.expander(
                    f"Block {index}: "
                    f"{calc['input']} → {calc['output']}"
                ):

                    x, y = calc["numbers"]

                    m = calc["matrix"]

                    st.markdown("**Step 1 — Convert letters into numbers**")

                    st.write(
                        f"{calc['input'][0]} = {x}, "
                        f"{calc['input'][1]} = {y}"
                    )

                    st.code(
                        f"Input Vector = [{x}, {y}]"
                    )

                    st.markdown("**Step 2 — Matrix multiplication**")

                    st.code(
                        f"| {m[0][0]}  {m[0][1]} |   | {x} |\n"
                        f"| {m[1][0]}  {m[1][1]} | × | {y} |"
                    )

                    st.markdown("**Step 3 — Calculate each row**")

                    st.write(
                        f"First row: "
                        f"({m[0][0]} × {x}) + "
                        f"({m[0][1]} × {y}) "
                        f"= {calc['first_raw']}"
                    )

                    st.write(
                        f"Second row: "
                        f"({m[1][0]} × {x}) + "
                        f"({m[1][1]} × {y}) "
                        f"= {calc['second_raw']}"
                    )

                    st.markdown("**Step 4 — Apply modulo 26**")

                    st.write(
                        f"{calc['first_raw']} mod 26 "
                        f"= {calc['output_numbers'][0]}"
                    )

                    st.write(
                        f"{calc['second_raw']} mod 26 "
                        f"= {calc['output_numbers'][1]}"
                    )

                    st.markdown("**Step 5 — Convert numbers into letters**")

                    st.write(
                        f"{calc['output_numbers'][0]} = "
                        f"{calc['output'][0]}, "
                        f"{calc['output_numbers'][1]} = "
                        f"{calc['output'][1]}"
                    )

                    st.success(
                        f"Final Block Result: {calc['output']}"
                    )

            # ==================================
            # DECRYPTION NOTE
            # ==================================

            if decrypt_button:

                st.info(
                    "Decryption uses the inverse key matrix "
                    "calculated modulo 26."
                )

                st.markdown("**Inverse Key Matrix:**")

                st.code(
                    f"| {inverse_matrix[0][0]}  "
                    f"{inverse_matrix[0][1]} |\n"
                    f"| {inverse_matrix[1][0]}  "
                    f"{inverse_matrix[1][1]} |"
                )

                st.caption(
                    "Any padding X added during encryption "
                    "remains in the decrypted output. "
                    "Remove it manually only if it was padding."
                )

        except ValueError as error:

            st.error(str(error))
