import streamlit as st


def flash(kind, message):
    """Save a message so it still shows after st.rerun()."""
    st.session_state.flash = (kind, message)


def show_flash():
    if "flash" in st.session_state:
        kind, message = st.session_state.pop("flash")
        getattr(st, kind)(message)


def section_label(row):
    """Readable label for a section in a dropdown."""
    return (f"#{row['SectionID']} · {row['CourseCode']} {row['CourseTitle']} · "
            f"{row['Day']} {row['StartTime']}–{row['EndTime']} · {row['Professor']}")
