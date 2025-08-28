import streamlit as st

from utils import st_justify

def how_to_use():
    
    col1, col2, col3 = st.columns([1,2,1])

    with col2:    

        # Title set using markdown
        st.markdown("<h1 style='text-align: center; color: black; font-size: 30px; '>How to use the multifuntionality potential and cost matrix</h1>", unsafe_allow_html=True)

        how_to_use_text = """
                    
    **Before you start**:

    - Select the area of interest where the assessment will be applied.
    - Identify which functions are relevant and prioritize them based on site-specific needs and prerequisites. 

    **Using the matrix**:

    **Assign weights to the different (sub)functions**:
    - Weight 1: all (sub)functions are equally important,
    - Weight 2, 3, …: a (sub) function is more important than others (2 = twice as important, 3 = three times as important etc.),
    - Weight 0: a (sub)function is not relevant.
    
    **Analyze the results**:
    - Changing the weights will alter the multifunctionality potential and/or total cost.
    - This will indicate which BGI elements are more or less favourable for your site-specific context.
    
    **Experiment**:
    - Try different weight combinations and identify the BGI elements best suited to your needs.
                
                """
        
        st_justify(how_to_use_text, spacing=2., align="justify")