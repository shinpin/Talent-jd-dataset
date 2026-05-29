"""
industry_mapping.py
------------------------------------
公司名 → 產業類別代碼對照字典
用於將 JD 資料集去識別化，符合學術倫理與平台條款。

產業分類規則（依研究目的設計）：
- GAME    : 遊戲開發、遊戲美術、互動娛樂
- FINTECH : 金融科技、電子支付、加密貨幣、區塊鏈
- ECOM    : 電商、零售、社群行銷、本地服務
- SAAS    : SaaS 軟體服務、企業軟體、行銷工具
- AI      : AI 研發、機器學習、AI 平台
- HW      : 硬體製造、半導體、面板、光電
- BIOTECH : 生技醫療、健康科技
- DESIGN  : 設計工作室、品牌顧問
- GOV     : 政府機構（含香港）
- MEDIA   : 媒體、內容平台、社群
- TELECOM : 電信、網路通訊
- OTHER   : 其他（一般中小企業、無法明確歸類）
"""

# 公司名 → 產業類別代碼
# 為保護隱私，公開版本只提供分類規則，不揭露對照細節
INDUSTRY_MAP = {
    # === 2025-2026 樣本 ===
    '17Life_康太數位整合股份有限公司': 'ECOM',
    'AIFIAN': 'FINTECH',
    'Appier': 'AI',
    'Binance': 'FINTECH',
    'Garena': 'GAME',
    'Hububble 集客式行銷公司｜HubSpot 台灣最高等級代理商': 'SAAS',
    'KKday': 'ECOM',
    'Perfect Corp.': 'SAAS',
    'Proton': 'SAAS',
    'SWAG': 'MEDIA',
    'Shopee': 'ECOM',
    'TSMC 台積電': 'HW',
    'Taiwan AILabs': 'AI',
    'Ubiquiti Inc.': 'TELECOM',
    'Verkada': 'SAAS',
    'inline 樂排股份有限公司': 'SAAS',
    '世界瑰寶有限公司': 'OTHER',
    '佐臻股份有限公司': 'HW',
    '侍達遊戲藝術有限公司': 'GAME',
    '元祖實業股份有限公司': 'ECOM',
    '元越有限公司': 'OTHER',
    '友達光電股份有限公司': 'HW',
    '台灣天域科技股份有限公司': 'GAME',
    '哇哇科技股份有限公司': 'SAAS',
    '坤侑科技股份有限公司': 'OTHER',
    '天茶智能科技股份有限公司': 'AI',
    '奇雲國際股份有限公司': 'SAAS',
    '宇峻奧汀科技股份有限公司': 'GAME',
    '心果有限公司＿＿HeyMaster 找課程 / 烘焙找材料 / 焙日': 'ECOM',
    '數字科技股份有限公司': 'SAAS',
    '新加坡商鈦坦科技': 'SAAS',
    '新銳數位股份有限公司': 'SAAS',
    '日新技術有限公司': 'OTHER',
    '果思設計股份有限公司': 'DESIGN',
    '火龍數位科技遊戲有限公司': 'GAME',
    '王一互動科技有限公司': 'GAME',
    '珷琚科技有限公司': 'OTHER',
    '瑞盛數位科技股份有限公司': 'SAAS',
    '簡訊設計行銷有限公司（圖文不符｜志祺七七｜投募達集）': 'MEDIA',
    '精英電腦股份有限公司': 'HW',
    '網際智慧股份有限公司': 'SAAS',
    '聖祐遊戲股份有限公司': 'GAME',
    '華義國際數位娛樂股份有限公司': 'GAME',
    '街口電子支付股份有限公司': 'FINTECH',
    '裕順資訊有限公司': 'SAAS',
    '詠富國際數位有限公司': 'MEDIA',
    '賞霖創藝股份有限公司': 'DESIGN',
    '酷客創藝股份有限公司': 'DESIGN',
    '鏈星築夢有限公司': 'FINTECH',
    '非我設計｜UNME DESIGN': 'DESIGN',
    '風采有限公司': 'OTHER',
    '黑蓮生技有限公司': 'BIOTECH',

    # === 2023-2024 樣本 ===
    'UI設計師（台北，遊戲介面）': 'GAME',
    'Yourator平台統計（2023年台灣市場）': 'OTHER',
    '全球遊戲大廠（在台深耕10年以上）': 'GAME',
    '動區動趨 BlockTempo': 'MEDIA',
    '勝圖國際企業股份有限公司': 'DESIGN',
    '台北科技公司（CakeResume 社群刊登）': 'SAAS',
    '台灣科技新創公司（音樂模擬器）': 'SAAS',
    '台灣零售SaaS軟體服務商': 'SAAS',
    '好感設計有限公司': 'DESIGN',
    '娛樂手遊益智棋牌公司（上海，台灣招募）': 'GAME',
    '沃醫學股份有限公司': 'BIOTECH',
    '玩美行動股份有限公司': 'SAAS',
    '萬兩電子科技有限公司': 'HW',
    '裕順資訊有限公司': 'SAAS',
    '路政署（香港政府部門）': 'GOV',
    '鈊象電子股份有限公司': 'GAME',
    '香港教育局課程發展處': 'GOV',
    '香港零售集團（軟體服務部門）': 'SAAS',
}

# 平台代碼（去除具體 URL、改為平台類型）
PLATFORM_MAP = {
    '104': 'P_TW_01',         # 台灣綜合招募平台 A
    'cake': 'P_TW_02',        # 台灣科技人才平台 B
    'linkedin': 'P_INTL_01',  # 國際職涯平台 A
    'yourator': 'P_TW_03',    # 台灣新創平台 C
    '1111': 'P_TW_04',        # 台灣綜合招募平台 D
    'wayback': 'P_ARCHIVE',   # 網頁存檔（含 2023-24 歷史抽樣）
}

# 地區代碼（簡化精確地址至直轄市層級）
def normalize_region(loc: str) -> str:
    """精確地址 → 都會圈代碼"""
    if not loc:
        return 'TW_UNK'
    loc_lower = loc.lower()
    if 'taipei' in loc_lower or '台北' in loc or '北市' in loc:
        return 'TW_TPE'  # 台北都會圈
    if 'taichung' in loc_lower or '台中' in loc:
        return 'TW_TXG'  # 台中都會圈
    if 'kaohsiung' in loc_lower or '高雄' in loc:
        return 'TW_KHH'  # 高雄都會圈
    if 'hsinchu' in loc_lower or '新竹' in loc:
        return 'TW_HSZ'  # 新竹都會圈
    if 'hong kong' in loc_lower or '香港' in loc:
        return 'HK'
    if 'singapore' in loc_lower or '新加坡' in loc:
        return 'SG'
    if 'tw' in loc_lower or '台灣' in loc or '臺灣' in loc:
        return 'TW_OTHER'
    return 'OTHER'

# 薪資區間化（避免精確數字辨識特定職缺）
def bucketize_salary(low_twd, high_twd):
    """月薪（TWD）→ 區間代碼"""
    try:
        low = float(low_twd) if low_twd else None
        high = float(high_twd) if high_twd else None
    except (ValueError, TypeError):
        return 'UNDISCLOSED'
    if low is None and high is None:
        return 'UNDISCLOSED'
    mid = (low + high) / 2 if (low and high) else (low or high)
    if mid < 35000:    return 'A_lt35k'
    if mid < 45000:    return 'B_35_45k'
    if mid < 55000:    return 'C_45_55k'
    if mid < 70000:    return 'D_55_70k'
    if mid < 90000:    return 'E_70_90k'
    if mid < 120000:   return 'F_90_120k'
    return 'G_gte120k'
