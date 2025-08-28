import streamlit as st

def st_justify(text: str, spacing: float = 1.5, align: str = "justify"):
    """
    Display text in Streamlit with custom line spacing and alignment.
    """
    st.markdown(
        f"""
        <div style="text-align: {align}; line-height: {spacing};">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )
