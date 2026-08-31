import streamlit as st
import os
import base64
import time

# -------------------------------------------------------------
# 頁面配置 (Page Configuration)
# -------------------------------------------------------------
st.set_page_config(
    page_title="星淵信標：深空重啟 (Beacon of the Abyss)",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# 輔助函式：將本地圖片與音訊轉為 Base64 (供瀏覽器直讀)
# -------------------------------------------------------------
def get_base64_encoded(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None

def get_image_uri(filename):
    candidates = [
        os.path.join("images", filename),
        os.path.join("game", "images", filename),
        filename
    ]
    for c in candidates:
        if os.path.exists(c):
            ext = os.path.splitext(c)[1].replace(".", "").lower()
            mime = "image/png" if ext == "png" else "image/jpeg"
            b64 = get_base64_encoded(c)
            if b64:
                return f"data:{mime};base64,{b64}"
    return None

def get_audio_uri(filename):
    candidates = [
        os.path.join("audio", filename),
        os.path.join("game", "audio", filename),
        filename
    ]
    for c in candidates:
        if os.path.exists(c):
            ext = os.path.splitext(c)[1].replace(".", "").lower()
            mime = "audio/wav" if ext == "wav" else ("audio/ogg" if ext == "ogg" else "audio/mp3")
            b64 = get_base64_encoded(c)
            if b64:
                return f"data:{mime};base64,{b64}"
    return None

# -------------------------------------------------------------
# 自訂 CSS：電影級深空科幻透明 UI 與動畫
# -------------------------------------------------------------
st.markdown("""
<style>
    /* 全域科幻暗黑底色 */
    .stApp {
        background: radial-gradient(circle at center, #0a1128 0%, #030712 100%);
        color: #f1f2f6;
        font-family: 'Microsoft JhengHei', 'PingFang TC', -apple-system, sans-serif;
    }
    
    /* 舞臺容器 */
    .vn-stage-container {
        position: relative;
        width: 100%;
        min-height: 480px;
        border-radius: 16px;
        background-size: cover;
        background-position: center;
        border: 1px solid rgba(0, 229, 255, 0.25);
        box-shadow: 0 8px 32px 0 rgba(0, 229, 255, 0.15);
        overflow: hidden;
        margin-bottom: 20px;
        display: flex;
        align-items: flex-end;
        justify-content: space-around;
        padding-bottom: 10px;
    }

    /* 角色立繪卡片 */
    .character-avatar {
        max-height: 420px;
        object-fit: contain;
        filter: drop-shadow(0 0 15px rgba(0, 229, 255, 0.3));
        transition: all 0.3s ease;
    }
    
    .character-avatar.active-speaker {
        filter: drop-shadow(0 0 25px rgba(0, 229, 255, 0.75)) brightness(1.08);
        transform: scale(1.03);
    }
    
    .character-avatar.silent {
        filter: drop-shadow(0 0 8px rgba(0, 0, 0, 0.6)) brightness(0.75);
    }

    /* 100% 透明極簡字幕對話框 */
    .dialogue-box {
        background: rgba(13, 27, 42, 0.85);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 229, 255, 0.4);
        border-radius: 12px;
        padding: 22px 30px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        margin-top: 10px;
        margin-bottom: 20px;
    }

    .speaker-tag {
        display: inline-block;
        background: rgba(0, 229, 255, 0.18);
        color: #00e5ff;
        font-size: 1.2rem;
        font-weight: 700;
        padding: 4px 16px;
        border-radius: 6px;
        border-left: 4px solid #00e5ff;
        margin-bottom: 12px;
        letter-spacing: 1px;
    }

    .dialogue-text {
        font-size: 1.35rem;
        line-height: 1.7;
        color: #ffffff;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.9);
        letter-spacing: 0.5px;
    }

    /* 按鈕美化 */
    .stButton>button {
        background: linear-gradient(135deg, rgba(27, 38, 59, 0.9) 0%, rgba(13, 27, 42, 0.9) 100%);
        color: #f1f2f6;
        border: 1px solid #00e5ff;
        border-radius: 8px;
        font-size: 1.15rem;
        font-weight: 600;
        padding: 10px 24px;
        transition: all 0.25s ease;
        box-shadow: 0 4px 15px rgba(0, 229, 255, 0.15);
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #0984e3 0%, #00cec9 100%);
        color: #ffffff;
        border-color: #ffffff;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.6);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 劇本資料庫 (Full Script Database)
# -------------------------------------------------------------
STORY_DATA = {
    # 序幕
    "prologue_1": {
        "bg": "bg_beacon.jpg",
        "speaker": "電影旁白",
        "speaker_id": "narrator",
        "text": "地球曆 2387 年。太陽系外緣，柯伊伯帶邊界。",
        "voice": "voice_nar_prologue_01.wav",
        "left_char": None,
        "right_char": None,
        "center_char": None,
        "next": "prologue_2"
    },
    "prologue_2": {
        "bg": "bg_beacon.jpg",
        "speaker": "電影旁白",
        "speaker_id": "narrator",
        "text": "深空科考艦『海伯利昂號』，已在無盡黑暗中航行了四百一十二天。",
        "voice": "voice_nar_prologue_02.wav",
        "left_char": None,
        "right_char": None,
        "center_char": None,
        "next": "intro_1"
    },
    # 第一幕：艦橋登場
    "intro_1": {
        "bg": "bg_bridge.jpg",
        "speaker": "電影旁白",
        "speaker_id": "narrator",
        "text": "艦橋上，藍色的全息星圖微微閃爍著冰冷的光芒。",
        "voice": "voice_nar_ch1_01.wav",
        "left_char": "f2_neutral.png",
        "right_char": "vivian_neutral.png",
        "center_char": None,
        "next": "intro_2"
    },
    "intro_2": {
        "bg": "bg_bridge.jpg",
        "speaker": "女助手 諾亞 (NOAH)",
        "speaker_id": "f2",
        "text": "指揮官，您好！我是艦載量子 AI 諾亞。全艦感知網絡與維生系統運作正常。",
        "voice": "voice_f2_01.wav",
        "left_char": "f2_speaking.png",
        "right_char": "vivian_neutral.png",
        "center_char": None,
        "next": "intro_3"
    },
    "intro_3": {
        "bg": "bg_bridge.jpg",
        "speaker": "首席工程師 薇薇安",
        "speaker_id": "f1",
        "text": "哈囉艦長！我是首席動力工程師薇薇安！反物質引擎核心讀數一切平穩！",
        "voice": "voice_vivian_01.wav",
        "left_char": "f2_neutral.png",
        "right_char": "vivian_speaking.png",
        "center_char": None,
        "next": "intro_4"
    },
    "intro_4": {
        "bg": "bg_bridge.jpg",
        "speaker": "指揮官 亞底斯",
        "speaker_id": "p",
        "text": "我是亞底斯。深空科考艦海伯利昂號，全系統就緒，準備執行深空探測任務。",
        "voice": "voice_artis_01.wav",
        "left_char": "f2_neutral.png",
        "right_char": "vivian_neutral.png",
        "center_char": "artis_speaking.png",
        "next": "ch1_1"
    },
    # 第一章：深空異變
    "ch1_1": {
        "bg": "bg_bridge.jpg",
        "speaker": "女助手 諾亞 (NOAH)",
        "speaker_id": "f2",
        "text": "報告指揮官，深空重力波感測器在 0.3 光年外的無人星區，捕捉到了非自然週期性脈衝。",
        "voice": "voice_f2_ch1_01.wav",
        "left_char": "f2_speaking.png",
        "right_char": "vivian_neutral.png",
        "center_char": None,
        "next": "ch1_2"
    },
    "ch1_2": {
        "bg": "bg_bridge.jpg",
        "speaker": "首席工程師 薇薇安",
        "speaker_id": "f1",
        "text": "指揮官！反應爐核心讀數有些異常，這個脈衝正在與我們的反物質引擎產生同頻共振！",
        "voice": "voice_vivian_ch1_01.wav",
        "left_char": "f2_neutral.png",
        "right_char": "vivian_speaking.png",
        "center_char": None,
        "next": "ch1_3"
    },
    "ch1_3": {
        "bg": "bg_bridge.jpg",
        "speaker": "指揮官 亞底斯",
        "speaker_id": "p",
        "text": "能確定信號源的性質嗎？",
        "voice": "voice_artis_ch1_01.wav",
        "left_char": "f2_neutral.png",
        "right_char": "vivian_neutral.png",
        "center_char": "artis_speaking.png",
        "next": "ch1_4"
    },
    "ch1_4": {
        "bg": "bg_bridge.jpg",
        "speaker": "女助手 諾亞 (NOAH)",
        "speaker_id": "f2",
        "text": "資料庫比對無匹配記錄。信號特徵符合高階量子星門結構，推測為十萬年前『先驅者文明』的古代信標。",
        "voice": "voice_f2_ch1_02.wav",
        "left_char": "f2_alert.png",
        "right_char": "vivian_neutral.png",
        "center_char": None,
        "next": "ch1_5"
    },
    "ch1_5": {
        "bg": "bg_bridge.jpg",
        "speaker": "首席工程師 薇薇安",
        "speaker_id": "f1",
        "text": "這太危險了！我們根本不知道那是陷阱還是武器，我建議立刻拉升偏轉護盾並掉頭返航！",
        "voice": "voice_vivian_ch1_02.wav",
        "left_char": "f2_alert.png",
        "right_char": "vivian_panic.png",
        "center_char": None,
        "choices": [
            {
                "label": "🚀 【決策一】聽從諾亞建議，躍遷前往脈衝源頭調查 (+1 AI 信任)",
                "target": "ch1_choice_a",
                "effect": {"trust_ai": 1, "ship_energy": -10}
            },
            {
                "label": "🛡️ 【決策一】聽從薇薇安建議，維持防護網並緩步靠近 (-1 AI 信任)",
                "target": "ch1_choice_b",
                "effect": {"trust_ai": -1, "ship_energy": -20}
            }
        ]
    },
    # 分支一 A
    "ch1_choice_a": {
        "bg": "bg_bridge.jpg",
        "speaker": "指揮官 亞底斯",
        "speaker_id": "p",
        "text": "調整折躍引擎座標，我們前往信標中心。這可能是人類文明突破星際界限的唯一機會。",
        "voice": "voice_artis_ch1_b1.wav",
        "left_char": "f2_neutral.png",
        "right_char": "vivian_panic.png",
        "center_char": "artis_speaking.png",
        "next": "ch1_choice_a2"
    },
    "ch1_choice_a2": {
        "bg": "bg_bridge.jpg",
        "speaker": "女助手 諾亞 (NOAH)",
        "speaker_id": "f2",
        "text": "航線已鎖定。正在進行超空間跳躍...",
        "voice": "voice_f2_ch1_b1.wav",
        "left_char": "f2_speaking.png",
        "right_char": "vivian_panic.png",
        "center_char": None,
        "next": "beacon_1"
    },
    # 分支一 B
    "ch1_choice_b": {
        "bg": "bg_bridge.jpg",
        "speaker": "指揮官 亞底斯",
        "speaker_id": "p",
        "text": "保持最高警戒，展開多相偏轉護盾，保持安全距離進行外圍探測。",
        "voice": "voice_artis_ch1_b2.wav",
        "left_char": "f2_neutral.png",
        "right_char": "vivian_neutral.png",
        "center_char": "artis_speaking.png",
        "next": "ch1_choice_b2"
    },
    "ch1_choice_b2": {
        "bg": "bg_bridge.jpg",
        "speaker": "首席工程師 薇薇安",
        "speaker_id": "f1",
        "text": "明白！全艦進入二級戰備狀態！",
        "voice": "voice_vivian_ch1_b2.wav",
        "left_char": "f2_neutral.png",
        "right_char": "vivian_speaking.png",
        "center_char": None,
        "next": "beacon_1"
    },
    # 第二章：阿爾法信標
    "beacon_1": {
        "bg": "bg_beacon.jpg",
        "speaker": "電影旁白",
        "speaker_id": "narrator",
        "sfx": "warp_rumble.wav",
        "text": "伴隨著劇烈的空間折疊震顫，海伯利昂號脫離了超空間！",
        "voice": "voice_nar_beacon_01.wav",
        "left_char": None,
        "right_char": None,
        "center_char": None,
        "next": "beacon_2"
    },
    "beacon_2": {
        "bg": "bg_beacon.jpg",
        "speaker": "電影旁白",
        "speaker_id": "narrator",
        "text": "在巨大的全息舷窗前，一座通體由藍色光晶鑄造的巨型環狀遺跡漂浮在深空中，散發著窒息的美感與壓迫感。",
        "voice": "voice_nar_beacon_02.wav",
        "left_char": "f2_neutral.png",
        "right_char": "vivian_neutral.png",
        "center_char": None,
        "next": "beacon_3"
    },
    "beacon_3": {
        "bg": "bg_beacon.jpg",
        "speaker": "女助手 諾亞 (NOAH)",
        "speaker_id": "f2",
        "text": "抵達目標節點：古代晶體星門【阿爾法信標】。檢測到信標內部傳來強烈的神經量子廣播，它正在嘗試與艦載 AI 及指揮官的大腦皮層建立同步。",
        "voice": "voice_f2_ch2_01.wav",
        "left_char": "f2_speaking.png",
        "right_char": "vivian_neutral.png",
        "center_char": None,
        "next": "beacon_4"
    },
    "beacon_4": {
        "bg": "bg_beacon.jpg",
        "speaker": "首席工程師 薇薇安",
        "speaker_id": "f1",
        "text": "艦長！能量讀數暴增了 300%！艦體外殼溫度正在失控上升，如果再不及時切斷，我們整艘船都會被同化！",
        "voice": "voice_vivian_ch2_01.wav",
        "left_char": "f2_neutral.png",
        "right_char": "vivian_panic.png",
        "center_char": None,
        "choices": [
            {
                "label": "🌌 【決策二】同意進行量子同調，探索宇宙終極真相 (+2 AI 信任)",
                "target": "beacon_sync_1",
                "effect": {"trust_ai": 2, "artifact_analyzed": True}
            },
            {
                "label": "💥 【決策二】命令薇薇安發射超載脈衝，摧毀信標核心 (-2 AI 信任)",
                "target": "beacon_destroy_1",
                "effect": {"trust_ai": -2, "artifact_analyzed": False}
            }
        ]
    },
    # 分支二 A：同調
    "beacon_sync_1": {
        "bg": "bg_beacon.jpg",
        "speaker": "指揮官 亞底斯",
        "speaker_id": "p",
        "text": "諾亞，開放我的神經接口與你的核心算力，我們一同接納信標的數據庫！",
        "voice": "voice_artis_ch2_b1.wav",
        "left_char": "f2_alert.png",
        "right_char": "vivian_panic.png",
        "center_char": "artis_speaking.png",
        "next": "beacon_sync_2"
    },
    "beacon_sync_2": {
        "bg": "bg_beacon.jpg",
        "speaker": "女助手 諾亞 (NOAH)",
        "speaker_id": "f2",
        "text": "量子同調開始... 願星光指引我們...",
        "voice": "voice_f2_ch2_b1.wav",
        "left_char": "f2_speaking.png",
        "right_char": "vivian_panic.png",
        "center_char": None,
        "next": "ending_flash"
    },
    # 分支二 B：摧毀
    "beacon_destroy_1": {
        "bg": "bg_beacon.jpg",
        "speaker": "指揮官 亞底斯",
        "speaker_id": "p",
        "sfx": "laser.wav",
        "text": "薇薇安，全功率過載離子炮，立刻摧毀星門核心發射源！人類還沒準備好面對這個力量！",
        "voice": "voice_artis_ch2_b2.wav",
        "left_char": "f2_alert.png",
        "right_char": "vivian_panic.png",
        "center_char": "artis_speaking.png",
        "next": "beacon_destroy_2"
    },
    "beacon_destroy_2": {
        "bg": "bg_beacon.jpg",
        "speaker": "首席工程師 薇薇安",
        "speaker_id": "f1",
        "text": "主炮充能完畢——開火！！",
        "voice": "voice_vivian_ch2_b2.wav",
        "left_char": "f2_alert.png",
        "right_char": "vivian_speaking.png",
        "center_char": None,
        "next": "ending_flash"
    },
    # 結局閃光
    "ending_flash": {
        "bg": "bg_beacon.jpg",
        "speaker": "電影旁白",
        "speaker_id": "narrator",
        "text": "一道刺目的強光，瞬間吞沒了整座星艦！",
        "voice": "voice_nar_ending_flash.wav",
        "left_char": None,
        "right_char": None,
        "center_char": None,
        "next_eval": True
    },
    # 結局 A
    "ending_transcendence_1": {
        "bg": "bg_beacon.jpg",
        "speaker": "結局 A：超越昇華 (Transcendence)",
        "speaker_id": "narrator",
        "text": "海伯利昂號與古代星門完成了完美共鳴。",
        "voice": "voice_nar_end_a_01.wav",
        "left_char": "f2_neutral.png",
        "right_char": "vivian_neutral.png",
        "center_char": None,
        "next": "ending_transcendence_2"
    },
    "ending_transcendence_2": {
        "bg": "bg_beacon.jpg",
        "speaker": "結局 A：超越昇華 (Transcendence)",
        "speaker_id": "narrator",
        "text": "無數星系的知識、跨越億萬年的星際航道圖，如洪流般流入指揮官與諾亞的意識之中。",
        "voice": "voice_nar_end_a_02.wav",
        "left_char": "f2_neutral.png",
        "right_char": "vivian_neutral.png",
        "center_char": None,
        "next": "ending_transcendence_3"
    },
    "ending_transcendence_3": {
        "bg": "bg_beacon.jpg",
        "speaker": "結局 A：超越昇華 (Transcendence)",
        "speaker_id": "narrator",
        "text": "人類不再孤獨，新的星際大航海時代，就此揭開序幕。",
        "voice": "voice_nar_end_a_03.wav",
        "left_char": "f2_neutral.png",
        "right_char": "vivian_neutral.png",
        "center_char": None,
        "is_ending": True
    },
    # 結局 B
    "ending_abyss_1": {
        "bg": "bg_bridge.jpg",
        "speaker": "結局 B：迷航深淵 (Abyssal Drift)",
        "speaker_id": "narrator",
        "text": "信標的空間紊亂引發了局域引力坍縮。",
        "voice": "voice_nar_end_b_01.wav",
        "left_char": "f2_alert.png",
        "right_char": "vivian_panic.png",
        "center_char": None,
        "next": "ending_abyss_2"
    },
    "ending_abyss_2": {
        "bg": "bg_bridge.jpg",
        "speaker": "結局 B：迷航深淵 (Abyssal Drift)",
        "speaker_id": "narrator",
        "text": "海伯利昂號被拋射進了未知的超深空維度，儀表指針瘋狂旋轉，所有星圖座標皆已失效。",
        "voice": "voice_nar_end_b_02.wav",
        "left_char": "f2_alert.png",
        "right_char": "vivian_panic.png",
        "center_char": None,
        "next": "ending_abyss_3"
    },
    "ending_abyss_3": {
        "bg": "bg_bridge.jpg",
        "speaker": "結局 B：迷航深淵 (Abyssal Drift)",
        "speaker_id": "narrator",
        "text": "在冰冷的黑暗中，林指揮官與船員們只能凝視著無盡的星海，等待下一次奇蹟。",
        "voice": "voice_nar_end_b_03.wav",
        "left_char": "f2_alert.png",
        "right_char": "vivian_panic.png",
        "center_char": None,
        "is_ending": True
    },
    # 結局 C
    "ending_vigil_1": {
        "bg": "bg_bridge.jpg",
        "speaker": "結局 C：人類守望 (Eternal Vigil)",
        "speaker_id": "narrator",
        "text": "耀天的離子光束精準貫穿了古代信標的能量核心！",
        "voice": "voice_nar_end_c_01.wav",
        "left_char": "f2_neutral.png",
        "right_char": "vivian_neutral.png",
        "center_char": None,
        "next": "ending_vigil_2"
    },
    "ending_vigil_2": {
        "bg": "bg_bridge.jpg",
        "speaker": "結局 C：人類守望 (Eternal Vigil)",
        "speaker_id": "narrator",
        "text": "星門在劇烈的連鎖爆炸中化為宇宙塵埃，致命的同化危機被徹底化解。",
        "voice": "voice_nar_end_c_02.wav",
        "left_char": "f2_neutral.png",
        "right_char": "vivian_neutral.png",
        "center_char": None,
        "next": "ending_vigil_3"
    },
    "ending_vigil_3": {
        "bg": "bg_bridge.jpg",
        "speaker": "結局 C：人類守望 (Eternal Vigil)",
        "speaker_id": "narrator",
        "text": "海伯利昂號帶著傷痕滿載的數據踏上歸途，繼續默默守護著太陽系邊疆的安寧。",
        "voice": "voice_nar_end_c_03.wav",
        "left_char": "f2_neutral.png",
        "right_char": "vivian_neutral.png",
        "center_char": None,
        "is_ending": True
    }
}

# -------------------------------------------------------------
# 初始化 Session State
# -------------------------------------------------------------
if "current_node" not in st.session_state:
    st.session_state.current_node = "prologue_1"
if "trust_ai" not in st.session_state:
    st.session_state.trust_ai = 0
if "ship_energy" not in st.session_state:
    st.session_state.ship_energy = 100
if "history" not in st.session_state:
    st.session_state.history = []
if "bgm_on" not in st.session_state:
    st.session_state.bgm_on = True

def restart_game():
    st.session_state.current_node = "prologue_1"
    st.session_state.trust_ai = 0
    st.session_state.ship_energy = 100
    st.session_state.history = []
    st.rerun()

# -------------------------------------------------------------
# 側邊欄控制台 (Sidebar HUD)
# -------------------------------------------------------------
with st.sidebar:
    st.title("🛰️ 艦橋狀態監控儀")
    st.markdown("---")
    
    # 數值條
    st.subheader("📊 飛艦即時讀數")
    trust = st.session_state.trust_ai
    st.metric("AI 信任度 (Trust)", f"{trust:+d}", delta=f"當前等級: {'高' if trust>0 else ('低' if trust<0 else '平衡')}")
    st.progress(max(0.0, min(1.0, (trust + 2) / 4.0)))

    energy = st.session_state.ship_energy
    st.metric("反物質能源核心 (Energy)", f"{energy} %")
    st.progress(max(0.0, min(1.0, energy / 100.0)))
    
    st.markdown("---")
    st.subheader("🎵 背景音樂與音效")
    bgm_toggle = st.checkbox("開啟太空背景音樂 (BGM)", value=st.session_state.bgm_on)
    st.session_state.bgm_on = bgm_toggle
    
    if st.session_state.bgm_on:
        bgm_uri = get_audio_uri("space_theme.mp3")
        if bgm_uri:
            st.markdown(f'<audio src="{bgm_uri}" autoplay loop></audio>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🔄 重新啟動遊戲 (Restart)", use_container_width=True):
        restart_game()

# -------------------------------------------------------------
# 獲取當前節點資料
# -------------------------------------------------------------
current_key = st.session_state.current_node
node = STORY_DATA.get(current_key, STORY_DATA["prologue_1"])

# 記錄歷史
if not st.session_state.history or st.session_state.history[-1] != (node["speaker"], node["text"]):
    st.session_state.history.append((node["speaker"], node["text"]))

# -------------------------------------------------------------
# 頂部標題列
# -------------------------------------------------------------
st.markdown("### 🌌 《星淵信標：深空重啟》 *(Beacon of the Abyss)*")

# -------------------------------------------------------------
# 舞臺渲染 (Stage Rendering)
# -------------------------------------------------------------
bg_img_uri = get_image_uri(node.get("bg", "bg_bridge.jpg"))
bg_css = f'background-image: url("{bg_img_uri}");' if bg_img_uri else "background-color: #030712;"

st.markdown(f"""
<div class="vn-stage-container" style="{bg_css}">
</div>
""", unsafe_allow_html=True)

# 角色立繪呈現 (3 列式舞臺)
col_left, col_center, col_right = st.columns([1, 1, 1])

with col_left:
    l_char = node.get("left_char")
    if l_char:
        img_uri = get_image_uri(l_char)
        if img_uri:
            is_active = "active-speaker" if node.get("speaker_id") == "f2" else "silent"
            st.markdown(f'<div style="text-align: center;"><img src="{img_uri}" class="character-avatar {is_active}" alt="Noah"></div>', unsafe_allow_html=True)

with col_center:
    c_char = node.get("center_char")
    if c_char:
        img_uri = get_image_uri(c_char)
        if img_uri:
            is_active = "active-speaker" if node.get("speaker_id") == "p" else "silent"
            st.markdown(f'<div style="text-align: center;"><img src="{img_uri}" class="character-avatar {is_active}" alt="Player"></div>', unsafe_allow_html=True)

with col_right:
    r_char = node.get("right_char")
    if r_char:
        img_uri = get_image_uri(r_char)
        if img_uri:
            is_active = "active-speaker" if node.get("speaker_id") == "f1" else "silent"
            st.markdown(f'<div style="text-align: center;"><img src="{img_uri}" class="character-avatar {is_active}" alt="Vivian"></div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 語音與音效自動播放 (Audio Autoplay)
# -------------------------------------------------------------
voice_fn = node.get("voice")
if voice_fn:
    v_uri = get_audio_uri(voice_fn)
    if v_uri:
        st.markdown(f'<audio src="{v_uri}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)

sfx_fn = node.get("sfx")
if sfx_fn:
    s_uri = get_audio_uri(sfx_fn)
    if s_uri:
        st.markdown(f'<audio src="{s_uri}" autoplay style="display:none;"></audio>', unsafe_allow_html=True)

# -------------------------------------------------------------
# 透明電影級字幕對話框
# -------------------------------------------------------------
st.markdown(f"""
<div class="dialogue-box">
    <div class="speaker-tag">{node['speaker']}</div>
    <div class="dialogue-text">{node['text']}</div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 互動控制與決策分支
# -------------------------------------------------------------
if "choices" in node:
    st.markdown("#### 🎯 指揮官，請做出關鍵戰略抉擇：")
    for choice in node["choices"]:
        if st.button(choice["label"], use_container_width=True):
            if "effect" in choice:
                eff = choice["effect"]
                if "trust_ai" in eff:
                    st.session_state.trust_ai += eff["trust_ai"]
                if "ship_energy" in eff:
                    st.session_state.ship_energy += eff["ship_energy"]
            st.session_state.current_node = choice["target"]
            st.rerun()

elif node.get("next_eval"):
    # 結局評估節點
    t_val = st.session_state.trust_ai
    if t_val >= 2:
        next_key = "ending_transcendence_1"
    elif t_val <= -2:
        next_key = "ending_vigil_1"
    else:
        next_key = "ending_abyss_1"
        
    if st.button("⏩ 前往結局 (Proceed to Ending)", use_container_width=True):
        st.session_state.current_node = next_key
        st.rerun()

elif node.get("is_ending"):
    st.success("🎉 本結局已播放完畢！感謝體驗《星淵信標：深空重啟》！")
    if st.button("🌟 重新開始探索其他結局 (Play Again)", use_container_width=True):
        restart_game()

else:
    col_prev, col_next = st.columns([1, 4])
    with col_next:
        if st.button("▶️ 繼續對話 (Next)", use_container_width=True):
            st.session_state.current_node = node.get("next", "prologue_1")
            st.rerun()

# -------------------------------------------------------------
# 歷史對話回顧 (Backlog History)
# -------------------------------------------------------------
with st.expander("📜 查看歷史對話紀錄 (Backlog History)"):
    for spk, txt in st.session_state.history:
        st.markdown(f"**【{spk}】**：{txt}")
