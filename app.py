import streamlit as st
import streamlit.components.v1 as components
import json
import os

# -------------------------------------------------------------
# 載入內嵌資源 (保證在 Streamlit Cloud 零路徑失誤 100% 發聲與顯圖)
# -------------------------------------------------------------
try:
    from audio_data import AUDIO_BASE64
except ImportError:
    AUDIO_BASE64 = {}

try:
    from image_data import IMAGE_BASE64
except ImportError:
    IMAGE_BASE64 = {}

# -------------------------------------------------------------
# 頁面配置 (Page Configuration - 寬版無縫模式)
# -------------------------------------------------------------
st.set_page_config(
    page_title="星淵信標：深空重啟 (Beacon of the Abyss)",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------------------
# 自訂 CSS：消除 Streamlit 預設留白，實現 100% 滿版沉浸式體驗
# -------------------------------------------------------------
st.markdown("""
<style>
    .main .block-container {
        max-width: 100% !important;
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }
    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 2rem !important;
    }
    .stApp {
        background-color: #030712 !important;
        color: #f1f2f6;
    }
    section[data-testid="stSidebar"] {
        background-color: #0d1b2a !important;
        border-right: 1px solid rgba(0, 229, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 側邊欄控制台 (Sidebar HUD)
# -------------------------------------------------------------
with st.sidebar:
    st.title("🛰️ 艦橋系統控制台")
    st.markdown("---")
    st.info("💡 **操作指南**：\n- 點擊畫面任意處即可直接推進劇情\n- 電影旁白已改為極簡無框懸浮字幕\n- 空間折疊具備強烈震顫與低頻重轟鳴！\n- 遊戲結局通關後背景音樂自動關閉！")
    if st.button("🔄 重新載入遊戲 (Restart)", use_container_width=True):
        st.rerun()

# -------------------------------------------------------------
# 完整劇本資料庫
# -------------------------------------------------------------
STORY_DATA = [
    # 序幕 (Prologue - 純文字無框電影旁白)
    {
        "id": "prologue_1",
        "bg": "bg_beacon.jpg",
        "speaker": "電影旁白",
        "speaker_id": "narrator",
        "text": "地球曆 2387 年。太陽系外緣，柯伊伯帶邊界。",
        "voice": "voice_nar_prologue_01.mp3",
        "left": None, "center": None, "right": None
    },
    {
        "id": "prologue_2",
        "bg": "bg_beacon.jpg",
        "speaker": "電影旁白",
        "speaker_id": "narrator",
        "text": "深空科考艦『海伯利昂號』，已在無盡黑暗中航行了四百一十二天。",
        "voice": "voice_nar_prologue_02.mp3",
        "left": None, "center": None, "right": None
    },
    # 第一幕：海伯利昂號艦橋與核心成員介紹
    {
        "id": "intro_1",
        "bg": "bg_bridge.jpg",
        "speaker": "電影旁白",
        "speaker_id": "narrator",
        "text": "艦橋上，藍色的全息星圖微微閃爍著冰冷的光芒。",
        "voice": "voice_nar_ch1_01.mp3",
        "left": {"char": "noah", "state": "neutral"},
        "center": None,
        "right": {"char": "vivian", "state": "neutral"}
    },
    {
        "id": "intro_2",
        "bg": "bg_bridge.jpg",
        "speaker": "女助手 諾亞 (NOAH)",
        "speaker_id": "f2",
        "text": "指揮官，您好！我是艦載量子 AI 諾亞。全艦感知網絡與維生系統運作正常。",
        "voice": "voice_f2_01.mp3",
        "left": {"char": "noah", "state": "speaking"},
        "center": None,
        "right": {"char": "vivian", "state": "neutral"}
    },
    {
        "id": "intro_3",
        "bg": "bg_bridge.jpg",
        "speaker": "首席工程師 薇薇安",
        "speaker_id": "f1",
        "text": "哈囉艦長！我是首席動力工程師薇薇安！反物質引擎核心讀數一切平穩！",
        "voice": "voice_vivian_01.mp3",
        "left": {"char": "noah", "state": "neutral"},
        "center": None,
        "right": {"char": "vivian", "state": "speaking"}
    },
    {
        "id": "intro_4",
        "bg": "bg_bridge.jpg",
        "speaker": "指揮官 亞底斯",
        "speaker_id": "p",
        "text": "我是亞底斯。深空科考艦海伯利昂號，全系統就緒，準備執行深空探測任務。",
        "voice": "voice_artis_01.mp3",
        "left": {"char": "noah", "state": "neutral"},
        "center": {"char": "artis", "state": "speaking"},
        "right": {"char": "vivian", "state": "neutral"}
    },
    # 第一章：星艦艦橋的異變
    {
        "id": "ch1_1",
        "bg": "bg_bridge.jpg",
        "speaker": "女助手 諾亞 (NOAH)",
        "speaker_id": "f2",
        "text": "報告指揮官，深空重力波感測器在 0.3 光年外的無人星區，捕捉到了非自然週期性脈衝。",
        "voice": "voice_f2_ch1_01.mp3",
        "left": {"char": "noah", "state": "speaking"},
        "center": None,
        "right": {"char": "vivian", "state": "neutral"}
    },
    {
        "id": "ch1_2",
        "bg": "bg_bridge.jpg",
        "speaker": "首席工程師 薇薇安",
        "speaker_id": "f1",
        "text": "指揮官！反應爐核心讀數有些異常，這個脈衝正在與我們的反物質引擎產生同頻共振！",
        "voice": "voice_vivian_ch1_01.mp3",
        "left": {"char": "noah", "state": "neutral"},
        "center": None,
        "right": {"char": "vivian", "state": "speaking"}
    },
    {
        "id": "ch1_3",
        "bg": "bg_bridge.jpg",
        "speaker": "指揮官 亞底斯",
        "speaker_id": "p",
        "text": "能確定信號源的性質嗎？",
        "voice": "voice_artis_ch1_01.mp3",
        "left": {"char": "noah", "state": "neutral"},
        "center": {"char": "artis", "state": "speaking"},
        "right": {"char": "vivian", "state": "neutral"}
    },
    {
        "id": "ch1_4",
        "bg": "bg_bridge.jpg",
        "speaker": "女助手 諾亞 (NOAH)",
        "speaker_id": "f2",
        "text": "資料庫比對無匹配記錄。信號特徵符合高階量子星門結構，推測為十萬年前『先驅者文明』的古代信標。",
        "voice": "voice_f2_ch1_02.mp3",
        "left": {"char": "noah", "state": "alert"},
        "center": None,
        "right": {"char": "vivian", "state": "neutral"}
    },
    {
        "id": "ch1_5",
        "bg": "bg_bridge.jpg",
        "speaker": "首席工程師 薇薇安",
        "speaker_id": "f1",
        "text": "這太危險了！我們根本不知道那是陷阱還是武器，我建議立刻拉升偏轉護盾並掉頭返航！",
        "voice": "voice_vivian_ch1_02.mp3",
        "left": {"char": "noah", "state": "alert"},
        "center": None,
        "right": {"char": "vivian", "state": "panic"},
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
    {
        "id": "ch1_choice_a",
        "bg": "bg_bridge.jpg",
        "speaker": "指揮官 亞底斯",
        "speaker_id": "p",
        "text": "調整折躍引擎座標，我們前往信標中心。這可能是人類文明突破星際界限的唯一機會。",
        "voice": "voice_artis_ch1_b1.mp3",
        "left": {"char": "noah", "state": "neutral"},
        "center": {"char": "artis", "state": "speaking"},
        "right": {"char": "vivian", "state": "panic"}
    },
    {
        "id": "ch1_choice_a2",
        "bg": "bg_bridge.jpg",
        "speaker": "女助手 諾亞 (NOAH)",
        "speaker_id": "f2",
        "text": "航線已鎖定。正在進行超空間跳躍...",
        "voice": "voice_f2_ch1_b1.mp3",
        "left": {"char": "noah", "state": "speaking"},
        "center": None,
        "right": {"char": "vivian", "state": "panic"},
        "next_override": "beacon_1"
    },
    # 分支一 B
    {
        "id": "ch1_choice_b",
        "bg": "bg_bridge.jpg",
        "speaker": "指揮官 亞底斯",
        "speaker_id": "p",
        "text": "保持最高警戒，展開多相偏轉護盾，保持安全距離進行外圍探測。",
        "voice": "voice_artis_ch1_b2.mp3",
        "left": {"char": "noah", "state": "neutral"},
        "center": {"char": "artis", "state": "speaking"},
        "right": {"char": "vivian", "state": "neutral"}
    },
    {
        "id": "ch1_choice_b2",
        "bg": "bg_bridge.jpg",
        "speaker": "首席工程師 薇薇安",
        "speaker_id": "f1",
        "text": "明白！全艦進入二級戰備狀態！",
        "voice": "voice_vivian_ch1_b2.mp3",
        "left": {"char": "noah", "state": "neutral"},
        "center": None,
        "right": {"char": "vivian", "state": "speaking"},
        "next_override": "beacon_1"
    },
    # 第二章：古代外星晶體星門 (空間折疊震顫音效與強光震撼)
    {
        "id": "beacon_1",
        "bg": "bg_beacon.jpg",
        "speaker": "電影旁白",
        "speaker_id": "narrator",
        "sfx": "warp_rumble.mp3",
        "shake": True,
        "text": "伴隨著劇烈的空間折疊震顫，海伯利昂號脫離了超空間！",
        "voice": "voice_nar_beacon_01.mp3",
        "left": None, "center": None, "right": None
    },
    {
        "id": "beacon_2",
        "bg": "bg_beacon.jpg",
        "speaker": "電影旁白",
        "speaker_id": "narrator",
        "text": "在巨大的全息舷窗前，一座通體由藍色光晶鑄造的巨型環狀遺跡漂浮在深空中，散發著窒息的美感與壓迫感。",
        "voice": "voice_nar_beacon_02.mp3",
        "left": {"char": "noah", "state": "neutral"},
        "center": None,
        "right": {"char": "vivian", "state": "neutral"}
    },
    {
        "id": "beacon_3",
        "bg": "bg_beacon.jpg",
        "speaker": "女助手 諾亞 (NOAH)",
        "speaker_id": "f2",
        "text": "抵達目標節點：古代晶體星門【阿爾法信標】。檢測到信標內部傳來強烈的神經量子廣播，它正在嘗試與艦載 AI 及指揮官的大腦皮層建立同步。",
        "voice": "voice_f2_ch2_01.mp3",
        "left": {"char": "noah", "state": "speaking"},
        "center": None,
        "right": {"char": "vivian", "state": "neutral"}
    },
    {
        "id": "beacon_4",
        "bg": "bg_beacon.jpg",
        "speaker": "首席工程師 薇薇安",
        "speaker_id": "f1",
        "text": "艦長！能量讀數暴增了 300%！艦體外殼溫度正在失控上升，如果再不及時切斷，我們整艘船都會被同化！",
        "voice": "voice_vivian_ch2_01.mp3",
        "left": {"char": "noah", "state": "neutral"},
        "center": None,
        "right": {"char": "vivian", "state": "panic"},
        "choices": [
            {
                "label": "🌌 【決策二】同意進行量子同調，探索宇宙終極真相 (+2 AI 信任)",
                "target": "beacon_sync_1",
                "effect": {"trust_ai": 2}
            },
            {
                "label": "💥 【決策二】命令薇薇安發射超載脈衝，摧毀信標核心 (-2 AI 信任)",
                "target": "beacon_destroy_1",
                "effect": {"trust_ai": -2}
            }
        ]
    },
    # 分支二 A
    {
        "id": "beacon_sync_1",
        "bg": "bg_beacon.jpg",
        "speaker": "指揮官 亞底斯",
        "speaker_id": "p",
        "text": "諾亞，開放我的神經接口與你的核心算力，我們一同接納信標的數據庫！",
        "voice": "voice_artis_ch2_b1.mp3",
        "left": {"char": "noah", "state": "alert"},
        "center": {"char": "artis", "state": "speaking"},
        "right": {"char": "vivian", "state": "panic"}
    },
    {
        "id": "beacon_sync_2",
        "bg": "bg_beacon.jpg",
        "speaker": "女助手 諾亞 (NOAH)",
        "speaker_id": "f2",
        "text": "量子同調開始... 願星光指引我們...",
        "voice": "voice_f2_ch2_b1.mp3",
        "left": {"char": "noah", "state": "speaking"},
        "center": None,
        "right": {"char": "vivian", "state": "panic"},
        "next_override": "ending_flash"
    },
    # 分支二 B
    {
        "id": "beacon_destroy_1",
        "bg": "bg_beacon.jpg",
        "speaker": "指揮官 亞底斯",
        "speaker_id": "p",
        "sfx": "laser.mp3",
        "shake": True,
        "text": "薇薇安，全功率過載離子炮，立刻摧毀星門核心發射源！人類還沒準備好面對這個力量！",
        "voice": "voice_artis_ch2_b2.mp3",
        "left": {"char": "noah", "state": "alert"},
        "center": {"char": "artis", "state": "speaking"},
        "right": {"char": "vivian", "state": "panic"}
    },
    {
        "id": "beacon_destroy_2",
        "bg": "bg_beacon.jpg",
        "speaker": "首席工程師 薇薇安",
        "speaker_id": "f1",
        "text": "主炮充能完畢——開火！！",
        "voice": "voice_vivian_ch2_b2.mp3",
        "left": {"char": "noah", "state": "alert"},
        "center": None,
        "right": {"char": "vivian", "state": "speaking"},
        "next_override": "ending_flash"
    },
    # 結局判定閃光
    {
        "id": "ending_flash",
        "bg": "bg_beacon.jpg",
        "speaker": "電影旁白",
        "speaker_id": "narrator",
        "shake": True,
        "text": "一道刺目的強光，瞬間吞沒了整座星艦！",
        "voice": "voice_nar_ending_flash.mp3",
        "left": None, "center": None, "right": None,
        "next_eval": True
    },
    # 結局 A (遊戲結束自動關閉背景音樂)
    {
        "id": "ending_transcendence_1",
        "bg": "bg_beacon.jpg",
        "speaker": "結局 A：超越昇華 (Transcendence)",
        "speaker_id": "narrator",
        "text": "海伯利昂號與古代星門完成了完美共鳴。無數星系的知識流入指揮官與諾亞的意識之中，新的大航海時代就此揭開序幕。",
        "voice": "voice_nar_end_a_01.mp3",
        "left": {"char": "noah", "state": "neutral"},
        "center": None,
        "right": {"char": "vivian", "state": "neutral"},
        "is_ending": True
    },
    # 結局 B (遊戲結束自動關閉背景音樂)
    {
        "id": "ending_abyss_1",
        "bg": "bg_bridge.jpg",
        "speaker": "結局 B：迷航深淵 (Abyssal Drift)",
        "speaker_id": "narrator",
        "text": "信標引發了局域引力坍縮，海伯利昂號被拋射進未知的超深空維度，林指揮官與船員們只能凝視著無盡的星海，等待下一次奇蹟。",
        "voice": "voice_nar_end_b_01.mp3",
        "left": {"char": "noah", "state": "alert"},
        "center": None,
        "right": {"char": "vivian", "state": "panic"},
        "is_ending": True
    },
    # 結局 C (遊戲結束自動關閉背景音樂)
    {
        "id": "ending_vigil_1",
        "bg": "bg_bridge.jpg",
        "speaker": "結局 C：人類守望 (Eternal Vigil)",
        "speaker_id": "narrator",
        "text": "離子光束精準摧毀了信標核心，海伯利昂號滿載數據踏上歸途，繼續默默守護著太陽系邊疆的安寧。",
        "voice": "voice_nar_end_c_01.mp3",
        "left": {"char": "noah", "state": "neutral"},
        "center": None,
        "right": {"char": "vivian", "state": "neutral"},
        "is_ending": True
    }
]

story_json = json.dumps(STORY_DATA, ensure_ascii=False)
images_json = json.dumps(IMAGE_BASE64, ensure_ascii=False)
audio_json = json.dumps(AUDIO_BASE64, ensure_ascii=False)

# -------------------------------------------------------------
# 100% 滿版電影級劇院 (結局自動停止音樂)
# -------------------------------------------------------------
full_stage_html = f"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    * {{
        box-sizing: border-box;
        user-select: none;
        -webkit-user-select: none;
    }}
    html, body {{
        margin: 0;
        padding: 0;
        width: 100vw;
        height: 100vh;
        background: #030712;
        font-family: 'Microsoft JhengHei', 'PingFang TC', -apple-system, sans-serif;
        overflow: hidden;
    }}
    
    #vn-theater {{
        position: relative;
        width: 100vw;
        height: 98vh;
        background-color: #050811;
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        transition: background-image 0.5s ease-in-out;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        overflow: hidden;
        border-radius: 12px;
        border: 1px solid rgba(0, 229, 255, 0.3);
        box-shadow: 0 0 40px rgba(0, 229, 255, 0.15);
        cursor: pointer;
    }}

    .top-hud {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 24px;
        background: linear-gradient(180deg, rgba(3, 7, 18, 0.85) 0%, rgba(3, 7, 18, 0) 100%);
        z-index: 100;
    }}
    .game-title {{
        color: #00e5ff;
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-shadow: 0 0 12px rgba(0, 229, 255, 0.7);
    }}
    .hud-meters {{
        display: flex;
        gap: 20px;
        align-items: center;
    }}
    .meter-badge {{
        background: rgba(13, 27, 42, 0.85);
        border: 1px solid #00e5ff;
        border-radius: 20px;
        padding: 5px 14px;
        color: #f1f2f6;
        font-size: 0.9rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    .bgm-btn {{
        background: rgba(13, 27, 42, 0.85);
        border: 1px solid #00e5ff;
        color: #00e5ff;
        border-radius: 20px;
        padding: 5px 14px;
        font-size: 0.9rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    .bgm-btn:hover {{
        background: #00e5ff;
        color: #030712;
        box-shadow: 0 0 15px #00e5ff;
    }}

    .character-stage {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: flex-end;
        justify-content: space-around;
        padding-bottom: 210px;
        pointer-events: none;
        z-index: 10;
    }}
    .char-column {{
        flex: 1;
        height: 100%;
        display: flex;
        align-items: flex-end;
        justify-content: center;
    }}
    .char-sprite {{
        max-height: 520px;
        max-width: 90%;
        object-fit: contain;
        transition: transform 0.3s ease, filter 0.3s ease;
        filter: drop-shadow(0 0 12px rgba(0, 0, 0, 0.8));
    }}
    .active-speaker {{
        filter: drop-shadow(0 0 30px rgba(0, 229, 255, 0.9)) brightness(1.1);
        transform: scale(1.04);
    }}
    .silent-char {{
        filter: drop-shadow(0 0 8px rgba(0, 0, 0, 0.8)) brightness(0.68);
    }}

    @keyframes warpTremorAnim {{
        0% {{ transform: translate(0, 0) scale(1); filter: brightness(1); }}
        8% {{ transform: translate(-10px, 8px) scale(1.03); filter: brightness(3.0); }}
        16% {{ transform: translate(10px, -8px) scale(1.04); filter: brightness(2.2); }}
        24% {{ transform: translate(-8px, -6px) scale(1.03); filter: brightness(1.6); }}
        32% {{ transform: translate(8px, 6px) scale(1.02); filter: brightness(1.3); }}
        40% {{ transform: translate(-6px, 4px) scale(1.01); }}
        50% {{ transform: translate(6px, -4px) scale(1.01); }}
        65% {{ transform: translate(-3px, 2px) scale(1); }}
        80% {{ transform: translate(3px, -2px) scale(1); }}
        100% {{ transform: translate(0, 0) scale(1); filter: brightness(1); }}
    }}
    .screen-warp-tremor {{
        animation: warpTremorAnim 2.2s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
    }}

    @keyframes alertGlow {{
        0% {{ filter: drop-shadow(0 0 15px rgba(0, 229, 255, 0.6)); }}
        50% {{ filter: drop-shadow(0 0 35px rgba(0, 229, 255, 1.0)) brightness(1.18); }}
        100% {{ filter: drop-shadow(0 0 15px rgba(0, 229, 255, 0.6)); }}
    }}
    @keyframes panicShake {{
        0% {{ transform: translate(0, 0); }}
        25% {{ transform: translate(-3px, 2px); }}
        50% {{ transform: translate(3px, -2px); }}
        75% {{ transform: translate(-2px, -1px); }}
        100% {{ transform: translate(0, 0); }}
    }}
    .emotion-alert {{
        animation: alertGlow 1.5s infinite ease-in-out;
    }}
    .emotion-panic {{
        animation: panicShake 0.4s infinite ease-in-out;
    }}

    .bottom-hud {{
        position: relative;
        z-index: 50;
        padding: 0 30px 24px 30px;
        background: linear-gradient(0deg, rgba(3, 7, 18, 0.95) 0%, rgba(3, 7, 18, 0.5) 80%, rgba(3, 7, 18, 0) 100%);
    }}
    
    .dialogue-box.character-mode {{
        background: rgba(13, 27, 42, 0.88);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(0, 229, 255, 0.45);
        border-radius: 14px;
        padding: 20px 28px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.7);
        position: relative;
    }}
    
    .dialogue-box.narrator-mode {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        backdrop-filter: none !important;
        -webkit-backdrop-filter: none !important;
        padding: 10px 40px 18px 40px;
        text-align: center;
        position: relative;
    }}

    .name-badge {{
        display: inline-block;
        background: rgba(0, 229, 255, 0.22);
        color: #00e5ff;
        font-size: 1.3rem;
        font-weight: 800;
        padding: 4px 18px;
        border-radius: 6px;
        border-left: 4px solid #00e5ff;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }}

    .text-content.character-text {{
        font-size: 1.4rem;
        line-height: 1.7;
        color: #ffffff;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.95);
        letter-spacing: 0.5px;
        min-height: 55px;
    }}

    .text-content.narrator-text {{
        font-size: 1.55rem;
        line-height: 1.8;
        color: #f1f2f6;
        font-weight: 600;
        font-style: italic;
        letter-spacing: 1.2px;
        text-shadow: 
            2px 2px 6px rgba(0, 0, 0, 0.95),
            -2px -2px 6px rgba(0, 0, 0, 0.95),
            0 0 15px rgba(0, 229, 255, 0.4);
        min-height: 55px;
    }}

    .click-prompt {{
        position: absolute;
        right: 24px;
        bottom: 12px;
        font-size: 0.95rem;
        color: #00e5ff;
        font-weight: bold;
        animation: alertGlow 1s infinite alternate;
    }}

    .choices-overlay {{
        position: absolute;
        top: 40%;
        left: 50%;
        transform: translate(-50%, -50%);
        display: flex;
        flex-direction: column;
        gap: 16px;
        width: 80%;
        max-width: 720px;
        z-index: 200;
    }}
    .choice-btn {{
        background: linear-gradient(135deg, rgba(13, 27, 42, 0.95) 0%, rgba(27, 38, 59, 0.95) 100%);
        color: #f1f2f6;
        border: 1px solid #00e5ff;
        border-radius: 10px;
        font-size: 1.25rem;
        font-weight: 700;
        padding: 16px 28px;
        cursor: pointer;
        transition: all 0.25s ease;
        box-shadow: 0 4px 20px rgba(0, 229, 255, 0.25);
        text-align: left;
    }}
    .choice-btn:hover {{
        background: linear-gradient(135deg, #0984e3 0%, #00cec9 100%);
        color: #ffffff;
        box-shadow: 0 0 25px rgba(0, 229, 255, 0.8);
        transform: translateY(-2px);
    }}

    #start-gate {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle at center, #0a1128 0%, #030712 95%);
        z-index: 999;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 20px;
    }}
    .start-title {{
        color: #00e5ff;
        font-size: 2.8rem;
        font-weight: 900;
        text-shadow: 0 0 25px rgba(0, 229, 255, 0.8);
        text-align: center;
    }}
    .start-btn {{
        background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
        color: #ffffff;
        border: none;
        border-radius: 12px;
        font-size: 1.4rem;
        font-weight: 800;
        padding: 16px 42px;
        cursor: pointer;
        box-shadow: 0 0 30px rgba(0, 206, 201, 0.6);
        transition: all 0.3s ease;
    }}
    .start-btn:hover {{
        transform: scale(1.06);
        box-shadow: 0 0 45px rgba(0, 229, 255, 0.9);
    }}
</style>
</head>
<body>

<div id="vn-theater" onclick="handleStageClick(event)">
    <div id="start-gate">
        <div class="start-title">🌌 《星淵信標：深空重啟》</div>
        <p style="color: #a4b0be; font-size: 1.25rem;">100% 滿版電影級全語音互動式視覺小說</p>
        <button class="start-btn" onclick="startGame(event)">🚀 啟動艦橋通訊系統 (進入遊戲)</button>
    </div>

    <div class="top-hud">
        <div class="game-title">BEACON OF THE ABYSS // 星淵信標</div>
        <div class="hud-meters">
            <div class="meter-badge">🤖 AI 信任度: <span id="trust-val" style="color: #00e5ff; font-weight: bold;">0</span></div>
            <div class="meter-badge">⚡ 反物質能源: <span id="energy-val" style="color: #55efc4; font-weight: bold;">100%</span></div>
            <button class="bgm-btn" id="bgmToggleBtn" onclick="toggleBGM(event)">🎵 BGM: 播放中</button>
        </div>
    </div>

    <div class="character-stage">
        <div class="char-column" id="slot-left"></div>
        <div class="char-column" id="slot-center"></div>
        <div class="char-column" id="slot-right"></div>
    </div>

    <div id="choices-container" class="choices-overlay" style="display: none;"></div>

    <div class="bottom-hud">
        <div id="dialogue-box" class="dialogue-box character-mode">
            <div id="speaker-tag" class="name-badge">電影旁白</div>
            <div id="dialogue-text" class="text-content character-text">正在加載全艦感知網絡...</div>
            <div class="click-prompt">▼ 點擊畫面任意處繼續 (NEXT)</div>
        </div>
    </div>
</div>

<audio id="voiceAudio"></audio>
<audio id="sfxAudio"></audio>
<audio id="bgmAudio" loop></audio>

<script>
    const story = {story_json};
    const images = {images_json};
    const audios = {audio_json};

    let currentIndex = 0;
    let trustAI = 0;
    let shipEnergy = 100;
    let isBgmPlaying = false;
    let lipFlapTimer = null;
    let isMouthOpen = false;

    const theater = document.getElementById("vn-theater");
    const dialogueBox = document.getElementById("dialogue-box");
    const speakerTag = document.getElementById("speaker-tag");
    const dialogueText = document.getElementById("dialogue-text");
    const choicesContainer = document.getElementById("choices-container");
    const voiceAudio = document.getElementById("voiceAudio");
    const sfxAudio = document.getElementById("sfxAudio");
    const bgmAudio = document.getElementById("bgmAudio");
    const startGate = document.getElementById("start-gate");

    function getImageSrc(fn) {{
        if (!fn) return "";
        if (images[fn]) return images[fn];
        return "images/" + fn;
    }}

    function getAudioSrc(fn) {{
        if (!fn) return "";
        let base = fn.replace(/\.[^/.]+$/, "");
        let mp3Name = base + ".mp3";
        if (audios[mp3Name]) return "data:audio/mp3;base64," + audios[mp3Name];
        if (audios[fn]) return "data:audio/mp3;base64," + audios[fn];
        return "audio/" + mp3Name;
    }}

    function startGame(e) {{
        if (e) e.stopPropagation();
        startGate.style.display = "none";
        
        let bgmSrc = getAudioSrc("space_theme.mp3");
        if (bgmSrc) {{
            bgmAudio.src = bgmSrc;
            bgmAudio.volume = 0.35;
            bgmAudio.play().then(() => {{
                isBgmPlaying = true;
                const btn = document.getElementById("bgmToggleBtn");
                if (btn) btn.innerText = "🎵 BGM: 播放中";
            }}).catch(e => console.log(e));
        }}
        renderNode(0);
    }}

    function toggleBGM(e) {{
        if (e) e.stopPropagation();
        const btn = document.getElementById("bgmToggleBtn");
        if (isBgmPlaying) {{
            bgmAudio.pause();
            isBgmPlaying = false;
            btn.innerText = "🔇 BGM: 已暫停";
        }} else {{
            bgmAudio.play();
            isBgmPlaying = true;
            btn.innerText = "🎵 BGM: 播放中";
        }}
    }}

    function renderNode(index) {{
        if (index >= story.length) return;
        currentIndex = index;
        const node = story[index];

        // 🌟 遊戲結束自動停止背景音樂 (Auto Stop BGM on Game Ending)
        if (node.is_ending) {{
            bgmAudio.pause();
            bgmAudio.currentTime = 0;
            isBgmPlaying = false;
            const btn = document.getElementById("bgmToggleBtn");
            if (btn) btn.innerText = "🔇 BGM: 遊戲結束已停止";
        }}

        // 1. 背景滿版更換
        let bgSrc = getImageSrc(node.bg);
        if (bgSrc) {{
            theater.style.backgroundImage = "url('" + bgSrc + "')";
        }}

        // 2. 空間折疊劇烈震顫與音效觸發
        theater.classList.remove("screen-warp-tremor");
        if (node.shake) {{
            void theater.offsetWidth;
            theater.classList.add("screen-warp-tremor");
        }}

        if (node.sfx) {{
            let sfxSrc = getAudioSrc(node.sfx);
            if (sfxSrc) {{
                sfxAudio.src = sfxSrc;
                sfxAudio.volume = 1.0;
                sfxAudio.play().catch(e => console.log(e));
            }}
        }}

        // 3. 電影旁白 vs 角色發言介面風格切換
        if (node.speaker_id === "narrator") {{
            dialogueBox.className = "dialogue-box narrator-mode";
            speakerTag.style.display = "none";
            dialogueText.className = "text-content narrator-text";
        }} else {{
            dialogueBox.className = "dialogue-box character-mode";
            speakerTag.style.display = "inline-block";
            speakerTag.innerText = node.speaker;
            dialogueText.className = "text-content character-text";
        }}
        dialogueText.innerText = node.text;

        // 4. 角色立繪呈現與動態對嘴綁定
        renderSlot("slot-left", node.left, node.speaker_id == "f2");
        renderSlot("slot-center", node.center, node.speaker_id == "p");
        renderSlot("slot-right", node.right, node.speaker_id == "f1");

        // 5. 語音播放與嘴唇即時開闔
        if (lipFlapTimer) clearInterval(lipFlapTimer);
        
        let voiceSrc = getAudioSrc(node.voice);
        if (voiceSrc) {{
            voiceAudio.src = voiceSrc;
            voiceAudio.volume = 1.0;
            voiceAudio.play().then(() => {{
                startLipFlap(node.speaker_id);
            }}).catch(e => console.log(e));

            voiceAudio.onended = () => stopLipFlap(node.speaker_id);
            voiceAudio.onpause = () => stopLipFlap(node.speaker_id);
        }}

        // 6. 分支選單判定
        if (node.choices) {{
            choicesContainer.innerHTML = "";
            choicesContainer.style.display = "flex";
            node.choices.forEach(ch => {{
                let btn = document.createElement("button");
                btn.className = "choice-btn";
                btn.innerText = ch.label;
                btn.onclick = (e) => {{
                    e.stopPropagation();
                    if (ch.effect) {{
                        if (ch.effect.trust_ai) trustAI += ch.effect.trust_ai;
                        if (ch.effect.ship_energy) shipEnergy += ch.effect.ship_energy;
                        updateMeters();
                    }}
                    choicesContainer.style.display = "none";
                    jumpToId(ch.target);
                }};
                choicesContainer.appendChild(btn);
            }});
        }} else {{
            choicesContainer.style.display = "none";
        }}
    }}

    function renderSlot(slotId, charObj, isSpeaker) {{
        const slot = document.getElementById(slotId);
        if (!charObj) {{
            slot.innerHTML = "";
            return;
        }}
        let cName = charObj.char;
        let cState = charObj.state;
        let fn = cName + "_" + cState + ".png";
        let src = getImageSrc(fn);
        if (!src) src = getImageSrc(cName + "_neutral.png");

        let activeClass = isSpeaker ? "active-speaker" : "silent-char";
        let emotionClass = "";
        if (cState == "alert") emotionClass = "emotion-alert";
        if (cState == "panic") emotionClass = "emotion-panic";

        slot.innerHTML = `<img id="img-${{cName}}" src="${{src}}" class="char-sprite ${{activeClass}} ${{emotionClass}}">`;
    }}

    function startLipFlap(speakerId) {{
        let charName = "";
        if (speakerId == "f2") charName = "noah";
        else if (speakerId == "f1") charName = "vivian";
        else if (speakerId == "p") charName = "artis";
        else return;

        const img = document.getElementById("img-" + charName);
        if (!img) return;

        const neutralSrc = getImageSrc(charName + "_neutral.png");
        const speakingSrc = getImageSrc(charName + "_speaking.png");

        if (lipFlapTimer) clearInterval(lipFlapTimer);
        lipFlapTimer = setInterval(() => {{
            isMouthOpen = !isMouthOpen;
            img.src = isMouthOpen ? speakingSrc : neutralSrc;
        }}, 180);
    }}

    function stopLipFlap(speakerId) {{
        if (lipFlapTimer) clearInterval(lipFlapTimer);
        let charName = "";
        if (speakerId == "f2") charName = "noah";
        else if (speakerId == "f1") charName = "vivian";
        else if (speakerId == "p") charName = "artis";
        else return;

        const img = document.getElementById("img-" + charName);
        if (img) {{
            img.src = getImageSrc(charName + "_neutral.png");
        }}
    }}

    function handleStageClick(e) {{
        const node = story[currentIndex];
        if (node.choices && choicesContainer.style.display != "none") return;
        
        if (node.next_eval) {{
            if (trustAI >= 2) jumpToId("ending_transcendence_1");
            else if (trustAI <= -2) jumpToId("ending_vigil_1");
            else jumpToId("ending_abyss_1");
            return;
        }}

        if (node.next_override) {{
            jumpToId(node.next_override);
            return;
        }}

        // 結局播放完畢確認
        if (node.is_ending) {{
            if (confirm("🎉 本結局已播放完畢！是否重新開始探索其他結局？")) {{
                trustAI = 0;
                shipEnergy = 100;
                updateMeters();
                // 重新播放 BGM
                let bgmSrc = getAudioSrc("space_theme.mp3");
                if (bgmSrc) {{
                    bgmAudio.src = bgmSrc;
                    bgmAudio.volume = 0.35;
                    bgmAudio.play().then(() => {{
                        isBgmPlaying = true;
                        const btn = document.getElementById("bgmToggleBtn");
                        if (btn) btn.innerText = "🎵 BGM: 播放中";
                    }}).catch(e => console.log(e));
                }}
                renderNode(0);
            }}
            return;
        }}

        renderNode(currentIndex + 1);
    }}

    function jumpToId(targetId) {{
        let idx = story.findIndex(n => n.id === targetId);
        if (idx !== -1) {{
            renderNode(idx);
        }}
    }}

    function updateMeters() {{
        document.getElementById("trust-val").innerText = (trustAI >= 0 ? "+" : "") + trustAI;
        document.getElementById("energy-val").innerText = shipEnergy + "%";
    }}
</script>
</body>
</html>
"""

# 渲染 100% 滿版沉浸式 HTML5 視覺小說劇院
components.html(full_stage_html, height=750, scrolling=False)
