import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title = "Vogels",
    layout='wide'
    )


st.subheader("Parameters:")
col1, col2, col3 = st.columns(3)
Perm = col1.number_input("Permeability (md):")
Height = col1.number_input("Height (ft):")
Bo = col1.number_input("Bo:")
Vis = col2.number_input("Viscosity (cp):")
Re = col2.number_input("Re(ft):")
Rw = col2.number_input("Rw (ft):")
Skin = col3.number_input("Skin:")
Pi = col3.number_input("Initial or Average Pressure (psi):")
Pb = col3.number_input("Bubble Point Pressure (psi) :")
ln = np.log
conversion = 1
j_Pi = 0
q_max = 0
data = []

def productivity_index():
    a = (Perm * Height)
    b = 141.2 * Bo * Vis
    c = ln(Re / Rw) - 0.75 + Skin
    j = round(a / (b * c), 4) 
    return j

def flowrate_qv():
    q_max = round(((j * Pi) / 1.8), 4)
    return q_max

def flowrate_qb():
    q_Pb = round(j * (Pi - Pb), 4)
    return q_Pb

def flowrate_belowBubble():
    for i in range(0, int(Pi), 100):
        a = i / Pi
        b = (1 - 0.2 * a - 0.8 * a**2)  
        c = q_max * b  
        row = {"Pressure": i, "Flowrate": c / conversion}
        data.append(row)

if st.button("Proceed"):
    if Pi <= Pb:
        j = productivity_index()
        q_max = flowrate_qv()
        
        row = {"Pressure": Pi, "Flowrate": 0}
        data.append(row)    
        
        flowrate_belowBubble()
    
        # Sort data in ascending order based on "Pressure"
        data.sort(key=lambda x: x["Pressure"])
    
        data = pd.DataFrame(data)
        st.subheader("Result:")
        st.dataframe(data)
    
        st.write(f'Productivity Index (j): {j} STB/d-psi')
        st.write(f'Absolute Open Flow (qmax) {q_max / conversion} STB/day')
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Flowrate'], y=data['Pressure'], mode='lines+markers', name='Graph'))
        fig.update_layout(
            title='IPR Curve', 
            xaxis_title='Flowrate (STB/day)', 
            yaxis_title='Pressure', 
            height=1000,
            width=1000
                    )
        
        fig.update_xaxes(
            nticks=5,
            minor_ticks='inside',
            minor_showgrid=True,
            showline=True,
            anchor='free',
            rangemode='tozero',
            gridcolor='lightgray',
            gridwidth=2,
            )
    
        st.plotly_chart(fig, use_container_width=False, theme=None)
