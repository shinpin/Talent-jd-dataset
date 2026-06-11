# JD Coded Dataset for AJF Framework Study

> **大中華區美術設計人才市場職缺編碼資料集 (2025-2026)**
> JD × AJF 三維交叉比對 ｜ Talent- 人才策略系列 v3.0

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20444031.svg)](https://doi.org/10.5281/zenodo.20444031)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Status: v3.0](https://img.shields.io/badge/Status-v3.0-green.svg)]()

---

## 📥 Quick Access / 快速下載

> 審查委員、評審教授請由此直接取得論文與簡報

| 項目 | 連結 | 說明 |
|---|---|---|
| 📄 **論文全文** | [下載 PDF](https://github.com/shinpin/Talent-jd-dataset/blob/main/paper/115076_%E6%9D%8E%E4%B8%96%E5%BD%AC_AI%E6%99%82%E4%BB%A3%E7%BE%8E%E8%A1%93%E8%81%B7%E8%83%BD%E8%AE%8A%E5%8C%96%E4%B9%8B%E6%8E%A2%E7%B4%A2%E6%80%A7%E7%A0%94%E7%A9%B6.pdf) | AI 時代美術職能變化之探索性研究（SLTM 2026） |
| 📊 **研究簡報** | [下載 PPTX](https://github.com/shinpin/Talent-jd-dataset/blob/main/slides/%E7%B0%A1%E5%A0%B1_AI%20%E6%99%82%E4%BB%A3%20%E7%BE%8E%E8%A1%93%E8%81%B7%E8%83%BD%E8%AE%8A%E5%8C%96%20%E4%B9%8B%E6%8E%A2%E7%B4%A2%E6%80%A7%E7%A0%94%E7%A9%B6_Final_P23_0611_s.pptx) | SLTM 2026 發表簡報（P23） |
| 🗃️ **研究資料集** | [Zenodo DOI](https://doi.org/10.5281/zenodo.20444031) | JD 編碼資料集 v3（含附錄 A、B） |

---

## 📋 基本資訊

| 項目 | 內容 |
|---|---|
| **論文** | AI 時代美術職能變化之探索性研究 |
| **作者** | 李世彬（Lee Ben） |
| **機構** | 華梵大學 美術與文創學系（跨智慧科技學系） |
| **指導教授** | 唐政元 教授 |
| **會議** | 2026 智慧生活科技與管理研討會（SLTM 2026） |
| **聯絡** | benarcell@gmail.com |
| **版本** | v3.0 |
| **發布日期** | 2026-06-11 |
| **Zenodo Concept DOI** | [10.5281/zenodo.20444031](https://doi.org/10.5281/zenodo.20444031) |
| **Zenodo v3 DOI** | [10.5281/zenodo.20650060](https://doi.org/10.5281/zenodo.20650060) |

---

## ⚠️ 使用限制聲明（請先閱讀）

**本資料集為探索性研究樣本（n=51），有以下重要限制與規範，使用前請務必了解：**

### 🔴 樣本限制

- 樣本數量：**51 筆**（現況 31 + 基線 20），屬**質性探索**範疇，**不具大規模統計代表性**
- 取樣範圍：大中華地區（台灣為主）2025/5 – 2026/5
- 抽樣方法：詳見 [METHODOLOGY.md](METHODOLOGY.md)，請務必閱讀後再行推論

### 🟡 使用須知（依 CC BY 4.0 授權）

| 您可以做 ✅ | 您不可以做 ❌ |
|---|---|
| 下載、複製、散布 | 嘗試逆向工程還原原始公司或職缺 |
| 修改、改作、重組 | 在未閱讀 METHODOLOGY 情況下做大樣本推論 |
| 商業使用 | 移除或偽造原作者署名 |
| 在新研究中引用 | 未標註本資料集之 DOI 而再利用 |

### 📝 引用要求

**請在任何使用本資料集的論文、報告、簡報中標明來源：**

```bibtex
@dataset{lee_2026_jd_ajf,
  author       = {李世彬 and Lee, Shih-Pin (Ben)},
  title        = {JD Coded Dataset for AJF Framework Study},
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v3},
  doi          = {10.5281/zenodo.20444031},
  url          = {https://doi.org/10.5281/zenodo.20444031}
}
```

中文引用格式：

```
李世彬 (2026)。JD Coded Dataset for AJF Framework Study (v3)
[資料集]。Zenodo。https://doi.org/10.5281/zenodo.20444031
```

---

## 📂 檔案結構

```
Talent-jd-dataset/
├── README.md                  ← 本文件
├── CODEBOOK.md                ← ⭐ 欄位定義與編碼規則
├── METHODOLOGY.md             ← ⭐ 取樣方法與分析步驟
├── APPENDIX_II_compliant.md   ← 論文附錄二 (合規版)
├── CHANGELOG.md               ← 版本更新記錄
├── LICENSE.txt                ← CC BY 4.0 授權全文
├── paper/
│   └── 115076_李世彬_AI時代美術職能變化之探索性研究.pdf  ← ⭐ 論文全文
├── slides/
│   └── 簡報_AI 時代 美術職能變化 之探索性研究_Final_P23_0611_s.pptx  ← ⭐ 發表簡報
├── data/
│   ├── jd_master_coded_v1.csv             ← 主資料集
│   ├── jd_master_coded_v1.json
│   ├── jd_2025_2026_coded.csv             ← 現況樣本 (31 筆)
│   ├── jd_2025_2026_coded.json
│   ├── jd_2023_2024_baseline_coded.csv    ← 基線對照 (20 筆)
│   └── jd_2023_2024_baseline_coded.json
└── scripts/
    ├── industry_mapping.py    ← 公司→產業類別映射（不含公司名）
    └── anonymize.py           ← 去識別化 ETL 程式
```

---

## 🔒 隱私與合規

### 已去識別化處理

本資料集為**研究者再加工後之編碼樣本**，**不含**下列原始資訊：

- ❌ 公司名稱（以 12 類產業代碼取代）
- ❌ 職缺完整文字 / 工作內容描述
- ❌ 職缺原始連結（URL）
- ❌ 來源平台名稱（以平台屬性代碼取代）
- ❌ 任何聯絡人個資（姓名、Email、電話）
- ❌ 精確發布日期（僅保留年份）

### 合規依據

1. **平台服務條款**：不重新發布、不商業性散布原始職缺內容
2. **著作權法**：採用「研究目的之合理使用」，僅公開編碼後之結構化結果
3. **個資法**：未涉及任何自然人個資；公司資訊以類別代碼揭露
4. **學術倫理**：研究結果可重現性以方法論說明 + 編碼資料達成

### 申請查閱原始資料（同行驗證）

若您為學術研究目的，須查閱原始資料以進行同行驗證：

- **Email**：benarcell@gmail.com
- **主旨**：`[AJF Dataset Verification Request] 您的姓名 / 機構`
- **需附**：研究計畫摘要、IRB 編號（若適用）、使用目的

作者將於 14 日內回覆。經審核後以**保密同意書（NDA）**方式提供查驗管道，**不直接傳輸原始檔案**。

---

## 🔄 版本管理（三層架構）

| 層次 | 用途 | 連結 |
|---|---|---|
| **GitHub** | 版本控制 + 開發歷史 | 本 Repo |
| **Zenodo** | 學術引用（不變的 DOI） | [Concept DOI](https://doi.org/10.5281/zenodo.20444031) |
| **pplx.app** | 互動式分析閱讀（個人開放） | (內部使用) |

### 版本歷史

| 版本 | 日期 | DOI | 變更摘要 |
|---|---|---|---|
| v3.0 | 2026-06-11 | [zenodo.20650060](https://doi.org/10.5281/zenodo.20650060) | 新增 SLTM 2026 論文全文 PDF 及發表簡報 |
| v2.0 | 2026-06-08 | [zenodo.20587461](https://doi.org/10.5281/zenodo.20587461) | 新增附錄 A（跨職能驗證 N=62）、附錄 B（Persona×LLM 模擬） |
| v1.0 | 2026-05-29 | [zenodo.20444032](https://doi.org/10.5281/zenodo.20444032) | 首次發布 |

詳見 [CHANGELOG.md](CHANGELOG.md)

---

## 🛠 相關工具

- **合規檢查工具**：[Talent-tool-compliance-checker](https://github.com/shinpin/Talent-tool-compliance-checker)（私人）— 用於本資料集每次更新前的合規自動掃描

---

## 🙏 致謝

感謝**唐政元教授**之指導，以及**華梵大學跨智慧科技學系**提供之研究環境。本研究未接受任何商業組織之資金或資料贊助。

---

## 📜 授權

本資料集採用 [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) 授權。詳見 [LICENSE.txt](LICENSE.txt)。
