# utils/styling.py
import streamlit as st

def inject_mobile_css():
    """
    Injects CSS font scaling tweaks only for mobile devices.
    """
    st.markdown("""
        <style>
        @media only screen and (max-width: 768px) {

            h1 { font-size: 1.7rem !important; }
            h2 { font-size: 1.5rem !important; }
            h3 { font-size: 1.4rem !important; }

            table td, table th {
                font-size: 1rem !important;
            }

            /* Style the label in st.metric() */
            div[data-testid="metric-container"] > div:first-child {
                font-size: 1rem !important;
                font-weight: 700;
            }
        }
        </style>
    """, unsafe_allow_html=True)


def is_mobile() -> bool:
    """
    Checks the user agent to guess if the user is on mobile.
    Only works in deployed mode (Streamlit sharing, etc).
    """
    try:
        user_agent = st.session_state.get("_user_agent")
        if not user_agent:
            user_agent = st.query_params.get("_user_agent", [""])[0]
            st.session_state["_user_agent"] = user_agent
        return any(mobile in user_agent.lower() for mobile in ["iphone", "android", "mobile"])
    except:
        return False