import time
from datetime import datetime

import requests
import streamlit as st

# ---- Page config ----
st.set_page_config(page_title="📖 VerseQuest", layout="wide")

# ---- Bible chapters ----
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


def calculate_score(user_answers, correct_answers):
    return sum(u == c for u, c in zip(user_answers, correct_answers))


def get_feedback(score_percent):
    if score_percent == 100:
        return "🌟 Perfect score! You're a Bible Master!"
    elif score_percent >= 80:
        return "💪 Great job! Keep it up!"
    elif score_percent >= 60:
        return "🙂 Good try! A little more study will help."
    else:
        return "📘 Keep practicing! You’re growing."


# ---- SIDEBAR ----
st.sidebar.title("📚 Bible Chapter Picker")
selected_book = st.sidebar.selectbox("Choose a book:", list(bible_chapters.keys()))
st.sidebar.markdown("### Choose a Chapter:")

# Store selected chapter in session state
if "selected_chapter" not in st.session_state:
    st.session_state.selected_chapter = 1

cols = st.sidebar.columns(3)
for i in range(bible_chapters[selected_book]):
    col = cols[i % 3]
    if col.button(str(i + 1), key=f"chap_{i+1}"):
        st.session_state.selected_chapter = i + 1

if st.sidebar.button("🚀 Start Quiz"):
    selected_chapter = st.session_state.selected_chapter
    selected_passage = f"{selected_book} {selected_chapter}"

    # Show a loading button and spinner
    with st.spinner("Fetching your quiz question..."):
        response = requests.get(
            f"https://versequest.onrender.com/get-question?chapter={selected_passage}"
        )

    # Handle the response after fetching data
    if response.status_code == 200:
        if (
            "content" in response.json()
            and "question_text" in response.json()["content"]
        ):
            st.session_state.result = response.json()["content"]
            st.session_state.current_question_idx = 0
            st.session_state.user_answers = []
            st.session_state.chapter = selected_passage
            st.session_state.timer_start = time.time()
            st.rerun()
        else:
            st.sidebar.error("❌ Malformed or incomplete data. Try again.")
    else:
        st.sidebar.error("❌ Something went wrong. Please try again.")


# ---- MAIN SECTION ----
st.title("🎯 VerseQuest")

# If there are results, start displaying the quiz
if "result" in st.session_state and st.session_state.current_question_idx < len(
    st.session_state.result["question_text"]
):
    idx = st.session_state.current_question_idx
    total = len(st.session_state.result["question_text"])
    st.session_state.total = total
    question = st.session_state.result["question_text"][idx]
    options = st.session_state.result["options"][idx]

    st.markdown(
        f"### 📖 {st.session_state.chapter} &nbsp;|&nbsp; Question {idx + 1}/{total}"
    )
    st.progress((idx + 1) / total)
    st.write(f"**Q{idx + 1}.** {question}")
    answer = st.radio("Select an answer:", options, index=None, key=f"q_{idx}")

    if st.button("Next ➡️"):
        if answer is None:
            st.warning("⛔ Choose an answer or wait for timeout.")
        else:
            st.session_state.user_answers.append(answer)
            st.session_state.current_question_idx += 1
            st.rerun()

elif "result" in st.session_state and st.session_state.current_question_idx == len(
    st.session_state.result["question_text"]
):
    correct = st.session_state.result["correct_answer"]
    user = st.session_state.user_answers
    score = calculate_score(user, correct)
    percent = round(score / int(st.session_state.total) * 100)

    # Save past scores
    if "quiz_completed" not in st.session_state:
        if "history" not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append(
            {
                "chapter": st.session_state.chapter,
                "score": f"{score}/{st.session_state.total}",
                "percent": f"{percent}%",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
        )
    st.session_state.quiz_completed = True

    st.balloons()
    st.markdown("## ✅ Quiz Completed!")
    st.metric("Your Score", f"{score}/{st.session_state.total}")
    st.metric("Percentage", f"{percent}%")
    st.info(get_feedback(percent))

    with st.expander("📋 Review Your Answers", expanded=True):
        for i in range(int(st.session_state.total)):
            q = st.session_state.result["question_text"][i]
            a = st.session_state.result["correct_answer"][i]
            u = st.session_state.user_answers[i]
            opts = st.session_state.result["options"][i]

            st.markdown(f"**Q{i+1}.** {q}")
            for opt in opts:
                if opt == a:
                    st.success(f"✔️ {opt}")
                elif opt == u:
                    st.error(f"❌ {opt}")
                else:
                    st.write(opt)
            st.markdown("---")

    if st.button("🔁 Try Another Chapter"):
        for key in list(st.session_state.keys()):
            if key not in ["history"]:
                del st.session_state[key]
        st.rerun()

elif "history" in st.session_state and len(st.session_state.history) > 0:
    st.markdown("### 📜 Past Quizzes")
    for record in reversed(st.session_state.history):
        st.markdown(
            f"**{record['chapter']}** — {record['score']} ({record['percent']}) &nbsp;&nbsp; _{record['time']}_"
        )

else:
    st.markdown("👉 Use the sidebar to pick a chapter and start the quiz.")
