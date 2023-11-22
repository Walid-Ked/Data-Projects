import streamlit as st

st.set_page_config(layout="wide")
st.markdown("""
        <style>
                .block-container {
                    padding-top: 2rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
    """, unsafe_allow_html=True)

def metric_box(title = None, number = None, color = None):
    wch_colour_box = (0,204,102)
    wch_colour_font = (0,0,0)
    fontsize = 30
    valign = "left"
    iconname = "fas fa-asterisk"
    sline = title
    number = number

    htmlstr = f"""<p style='background-color: {color}; 
                            color: rgb({wch_colour_font[0]}, 
                                    {wch_colour_font[1]}, 
                                    {wch_colour_font[2]}, 0.75); 
                            font-size: {fontsize}px; 
                            border-radius: 3px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:25px;'>
                            <i class='{iconname} fa-xs'></i> {number}
                            </style><BR><span style='font-size: 25px; margin-left:0px; 
                            margin-top: 0;'>{sline}</style></span></p>"""
    return st.markdown(htmlstr, unsafe_allow_html=True)
