"""
anonymize.py
------------------------------------
將原始 JD 資料轉換為符合學術倫理的去識別化編碼版本。

去識別化處理：
  公司名稱      → 產業類別代碼（GAME, FINTECH, SAAS, ...）
  原始 JD 文案  → 完全移除（保留結構性技能標籤）
  URL          → 平台類型代碼（P_TW_01, P_INTL_01, ...）
  精確地點      → 都會圈代碼（TW_TPE, TW_HSZ, HK, ...）
  精確薪資      → 薪資區間代碼（A_lt35k, B_35_45k, ...）
  職稱          → 移除前綴公司名後的標準化職稱

保留欄位：
  研究編碼 ID, 年份, 產業類別, 都會圈, 職涯層級,
  薪資區間, AI 工具標記, 軟體工具（標準化）,
  L1-L4 技能分類, AJF Step 標記
"""

import json
import csv
import sys
from pathlib import Path
from collections import OrderedDict

sys.path.insert(0, str(Path(__file__).parent))
from industry_mapping import INDUSTRY_MAP, PLATFORM_MAP, normalize_region, bucketize_salary

# 載入論文方法論裡的技能分層字典
SKILL_TIER_MAP = {
    # L1 純執行層 (純技術操作)
    'Photoshop': 'L1', 'Illustrator': 'L1', 'InDesign': 'L1',
    'After Effects': 'L1', 'Premiere': 'L1', 'Sketch': 'L1',
    'Figma': 'L1', 'XD': 'L1', 'Canva': 'L1', 'Procreate': 'L1',
    '3ds Max': 'L1', 'Maya': 'L1', 'Blender': 'L1', 'ZBrush': 'L1',
    'Unity': 'L1', 'Unreal': 'L1', 'Substance': 'L1', 'Spine': 'L1',
    'Excel': 'L1', 'PowerPoint': 'L1', 'Word': 'L1',
    'HTML': 'L1', 'CSS': 'L1', 'HTML/CSS': 'L1',
    'Icon': 'L1', 'Banner': 'L1', '修圖': 'L1', '排版': 'L1',
    '平面設計': 'L1', '插畫': 'L1', '粒子系統': 'L1',
    '動態設計': 'L1', '動畫設計': 'L1', '資訊圖表設計': 'L1',

    # L2 應用層（執行 + 部分判斷）
    'UI設計': 'L2', 'UX設計': 'L2', 'UI/UX設計': 'L2',
    '使用者介面設計': 'L2', '使用者體驗設計': 'L2',
    '視覺設計': 'L2', '品牌設計': 'L2', '識別設計': 'L2',
    '網頁設計': 'L2', 'App 設計': 'L2',
    '原型設計': 'L2', '線框圖': 'L2', '互動設計': 'L2',
    '社群經營': 'L2', '廣告投放': 'L2', '內容行銷': 'L2',
    '作品集': 'L2',

    # L3 軟技能（溝通協作）
    '溝通協調': 'L3', '溝通能力': 'L3', '簡報能力': 'L3',
    '跨部門合作': 'L3', '跨部門協調': 'L3', '團隊合作': 'L3',
    '主動積極': 'L3', '抗壓性': 'L3', '時間管理': 'L3',
    '細心': 'L3', '邏輯思考': 'L3', '創意發想': 'L3',
    '需求訪談': 'L3', '使用者研究': 'L3',

    # L4 判斷層（風格、標框、創意方向、品質判斷）
    '提案': 'L4_A', '提案能力': 'L4_A',  # Step A 啟用
    '風格制定': 'L4_J', '視覺風格': 'L4_J', '美術風格': 'L4_J',
    '品質標框': 'L4_J', '品質標準': 'L4_J', '品質判斷': 'L4_J',
    '設計規範': 'L4_J', 'Design System': 'L4_J',
    '創意方向': 'L4_F', '創意總監': 'L4_F', '美術指導': 'L4_F',
    '設計策略': 'L4_F', '行業標框': 'L4_F',
    'Workflow 設計': 'L4_J', '流程設計': 'L4_J',

    # AI 工具操作（獨立分類）
    'AI生成': 'AI', 'Midjourney': 'AI', 'Stable Diffusion': 'AI',
    'ChatGPT': 'AI', 'GPT': 'AI', 'Claude': 'AI',
    'AI 工具': 'AI', 'AI工具': 'AI', '生成式 AI': 'AI',
}

def classify_skill(skill: str) -> str:
    """技能字串 → 層級代碼"""
    skill = skill.strip()
    if skill in SKILL_TIER_MAP:
        return SKILL_TIER_MAP[skill]
    # 模糊比對
    for key, tier in SKILL_TIER_MAP.items():
        if key.lower() in skill.lower() or skill.lower() in key.lower():
            return tier
    return 'UNCLASSIFIED'

def normalize_title(title: str, company: str) -> str:
    """移除公司前綴的標準化職稱"""
    if not title:
        return 'UNKNOWN'
    # 移除常見公司名前綴
    for prefix in [company, company.split(' ')[0] if ' ' in company else '']:
        if prefix and prefix in title:
            title = title.replace(prefix, '').strip(' ｜|【】[]()／/-—–·:：')
    return title[:60]  # 截斷以免太長

def encode_skills(skills_str: str) -> dict:
    """將分號分隔的技能字串 → 層級計數"""
    if not skills_str:
        return {'L1': [], 'L2': [], 'L3': [], 'L4_A': [], 'L4_J': [], 'L4_F': [], 'AI': [], 'UNCLASSIFIED': []}
    skills = [s.strip() for s in skills_str.replace('、', ';').replace(',', ';').split(';') if s.strip()]
    bucket = {'L1': [], 'L2': [], 'L3': [], 'L4_A': [], 'L4_J': [], 'L4_F': [], 'AI': [], 'UNCLASSIFIED': []}
    for s in skills:
        tier = classify_skill(s)
        bucket[tier].append(s)
    return bucket

# ============================================
# 主要 ETL：2025-2026 主資料集
# ============================================
def anonymize_main_csv(input_path: str, output_csv: str, output_json: str):
    with open(input_path, encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))

    coded_rows = []
    for i, r in enumerate(rows, 1):
        company = r['Company'].strip()
        industry = INDUSTRY_MAP.get(company, 'OTHER')
        platform = PLATFORM_MAP.get(r['Source'].lower().strip(), 'P_UNKNOWN')

        all_skills_str = '; '.join(filter(None, [
            r.get('Software/Tools', ''),
            r.get('Hard Skills', ''),
            r.get('Soft Skills', ''),
        ]))
        skill_buckets = encode_skills(all_skills_str)

        ajf_step_a = bool(skill_buckets['L4_A'])
        ajf_step_j = bool(skill_buckets['L4_J'])
        ajf_step_f = bool(skill_buckets['L4_F'])

        coded = OrderedDict([
            ('coded_id', f'JD-2025-{i:03d}'),
            ('year', 2025),
            ('industry_code', industry),
            ('region_code', normalize_region(r['Location'])),
            ('platform_code', platform),
            ('category', r['Category']),
            ('seniority', r.get('Seniority', 'UNKNOWN')),
            ('years_required_min', r.get('Years Required', '')),
            ('salary_bucket', bucketize_salary(r.get('Monthly Low (TWD)'), r.get('Monthly High (TWD)'))),
            ('skill_count_L1', len(skill_buckets['L1'])),
            ('skill_count_L2', len(skill_buckets['L2'])),
            ('skill_count_L3', len(skill_buckets['L3'])),
            ('skill_count_L4_A', len(skill_buckets['L4_A'])),
            ('skill_count_L4_J', len(skill_buckets['L4_J'])),
            ('skill_count_L4_F', len(skill_buckets['L4_F'])),
            ('skill_count_AI', len(skill_buckets['AI'])),
            ('skill_count_unclassified', len(skill_buckets['UNCLASSIFIED'])),
            ('ajf_step_a_triggered', ajf_step_a),
            ('ajf_step_j_triggered', ajf_step_j),
            ('ajf_step_f_triggered', ajf_step_f),
            ('skills_L1', '; '.join(skill_buckets['L1'])),
            ('skills_L2', '; '.join(skill_buckets['L2'])),
            ('skills_L3', '; '.join(skill_buckets['L3'])),
            ('skills_L4', '; '.join(skill_buckets['L4_A'] + skill_buckets['L4_J'] + skill_buckets['L4_F'])),
            ('skills_AI', '; '.join(skill_buckets['AI'])),
        ])
        coded_rows.append(coded)

    # 輸出 CSV
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(coded_rows[0].keys()))
        writer.writeheader()
        writer.writerows(coded_rows)

    # 輸出 JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(coded_rows, f, ensure_ascii=False, indent=2)

    print(f'[✓] {len(coded_rows)} 筆 2025 樣本已編碼')
    return coded_rows

# ============================================
# 2023-2024 歷史基線資料
# ============================================
def anonymize_historical_json(input_path: str, output_csv: str, output_json: str):
    with open(input_path, encoding='utf-8') as f:
        data = json.load(f)

    coded_rows = []
    for i, d in enumerate(data, 1):
        company = d.get('company', '').strip()
        industry = INDUSTRY_MAP.get(company, 'OTHER')
        platform_raw = d.get('source_platform', '').lower()
        # 從 source_platform 推斷
        if 'cake' in platform_raw: platform = 'P_TW_02'
        elif '104' in platform_raw: platform = 'P_TW_01'
        elif 'linkedin' in platform_raw: platform = 'P_INTL_01'
        elif 'yourator' in platform_raw: platform = 'P_TW_03'
        elif '1111' in platform_raw: platform = 'P_TW_04'
        elif 'wayback' in platform_raw or 'archive' in platform_raw: platform = 'P_ARCHIVE'
        else: platform = 'P_UNKNOWN'

        skills_raw = d.get('required_skills', [])
        if isinstance(skills_raw, list):
            all_skills_str = '; '.join(skills_raw)
        else:
            all_skills_str = str(skills_raw)
        skill_buckets = encode_skills(all_skills_str)

        # 薪資處理
        salary = d.get('salary', '')
        salary_bucket = 'UNDISCLOSED'
        if salary:
            # 嘗試解析 "40,000-50,000" 之類格式
            import re
            nums = re.findall(r'(\d{2,3}[,，]?\d{0,3})', str(salary).replace('K', '000').replace('k', '000'))
            if nums:
                clean_nums = [int(n.replace(',', '').replace('，', '')) for n in nums if n]
                if len(clean_nums) >= 2:
                    salary_bucket = bucketize_salary(clean_nums[0], clean_nums[1])
                elif len(clean_nums) == 1:
                    salary_bucket = bucketize_salary(clean_nums[0], clean_nums[0])

        coded = OrderedDict([
            ('coded_id', f'JD-2023-{i:03d}'),
            ('year', d.get('year', 2023)),
            ('industry_code', industry),
            ('region_code', normalize_region(d.get('location', ''))),
            ('platform_code', platform),
            ('category', 'design'),
            ('seniority', d.get('experience_years', 'UNKNOWN')),
            ('years_required_min', d.get('experience_years', '')),
            ('salary_bucket', salary_bucket),
            ('skill_count_L1', len(skill_buckets['L1'])),
            ('skill_count_L2', len(skill_buckets['L2'])),
            ('skill_count_L3', len(skill_buckets['L3'])),
            ('skill_count_L4_A', len(skill_buckets['L4_A'])),
            ('skill_count_L4_J', len(skill_buckets['L4_J'])),
            ('skill_count_L4_F', len(skill_buckets['L4_F'])),
            ('skill_count_AI', len(skill_buckets['AI'])),
            ('skill_count_unclassified', len(skill_buckets['UNCLASSIFIED'])),
            ('ajf_step_a_triggered', bool(skill_buckets['L4_A'])),
            ('ajf_step_j_triggered', bool(skill_buckets['L4_J'])),
            ('ajf_step_f_triggered', bool(skill_buckets['L4_F'])),
            ('skills_L1', '; '.join(skill_buckets['L1'])),
            ('skills_L2', '; '.join(skill_buckets['L2'])),
            ('skills_L3', '; '.join(skill_buckets['L3'])),
            ('skills_L4', '; '.join(skill_buckets['L4_A'] + skill_buckets['L4_J'] + skill_buckets['L4_F'])),
            ('skills_AI', '; '.join(skill_buckets['AI'])),
        ])
        coded_rows.append(coded)

    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(coded_rows[0].keys()))
        writer.writeheader()
        writer.writerows(coded_rows)
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(coded_rows, f, ensure_ascii=False, indent=2)

    print(f'[✓] {len(coded_rows)} 筆 2023-24 基線已編碼')
    return coded_rows

# ============================================
# 主程式
# ============================================
if __name__ == '__main__':
    BASE = Path('/home/user/workspace/zenodo_pkg/data')
    BASE.mkdir(parents=True, exist_ok=True)

    main_rows = anonymize_main_csv(
        '/home/user/workspace/jd_report_2026/dist/public/jd_master.csv',
        BASE / 'jd_2025_2026_coded.csv',
        BASE / 'jd_2025_2026_coded.json',
    )
    hist_rows = anonymize_historical_json(
        '/home/user/workspace/jd_analysis/jds_2023_2024_design.json',
        BASE / 'jd_2023_2024_baseline_coded.csv',
        BASE / 'jd_2023_2024_baseline_coded.json',
    )

    # 合併為單一檔案
    all_rows = main_rows + hist_rows
    with open(BASE / 'jd_master_coded_v1.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(all_rows[0].keys()))
        writer.writeheader()
        writer.writerows(all_rows)
    with open(BASE / 'jd_master_coded_v1.json', 'w', encoding='utf-8') as f:
        json.dump(all_rows, f, ensure_ascii=False, indent=2)

    print(f'\n[✓] 合併版：{len(all_rows)} 筆')
    print(f'    輸出位置：{BASE}')

    # 打印產業分佈統計
    from collections import Counter
    print('\n=== 產業分佈 ===')
    for ind, n in Counter(r['industry_code'] for r in all_rows).most_common():
        print(f'  {ind:12s} : {n}')
    print('\n=== 地區分佈 ===')
    for reg, n in Counter(r['region_code'] for r in all_rows).most_common():
        print(f'  {reg:12s} : {n}')
    print('\n=== 薪資區間分佈 ===')
    for s, n in Counter(r['salary_bucket'] for r in all_rows).most_common():
        print(f'  {s:14s} : {n}')
