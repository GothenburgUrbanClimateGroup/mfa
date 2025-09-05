import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
from matplotlib.path import Path
import seaborn as sns
import io
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Used to save matplotlib figures with download buttons
def fig_to_bytes(fig, fmt="png"):
    buf = io.BytesIO()
    # High DPI for crisp PNGs; ignored for vector formats
    dpi = 300 if fmt in ("png", "jpg", "jpeg") else None
    fig.savefig(buf, format=fmt, bbox_inches="tight", dpi=dpi)
    buf.seek(0)
    return buf

# Optional: map format to MIME type for nicer downloads
MIME = {"png": "image/png", "svg": "image/svg+xml", "pdf": "application/pdf"}

# Function to change the weighting in the matrix
def function_weighting(df_mfa, df_weights):
    #
    df_w = np.ones((df_weights.shape[0], 1))
    df_w[:,0] = df_weights['Weights'].copy().to_numpy()
    
    # Potential and weights for water management and treatment
    df_water = df_mfa.iloc[0:2].copy()
    df_weight_water = df_w[0:2].copy()

    # Potential and weights for heat stress reduction
    # Outdoors
    df_heat_out = df_mfa.iloc[2:4].copy()
    df_weight_heat_out = df_w[2:4].copy()

    # Indoors
    df_heat_in = df_mfa.iloc[4].copy()
    df_weight_heat_in = df_w[4].copy()

    # Weights for heat stress reduction
    df_weight_heat_sum = (df_weight_heat_out.mean() + df_weight_heat_in)
    df_weight_heat_mean = (df_weight_heat_out.mean() + df_weight_heat_in)/2
  
    # Potential and weights for recreation
    df_rec = df_mfa.iloc[5:8].copy()
    df_weight_rec = df_w[5:8].copy()

    # Sum mean weights
    sum_mean_weights = (df_weight_water.mean() + df_weight_heat_mean.mean() + df_weight_rec.mean()).mean()
    
    # Weighted values for water, heat and recreation
    weighted_water = ((df_water * df_weight_water).sum() / df_weight_water.sum()) * (df_weight_water.mean()/sum_mean_weights)
    weighted_heat = (((df_heat_out * df_weight_heat_out).sum() / (df_weight_heat_out > 0).sum() + (df_heat_in * df_weight_heat_in)) / df_weight_heat_sum) * (df_weight_heat_mean/sum_mean_weights)
    weighted_rec = ((df_rec * df_weight_rec).sum() / df_weight_rec.sum()) * (df_weight_rec.mean()/sum_mean_weights)
    
    # Replace nan with zero if function is removed, i.e. weights are set to zero.
    weighted_water[weighted_water.isna()] = 0
    weighted_heat[weighted_heat.isna()] = 0
    weighted_rec[weighted_rec.isna()] = 0
    # Multifuntionality potential
    weighted_mfa = (weighted_water + weighted_heat + weighted_rec).round(1)

    # Construction and weights
    df_constr = df_mfa.iloc[9].copy()
    df_weight_constr = df_w[8].copy()

    # Maintenance and weights
    df_main = df_mfa.iloc[10].copy()
    df_weight_main = df_w[9].copy()
    
    # Weighted costs
    weighted_costs = (df_constr * df_weight_constr + df_main * df_weight_main)/(df_weight_constr + df_weight_main)

    return weighted_mfa, weighted_costs

# mfa tab
def mfa_tool():
    # Read excel file to plot in heatmap, scatter, etc.
    mfa = pd.read_excel('MFA.xlsx')
    mfa_copy = mfa.copy()
    mfa_columns = mfa.iloc[1, 5:].to_numpy().astype(str)
    mfa = mfa.iloc[3:, 5:]
    mfa.columns = mfa_columns

    mfa_functions = mfa_copy.iloc[3:, 1].astype(str)
    for i in np.arange(mfa_functions.shape[0]):
        #print(mfa_functions.iloc[i])
        if mfa_functions.iloc[i] == 'nan':
            mfa_functions.iloc[i] = ''
        elif mfa_functions.iloc[i] == 'Outdoor nighttime':
            mfa_functions.iloc[i] = 'Outdoor daytime'
        elif mfa_functions.iloc[i-1] == 'Outdoor daytime':
            mfa_functions.iloc[i] = 'Outdoor nighttime'

    mfa_functions.iloc[2] = 'Outdoor heat reduction (D)'
    mfa_functions.iloc[3] = 'Outdoor heat reduction (N)'
    mfa_functions.iloc[4] = 'Indoor heat reduction'
    mfa_functions.iloc[8] = 'Multifunctionality potential'
    mfa_functions.iloc[9] = 'Construction costs'
    mfa_functions.iloc[10] = 'Maintenance costs'
    mfa_functions.iloc[11] = 'Total costs'

    mfa.set_index(mfa_functions, inplace=True)
    mfa.index = mfa.index.str.lstrip()
    mfa.index.name = None

    mfa = mfa.astype(float)
    mfa = mfa.round(1)

    # Weights dataframe
    df_row_names = np.array(['Runoff volume management', 
                            'Runoff pollution reduction',
                            'Outdoor heat reduction (D)',
                            'Outdoor heat reduction (N)',
                            'Indoor heat reduction',
                            'Aesthetics',
                            'Use (passive)',
                            'Use (active)',
                            'Construction',
                            'Maintenance'])
    df_weights = pd.DataFrame(df_row_names, columns=['Function'])
    df_weights['Weights'] = np.ones((df_row_names.shape[0]))

    # Create two columns to show weights dataframe and mfa table
    col1, col2, col3 = st.columns([.2, .45, .35], gap="small")
    container_height = 550

    with col1:
        with st.container(height=container_height, border=True):
            set_row_height = 42

            # Configure grid options
            gb = GridOptionsBuilder.from_dataframe(df_weights)
            gb.configure_column("Function", editable=False)
            # gb.configure_column("Weights", editable=True, type=["numericColumn"])
            # Configure Weights column (integers only, left aligned)
            gb.configure_column(
                "Weights", 
                editable=True, 
                type=["numericColumn"],
                precision=0,  # No decimal places (integers only)
                cellEditor='agNumberCellEditor',
                cellEditorParams={
                    'min': 0,
                    'max': 10,
                    'precision': 0,  # This ensures integers only
                    'step': 1,        # Step by 1 (whole numbers)
                    #'showStepperButtons': True
                },
                valueFormatter="value",  # Display as-is (no formatting)
                cellStyle={'textAlign': 'left'},  # Left align the values
                headerClass='left-align-header'   # Left align the header
            )

            # Apply custom CSS to all cells
            gb.configure_default_column(
                cellStyle={'fontSize': '12px'}  # Default font size for all cells
            )

            # Set font size and other styling
            gb.configure_grid_options(
                domLayout='normal',
                suppressRowClickSelection=True,
                rowHeight=set_row_height  # your variable
            )

            gridOptions = gb.build()

            # Display the grid
            grid_response = AgGrid(
                df_weights,
                gridOptions=gridOptions,
                update_mode=GridUpdateMode.VALUE_CHANGED,
                height=len(df_weights) * set_row_height + 50,
                allow_unsafe_jscode=True,
                theme='streamlit'
            )

            # Get the updated dataframe
            df_weights = grid_response['data']

    #############################################
    ### HEATMAP ###
    # Heatmap plot
    # Update mfa
    updated_mfp, updated_costs = function_weighting(mfa.copy(), df_weights.copy())
    mfa.iloc[8] = updated_mfp
    mfa.iloc[11] = updated_costs

    # Heat map
    heatmap = plt.figure(figsize = (20, 10))
    ax = heatmap.add_subplot(111)

    sns.heatmap(mfa, ax=ax, square=True, annot=True, cmap="Greens", cbar=False, linewidth=.5, annot_kws={"fontsize": 20})
    ax.xaxis.tick_top()
    ax.tick_params(axis='x', labelrotation=90)
    ax.tick_params(axis='both', which='major', labelsize=20)

    # Set Multifunctionality potential label to bold
    ax.get_yticklabels()[8].set_weight("bold")
    # Set Total costs label to bold
    ax.get_yticklabels()[11].set_weight("bold")

    # Mark Multifunctionality potential in heat map (box)
    wanted_index = 8
    x, y, w, h = 0, wanted_index, mfa.shape[1], 1
    ax.add_patch(Rectangle((x, y), w, h, fill=False, edgecolor='b', lw=4, clip_on=False))

    # Mark Total costs in heat map (box)
    wanted_index = 11
    x, y, w, h = 0, wanted_index, mfa.shape[1], 1
    ax.add_patch(Rectangle((x, y), w, h, fill=False, edgecolor='b', lw=4, clip_on=False))

    #############################################
    ### SCATTER PLOT ###
    # Scatter plot
    mfa_scatter = mfa.iloc[[8, 11]].transpose().reset_index()
    mfa_scatter.columns = ['Element', 'Multifunctionality potential', 'Maintenance and construction costs']

    mfa_scatter['Maintenance and construction costs'] = np.abs(mfa_scatter['Maintenance and construction costs'].to_numpy() - 5) + 1

    # Bottom left patch
    verts1 = [
    (0., 0.), (0., 3.), (3., 3.), (3., 0.), (0., 0.),
    ]

    # Upper left patch
    verts2 = [
    (0., 3.), (0., 6.), (3., 6.), (3., 3.), (0., 0.),
    ]

    # Upper right patch
    verts3 = [
    (3., 3.), (3., 6.), (6., 6.), (6., 3.), (0., 0.),
    ]

    # Bottom right patch
    verts4 = [
    (3., 0.), (3., 3.), (6., 3.), (6., 0.), (0., 0.),
    ]

    codes = [
        Path.MOVETO,
        Path.LINETO,
        Path.LINETO,
        Path.LINETO,
        Path.CLOSEPOLY,
    ]

    path1 = Path(verts1, codes)
    path2 = Path(verts2, codes)
    path3 = Path(verts3, codes)
    path4 = Path(verts4, codes)

    scatter, ax1 = plt.subplots(figsize=(10, 10))

    # Generate the "Greens" palette with 5 colors
    greens_palette = sns.color_palette("Greens", 5)

    # Extract the RGB values at positions 2, 3, 4, and 5 (index starts from 0)
    patch1 = patches.PathPatch(path1, facecolor=greens_palette[1], edgecolor=None, linestyle='')
    ax1.add_patch(patch1)
    patch2 = patches.PathPatch(path2, facecolor=greens_palette[4], edgecolor=None, linestyle='')
    ax1.add_patch(patch2)
    patch3 = patches.PathPatch(path3, facecolor=greens_palette[3], edgecolor=None, linestyle='')
    ax1.add_patch(patch3)
    patch4 = patches.PathPatch(path4, facecolor=greens_palette[2], edgecolor=None, linestyle='')
    ax1.add_patch(patch4)
    splot = sns.scatterplot(data=mfa_scatter, y='Multifunctionality potential', x='Maintenance and construction costs', ax=ax1, c='k')

    def label_point(x, y, val, ax):
        a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
        for i, point in a.iterrows():
            ax.text(point['x']+.02, point['y'], str(point['val']), fontsize=14)
        
    label_point(mfa_scatter['Maintenance and construction costs'], mfa_scatter['Multifunctionality potential'], mfa_scatter['Element'].astype(str), ax1)

    ax1.set_xlim(0.9, 5.1)
    ax1.set_ylim(0.9, 5.1)
    ax1.set_xticks(np.array([1, 5]), labels=['Lowest', 'Highest'])
    ax1.set_yticks(np.array([1, 5]), labels=['Lowest', 'Highest'])

    ax1.tick_params(axis='both', which='major', labelsize=20)

    ax1.set_ylabel('Multifunctionality potential', fontsize=20) # , fontweight='bold'
    # ax1.set_xlabel('Maintenance and construction costs ', fontsize=20) # , fontweight='bold'
    ax1.set_xlabel('Costs ', fontsize=20) # , fontweight='bold'

    with col2:
        with st.container(height=container_height, border=True):    
            st.pyplot(heatmap, bbox_inches='tight', pad_inches=0, use_container_width=True)

            _, bcol = st.columns([3, 1])
            with bcol:

                # Download button heatmap
                st.download_button(
                    f"Download heatmap",
                    data=fig_to_bytes(heatmap, 'png'),
                    file_name=f"heatmap.png",
                    mime=MIME['png'],
                    on_click="ignore",
                    use_container_width=True,
                )            

                # Download button scatter
                st.download_button(
                    f"Download scatter",
                    data=fig_to_bytes(scatter, 'png'),
                    file_name=f"scatter.png",
                    mime=MIME['png'],
                    on_click="ignore",
                    use_container_width=True,
                )

    # Show in streamlit
    with col3:
        with st.container(height=container_height, border=True):   
            st.pyplot(scatter, bbox_inches='tight')