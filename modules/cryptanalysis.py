import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import string


# ==========================================
# ENGLISH LETTER FREQUENCIES
# ==========================================

ENGLISH_FREQUENCY = {
    "A": 8.167, "B": 1.492, "C": 2.782,
    "D": 4.253, "E": 12.702, "F": 2.228,
    "G": 2.015, "H": 6.094, "I": 6.966,
    "J": 0.153, "K": 0.772, "L": 4.025,
    "M": 2.406, "N": 6.749, "O": 7.507,
    "P": 1.929, "Q": 0.095, "R": 5.987,
    "S": 6.327, "T": 9.056, "U": 2.758,
    "V": 0.978, "W": 2.360, "X": 0.150,
    "Y": 1.974, "Z": 0.074
}


# ==========================================
# FREQUENCY ANALYSIS
# ==========================================

def analyze_frequency(text):

    cleaned_text = "".join(
        char for char in text.upper()
        if char in string.ascii_uppercase
    )

    total_letters = len(cleaned_text)

    if total_letters == 0:
        return None

    counts = Counter(cleaned_text)

    results = []

    for letter in string.ascii_uppercase:

        count = counts.get(letter, 0)
        percentage = (count / total_letters) * 100

        results.append({
            "Letter": letter,
            "Count": count,
            "Frequency (%)": round(percentage, 2),
            "English Frequency (%)": ENGLISH_FREQUENCY[letter]
        })

    return pd.DataFrame(results)


# ==========================================
# MAIN MODULE
# ==========================================

def render_cryptanalysis():

    st.title("🔍 Cryptanalysis Lab")

    st.markdown(
        "Study encrypted text using statistical "
        "and letter frequency analysis."
    )

    st.info(
        "Educational laboratory: this module demonstrates "
        "statistical analysis of classical ciphertext."
    )

    ciphertext = st.text_area(
        "Enter Ciphertext",
        placeholder="Example: HIAT",
        height=150
    )

    if st.button("Analyze Ciphertext", use_container_width=True):

        if not ciphertext.strip():

            st.warning("Please enter some ciphertext.")

        else:

            df = analyze_frequency(ciphertext)

            if df is None:

                st.warning(
                    "No English letters found in the input."
                )

            else:

                st.session_state["frequency_data"] = df
                st.session_state["analyzed_text"] = ciphertext

    if "frequency_data" in st.session_state:

        df = st.session_state["frequency_data"]

        st.divider()

        st.subheader("📊 Analysis Summary")

        total_letters = int(df["Count"].sum())

        most_common = df.loc[
            df["Count"].idxmax(), "Letter"
        ]

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Letters", total_letters)

        col2.metric("Most Frequent Letter", most_common)

        col3.metric(
            "Unique Letters",
            int((df["Count"] > 0).sum())
        )

        st.divider()

        # Frequency table
        st.subheader("1. Letter Frequency Table")

        st.dataframe(
            df.sort_values(
                by="Count",
                ascending=False
            ),
            use_container_width=True,
            hide_index=True
        )

        # Distribution graph
        st.divider()

        st.subheader("2. Letter Distribution Graph")

        fig, ax = plt.subplots(figsize=(12, 5))

        ax.bar(
            df["Letter"],
            df["Frequency (%)"]
        )

        ax.set_xlabel("Letters")
        ax.set_ylabel("Frequency (%)")
        ax.set_title("Ciphertext Letter Distribution")

        ax.grid(axis="y", alpha=0.3)

        st.pyplot(fig)
        plt.close(fig)

        # English comparison
        st.divider()

        st.subheader("3. English Frequency Comparison")

        fig2, ax2 = plt.subplots(figsize=(12, 5))

        ax2.plot(
            df["Letter"],
            df["Frequency (%)"],
            marker="o",
            label="Ciphertext"
        )

        ax2.plot(
            df["Letter"],
            df["English Frequency (%)"],
            marker="x",
            label="Typical English"
        )

        ax2.set_xlabel("Letters")
        ax2.set_ylabel("Frequency (%)")
        ax2.set_title("Ciphertext vs English Letter Frequency")

        ax2.legend()
        ax2.grid(alpha=0.3)

        st.pyplot(fig2)
        plt.close(fig2)

        # Educational explanation
        st.divider()

        st.subheader("4. Understanding the Results")

        st.write(
            f"The most frequent letter in your ciphertext "
            f"is **{most_common}**."
        )

        st.write(
            "Frequency analysis studies how often letters "
            "appear in a message."
        )

        st.write(
            "In ordinary English text, E, T, A, O and I "
            "are among the commonly occurring letters."
        )

        st.warning(
            "Important: Frequency analysis can reveal statistical "
            "patterns, but it does not guarantee recovery of a "
            "Hill Cipher key. Results depend on the cipher, "
            "message length and available information."
        )

    st.divider()

    with st.expander("📘 What is Cryptanalysis?"):

        st.write(
            "Cryptanalysis is the study of analyzing encrypted "
            "messages to understand their patterns and weaknesses."
        )

        st.write(
            "**Frequency Analysis:** Examines how often each "
            "letter appears in ciphertext."
        )

        st.write(
            "**Letter Distribution:** Displays letter counts "
            "and percentages in a graph."
        )

        st.write(
            "**English Comparison:** Compares ciphertext "
            "frequencies with typical English letter frequencies."
        )
