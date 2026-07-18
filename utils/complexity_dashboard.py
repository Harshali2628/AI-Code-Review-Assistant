import streamlit as st


def display_complexity_dashboard(grade):

    if grade is None:
        return

    if grade == "A":
        st.success("🟢 Excellent Maintainability")

    elif grade == "B":
        st.info("🟡 Good Maintainability")

    else:
        st.error("🔴 Complex Code")

    st.metric(
        "Complexity Grade",
        grade
    )