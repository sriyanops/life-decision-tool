# src/app.py
from __future__ import annotations

import base64
import importlib
from pathlib import Path

import streamlit as st

import nav
import state

# -----------------------------
# CONFIG
# -----------------------------
APP_TITLE = "Life Decision Tool"
DEDICATION = "Dedicated to Eesha S - Built by Sriyan"  # change anytime

PAGES = [
    ("Home", "screens.home"),
    ("Category", "screens.category"),
    ("Limits", "screens.constraints"),
    ("Options", "screens.options"),
    ("Compare", "screens.compare"),
    ("Past Decisions", "screens.past"),
    ("Load Decision", "screens.load"),
]

# Sidebar display labels (keeps internal page keys unchanged)
NAV_LABELS: dict[str, str] = {
    "Home": "Home",
    "Category": "Category",
    "Limits": "Limits",
    "Options": "Options",
    "Compare": "Compare",
    "Past Decisions": "Past",
    "Load Decision": "Load",
}


# -----------------------------
# THEME / FONT
# -----------------------------
def _load_ttf_as_base64(ttf_path: Path) -> str:
    if not ttf_path.exists():
        raise FileNotFoundError(f"Font file not found: {ttf_path}")
    return base64.b64encode(ttf_path.read_bytes()).decode("utf-8")


def apply_global_theme() -> None:
    root = Path(__file__).resolve().parents[1]  # project root
    font_path = root / "assets" / "THEBOLDFONT-FREEVERSION.ttf"
    font_b64 = _load_ttf_as_base64(font_path)

    st.markdown(
        f"""
<style>
@font-face {{
  font-family: "LifeDecisionFont";
  src: url(data:font/ttf;base64,{font_b64}) format("truetype");
  font-weight: 400;
  font-style: normal;
}}

:root {{
  --bg: #0b0d10;
  --panel: #0f1217;
  --panel2: rgba(15,18,23,.55);
  --text: #e9eef5;
  --muted: rgba(233,238,245,.72);
  --amber: #f2a81d;
  --amber2: #c57f0f;
  --stroke: rgba(242,168,29,.35);
}}

/* Base typography */
html, body, [class*="css"] {{
  font-family: "LifeDecisionFont" !important;
  background: var(--bg) !important;
  color: var(--text) !important;
}}

h1,h2,h3,h4,h5,h6,p,span,div,label,button,input,textarea {{
  font-family: "LifeDecisionFont" !important;
  letter-spacing: .3px;
}}

div.block-container {{
  padding-top: 2.2rem !important;
  padding-bottom: 2.5rem !important;
}}

h1 {{ margin-bottom: .35rem !important; }}
h2 {{ margin-bottom: .35rem !important; }}
h3 {{ margin-bottom: .25rem !important; }}

div[data-testid="stMarkdownContainer"] p {{
  margin-bottom: .35rem !important;
}}

hr {{
  border: none !important;
  height: 1px !important;
  background: rgba(242,168,29,.18) !important;
  margin: .9rem 0 !important;
}}

.small-muted {{
  opacity: .65;
  font-size: .9rem;
}}

/* ✅ Home title centering fix (home.py uses .home-wrap) */
.home-wrap {{
  width: 100% !important;
}}

/* Inputs */
textarea, input {{
  background: rgba(255,255,255,.03) !important;
  border: 1px solid rgba(255,255,255,.10) !important;
  color: var(--text) !important;
  border-radius: 12px !important;
}}
textarea:focus, input:focus {{
  outline: none !important;
  border-color: rgba(242,168,29,.55) !important;
  box-shadow: 0 0 0 2px rgba(242,168,29,.15) !important;
}}

/* Buttons */
.stButton > button {{
  font-family: "LifeDecisionFont" !important;
  background: var(--amber) !important;
  color: #120c02 !important;
  border: 1px solid var(--stroke) !important;
  border-radius: 999px !important;
  padding: .85rem 1.1rem !important;
  box-shadow: 0 0 0 2px rgba(0,0,0,.35) inset, 0 10px 28px rgba(0,0,0,.35);
}}
.stButton > button:hover {{
  background: #ffc24c !important;
  border-color: rgba(255,194,76,.55) !important;
}}
.stButton > button:disabled {{
  opacity: .55 !important;
  cursor: not-allowed !important;
}}

/* Sidebar base */
section[data-testid="stSidebar"] {{
  background: linear-gradient(180deg, #0d1015 0%, #0a0c10 100%) !important;
  border-right: 1px solid rgba(255,255,255,.06);
}}
section[data-testid="stSidebar"] * {{
  font-family: "LifeDecisionFont" !important;
  color: var(--text) !important;
}}

/* Sidebar nav spacing cleanup */
section[data-testid="stSidebar"] div[role="radiogroup"] {{
  gap: 0.20rem !important;
}}
section[data-testid="stSidebar"] div[role="radiogroup"] label {{
  padding: 0.18rem 0.25rem !important;
}}
section[data-testid="stSidebar"] p {{
  margin: 0.12rem 0 !important;
}}

/* ✅ Prevent wrap on radio labels (fixes Past/Load splitting) */
section[data-testid="stSidebar"] div[role="radiogroup"] label {{
  line-height: 1.05 !important;
}}
section[data-testid="stSidebar"] div[role="radiogroup"] label > div {{
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}}

/* Header toggle button -> MENU */
button[kind="headerNoPadding"] {{
  background: rgba(255,255,255,.03) !important;
  border: 1px solid rgba(255,255,255,.10) !important;
  border-radius: 12px !important;
  box-shadow: none !important;
  transition: transform 140ms ease, border-color 140ms ease, background 140ms ease;
}}
button[kind="headerNoPadding"]:hover {{
  border-color: rgba(242,168,29,.45) !important;
  background: rgba(242,168,29,.08) !important;
  transform: translateY(-1px);
}}
button[kind="headerNoPadding"]:active {{
  transform: translateY(0px) scale(0.98);
}}
button[kind="headerNoPadding"] span[data-testid="stIconMaterial"] {{
  color: transparent !important;
  position: relative !important;
  display: inline-block !important;
  width: 3.2rem !important;
  height: 1.2rem !important;
}}
button[kind="headerNoPadding"] span[data-testid="stIconMaterial"]::after {{
  content: "MENU";
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: "LifeDecisionFont" !important;
  font-size: 0.70rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: rgba(231, 231, 231, 0.78) !important;
  opacity: 0.95;
  transform: translateY(0);
  transition: transform 160ms ease, opacity 160ms ease;
}}
button[kind="headerNoPadding"]:hover span[data-testid="stIconMaterial"]::after {{
  opacity: 1;
  transform: translateY(-1px);
}}
</style>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------
# NAV
# -----------------------------
def render_sidebar() -> None:
    page_names = [p[0] for p in PAGES]
    current = nav.get_page()

    # sync BEFORE widget creation
    st.session_state["nav_radio"] = current

    def _on_nav_change() -> None:
        choice = st.session_state.get("nav_radio")
        if choice and choice != st.session_state.get("page"):
            st.session_state.page = choice

    with st.sidebar:
        st.markdown(f"## 🧭 {APP_TITLE}")
        st.markdown("<div class='small-muted'>NAVIGATE</div>", unsafe_allow_html=True)

        st.radio(
            label="Navigation",
            options=page_names,
            key="nav_radio",
            label_visibility="collapsed",
            on_change=_on_nav_change,
            format_func=lambda x: NAV_LABELS.get(x, x),
        )

        st.markdown("---")
        st.markdown(
            f"<div class='small-muted' style='margin-top:6px; font-style: italic;'>{DEDICATION}</div>",
            unsafe_allow_html=True,
        )


# -----------------------------
# PAGE RENDER
# -----------------------------
def render_page(page_name: str) -> None:
    module_name = dict(PAGES)[page_name]
    mod = importlib.import_module(module_name)
    if not hasattr(mod, "render"):
        raise AttributeError(f"Module '{module_name}' must define a render() function.")
    mod.render()


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    state.init_state()
    apply_global_theme()
    render_sidebar()
    render_page(nav.get_page())


if __name__ == "__main__":
    main()
