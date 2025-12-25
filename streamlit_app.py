import streamlit as st

from santa import secret_santa_imperative

__version__ = "0.1.0"

st.set_page_config(page_title="Secret Santa (Derangement)", page_icon="🎁", layout="centered")

st.sidebar.markdown(f"**Version:** {__version__}")

st.title("Secret Santa (Derangement)")
st.caption("Add names one-by-one, then generate a no-self-assignment mapping.")


if "names" not in st.session_state:
    st.session_state.names = []
if "assignments" not in st.session_state:
    st.session_state.assignments = None


with st.form("add_name", clear_on_submit=True):
    name = st.text_input("Name", placeholder="e.g. Alice")
    submitted = st.form_submit_button("Add")

if submitted:
    cleaned = name.strip()
    if not cleaned:
        st.error("Please enter a name.")
    else:
        existing_lower = {n.casefold() for n in st.session_state.names}
        if cleaned.casefold() in existing_lower:
            st.warning("That name is already in the list.")
        else:
            st.session_state.names.append(cleaned)
            st.session_state.assignments = None
            st.success(f"Added: {cleaned}")


col1, col2, col3 = st.columns(3)
with col1:
    st.metric("People", len(st.session_state.names))
with col2:
    if st.button("Remove last", disabled=len(st.session_state.names) == 0):
        st.session_state.names.pop()
        st.session_state.assignments = None
with col3:
    if st.button("Clear all", disabled=len(st.session_state.names) == 0):
        st.session_state.names = []
        st.session_state.assignments = None


if st.session_state.names:
    with st.expander("Participants (edit)", expanded=True):
        st.caption("Tip: after editing a cell, press Enter to apply it.")

        current_names = st.session_state.names
        edited_rows = st.data_editor(
            [{"Name": n} for n in current_names],
            key="participants_editor",
            hide_index=True,
            use_container_width=True,
        )

        edited_names = [str(row.get("Name", "")).strip() for row in edited_rows]
        if edited_names != current_names:
            if any(not n for n in edited_names):
                st.error("Names cannot be blank.")
            else:
                lowered = [n.casefold() for n in edited_names]
                if len(set(lowered)) != len(lowered):
                    st.error("Names must be unique (case-insensitive).")
                else:
                    st.session_state.names = edited_names
                    st.session_state.assignments = None


st.divider()

seed = st.text_input(
    "Optional seed (for reproducibility)",
    value="",
    help="Leave blank for a fresh random assignment each time. Use the same seed to reproduce the same result.",
)

can_generate = len(st.session_state.names) >= 2
if st.button("Generate derangement", disabled=not can_generate):
    names = st.session_state.names
    mapping = secret_santa_imperative(len(names), seed=seed or None)
    st.session_state.assignments = {names[g - 1]: names[r - 1] for g, r in mapping.items()}


if not can_generate:
    st.info("Add at least 2 names to generate assignments.")

if st.session_state.assignments:
    st.subheader("Assignments (admin view)")

    rows = [
        {"Giver": giver, "Recipient": recipient}
        for giver, recipient in sorted(st.session_state.assignments.items(), key=lambda kv: kv[0].casefold())
    ]
    st.table(rows)

    st.caption("Copy/paste friendly")
    text = "\n".join(f"{row['Giver']} -> {row['Recipient']}" for row in rows)
    st.code(text, language="text")
