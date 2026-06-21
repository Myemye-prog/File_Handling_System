"""
File Flex — a vibrant glassmorphic console for file CRUD operations.
Run with:  streamlit run file_flex_app.py
"""

import streamlit as st
from pathlib import Path
from datetime import datetime

# ----------------------------------------------------------------------------
# Config
# ----------------------------------------------------------------------------
VAULT_DIR = Path("vault_files")
VAULT_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="File Flex — file ops console",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

OP_COLORS = {
    "create": ("#34D399", "#10B981"),   # green
    "read":   ("#38BDF8", "#0EA5E9"),   # blue
    "update": ("#FBBF24", "#F59E0B"),   # amber
    "delete": ("#FB7185", "#E11D48"),   # rose
    "browse": ("#C084FC", "#A855F7"),   # violet
}

# ----------------------------------------------------------------------------
# State
# ----------------------------------------------------------------------------
if "log" not in st.session_state:
    st.session_state.log = []

if "nav" not in st.session_state:
    st.session_state.nav = "create"


def log(level: str, message: str):
    st.session_state.log.insert(0, (level, message, datetime.now().strftime("%H:%M:%S")))
    st.session_state.log = st.session_state.log[:30]


def safe_path(name: str) -> Path:
    return VAULT_DIR / Path(name).name


# ----------------------------------------------------------------------------
# Styling
# ----------------------------------------------------------------------------
st.markdown(
    """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

<style>
:root{
  --violet: #8B5CF6;
  --fuchsia: #EC4899;
  --cyan: #22D3EE;
  --green: #34D399;
  --amber: #FBBF24;
  --rose: #FB7185;
  --ink: #0F0B1E;
  --glass: rgba(255,255,255,0.06);
  --glass-border: rgba(255,255,255,0.14);
  --text: #F4F2FF;
  --muted: #B7AFD9;
}

html, body, [class*="css"]{ font-family: 'Inter', sans-serif; }

.stApp{
  background:
    radial-gradient(circle at 8% 12%, rgba(139,92,246,0.45) 0%, transparent 38%),
    radial-gradient(circle at 92% 18%, rgba(236,72,153,0.35) 0%, transparent 40%),
    radial-gradient(circle at 50% 100%, rgba(34,211,238,0.30) 0%, transparent 45%),
    linear-gradient(160deg, #0F0B1E 0%, #1A1030 55%, #150E2A 100%);
  background-attachment: fixed;
  color: var(--text);
}

@keyframes float{
  0%,100%{ transform: translate(0,0) scale(1); }
  50%{ transform: translate(-18px,22px) scale(1.06); }
}
.orb{
  position: fixed; border-radius: 50%; filter: blur(70px); opacity: 0.55; z-index: 0; pointer-events:none;
}
.orb1{ width:380px; height:380px; top:-120px; left:-100px; background: var(--violet); animation: float 14s ease-in-out infinite; }
.orb2{ width:320px; height:320px; bottom:-100px; right:-80px; background: var(--cyan); animation: float 18s ease-in-out infinite reverse; }
.orb3{ width:260px; height:260px; top:40%; right:10%; background: var(--fuchsia); animation: float 16s ease-in-out infinite; }

section[data-testid="stSidebar"]{
  background: rgba(15,11,30,0.65);
  backdrop-filter: blur(18px);
  border-right: 1px solid var(--glass-border);
}

#MainMenu, footer, header[data-testid="stHeader"]{ visibility: hidden; }

/* ---------- glass card ---------- */
.glass{
  background: var(--glass);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  border-radius: 20px;
  padding: 30px 34px;
  margin-bottom: 22px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.35);
  position: relative; z-index: 1;
}

/* ---------- hero ---------- */
.hero-title{
  font-family: 'Sora', sans-serif;
  font-weight: 800;
  font-size: 2.7rem;
  letter-spacing: -0.02em;
  margin: 0;
  background: linear-gradient(95deg, #fff 10%, var(--cyan) 55%, var(--fuchsia) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.hero-sub{
  font-size: 14.5px;
  color: var(--muted);
  margin-top: 8px;
}
.badge-row{ display:flex; gap:8px; margin-top: 16px; flex-wrap: wrap; }
.pill{
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  padding: 5px 11px;
  border-radius: 999px;
  border: 1px solid var(--glass-border);
  color: var(--muted);
  background: rgba(255,255,255,0.04);
}

/* ---------- sidebar nav ---------- */
.nav-path{
  font-family: 'Sora', sans-serif;
  font-size: 11px;
  font-weight: 600;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin: 20px 4px 8px 4px;
}
div[data-testid="stSidebar"] .stButton button{
  width: 100%;
  text-align: left;
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--glass-border);
  color: var(--muted);
  font-family: 'Sora', sans-serif;
  font-weight: 600;
  font-size: 13.5px;
  padding: 11px 14px;
  border-radius: 12px;
  margin-bottom: 6px;
  transition: all 0.18s ease;
}
div[data-testid="stSidebar"] .stButton button:hover{
  background: linear-gradient(95deg, rgba(139,92,246,0.25), rgba(236,72,153,0.25));
  border-color: rgba(255,255,255,0.3);
  color: #fff;
  transform: translateX(3px);
}

/* ---------- op chip ---------- */
.op-label{
  display:inline-flex; align-items:center; gap:8px;
  font-family: 'Sora', sans-serif;
  font-weight: 700;
  font-size: 13px;
  padding: 7px 16px;
  border-radius: 999px;
  margin-bottom: 16px;
}
.op-desc{ color: var(--muted); font-size: 14.5px; margin-bottom: 24px; }

/* ---------- inputs ---------- */
.stTextInput input, .stTextArea textarea{
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid var(--glass-border) !important;
  color: var(--text) !important;
  border-radius: 12px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus{
  border-color: var(--cyan) !important;
  box-shadow: 0 0 0 2px rgba(34,211,238,0.35) !important;
}
.stTextInput label, .stTextArea label, .stRadio label p{
  color: var(--muted) !important;
  font-family: 'Sora', sans-serif !important;
  font-weight: 600 !important;
  font-size: 12.5px !important;
}

.stFormSubmitButton button{
  background: linear-gradient(95deg, var(--violet), var(--fuchsia)) !important;
  color: #fff !important;
  border: none !important;
  font-family: 'Sora', sans-serif !important;
  font-weight: 700 !important;
  border-radius: 12px !important;
  padding: 0.6rem 1.6rem !important;
  box-shadow: 0 6px 20px rgba(236,72,153,0.35);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stFormSubmitButton button:hover{
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 10px 28px rgba(236,72,153,0.5);
}

/* ---------- console log ---------- */
.console{
  font-family: 'JetBrains Mono', monospace;
  font-size: 12.5px;
  background: rgba(0,0,0,0.25);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  padding: 16px 18px;
  max-height: 260px;
  overflow-y: auto;
}
.log-line{ padding: 4px 0; color: var(--muted); }
.log-ok{ color: var(--green); }
.log-err{ color: var(--rose); }
.log-time{ color: #6E6594; margin-right: 8px; }

/* ---------- file chip list ---------- */
.file-chip{
  display:inline-block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11.5px;
  background: rgba(34,211,238,0.1);
  border: 1px solid rgba(34,211,238,0.3);
  color: var(--cyan);
  padding: 5px 11px;
  border-radius: 999px;
  margin: 3px 6px 3px 0;
}

/* ---------- row item (browse) ---------- */
.row-item{
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  padding: 10px 4px;
  border-bottom: 1px solid var(--glass-border);
  display:flex; justify-content:space-between;
}
</style>

<div class="orb orb1"></div>
<div class="orb orb2"></div>
<div class="orb orb3"></div>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Sidebar navigation
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        "<div class='hero-title' style='font-size:1.5rem;'>✨ File Flex</div>"
        "<div class='hero-sub'>your file-ops control deck</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='nav-path'>Operations</div>", unsafe_allow_html=True)
    nav_items = [
        ("create", "✚  Create"),
        ("read", "👁  Read"),
        ("update", "✎  Update"),
        ("delete", "🗑  Delete"),
        ("browse", "🗂  Browse"),
    ]
    for key, label in nav_items:
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.nav = key

    st.markdown("<div class='nav-path'>Vault Contents</div>", unsafe_allow_html=True)
    files = sorted(p.name for p in VAULT_DIR.iterdir() if p.is_file())
    if files:
        st.markdown(
            "".join(f"<span class='file-chip'>{f}</span>" for f in files),
            unsafe_allow_html=True,
        )
    else:
        st.markdown("<span style='color:#6E6594; font-size:12px;'>Vault is empty</span>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.markdown(
    """
<div class="glass">
  <div class="hero-title">File Flex</div>
  <div class="hero-sub">Create, read, update and delete files through one clean, glowing dashboard.</div>
  <div class="badge-row">
    <span class="pill">⚡ instant ops</span>
    <span class="pill">🔒 sandboxed vault</span>
    <span class="pill">🟢 live console</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Operation panel
# ----------------------------------------------------------------------------
nav = st.session_state.nav
c1, c2 = OP_COLORS[nav]
op_style = f"background: linear-gradient(95deg, {c1}, {c2}); color:#10081F;"

st.markdown(f"<div class='glass'>", unsafe_allow_html=True)

labels = {
    "create": ("✚ CREATE", "Make a new file inside the vault. Fails if a file with that name already exists."),
    "read": ("👁 READ", "Open a file and print its contents to the console below."),
    "update": ("✎ UPDATE", "Rename, append to, or overwrite an existing file."),
    "delete": ("🗑 DELETE", "Permanently remove a file from the vault. This cannot be undone."),
    "browse": ("🗂 BROWSE", "Everything currently sitting in the vault."),
}
title, desc = labels[nav]
st.markdown(f"<span class='op-label' style='{op_style}'>{title}</span>", unsafe_allow_html=True)
st.markdown(f"<div class='op-desc'>{desc}</div>", unsafe_allow_html=True)

if nav == "create":
    with st.form("create_form", clear_on_submit=False):
        name = st.text_input("File name", placeholder="notes.txt")
        data = st.text_area("Contents", placeholder="Type what goes inside the file…", height=140)
        submitted = st.form_submit_button("Create file")
    if submitted:
        if not name.strip():
            log("err", "No file name given.")
        else:
            path = safe_path(name)
            if path.exists():
                log("err", f"'{path.name}' already exists.")
            else:
                try:
                    path.write_text(data)
                    log("ok", f"Created '{path.name}' ({len(data)} chars).")
                    st.rerun()
                except Exception as e:
                    log("err", f"Could not create file: {e}")

elif nav == "read":
    with st.form("read_form"):
        name = st.text_input("File name", placeholder="notes.txt")
        submitted = st.form_submit_button("Read file")
    if submitted:
        if not name.strip():
            log("err", "No file name given.")
        else:
            path = safe_path(name)
            if not path.exists():
                log("err", f"'{path.name}' does not exist.")
            else:
                try:
                    content = path.read_text()
                    log("ok", f"Read '{path.name}' ({len(content)} chars).")
                    st.code(content if content else "(empty file)", language=None)
                except Exception as e:
                    log("err", f"Could not read file: {e}")

elif nav == "update":
    name = st.text_input("File name", placeholder="notes.txt", key="upd_name")
    mode = st.radio("Action", ["Rename", "Append", "Overwrite"], horizontal=True)

    if mode == "Rename":
        with st.form("rename_form"):
            new_name = st.text_input("New name", placeholder="renamed.txt")
            submitted = st.form_submit_button("Rename file")
        if submitted:
            path = safe_path(name)
            new_path = safe_path(new_name)
            if not path.exists():
                log("err", f"'{path.name}' does not exist.")
            elif new_path.exists():
                log("err", f"'{new_path.name}' already exists.")
            else:
                try:
                    path.rename(new_path)
                    log("ok", f"Renamed '{path.name}' → '{new_path.name}'.")
                    st.rerun()
                except Exception as e:
                    log("err", f"Could not rename file: {e}")

    elif mode == "Append":
        with st.form("append_form"):
            data = st.text_area("Text to append", height=120)
            submitted = st.form_submit_button("Append")
        if submitted:
            path = safe_path(name)
            if not path.exists():
                log("err", f"'{path.name}' does not exist.")
            else:
                try:
                    with open(path, "a") as f:
                        f.write("\n" + data)
                    log("ok", f"Appended {len(data)} chars to '{path.name}'.")
                except Exception as e:
                    log("err", f"Could not append: {e}")

    else:
        with st.form("overwrite_form"):
            data = st.text_area("New contents", height=120)
            submitted = st.form_submit_button("Overwrite")
        if submitted:
            path = safe_path(name)
            if not path.exists():
                log("err", f"'{path.name}' does not exist.")
            else:
                try:
                    path.write_text(data)
                    log("ok", f"Overwrote '{path.name}' ({len(data)} chars).")
                except Exception as e:
                    log("err", f"Could not overwrite: {e}")

elif nav == "delete":
    with st.form("delete_form"):
        name = st.text_input("File name", placeholder="notes.txt")
        submitted = st.form_submit_button("Delete file")
    if submitted:
        if not name.strip():
            log("err", "No file name given.")
        else:
            path = safe_path(name)
            if not path.exists():
                log("err", f"'{path.name}' does not exist.")
            else:
                try:
                    path.unlink()
                    log("ok", f"Deleted '{path.name}'.")
                    st.rerun()
                except Exception as e:
                    log("err", f"Could not delete file: {e}")

else:  # browse
    files = sorted(VAULT_DIR.iterdir(), key=lambda p: p.name)
    if not files:
        st.markdown("<span style='color:#6E6594;'>The vault is empty. Create a file to get started.</span>", unsafe_allow_html=True)
    else:
        for p in files:
            size = p.stat().st_size
            st.markdown(
                f"<div class='row-item'><span>📄 {p.name}</span>"
                f"<span style='color:var(--muted);'>{size} bytes</span></div>",
                unsafe_allow_html=True,
            )

st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Console log
# ----------------------------------------------------------------------------
st.markdown("<div class='nav-path' style='margin-left:0;'>Console Output</div>", unsafe_allow_html=True)
if st.session_state.log:
    lines = []
    for level, message, ts in st.session_state.log:
        cls = {"ok": "log-ok", "err": "log-err"}.get(level, "")
        tag = {"ok": "✓", "err": "✕"}.get(level, "·")
        lines.append(f"<div class='log-line'><span class='log-time'>{ts}</span><span class='{cls}'>{tag} {message}</span></div>")
    st.markdown(f"<div class='console'>{''.join(lines)}</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='console'><span class='log-line'>Waiting for your first command…</span></div>", unsafe_allow_html=True)
