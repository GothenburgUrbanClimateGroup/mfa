import streamlit as st

from utils import st_justify

def about_matrix():

    # Title set using markdown
    st.markdown("<h1 style='text-align: center; color: black; font-size: 30px; '>About the multifuntionality potential and cost matrix</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        about_text = """

        For detailed description of the matrix, functions, costs, BGI elements and assessment see [Thorsson et al. (2025)](https://doi.org/10.1016/j.cities.2025.106239). 
        In the supplmentary to the scientific paper you can also find an editable Excel file of the matrix if you want to use it locally on your computer.

        The Multifunctional Potential and Cost Matrix provides an integrated assessment of the benefits and costs of urban blue-green 
        infrastructure (BGI) elements. Firstly, the potential to provide three functions: urban stormwater management, heat stress reduction 
        and recreation, is assessed based on scientific evidence. Secondly, the combined performance across these three functions, i.e. 
        the **multifunctionality potential**, is related to costs of initial construction and long-term maintenance to support planning decisions.

        Each function is divided into sub-functions:

        - Urban stormwater management: runoff volume management and pollution reduction.

        - Heat stress reduction: outdoor cooling (daytime and nighttime) and indoor cooling.

        - Recreation: active use, passive use, and aesthetic appeal.

        Initial construction costs include expenses for purchasing, building and establishing the BGI element, but do not cover land preparation 
        before construction, such as clearing the land of any disturbances. Maintenance costs include ongoing long-term management, such as pruning, 
        hedge maintenance, lawn mowing and leaf collection. For calculating maintenance costs, it is assumed that the construction work and the 
        establishment of the BGI element habe been implemented well.

        The matrix includes twenty common BGI elements: green wall, green roof, rain garden, rain barrel, lawn, meadow, flowerbed, shrub, single tree, 
        grove of trees, street tree, road verge, permeable pavement, ditch, swale, small green area, large park, urban forest, water course and pond. 
        Some of the elements are further divided into low and high vegetation, small and large, and dry and wet. Although rain barrels and permeable 
        pavements are not strictly blue or green by definition, they are included as they are widely recognized as blue-green solutions within the 
        broader context of sustainable drainage systems.

        The potential of each element to provide different (sub)functions is assessed on a linear nominal scale from 1 (lowest potential) to 5 
        (highest potential). These values represent the potential per unit area, accounting for differences in:

        - Element characteristics (e.g., species, diversity, morphology, and vitality),

        - Growing conditions (e.g., access to water, nutrition, and light), and

        - Size (e.g., a single tree vs a large park).

        Similarly, construction costs and long-term maintenance costs are assessed per unit area on a linear nominal scale from 1 (highest cost) 
        to 5 (lowest cost). The matrix also allows users to apply weighting to each function and cost, as their relative importance is context dependent.

        The matrix is designed to support well-informed, integrated decision-making and to raise awareness of the functions and costs associated 
        with different BGI elements. It provides practical guidance for selecting the most favourable BGI element(s), whether for single or multiple 
        functions, by relating performance to costs in the context of site-specific conditions and needs.

        The assessment of (sub)functions and costs has been developed in a Swedish context, but it is considered applicable in most geographical and 
        climate regions. Nevertheless, users are

        encouraged to reassess the scores to reflect local conditions and to examine potential synergies and trade-offs. For more detailed and 
        site-specific assessment of costs and (sub)functions, the use of monetary cost models and biogeophysical models is recommended.        

        """

        st_justify(about_text, spacing=2., align="justify")