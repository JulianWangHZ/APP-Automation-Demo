<div align="center">

# 🚀 Swift Appium 測試框架

一個強大的 Swift 應用程式自動化測試框架，支援 iOS 平台。

[![Platform](https://img.shields.io/badge/Platform-iOS-blue)]()
[![Appium](https://img.shields.io/badge/Appium-2.0-purple)]()
[![Python](https://img.shields.io/badge/Python-3.x-yellow)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

[English](README.md) | [中文](README_zh.md)

</div>
## 📊 專案概覽

本框架為 Swift 應用程式提供全面的自動化測試，包含詳細報告和 CI/CD 整合。

### 🧪 最新測試報告

- **[iOS E2E 測試報告](https://ios-e2e-automation-demo.netlify.app)** - 查看最新 iOS 自動化測試結果

### 🚀 主要功能

- **iOS 平台支援**: 全面的 iOS 測試能力
- **自動化 CI/CD**: GitHub Actions 整合，支援排程和手動觸發
- **完整報告**: Allure 報告，提供詳細測試洞察
- **實體裝置測試**: BrowserStack 整合，支援實體裝置測試
- **元素檢查**: 多種元素定位和檢查工具

# 📋 目錄

- [🚀 Swift Appium 測試框架](#-swift-appium-測試框架)
  - [📊 專案概覽](#-專案概覽)
    - [🧪 最新測試報告](#-最新測試報告)
    - [🚀 主要功能](#-主要功能)
- [📋 目錄](#-目錄)
    - [必要軟體](#必要軟體)
    - [套件安裝](#套件安裝)
    - [Appium 設定](#appium-設定)
    - [WebDriverAgent 設定 (僅 iOS)](#webdriveragent-設定-僅-ios)
  - [執行測試](#執行測試)
    - [啟動 Appium 伺服器](#啟動-appium-伺服器)
    - [基本測試執行](#基本測試執行)
    - [報告生成命令](#報告生成命令)
    - [生成測試報告](#生成測試報告)
    - [📊 即時測試報告](#-即時測試報告)
    - [Appium Inspector](#appium-inspector)
      - [iOS {模擬器} 配置](#ios-模擬器-配置)
      - [iOS {實體裝置} 配置](#ios-實體裝置-配置)
    - [使用 Appium Inspector](#使用-appium-inspector)
    - [uiauto.dev 工具](#uiautodev-工具)
      - [前置需求](#前置需求)
      - [安裝](#安裝)
      - [啟動方式](#啟動方式)
      - [主要功能](#主要功能)
      - [配置步驟](#配置步驟)
      - [使用 uiauto.dev](#使用-uiautodev)
    - [查找裝置 UDID](#查找裝置-udid)

<h1 id="system-requirements">💻 系統需求</h1>

### 必要軟體

| 軟體    | 版本       | 用途     |
| ------- | ---------- | -------- |
| Xcode   | 15.4+      | iOS 測試 |
| Node.js | Latest LTS | 執行環境 |
| Python  | 3.x        | 測試腳本 |

### 套件安裝

<h1 id="installation-guide">🔧 安裝指南</h1>

### Appium 設定

```bash
# 全域安裝 Appium
npm install -g appium

# 安裝 iOS 驅動程式
appium driver install xcuitest
```

<h1 id="environment-setup">⚙️ 環境設定</h1>

1. **建立 Python 虛擬環境**

```bash
# 建立虛擬環境
python3 -m venv venv

# 啟動虛擬環境
# macOS/Linux:
source venv/bin/activate

# Windows:
# venv\Scripts\activate
```

2. **安裝依賴套件**

```bash
# 在虛擬環境中安裝依賴套件
pip install -r requirements.txt
```

3. **配置環境變數**

```bash
# .env
APPIUM_OS="ios"
IMPLICIT_WAIT=15
NO_RESET="True"
AUTO_ACCEPT_ALERTS="True"
IOS_APP_BUNDLE_ID=com.rafaelsoh.dime
IOS_APP_PATH="/path/to/your/Dime.app"
#UDID="4BEC1422-4429-4EAD-B850-C296B013A210" #可選
```

**注意：** 執行測試前請務必啟動虛擬環境：

```bash
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

### WebDriverAgent 設定 (僅 iOS)

1. 複製 [WebDriverAgent](https://github.com/appium/WebDriverAgent)
2. 在 Xcode 中開啟 WebDriverAgent.xcodeproj
3. 選擇 WebDriverAgentRunner 並執行測試

## 執行測試

1. **平台特定設定**

<details>
<summary>iOS 設定</summary>

1. 複製 WebDriverAgent:

```bash
git clone https://github.com/appium/WebDriverAgent
```

2. 在 Xcode 中開啟 WebDriverAgent.xcodeproj
3. 選擇 WebDriverAgentRunner 並執行測試
</details>

<h1 id="running-tests">🧨 執行測試</h1>

### 啟動 Appium 伺服器

```bash
# 本地啟動
appium
```

啟動 Appium 後，您應該會看到類似這樣的內容：

![Appium Server Started](./images/img1.png)

<h1 id="test-execution-commands">⌨️ 測試執行命令</h1>

### 基本測試執行

```bash
# 執行所有測試並顯示詳細輸出
pytest -v

# 執行帶有回歸標記的測試
pytest -k "regression"

# 按關鍵字執行測試
pytest -k "login_invalid_email"

# 執行特定測試檔案
pytest tests/steps/ios/test_01_ios_onboarding_steps.py
```

### 報告生成命令

```bash
# 執行測試並生成 Allure 報告 (基本)
pytest --alluredir=./allure-results

# 執行所有測試包括跳過的測試並生成 Allure 報告
pytest -v --alluredir=./allure-results

# 生成並開啟 Allure 報告
allure serve ./allure-results
```

<h1 id="test-execution-reports">📊 測試執行與報告</h1>

```bash
# 執行所有測試並生成 Allure 報告 (主要用途)
# 測試執行後會自動生成 allure 報告，然後將結果發送到 slack 頻道
pytest --alluredir=./allure-results

# 重新執行失敗的測試 (次要用途)
pytest --lf --alluredir=./allure-results --reruns 3
```

### 生成測試報告

```bash
# 生成靜態報告 (主要用途)
allure generate allure-results -o allure-report --clean

# 啟動報告伺服器 (次要用途)
allure serve allure-results
```

### 📊 即時測試報告

查看我們 CI/CD 管道的最新自動化測試結果：

- **[iOS E2E 測試報告](https://ios-e2e-automation-demo.netlify.app)** - 最新 iOS 測試結果，包含詳細洞察

這些報告在每次測試執行後自動生成並部署，提供：

- **測試統計**: 通過/失敗率和執行時間
- **詳細洞察**: 測試執行分析和趨勢
- **截圖**: 測試執行的視覺證據
- **錯誤詳情**: 全面的失敗分析

<h1 id="element-location-tools">🔍 元素定位工具</h1>

### Appium Inspector

- 下載 Appium Inspector
- 配置 Appium 伺服器
- 啟動 Appium 伺服器
- 啟動 Appium Inspector
- 配置期望功能

#### iOS {模擬器} 配置

```json
{
  "platformName": "ios",
  "appium:deviceName": "iPhone 15",
  "appium:automationName": "XCUITest",
  "appium:platformVersion": "17.2",
  "appium:app": "/path/to/your/ios/AppName.app",
  "appium:noReset": true,
  "appium:autoAcceptAlerts": true
}
```

#### iOS {實體裝置} 配置

```json
{
  "platformName": "ios",
  "appium:deviceName": "iPhone",
  "appium:automationName": "XCUITest",
  "appium:platformVersion": "17.5",
  "appium:udid": "YOUR-PERSONAL-UUID",
  "appium:noReset": true,
  "appium:autoAcceptAlerts": true
}
```

### 使用 Appium Inspector

<div align="center">
  <img src="./images/img2.png" alt="Appium Inspctor Tool" width="600">
</div>

### uiauto.dev 工具

[uiauto.dev](https://uiauto.dev/) 是一個強大的基於網頁的移動應用程式元素檢查工具。相比 Appium Inspector，它提供了更友善的使用者介面，並支援 iOS 平台。

#### 前置需求

- Python 3.8 或更高版本
- 本地運行的 Appium 伺服器

#### 安裝

```bash
# 安裝 uiauto.dev
pip3 install -U uiautodev
```

#### 啟動方式

```bash
# 方法 1: 直接命令
uiauto.dev

# 方法 2: Python 模組
python3 -m uiautodev
```

#### 主要功能

- 基於網頁的介面 (無需安裝)
- 即時元素檢查
- 支援 iOS
- 元素層次結構視覺化
- XPath 和無障礙 ID 生成
- 截圖捕獲和元素高亮

#### 配置步驟

1. 啟動您的 Appium 伺服器
2. 連接您的裝置或模擬器
3. 配置期望功能

#### 使用 uiauto.dev

1. 輸入您的 Appium 伺服器 URL (預設: http://localhost:4723)
2. 配置期望功能
3. 點擊 "Start Session"
4. 使用介面來：
   - 檢查元素
   - 生成定位器
   - 截圖
   - 查看元素層次結構

<div align="center">
  <img src="./images/uiauto-dev.png" alt="uiauto.dev Interface" width="600">
</div>

<h1 id="device-configuration">📱 裝置配置</h1>

### 查找裝置 UDID

```bash
# iOS 模擬器
xcrun simctl list devices
```

<h1 id="references">📚 參考資料</h1>

- [Appium 文件](https://appium.io/docs/en/latest/)
- [XCUITest 驅動程式](https://github.com/appium/appium-xcuitest-driver)

<h1 id="troubleshooting">❗ 故障排除</h1>

<details>
<summary>WebDriverAgent 安裝失敗</summary>

1. 檢查以下項目：

- 驗證 Xcode 命令列工具安裝
- 在 Xcode 中重新建置 WebDriverAgent
- 檢查簽名憑證
</details>

<details>
<summary>Appium 伺服器連接問題</summary>

1. 檢查以下項目：

- 驗證埠口配置
- 檢查伺服器權限
- 檢視伺服器日誌
</details>

---
