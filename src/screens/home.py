# src/screens/home.py
from __future__ import annotations

import streamlit as st
import nav


def render() -> None:
    st.markdown(
        """
        <style>
        /* Home-only layout: we center the entire "stage" in a middle column */
        .home-wrap{
            display:flex;
            flex-direction:column;
            align-items:center;
            justify-content:center;
            text-align:center;
            padding: 28px 0 10px 0;
        }

        .home-title{
            font-size: 3.1rem;
            font-weight: 900;
            letter-spacing: 0.6px;
            line-height: 1.05;
            margin: 0;
        }

        .home-sub{
            margin-top: 10px;
            margin-bottom: 26px;
            font-size: 1.05rem;
            color: rgba(233,233,233,0.72);
        }

        .home-divider{
            width: 520px;
            max-width: 92vw;
            height: 1px;
            background: rgba(245,166,35,0.22);
            margin: 14px 0 26px 0;
        }

        /* Big primary button */
        .btn-primary .stButton > button{
            min-width: 520px !important;
            max-width: 92vw !important;
            border-radius: 999px !important;
            padding: 1.05rem 1.2rem !important;
            font-weight: 900 !important;
        }

        /* Secondary buttons: match the "cardy" feel + consistent height */
        .btn-secondary .stButton > button{
            border-radius: 999px !important;
            padding: 1.0rem 1.1rem !important;
            font-weight: 900 !important;
        }

        .home-footer{
            margin-top: 30px;
            width: 520px;
            max-width: 92vw;
            opacity: .62;
            font-size: .9rem;
            text-align:center;
            margin-left: auto;
            margin-right: auto;
        }

        @keyframes homeFadeUp {
            from { opacity: 0; transform: translateY(6px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        .home-anim{
            animation: homeFadeUp 260ms ease-out;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Hard-center the entire page content so it never "looks" offset.
    # Middle column is the stage; side columns are spacers.
    left, mid, right = st.columns([1, 3, 1], gap="large")

    with mid:
        st.markdown(
            """
            <div class="home-wrap home-anim">
                <h1 class="home-title">Life Decision Tool</h1>
                <div class="home-sub">Evaluate your options with clarity.</div>
                <div class="home-divider"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="btn-primary home-anim">', unsafe_allow_html=True)
        if st.button("Start Decision", use_container_width=True, key="home_start"):
            nav.set_page(nav.CATEGORY)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("")
        b1, b2 = st.columns([1, 1], gap="large")

        with b1:
            st.markdown('<div class="btn-secondary home-anim">', unsafe_allow_html=True)
            if st.button("View Past Decisions", use_container_width=True, key="home_past"):
                nav.set_page(nav.PAST)
            st.markdown("</div>", unsafe_allow_html=True)

        with b2:
            st.markdown('<div class="btn-secondary home-anim">', unsafe_allow_html=True)
            if st.button("Load Saved Decision", use_container_width=True, key="home_load"):
                nav.set_page(nav.LOAD)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="home-footer home-anim">
                v0.1 — human on the surface, structured underneath.
            </div>
            """,
            unsafe_allow_html=True,
        )
