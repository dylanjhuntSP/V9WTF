import streamlit as st
import json, os

st.set_page_config(page_title="WTF is Up?", page_icon=None, layout="centered")

DATA_DIR = os.path.dirname(__file__)
with open(os.path.join(DATA_DIR, "content.json"), "r", encoding="utf-8") as f:
    CONTENT = json.load(f)

def init_state():
    ss = st.session_state
    ss.setdefault("phase", "welcome")
    ss.setdefault("handle", "")
    ss.setdefault("age_bracket", "13-15")
    ss.setdefault("adjective", "")
    ss.setdefault("animal", "")
    ss.setdefault("selected_moods", set())
    ss.setdefault("selected_scenarios", set())
    ss.setdefault("technique", None)
    ss.setdefault("time_choice", None)
    ss.setdefault("theme_color", "#AAB7F8")
    ss.setdefault("bg_anim", "Penguin")
    ss.setdefault("show_welcome_overlay", True)

init_state()

PRIMARY = "#AAB7F8"
TEXT = "#1f2937"

TECH_COLORS = {
    "Breath Work": "#CFE8FF",
    "Mindfulness": "#FFFACD",
    "Thinking Techniques": "#F8CFE3",
    "Other": "#E6E6FA"
}

def apply_css(bg_color=None, radial=False):
    theme = st.session_state.get("theme_color", PRIMARY)
    accent = bg_color or theme
    gradient_css = ""
    if radial:
        gradient_css = (
            f"background: radial-gradient(circle at 50% 35%, #FFFFFF 0%, #FFFFFF 24%, {accent} 76%, {accent} 100%) !important;"
        )
    st.markdown(
        f"""
        <style>
          .stApp {{ background: {accent}; {gradient_css} }}
          h1,h2,h3,p, label, div, span {{ color: {TEXT}; }}
          .header-bar {{ text-align:center; margin: 6px 0 8px 0; }}
          .header-title {{ font-weight: 900; font-size: 22px; padding: 4px 10px;
            border-radius: 10px; background: rgba(255,255,255,0.65);
            border: 1px solid rgba(0,0,0,0.06); display:inline-block; }}
          .hero {{ text-align:center; margin-top:8px; }}
          .hero h1 {{ font-size: 46px; font-weight: 900; margin: 0; }}
          .hero h3 {{ font-size: 18px; font-weight: 800; margin: 2px 0 12px 0; opacity:.9 }}
          .center-card {{ background: white; border-radius: 16px; padding: 18px 20px;
            box-shadow: 0 10px 24px rgba(0,0,0,0.12); border: 1px solid rgba(0,0,0,0.05); }}
          .question-title {{ text-align:center; font-weight: 900; font-size: 30px; margin: 8px 0 12px 0; }}
          .pill {{ display:inline-block; padding:8px 14px; border-radius:999px;
            background: rgba(255,255,255,0.9); border:1px solid rgba(0,0,0,0.06); margin:6px 6px 0 0; font-weight:700; }}
          .footer-note {{ position:fixed; bottom:8px; left:50%; transform:translateX(-50%);
            background: rgba(255,255,255,0.85); padding:6px 12px; border-radius:999px;
            font-size:12px; border:1px solid rgba(0,0,0,0.06); z-index:10; }}
          /* Ring grid */
          .ring {{ display:grid; grid-template-columns: repeat(7, 1fr); gap:12px; max-width: 900px; margin: 0 auto; }}
          .ring .spacer {{ visibility:hidden; }}
          .ring .centerbox {{ grid-column: 3 / span 3; }}
          /* "Modal" card look */
          .modal-card {{ max-width: 900px; width: 92%; background: white; border-radius: 16px;
            padding: 18px 20px; border: 1px solid rgba(0,0,0,0.06); box-shadow: 0 18px 40px rgba(0,0,0,.25); }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_bg_animation():
    html = """
    <style>
      @keyframes waddle {
        0%   { transform: translateX(-10vw); opacity: .0; }
        5%   { opacity: .95; }
        50%  { transform: translateX(50vw) translateY(-2px); }
        100% { transform: translateX(115vw); opacity: .0; }
      }
      @keyframes prints {
        0%   { opacity: 0; }
        10%  { opacity: .7; }
        80%  { opacity: .3; }
        100% { opacity: 0; }
      }
      .penguin { font-size: 42px; line-height: 1; position:absolute; bottom: 12%;
        animation: waddle var(--dur) linear infinite; animation-delay: var(--delay);
        filter: drop-shadow(0 6px 10px rgba(0,0,0,.12)); }
      .track { position: absolute; bottom: calc(12% - 6px); width: 12px; height: 8px; border-radius: 50%;
        background: rgba(255,255,255,.8); box-shadow: 2px 1px 0 rgba(0,0,0,.06);
        animation: prints var(--dur) linear infinite; animation-delay: var(--delay); }
    </style>
    <div style="position:fixed; inset:0; pointer-events:none; z-index:0; overflow:hidden;">
      <div class="penguin" style="--dur: 28s; --delay: 0s; left:-10vw;">🐧</div>
      """ + "".join([f"<div class='track' style='--dur:28s; --delay:0s; left:{x}vw;'></div>" for x in range(-8,112,6)]) + """
      <div class="penguin" style="--dur: 34s; --delay: 7s; left:-10vw; bottom: 18%;">🐧</div>
      """ + "".join([f"<div class='track' style='--dur:34s; --delay:7s; left:{x}vw; bottom: 18%;'></div>" for x in range(-8,112,7)]) + """
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def header():
    st.markdown("<div class='header-bar'><span class='header-title'>WTF is Up</span></div>", unsafe_allow_html=True)

def footer():
    st.markdown("<div class='footer-note'>In the U.S., call <b>911</b> for emergencies • Call or text <b>988</b> for mental health crises.</div>", unsafe_allow_html=True)

def recommend(tags, minutes, age_bracket, technique=None):
    items = CONTENT["items"]
    def ok_age(item_age):
        if age_bracket == "13-15" and item_age.startswith("16"):
            return False
        return True
    def score(it):
        if technique and it.get("technique") != technique: 
            return -1e9
        if not ok_age(it.get("age_range","13-18")): 
            return -1e9
        if minutes is not None and it.get("minutes", 10) > minutes: 
            return -1e9
        overlap = len(set(it.get("tags", [])) & set(tags))
        time_fit = 1.0 if it.get("minutes", 10) <= minutes else 0.0
        return overlap*2 + time_fit
    ranked = sorted(items, key=lambda x: score(x), reverse=True)
    out = [x for x in ranked if score(x) > -1e5]
    return out[:4] if out else ranked[:2]

def mood_ring_page():
    apply_css(bg_color="#AAB7F8", radial=True)
    render_bg_animation()
    st.markdown("<div class='question-title'>How Do You Feel Today?</div>", unsafe_allow_html=True)
    moods = ["Anxious","Sad","Angry","Stressed","Panic","Overwhelmed","Lonely","Sleep problems",
             "School pressure","Family conflict","Bullying","Sports pressure","Focus","Motivation",
             "Breakup","Friend drama","Body image","Social media","Rumination","Worry"]
    top, mid, bot = moods[:7], moods[7:13], moods[13:]
    st.markdown("<div class='ring'>", unsafe_allow_html=True)
    cols = st.columns(7)
    for i, m in enumerate(top):
        with cols[i]:
            if st.button(m, key=f"m1_{i}"):
                s = set(st.session_state.get("selected_moods", set()))
                s.remove(m) if m in s else s.add(m)
                st.session_state.selected_moods = s; st.rerun()
    cols = st.columns(7)
    for i in range(7):
        with cols[i]:
            if i in (0,6):
                m = mid[0] if i==0 and len(mid)>0 else (mid[1] if i==6 and len(mid)>1 else None)
                if m and st.button(m, key=f"m2_{i}"):
                    s = set(st.session_state.get("selected_moods", set()))
                    s.remove(m) if m in s else s.add(m)
                    st.session_state.selected_moods = s; st.rerun()
            elif i==2:
                st.markdown("<div class='centerbox center-card'><div style='text-align:center; font-weight:900; font-size:24px;'>How Do You Feel?</div><div style='font-size:12px; opacity:.8;'>Tap a few that fit.</div></div>", unsafe_allow_html=True)
            elif i==1 and len(mid)>2:
                m = mid[2]
                if st.button(m, key=f"m2b_{i}"):
                    s = set(st.session_state.get("selected_moods", set()))
                    s.remove(m) if m in s else s.add(m)
                    st.session_state.selected_moods = s; st.rerun()
            elif i==5 and len(mid)>3:
                m = mid[3]
                if st.button(m, key=f"m2b_{i}"):
                    s = set(st.session_state.get("selected_moods", set()))
                    s.remove(m) if m in s else s.add(m)
                    st.session_state.selected_moods = s; st.rerun()
            else:
                st.markdown("<div class='spacer'>.</div>", unsafe_allow_html=True)
    cols = st.columns(7)
    for i in range(7):
        if i < len(bot):
            m = bot[i]
            if st.button(m, key=f"m3_{i}"):
                s = set(st.session_state.get("selected_moods", set()))
                s.remove(m) if m in s else s.add(m)
                st.session_state.selected_moods = s; st.rerun()
        else:
            st.markdown("<div class='spacer'>.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    chosen = st.session_state.get("selected_moods", set())
    if chosen:
        st.markdown("".join([f"<span class='pill'>{x}</span>" for x in chosen]), unsafe_allow_html=True)

def techniques_page():
    apply_css(bg_color="#AAB7F8", radial=False)
    render_bg_animation()
    st.markdown("<div class='question-title'>How Should We Fix This?</div>", unsafe_allow_html=True)
    techs = ["Breath Work","Mindfulness","Thinking Techniques","Other"]
    cols = st.columns(4)
    desc = {
        "Breath Work": ["Box Breathing 4-4-4-4","4-7-8 Breathing","Coherent Breathing","Pursed-Lip Breathing"],
        "Mindfulness": ["5-4-3-2-1 Senses","Body Scan (Mini)","Mindful Walking","Safe Place Imagery","PMR (Mini)"],
        "Thinking Techniques": ["Thought Record (CBT)","Evidence For/Against","Cognitive Defusion (ACT)","Problem-Solving","Opposite Action (DBT)"],
        "Other": ["Behavioral Activation","Values → Tiny Goal","Self‑Compassion Break","Journaling Prompt","Gratitude 3×3"]
    }
    steps = {
        "Breath Work": ["Sit comfortably.","Inhale through nose 4s.","Hold 4s.","Exhale through mouth 4s.","Repeat 4–6 rounds."],
        "Mindfulness": ["Pause & notice posture.","Name 5 things you see.","4 you feel, 3 you hear, 2 you smell, 1 you taste.","Slow breath for 3 rounds.","Notice any change."],
        "Thinking Techniques": ["Write the situation.","Rate emotion 0–10.","Write automatic thought.","List evidence for & against.","Try a fairer alternative thought."],
        "Other": ["Pick one tiny, helpful action.","Schedule when/where.","Do it for 2–5 mins.","Check in: mood now?","Optional: share with a trusted adult."]
    }
    for i,t in enumerate(techs):
        with cols[i]:
            with st.expander(t, expanded=False):
                st.markdown("**Try:** " + ", ".join(desc[t]))
                st.markdown("**Steps:**")
                for j, s in enumerate(steps[t], 1):
                    st.write(f"{j}. {s}")
                if st.button(f"Use {t}", key=f"use_{t}", use_container_width=True):
                    st.session_state.technique = t
                    st.session_state.theme_color = TECH_COLORS[t]
                    st.session_state.phase = "time"; st.rerun()
    if st.button("⬅ Back"): st.session_state.phase = "scenarios"; st.rerun()

def scenarios_page():
    apply_css(bg_color="#AAB7F8", radial=True)
    render_bg_animation()
    st.markdown("<div class='question-title'>Did Something Happen Today?</div>", unsafe_allow_html=True)
    scenarios = ["Argument with a friend","Got a bad grade","Sports pressure","Family conflict","Online drama","Felt left out"]
    cols = st.columns(3)
    for i, sc in enumerate(scenarios):
        with cols[i % 3]:
            if st.button(sc, key=f"sc_{i}"):
                s = set(st.session_state.get("selected_scenarios", set()))
                s.remove(sc) if sc in s else s.add(sc)
                st.session_state.selected_scenarios = s; st.rerun()
    chosen = st.session_state.get("selected_scenarios", set())
    if chosen:
        st.markdown("".join([f"<span class='pill'>{x}</span>" for x in chosen]), unsafe_allow_html=True)

def time_page():
    apply_css(bg_color=st.session_state.get("theme_color", PRIMARY), radial=False)
    render_bg_animation()
    st.markdown("<div class='question-title'>How much time do you have?</div>", unsafe_allow_html=True)
    times = [2,5,10,15,20]
    cols = st.columns(5)
    for i,t in enumerate(times):
        with cols[i]:
            if st.button(f"{t} min", key=f"time_{t}", use_container_width=True):
                st.session_state.time_choice = t
                st.session_state.phase = "plan"; st.rerun()
    if st.button("⬅ Back"): st.session_state.phase = "techniques"; st.rerun()

def plan_page():
    apply_css(bg_color=st.session_state.get("theme_color", PRIMARY), radial=False)
    render_bg_animation()
    st.markdown("<div class='question-title'>Your plan</div>", unsafe_allow_html=True)
    tags = [m.lower() for m in st.session_state.selected_moods]
    recs = recommend(tags, st.session_state.time_choice or 10, st.session_state.age_bracket, st.session_state.technique)
    if not recs:
        st.info("Here are a few safe starters.")
        recs = [x for x in CONTENT["items"] if x.get("technique")==st.session_state.technique][:3] or CONTENT["items"][:2]
    for it in recs:
        with st.container(border=True):
            st.markdown(f"**{it['title']}**")
            st.caption(it["summary"])
            st.write("Technique:", it.get("technique",""), " • Minutes:", it.get("minutes",5))
            if it.get("steps"):
                with st.expander("Steps"):
                    for i, s in enumerate(it["steps"], 1):
                        st.write(f"{i}. {s}")
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("Start over"):
            keep = st.session_state.get("bg_anim","Penguin")
            st.session_state.clear(); init_state()
            st.session_state.bg_anim = keep; st.rerun()
    with c2:
        if st.button("Pick different moods"): st.session_state.phase = "feelings"; st.rerun()
    with c3:
        if st.button("Back to time"): st.session_state.phase = "time"; st.rerun()

# ---------- FLOW ----------
apply_css()
header()
render_bg_animation()

# Cover hero
st.markdown("<div class='hero'><h1>WTF Is Up?</h1><h3>Lets&nbsp;&nbsp;&nbsp;Fix It</h3></div>", unsafe_allow_html=True)

# --- Welcome "modal": use native Streamlit widgets so the Close button is always clickable ---
if st.session_state.phase == "welcome" and st.session_state.show_welcome_overlay:
    spacer1, col, spacer2 = st.columns([1,2,1])
    with col:
        st.markdown("<div class='modal-card'>", unsafe_allow_html=True)
        st.markdown("### Welcome")
        st.write("This app shares supportive, clinician-approved self-help resources for teens. "
                 "It is educational and not a diagnosis or a substitute for professional care.")
        st.markdown("*In the U.S., call **911** for emergencies, or call/text **988** for mental health crises.*")
        if st.button("✕ Close (start)"):
            st.session_state.show_welcome_overlay = False
            st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()  # Halt rendering of the rest of the page until closed

# Name picking
if st.session_state.phase == "welcome" and not st.session_state.show_welcome_overlay:
    adjs = ["Ferocious","Curious","Gentle","Bold","Radiant","Calm","Brave","Witty","Kind","Steady","Swift","Bright"]
    animals = ["Penguin","Otter","Hawk","Dolphin","Panda","Tiger","Koala","Falcon","Fox","Seal","Heron","Lynx"]
    c1, c2, c3 = st.columns(3)
    with c2:
        st.session_state.adjective = st.selectbox("Pick an adjective", adjs, index=0)
        st.session_state.animal = st.selectbox("Pick an animal", animals, index=0)
        st.session_state.age_bracket = st.selectbox("Age range", ["13-15","16-18"], index=0)
        if st.button("Continue"):
            st.session_state.handle = f"{st.session_state.adjective} {st.session_state.animal}"
            st.session_state.phase = "feelings"; st.experimental_rerun()

elif st.session_state.phase == "feelings":
    mood_ring_page()
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("⬅ Back"): st.session_state.phase = "welcome"; st.experimental_rerun()
    with c2:
        if st.button("Clear feelings"): st.session_state.selected_moods = set(); st.experimental_rerun()
    with c3:
        if st.button("Next ➜", disabled=not bool(st.session_state.selected_moods)): st.session_state.phase = "scenarios"; st.experimental_rerun()

elif st.session_state.phase == "scenarios":
    st.markdown("<div class='question-title'>Did Something Happen Today?</div>", unsafe_allow_html=True)
    scenarios = ["Argument with a friend","Got a bad grade","Sports pressure","Family conflict","Online drama","Felt left out"]
    cols = st.columns(3)
    for i, sc in enumerate(scenarios):
        with cols[i % 3]:
            if st.button(sc, key=f"sc_{i}"):
                s = set(st.session_state.get("selected_scenarios", set()))
                s.remove(sc) if sc in s else s.add(sc)
                st.session_state.selected_scenarios = s; st.experimental_rerun()
    chosen = st.session_state.get("selected_scenarios", set())
    if chosen:
        st.markdown("".join([f"<span class='pill'>{x}</span>" for x in chosen]), unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("⬅ Back"): st.session_state.phase = "feelings"; st.experimental_rerun()
    with c3:
        if st.button("Next ➜"): st.session_state.phase = "techniques"; st.experimental_rerun()

elif st.session_state.phase == "techniques":
    st.markdown("<div class='question-title'>How Should We Fix This?</div>", unsafe_allow_html=True)
    techs = ["Breath Work","Mindfulness","Thinking Techniques","Other"]
    cols = st.columns(4)
    desc = {
        "Breath Work": ["Box Breathing 4-4-4-4","4-7-8 Breathing","Coherent Breathing","Pursed-Lip Breathing"],
        "Mindfulness": ["5-4-3-2-1 Senses","Body Scan (Mini)","Mindful Walking","Safe Place Imagery","PMR (Mini)"],
        "Thinking Techniques": ["Thought Record (CBT)","Evidence For/Against","Cognitive Defusion (ACT)","Problem-Solving","Opposite Action (DBT)"],
        "Other": ["Behavioral Activation","Values → Tiny Goal","Self‑Compassion Break","Journaling Prompt","Gratitude 3×3"]
    }
    steps = {
        "Breath Work": ["Sit comfortably.","Inhale through nose 4s.","Hold 4s.","Exhale through mouth 4s.","Repeat 4–6 rounds."],
        "Mindfulness": ["Pause & notice posture.","Name 5 things you see.","4 you feel, 3 you hear, 2 you smell, 1 you taste.","Slow breath for 3 rounds.","Notice any change."],
        "Thinking Techniques": ["Write the situation.","Rate emotion 0–10.","Write automatic thought.","List evidence for & against.","Try a fairer alternative thought."],
        "Other": ["Pick one tiny, helpful action.","Schedule when/where.","Do it for 2–5 mins.","Check in: mood now?","Optional: share with a trusted adult."]
    }
    for i,t in enumerate(techs):
        with cols[i]:
            with st.expander(t, expanded=False):
                st.markdown("**Try:** " + ", ".join(desc[t]))
                st.markdown("**Steps:**")
                for j, s in enumerate(steps[t], 1):
                    st.write(f"{j}. {s}")
                if st.button(f"Use {t}", key=f"use_{t}", use_container_width=True):
                    st.session_state.technique = t
                    st.session_state.theme_color = TECH_COLORS[t]
                    st.session_state.phase = "time"; st.experimental_rerun()
    if st.button("⬅ Back"): st.session_state.phase = "scenarios"; st.experimental_rerun()

elif st.session_state.phase == "time":
    st.markdown("<div class='question-title'>How much time do you have?</div>", unsafe_allow_html=True)
    times = [2,5,10,15,20]
    cols = st.columns(5)
    for i,t in enumerate(times):
        with cols[i]:
            if st.button(f"{t} min", key=f"time_{t}", use_container_width=True):
                st.session_state.time_choice = t
                st.session_state.phase = "plan"; st.experimental_rerun()
    if st.button("⬅ Back"): st.session_state.phase = "techniques"; st.experimental_rerun()

elif st.session_state.phase == "plan":
    st.markdown("<div class='question-title'>Your plan</div>", unsafe_allow_html=True)
    tags = [m.lower() for m in st.session_state.selected_moods]
    recs = recommend(tags, st.session_state.time_choice or 10, st.session_state.age_bracket, st.session_state.technique)
    if not recs:
        st.info("Here are a few safe starters.")
        recs = [x for x in CONTENT["items"] if x.get("technique")==st.session_state.technique][:3] or CONTENT["items"][:2]
    for it in recs:
        with st.container(border=True):
            st.markdown(f"**{it['title']}**")
            st.caption(it["summary"])
            st.write("Technique:", it.get("technique",""), " • Minutes:", it.get("minutes",5))
            if it.get("steps"):
                with st.expander("Steps"):
                    for i, s in enumerate(it["steps"], 1):
                        st.write(f"{i}. {s}")
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("Start over"):
            keep = st.session_state.get("bg_anim","Penguin")
            st.session_state.clear(); init_state()
            st.session_state.bg_anim = keep; st.experimental_rerun()
    with c2:
        if st.button("Pick different moods"): st.session_state.phase = "feelings"; st.experimental_rerun()
    with c3:
        if st.button("Back to time"): st.session_state.phase = "time"; st.experimental_rerun()

footer()
