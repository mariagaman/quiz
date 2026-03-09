import streamlit as st
import time

st.set_page_config(
    page_title="Quiz SQL Databases",
    page_icon="🧠",
    layout="centered"
)

QUESTIONS = [
    {
        "question": "1. Care este ordinea corectă a principalelor clauze într-un query SQL?",
        "options": [
            "SELECT → FROM → WHERE → GROUP BY → ORDER BY",
            "FROM → SELECT → WHERE → ORDER BY → GROUP BY",
            "SELECT → WHERE → FROM → GROUP BY → ORDER BY",
            "FROM → WHERE → SELECT → GROUP BY → ORDER BY"
        ],
        "answer": "SELECT → FROM → WHERE → GROUP BY → ORDER BY"
    },
    {
        "question": "2. Ce clauză SQL este folosită pentru a filtra rânduri înainte de agregare?",
        "options": [
            "GROUP BY",
            "WHERE",
            "HAVING",
            "ORDER BY"
        ],
        "answer": "WHERE"
    },
    {
        "question": "3. Ce tip de JOIN returnează doar rândurile care există în ambele tabele?",
        "options": [
            "LEFT JOIN",
            "RIGHT JOIN",
            "INNER JOIN",
            "FULL JOIN"
        ],
        "answer": "INNER JOIN"
    },
    {
        "question": "4. Ce constrângere este folosită pentru a lega două tabele?",
        "options": [
            "CHECK",
            "UNIQUE",
            "FOREIGN KEY",
            "NOT NULL"
        ],
        "answer": "FOREIGN KEY"
    },
    {
        "question": "5. Care comandă SQL face parte din categoria DML?",
        "options": [
            "CREATE",
            "INSERT",
            "ALTER",
            "DROP"
        ],
        "answer": "INSERT"
    },
    {
        "question": "6. Ce extensie a SQL este specifică pentru Microsoft SQL Server?",
        "options": [
            "PL/SQL",
            "T-SQL",
            "SQL+",
            "MySQL Script"
        ],
        "answer": "T-SQL"
    },
    {
        "question": "7. Care este diferența principală dintre WHERE și HAVING?",
        "options": [
            "WHERE filtrează rânduri înainte de agregare, HAVING după agregare",
            "HAVING filtrează rânduri înainte de agregare",
            "WHERE este folosit doar cu JOIN",
            "Nu există diferență"
        ],
        "answer": "WHERE filtrează rânduri înainte de agregare, HAVING după agregare"
    },
    {
        "question": "8. În T-SQL, ce comandă este folosită pentru a crea o procedură stocată?",
        "options": [
            "CREATE FUNCTION",
            "CREATE PROCEDURE",
            "CREATE SCRIPT",
            "CREATE METHOD"
        ],
        "answer": "CREATE PROCEDURE"
    },
    {
        "question": "9. Ce se întâmplă dacă execuți INNER JOIN între două tabele fără valori comune?",
        "options": [
            "Se returnează toate rândurile",
            "Se returnează rânduri cu NULL",
            "Nu se returnează niciun rând",
            "Se creează automat un nou tabel"
        ],
        "answer": "Nu se returnează niciun rând"
    },
    {
        "question": "10. În T-SQL, ce comandă este folosită pentru a anula modificările dintr-o tranzacție?",
        "options": [
            "COMMIT",
            "ROLLBACK",
            "CANCEL",
            "UNDO"
        ],
        "answer": "ROLLBACK"
    }
]

QUIZ_DURATION_SECONDS = 5 * 60


def init_state():
    defaults = {
        "quiz_started": False,
        "start_time": None,
        "submitted": False,
        "score": 0,
        "time_up": False
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def calculate_score():
    score = 0
    for i, q in enumerate(QUESTIONS):
        user_answer = st.session_state.get(f"q_{i}")
        if user_answer == q["answer"]:
            score += 1

    st.session_state.score = score
    st.session_state.submitted = True


init_state()

st.title("🧠 Quiz: SQL Databases")
st.write("Testează-ți cunoștințele despre bazele de date SQL.")

if not st.session_state.quiz_started:

    st.info("Ai 10 întrebări și 5 minute.")

    if st.button("▶️ Start quiz", use_container_width=True):
        st.session_state.quiz_started = True
        st.session_state.start_time = time.time()
        st.rerun()

else:

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(QUIZ_DURATION_SECONDS - elapsed, 0)

    minutes = remaining // 60
    seconds = remaining % 60

    st.markdown(
        f"<h1 style='text-align:center;color:red;'>⏳ {minutes:02d}:{seconds:02d}</h1>",
        unsafe_allow_html=True
    )

    progress = min(elapsed / QUIZ_DURATION_SECONDS, 1.0)
    st.progress(progress)

    if remaining == 0 and not st.session_state.submitted:
        st.session_state.time_up = True
        calculate_score()
        st.rerun()

    if not st.session_state.submitted:

        st.divider()

        for i, q in enumerate(QUESTIONS):
            st.radio(
                q["question"],
                q["options"],
                key=f"q_{i}",
                index=None
            )
            st.write("")

        if st.button("✅ Trimite răspunsurile", use_container_width=True):
            calculate_score()
            st.rerun()

    else:

        st.divider()

        if st.session_state.time_up:
            st.warning("⏰ Timpul a expirat!")

        score = st.session_state.score
        total = len(QUESTIONS)

        st.success(f"Scor final: {score}/{total}")

        st.subheader("Răspunsuri corecte")

        for i, q in enumerate(QUESTIONS):
            user_answer = st.session_state.get(f"q_{i}", "Fără răspuns")
            correct_answer = q["answer"]

            st.markdown(f"**{q['question']}**")

            if user_answer == correct_answer:
                st.markdown(f"✅ {user_answer}")
            else:
                st.markdown(f"❌ {user_answer}")
                st.markdown(f"Corect: {correct_answer}")

            st.write("")

    # timer live
    if st.session_state.quiz_started and not st.session_state.submitted:
        time.sleep(1)
        st.rerun()