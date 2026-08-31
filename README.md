# 🌌 《星淵信標：深空重啟》Streamlit 雲端視覺小說 Web 應用程式

這是一個可直接一鍵部署至 **[Streamlit Community Cloud (免費)](https://share.streamlit.io)** 的線上視覺小說 (Web Visual Novel)。

---

## 📁 專案目錄結構

```text
streamlit_web_vn/
│
├── app.py                      # Streamlit 核心視覺小說互動引擎
├── requirements.txt            # Python 雲端依賴套件 (streamlit, Pillow)
├── .streamlit/
│   └── config.toml             # 暗黑科幻主題色彩配置
│
├── images/                     # 100% 透明去背立繪 (PNG) 與 1080P 背景圖 (JPG)
└── audio/                      # AI 角色配音 (WAV/MP3) 與背景音樂 (BGM)
```

---

## 🚀 如何免費部署至 Streamlit Cloud 並取得永久專屬網址？

### 步驟 1：建立 GitHub 倉庫 (Repository)
1. 登入 [GitHub](https://github.com/)，點擊右上角 **【New repository】**。
2. 填寫倉庫名稱（例如：`beacon-of-the-abyss`），設為 **Public**，點擊 **【Create repository】**。
3. 將本資料夾 (`streamlit_web_vn`) 內的所有檔案與資料夾上傳至該 GitHub 倉庫。

### 步驟 2：登入 Streamlit Community Cloud
1. 前往 **[share.streamlit.io](https://share.streamlit.io/)**。
2. 點擊 **【Continue with GitHub】** 進行登入。

### 步驟 3：一鍵部署新應用 (Deploy an app)
1. 點擊右上角的 **【New app】** 按鈕。
2. 在設定欄位中填寫：
   - **Repository**：選擇您剛剛建立的 GitHub 倉庫（例如：`您的帳號/beacon-of-the-abyss`）。
   - **Branch**：`main`
   - **Main file path**：`app.py`
   - **App URL (選填)**：可自訂您的永久專屬網址（例如：`beacon-abyss.streamlit.app`）。
3. 點擊 **【Deploy!】** 按鈕。

---

### 🎉 大功告成！
等待 1 ~ 2 分鐘編譯完成後，Streamlit 會為您產生一個 **永久有效、免伺服器費用的公開網址 (HTTPS)**：
👉 **`https://your-custom-name.streamlit.app`**

全球任何人打開此網址，都可以直接在手機、平板或電腦瀏覽器中暢玩您的視覺小說！
