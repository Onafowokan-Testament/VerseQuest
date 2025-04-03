import json

import streamlit as st

# Number of chapters for each book in the Bible
bible_chapters = {
    "Genesis": 50,
    "Exodus": 40,
    "Leviticus": 27,
    "Numbers": 36,
    "Deuteronomy": 34,
    "Joshua": 24,
    "Judges": 21,
    "Ruth": 4,
    "1 Samuel": 31,
    "2 Samuel": 24,
    "1 Kings": 22,
    "2 Kings": 25,
    "1 Chronicles": 29,
    "2 Chronicles": 36,
    "Ezra": 10,
    "Nehemiah": 13,
    "Esther": 10,
    "Job": 42,
    "Psalms": 150,
    "Proverbs": 31,
    "Ecclesiastes": 12,
    "Song of Solomon": 8,
    "Isaiah": 66,
    "Jeremiah": 52,
    "Lamentations": 5,
    "Ezekiel": 48,
    "Daniel": 12,
    "Hosea": 14,
    "Joel": 3,
    "Amos": 9,
    "Obadiah": 1,
    "Jonah": 4,
    "Micah": 7,
    "Nahum": 3,
    "Habakkuk": 3,
    "Zephaniah": 3,
    "Haggai": 2,
    "Zechariah": 14,
    "Malachi": 4,
    "Matthew": 28,
    "Mark": 16,
    "Luke": 24,
    "John": 21,
    "Acts": 28,
    "Romans": 16,
    "1 Corinthians": 16,
    "2 Corinthians": 13,
    "Galatians": 6,
    "Ephesians": 6,
    "Philippians": 4,
    "Colossians": 4,
    "1 Thessalonians": 5,
    "2 Thessalonians": 3,
    "1 Timothy": 6,
    "2 Timothy": 4,
    "Titus": 3,
    "Philemon": 1,
    "Hebrews": 13,
    "James": 5,
    "1 Peter": 5,
    "2 Peter": 3,
    "1 John": 5,
    "2 John": 1,
    "3 John": 1,
    "Jude": 1,
    "Revelation": 22,
}

st.title("📖 Bible Quest")

# Select a Book
selected_book = st.selectbox(
    "Select a Book:", list(bible_chapters.keys()), key="book_select"
)

# If a book is selected, show chapters
if selected_book:
    num_chapters = bible_chapters[selected_book]
    st.subheader("Select a Chapter:")

    num_columns = 10
    chapter_buttons = list(range(1, num_chapters + 1))

    selected_chapter = None

    for i in range(0, len(chapter_buttons), num_columns):
        cols = st.columns(num_columns)

        for j in range(num_columns):
            if i + j < len(chapter_buttons):
                # Add a unique key to each button
                if cols[j].button(
                    str(chapter_buttons[i + j]),
                    key=f"chapter_{selected_book}_{chapter_buttons[i + j]}",
                ):
                    selected_chapter = chapter_buttons[i + j]

    if selected_chapter:
        st.write(f"Bible Chapter  **{selected_book} {selected_chapter}**")

# Start quiz button
if st.button("Start quiz", key="start_quiz"):
    selected_passage = f"{selected_book} {selected_chapter}"
    # response = requests.get(
    #     f"https://versequest.onrender.com/get-question?chapter={selected_passage}"
    # )

    # if response.status_code ==200:
    #     response = selected_passage.json()

    with open("response1.json", mode="r") as f:
        response = json.load(f)

    if "content" in response and "question_text" in response["content"]:
        result = response["content"]
        st.session_state.result = result
        st.session_state.current_question_idx = 0
        st.session_state.user_answers = []
        st.session_state.score = 0

        st.rerun()

    else:
        st.write("Error: Data is eiither maformed or incomplete")

if "result" in st.session_state and st.session_state.current_question_idx < 5:
    st.subheader(f"Question {st.session_state.current_question_idx +1}")
    st.write(
        st.session_state.result["question_text"][st.session_state.current_question_idx]
    )
    answer = st.radio(
        "pick an answer",
        st.session_state.result["options"][st.session_state.current_question_idx],
        index=None,
        key=f"Question_{st.session_state.current_question_idx }",
    )

    if st.button("Next"):
        st.session_state.user_answers.append(answer)
        st.session_state.current_question_idx += 1
        st.rerun()
    if st.session_state.current_question_idx == 5:
        st.rerun()


if "result" in st.session_state and st.session_state.current_question_idx == 5:
    st.subheader("Quiz completed")
    st.write(st.session_state.user_answers)
