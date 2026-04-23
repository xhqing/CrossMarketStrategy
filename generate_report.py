import os
import pandas as pd
from datetime import datetime
import pytz
import glob

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

bj_tz = pytz.timezone('Asia/Shanghai')
now_bj = datetime.now(bj_tz)
report_date = now_bj.strftime('%Y年%m月%d日')
timestamp_str = now_bj.strftime('%Y%m%d%H%M%S')

existing_reports = glob.glob(os.path.join(OUTPUT_DIR, 'YB_*.html'))
next_num = len(existing_reports) + 1
filename = f"YB_000{next_num}_{timestamp_str}.html"
filepath = os.path.join(OUTPUT_DIR, filename)

df_index = pd.read_csv(os.path.join(OUTPUT_DIR, 'index_data.csv'))
df_stock = pd.read_csv(os.path.join(OUTPUT_DIR, 'stock_data.csv'))
df_etf = pd.read_csv(os.path.join(OUTPUT_DIR, 'etf_data.csv'))

index_price_map = {}
for _, row in df_index.iterrows():
    try:
        index_price_map[row['指数名称']] = float(row['当前最新点数'])
    except (ValueError, TypeError):
        pass

stock_price_map = {}
for _, row in df_stock.iterrows():
    try:
        stock_price_map[row['股票代码']] = float(row['当前最新价格(HKD)'])
    except (ValueError, TypeError):
        pass

etf_price_map = {}
for _, row in df_etf.iterrows():
    try:
        etf_price_map[row['ETF代码']] = float(row['当前最新价格(HKD)'])
    except (ValueError, TypeError):
        pass

hsi = index_price_map.get('恒生指数', 26163.24)
hstech = index_price_map.get('恒生科技指数', 4963.94)
hscei = index_price_map.get('国企指数', 8801.78)
ndx = index_price_map.get('纳斯达克100指数', 26937.27)
spx = index_price_map.get('标普500指数', 7137.90)
dji = index_price_map.get('道琼斯工业指数', 49490.03)

def calc_rise(current, target):
    return round((target - current) / current * 100, 2)

def calc_fall(current, target):
    return round((target - current) / current * 100, 2)

index_analysis = [
    {"name": "恒生指数", "code": "HSI", "current": hsi, "trend": "震荡偏弱", "high": 28500, "low": 24000,
     "logic": "美伊停火协议到期但特朗普宣布无限期延长，地缘风险暂缓但不确定性仍存。科网股全线回调拖累指数，南向资金逆势净买入48.91亿港元提供底部支撑，市场呈现结构性分化格局。"},
    {"name": "恒生科技指数", "code": "HSTECH", "current": hstech, "trend": "震荡偏弱", "high": 5800, "low": 4400,
     "logic": "科网股普遍回调（腾讯跌2.89%、阿里跌3.52%、美团跌2.54%），AI概念高位获利回吐，但光通信板块逆势暴涨（剑桥科技涨21%、长飞光纤涨17%），板块内部分化加剧。"},
    {"name": "国企指数", "code": "HSCEI", "current": hscei, "trend": "震荡偏强", "high": 9800, "low": 8000,
     "logic": "中字头能源板块受益油价高位（布伦特101.90美元/桶），中海油获南向资金净买入4.75亿港元居首，银行板块高股息防御属性突出，估值修复逻辑持续。"},
    {"name": "纳斯达克100指数", "code": ".NDX", "current": ndx, "trend": "震荡偏强", "high": 30000, "low": 24000,
     "logic": "纳指4月22日反弹1.64%，停火延长提振风险偏好，Google Cloud Next大会催化AI算力预期，费半14连涨显示半导体景气度持续，但地缘风险仍压制估值扩张空间。"},
    {"name": "标普500指数", "code": ".SPX", "current": spx, "trend": "震荡偏强", "high": 7800, "low": 6500,
     "logic": "标普500反弹1.05%至7137.90点，停火延长缓解地缘担忧，一季报超预期比例近90%支撑盈利端，能源板块受益油价上涨，但美联储降息推迟至2027年限制估值上行。"},
    {"name": "道琼斯工业指数", "code": ".DJI", "current": dji, "trend": "震荡偏强", "high": 53000, "low": 45000,
     "logic": "道指反弹0.69%至49490.03点，传统行业盈利改善与油价成本压力对冲，GE Vernova等重磅财报超预期，金融和能源板块提供底部支撑，苹果换帅影响有限。"},
]

stock_analysis = [
    {"name": "腾讯控股", "code": "00700.HK", "price": stock_price_map.get("00700.HK", 504.00), "trend": "震荡偏弱", "high": 600, "low": 430, "view": "看多", "position": "加仓，建议仓位占比：8.00%",
     "logic": "AI赋能核心业务提升变现效率，微信AI搜索功能上线，但科网股整体回调短期承压，南向资金净卖出10.28亿港元，估值仍有修复空间。"},
    {"name": "阿里巴巴", "code": "09988.HK", "price": stock_price_map.get("09988.HK", 131.50), "trend": "震荡偏弱", "high": 170, "low": 105, "view": "观望", "position": "持有",
     "logic": "云业务AI收入快速增长，但中概股普跌拖累短期表现，遭南向资金大幅净卖出10.62亿港元居首，估值处于历史低位但短期缺乏催化。"},
    {"name": "小米", "code": "01810.HK", "price": stock_price_map.get("01810.HK", 31.80), "trend": "震荡偏强", "high": 42, "low": 26, "view": "看多", "position": "加仓，建议仓位占比：6.00%",
     "logic": "小米汽车SU7交付量持续攀升，IoT生态扩张，连续回购彰显信心，汽车业务放量带动估值重估。"},
    {"name": "快手", "code": "01024.HK", "price": stock_price_map.get("01024.HK", 45.34), "trend": "震荡偏弱", "high": 55, "low": 36, "view": "观望", "position": "持有",
     "logic": "短剧和电商GMV增长超预期，海外业务减亏，但科网股整体回调短期承压，盈利拐点确认需等待板块情绪回暖。"},
    {"name": "京东", "code": "09618.HK", "price": stock_price_map.get("09618.HK", 120.20), "trend": "震荡偏弱", "high": 150, "low": 100, "view": "观望", "position": "持有",
     "logic": "电商竞争加剧挤压利润率，物流优势难以完全转化为盈利，百亿补贴效果待验证，短期缺乏催化。"},
    {"name": "美团", "code": "03690.HK", "price": stock_price_map.get("03690.HK", 84.25), "trend": "震荡偏弱", "high": 105, "low": 68, "view": "看多", "position": "加仓，建议仓位占比：5.00%",
     "logic": "本地生活壁垒稳固，即时零售业务扩张，到店业务竞争趋缓，新业务减亏趋势明确，但科网股回调短期承压。"},
    {"name": "紫金矿业", "code": "02899.HK", "price": stock_price_map.get("02899.HK", 37.84), "trend": "震荡上行", "high": 50, "low": 30, "view": "看多", "position": "加仓，建议仓位占比：7.00%",
     "logic": "黄金价格屡创新高（现货4734.85美元/盎司），铜价受AI算力需求拉动涨至13470美元/吨，量价齐升逻辑清晰。"},
    {"name": "中芯国际", "code": "00981.HK", "price": stock_price_map.get("00981.HK", 59.30), "trend": "震荡偏强", "high": 75, "low": 48, "view": "看多", "position": "加仓，建议仓位占比：5.00%",
     "logic": "半导体国产化长期逻辑不变，成熟制程需求稳健，光通信板块暴涨带动芯片股情绪，费半14连涨提供外部支撑。"},
    {"name": "华虹半导体", "code": "01347.HK", "price": stock_price_map.get("01347.HK", 99.70), "trend": "震荡偏强", "high": 120, "low": 75, "view": "看多", "position": "持有",
     "logic": "获南向资金净买入2.56亿港元，功率半导体需求分化但AI算力需求拉动先进制程，光通信景气度外溢至半导体板块。"},
    {"name": "泡泡玛特", "code": "09992.HK", "price": stock_price_map.get("09992.HK", 160.20), "trend": "震荡偏强", "high": 200, "low": 130, "view": "看多", "position": "持有",
     "logic": "海外市场快速扩张，新IP持续孵化，获南向资金净买入3.31亿港元，出海逻辑验证中，但高估值需业绩持续超预期支撑。"},
    {"name": "中国神华", "code": "01088.HK", "price": stock_price_map.get("01088.HK", 46.52), "trend": "震荡偏强", "high": 55, "low": 38, "view": "看多", "position": "持有",
     "logic": "煤炭长协价格稳定，分红率维持高位，高股息防御属性突出，港股通持股比例67%显示资金认可度高。"},
    {"name": "宁德时代", "code": "03750.HK", "price": stock_price_map.get("03750.HK", 699.00), "trend": "震荡偏弱", "high": 900, "low": 560, "view": "看多", "position": "持有",
     "logic": "超级科技日发布第三代神行超充电池，但当日跌5.03%遭获利回吐，中石化拟出售850万股H股增添抛压，全球动力电池龙头地位稳固。"},
    {"name": "赣锋锂业", "code": "01772.HK", "price": stock_price_map.get("01772.HK", 78.30), "trend": "震荡偏弱", "high": 100, "low": 60, "view": "看空", "position": "减仓，建议仓位占比：-2.00%",
     "logic": "锂价低位震荡，产能扩张与需求恢复错配，锂电池股跌幅居前，行业供给过剩格局未根本改变。"},
    {"name": "昆仑能源", "code": "00135.HK", "price": stock_price_map.get("00135.HK", 7.69), "trend": "震荡偏强", "high": 9.5, "low": 6.5, "view": "看多", "position": "持有",
     "logic": "天然气销售量增长，管道资产注入预期，中石油体系内资源协同优势明显，估值偏低。"},
    {"name": "中国石油化工股份", "code": "00386.HK", "price": stock_price_map.get("00386.HK", 4.50), "trend": "震荡上行", "high": 5.8, "low": 3.8, "view": "看多", "position": "加仓，建议仓位占比：6.00%",
     "logic": "油价高位利好上游（布伦特101.90美元/桶），炼化价差修复，高股息特征在震荡市中具备吸引力，但国内油价下调820元/吨短期影响炼化利润。"},
    {"name": "国泰君安国际", "code": "01788.HK", "price": stock_price_map.get("01788.HK", 2.57), "trend": "震荡偏强", "high": 3.3, "low": 2.2, "view": "看多", "position": "持有",
     "logic": "港股成交额回升利好经纪业务（全日成交2283亿港元），中资券商股逆势活跃，财富管理转型推进。"},
    {"name": "中国宏桥", "code": "01378.HK", "price": stock_price_map.get("01378.HK", 36.30), "trend": "震荡上行", "high": 46, "low": 30, "view": "看多", "position": "加仓，建议仓位占比：5.00%",
     "logic": "铝价受地缘冲突支撑上涨（伦铝3622美元/吨+2.58%），产能优化推进，电解铝供给刚性约束，盈利弹性大。"},
    {"name": "招商银行", "code": "03968.HK", "price": stock_price_map.get("03968.HK", 50.90), "trend": "震荡偏强", "high": 62, "low": 43, "view": "看多", "position": "持有",
     "logic": "零售银行龙头地位稳固，财富管理业务恢复增长，资产质量优于同业，估值修复空间较大。"},
    {"name": "建设银行", "code": "00939.HK", "price": stock_price_map.get("00939.HK", 8.77), "trend": "震荡偏强", "high": 10.5, "low": 7.5, "view": "看多", "position": "持有",
     "logic": "信贷投放稳健，分红率维持30%以上，获南向资金5日增持21.21亿元，股息率超7%具备配置价值。"},
    {"name": "中国银行", "code": "03988.HK", "price": stock_price_map.get("03988.HK", 5.11), "trend": "震荡偏强", "high": 6.2, "low": 4.4, "view": "看多", "position": "持有",
     "logic": "国际化业务优势突出，跨境人民币结算量增长，外汇业务和跨境金融优势明显，高股息低估值特征突出。"},
    {"name": "汇丰控股", "code": "00005.HK", "price": stock_price_map.get("00005.HK", 144.00), "trend": "震荡偏强", "high": 168, "low": 125, "view": "看多", "position": "持有",
     "logic": "利率维持高位利好净息差，回购计划持续推进，亚洲业务增长强劲，股东回报力度大。"},
    {"name": "信达生物", "code": "01801.HK", "price": stock_price_map.get("01801.HK", 88.20), "trend": "震荡偏强", "high": 120, "low": 70, "view": "看多", "position": "加仓，建议仓位占比：5.00%",
     "logic": "PD-1海外授权推进，减重药物临床进展积极，创新药管线持续兑现，GLP-1赛道布局具备想象空间。"},
    {"name": "药明生物", "code": "02269.HK", "price": stock_price_map.get("02269.HK", 35.02), "trend": "震荡偏弱", "high": 45, "low": 25, "view": "看空", "position": "减仓，建议仓位占比：-3.00%",
     "logic": "美国生物安全法案影响持续，遭南向资金5日净卖出4.09亿元，海外订单恢复缓慢，地缘政治风险压制估值。"},
    {"name": "中国海洋石油", "code": "00883.HK", "price": stock_price_map.get("00883.HK", 26.88), "trend": "震荡上行", "high": 34, "low": 22, "view": "看多", "position": "加仓，建议仓位占比：8.00%",
     "logic": "布伦特原油突破100美元/桶直接受益，获南向资金净买入4.75亿港元居首，桶油成本行业最低，高股息+高盈利弹性双击。"},
    {"name": "中国石油股份", "code": "00857.HK", "price": stock_price_map.get("00857.HK", 10.65), "trend": "震荡上行", "high": 13.5, "low": 8.5, "view": "看多", "position": "加仓，建议仓位占比：7.00%",
     "logic": "油价高位运行利好上游（WTI 92.65美元/桶），天然气业务快速增长，地缘溢价直接受益，估值仍偏低。"},
    {"name": "工商银行", "code": "01398.HK", "price": stock_price_map.get("01398.HK", 7.13), "trend": "震荡偏强", "high": 8.5, "low": 6.0, "view": "看多", "position": "持有",
     "logic": "信贷规模稳健增长，不良率持续下降，获南向资金5日增持12.24亿元，股息率超8%防御配置价值突出。"},
    {"name": "比亚迪股份", "code": "01211.HK", "price": stock_price_map.get("01211.HK", 107.00), "trend": "震荡偏强", "high": 145, "low": 88, "view": "看多", "position": "持有",
     "logic": "新能源车全球销量龙头，海外放量打开第二增长曲线，智能化升级提升产品力，但锂电池板块回调短期承压。"},
    {"name": "香港交易所", "code": "00388.HK", "price": stock_price_map.get("00388.HK", 416.60), "trend": "震荡偏弱", "high": 520, "low": 350, "view": "观望", "position": "持有",
     "logic": "港股成交额回升利好（全日2283亿港元），但遭南向资金5日净卖出3.60亿元，市场回调影响情绪，短期缺乏催化。"},
    {"name": "友邦保险", "code": "01299.HK", "price": stock_price_map.get("01299.HK", 83.20), "trend": "震荡偏强", "high": 100, "low": 70, "view": "看多", "position": "持有",
     "logic": "连续15日回购累计斥资38.22亿港元，4月22日单日回购2.35亿港元，投行目标均价103.9港元，估值修复空间大。"},
    {"name": "中国人寿", "code": "02628.HK", "price": stock_price_map.get("02628.HK", 27.28), "trend": "震荡偏弱", "high": 35, "low": 22, "view": "观望", "position": "持有",
     "logic": "保险板块跌幅靠前，高利率环境影响险企投资端，但长期受益利率企稳，短期缺乏催化。"},
    {"name": "中国平安", "code": "02318.HK", "price": stock_price_map.get("02318.HK", 61.30), "trend": "震荡偏弱", "high": 75, "low": 50, "view": "观望", "position": "持有",
     "logic": "遭南向资金5日净卖出3.59亿元，金融板块整体承压，但综合金融龙头估值偏低，等待板块情绪回暖。"},
    {"name": "中国移动", "code": "00941.HK", "price": stock_price_map.get("00941.HK", 83.40), "trend": "震荡偏强", "high": 100, "low": 70, "view": "看多", "position": "持有",
     "logic": "获南向资金5日增持20.51亿元，6G标准与工程化攻坚期利好运营商，高股息+AI算力基建双重逻辑。"},
    {"name": "网易", "code": "09999.HK", "price": stock_price_map.get("09999.HK", 177.60), "trend": "震荡偏弱", "high": 220, "low": 140, "view": "观望", "position": "持有",
     "logic": "游戏版号持续获批，但科网股整体回调跌超2%，短期受市场情绪拖累，等待新游戏上线催化。"},
    {"name": "百度集团", "code": "09888.HK", "price": stock_price_map.get("09888.HK", 121.10), "trend": "震荡偏弱", "high": 155, "low": 95, "view": "观望", "position": "持有",
     "logic": "自动驾驶技术持续突破，AI大模型商业化推进，但科网股普跌拖累短期表现，估值处于相对低位。"},
    {"name": "理想汽车", "code": "02015.HK", "price": stock_price_map.get("02015.HK", 73.45), "trend": "震荡偏弱", "high": 95, "low": 55, "view": "观望", "position": "持有",
     "logic": "新能源车竞争加剧，特斯拉财报即将披露影响板块情绪，智能驾驶技术差异化竞争，短期缺乏催化。"},
    {"name": "小鹏汽车", "code": "09868.HK", "price": stock_price_map.get("09868.HK", 66.35), "trend": "震荡偏弱", "high": 85, "low": 45, "view": "看空", "position": "减仓，建议仓位占比：-2.00%",
     "logic": "遭南向资金5日净卖出4.40亿元，新能源车板块承压，交付量增速放缓，短期缺乏催化。"},
    {"name": "安踏体育", "code": "02020.HK", "price": stock_price_map.get("02020.HK", 84.80), "trend": "震荡偏强", "high": 105, "low": 68, "view": "看多", "position": "持有",
     "logic": "国潮消费龙头地位稳固，多品牌战略持续推进，估值相对合理，但消费板块整体偏弱短期承压。"},
    {"name": "地平线机器人", "code": "09660.HK", "price": stock_price_map.get("09660.HK", 7.63), "trend": "震荡偏弱", "high": 12, "low": 5, "view": "观望", "position": "持有",
     "logic": "AI芯片概念股，智能驾驶赛道长期空间大，但公司仍处亏损期，商业化进度待验证，短期随板块回调。"},
]

etf_analysis = [
    {"name": "盈富基金", "code": "02800.HK", "price": etf_price_map.get("02800.HK", 26.76), "trend": "震荡偏弱", "high": 30, "low": 23, "view": "看多", "position": "加仓，建议仓位占比：10.00%",
     "logic": "跟踪恒生指数，获南向资金5日大幅增持32.89亿元居首，港股通持股比例5.46%且持续上升，高股息+低估值配置价值突出。"},
    {"name": "南方恒生科技", "code": "03033.HK", "price": etf_price_map.get("03033.HK", 4.87), "trend": "震荡偏弱", "high": 6.0, "low": 4.0, "view": "观望", "position": "持有",
     "logic": "跟踪恒生科技指数，科网股全线回调短期承压，遭南向资金5日净卖出7.26亿元，但AI算力需求长期利好科技板块。"},
    {"name": "恒生中国企业", "code": "02828.HK", "price": etf_price_map.get("02828.HK", 89.73), "trend": "震荡偏强", "high": 105, "low": 75, "view": "看多", "position": "加仓，建议仓位占比：8.00%",
     "logic": "跟踪国企指数，中字头能源板块受益油价高位，获南向资金5日增持9.02亿元，持股占比单日大增5.05%，资金流入明显。"},
]

def make_index_data_link(val, source):
    try:
        url = str(source)
        if url.startswith('http'):
            return f'<a href="{url}" target="_blank">{val}</a>'
    except:
        pass
    return str(val)

index_table_rows = []
for _, row in df_index.iterrows():
    index_table_rows.append(
        f"<tr><td>{row['指数名称']}</td><td>{row['指数代码']}</td>"
        f"<td>{make_index_data_link(row['当前最新点数'], row['数据来源'])}</td>"
        f"<td>{row['当前最新点数对应时间戳']}</td>"
        f"<td>{make_index_data_link('来源', row['数据来源'])}</td></tr>"
    )
index_table_csv = "".join(index_table_rows)

stock_table_csv = df_stock.to_html(index=False, classes="data-table", border=0, escape=False)
etf_table_csv = df_etf.to_html(index=False, classes="data-table", border=0, escape=False)

def make_index_row(ia):
    high_rise = calc_rise(ia["current"], ia["high"])
    low_fall = calc_fall(ia["current"], ia["low"])
    return f"""<tr>
<td>{ia['name']}</td><td>{ia['code']}</td><td>{ia['current']:,.2f}</td>
<td>{ia['trend']}</td><td>{ia['high']:,.2f}</td><td>{high_rise}%</td>
<td>{ia['low']:,.2f}</td><td>{low_fall}%</td>
<td>{ia['logic']}</td>
</tr>"""

def make_stock_row(sa):
    high_rise = calc_rise(sa["price"], sa["high"])
    low_fall = calc_fall(sa["price"], sa["low"])
    return f"""<tr>
<td>{sa['name']}</td><td>{sa['code']}</td><td>{sa['price']:.2f}</td>
<td>{sa['trend']}</td><td>{sa['high']:.2f}</td><td>{high_rise}%</td>
<td>{sa['low']:.2f}</td><td>{low_fall}%</td>
<td>{sa['view']}</td><td>{sa['position']}</td>
<td>{sa['logic']}</td>
</tr>"""

def make_etf_row(ea):
    high_rise = calc_rise(ea["price"], ea["high"])
    low_fall = calc_fall(ea["price"], ea["low"])
    return f"""<tr>
<td>{ea['name']}</td><td>{ea['code']}</td><td>{ea['price']:.2f}</td>
<td>{ea['trend']}</td><td>{ea['high']:.2f}</td><td>{high_rise}%</td>
<td>{ea['low']:.2f}</td><td>{low_fall}%</td>
<td>{ea['view']}</td><td>{ea['position']}</td>
<td>{ea['logic']}</td>
</tr>"""

index_rows = "".join(make_index_row(ia) for ia in index_analysis)
stock_rows = "".join(make_stock_row(sa) for sa in stock_analysis)
etf_rows = "".join(make_etf_row(ea) for ea in etf_analysis)

html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>跨市场重大事件与港股龙头策略研判 - {report_date}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; line-height: 1.8; color: #2c3e50; background: #f8f9fa; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
.header {{ background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #3949ab 100%); color: white; padding: 40px; border-radius: 12px; margin-bottom: 30px; text-align: center; }}
.header h1 {{ font-size: 2em; margin-bottom: 10px; letter-spacing: 2px; }}
.header .date {{ font-size: 1.1em; opacity: 0.9; }}
.toc {{ background: white; padding: 30px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }}
.toc h2 {{ color: #1a237e; margin-bottom: 20px; border-bottom: 2px solid #1a237e; padding-bottom: 10px; }}
.toc ul {{ list-style: none; padding-left: 0; }}
.toc li {{ margin: 8px 0; }}
.toc a {{ color: #3949ab; text-decoration: none; font-size: 1.05em; transition: color 0.2s; }}
.toc a:hover {{ color: #1a237e; text-decoration: underline; }}
.toc .sub {{ padding-left: 25px; }}
.toc .sub a {{ font-size: 0.95em; color: #5c6bc0; }}
.section {{ background: white; padding: 30px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }}
.section h2 {{ color: #1a237e; margin-bottom: 20px; border-bottom: 2px solid #e8eaf6; padding-bottom: 10px; font-size: 1.5em; }}
.section h3 {{ color: #283593; margin: 20px 0 15px; font-size: 1.2em; }}
.section h4 {{ color: #3949ab; margin: 15px 0 10px; font-size: 1.05em; }}
.data-table {{ width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 0.9em; }}
.data-table th {{ background: #e8eaf6; color: #1a237e; padding: 12px 8px; text-align: center; font-weight: 600; border: 1px solid #c5cae9; }}
.data-table td {{ padding: 10px 8px; text-align: center; border: 1px solid #e0e0e0; }}
.data-table tr:nth-child(even) {{ background: #f5f5f5; }}
.data-table tr:hover {{ background: #e8eaf6; }}
.data-table a {{ color: #3949ab; text-decoration: underline; }}
.event-card {{ background: #f8f9fa; border-left: 4px solid #3949ab; padding: 15px 20px; margin: 15px 0; border-radius: 0 8px 8px 0; }}
.event-card h4 {{ color: #1a237e; margin-bottom: 8px; }}
.event-card .time {{ color: #e65100; font-weight: 600; font-size: 0.9em; }}
.scenario {{ display: inline-block; padding: 3px 10px; border-radius: 4px; font-size: 0.85em; margin: 3px; }}
.scenario.base {{ background: #e3f2fd; color: #1565c0; }}
.scenario.optimistic {{ background: #e8f5e9; color: #2e7d32; }}
.scenario.pessimistic {{ background: #fce4ec; color: #c62828; }}
.tag {{ display: inline-block; padding: 2px 8px; border-radius: 3px; font-size: 0.8em; margin: 2px; }}
.tag.up {{ background: #e8f5e9; color: #2e7d32; }}
.tag.down {{ background: #fce4ec; color: #c62828; }}
.tag.neutral {{ background: #fff3e0; color: #e65100; }}
.tag.strong {{ background: #e3f2fd; color: #1565c0; }}
.reasoning-chain {{ background: #f3e5f5; padding: 20px; border-radius: 8px; margin: 15px 0; }}
.reasoning-chain h4 {{ color: #6a1b9a; }}
.ref-list {{ font-size: 0.9em; }}
.ref-list li {{ margin: 8px 0; }}
.ref-list a {{ color: #3949ab; }}
.footer {{ text-align: center; color: #9e9e9e; padding: 20px; font-size: 0.85em; }}
.disclaimer {{ background: #fff3e0; padding: 15px; border-radius: 8px; margin: 20px 0; font-size: 0.85em; color: #e65100; }}
</style>
</head>
<body>
<div class="container">

<div class="header">
<h1>跨市场重大事件与港股龙头策略研判</h1>
<div class="date">报告日期：{report_date}（北京时间）</div>
</div>

<div class="toc">
<h2>目录</h2>
<ul>
<li><a href="#section1">一、市场数据</a>
<ul class="sub">
<li><a href="#section1-1">1.1 指数数据表</a></li>
<li><a href="#section1-2">1.2 个股数据表</a></li>
<li><a href="#section1-3">1.3 ETF数据表</a></li>
</ul>
</li>
<li><a href="#section2">二、重大事件分析</a>
<ul class="sub">
<li><a href="#section2-1">2.1 近期已发生的重大事件</a></li>
<li><a href="#section2-2">2.2 未来一周将要发生的重大事件</a></li>
<li><a href="#section2-3">2.3 重点关注领域</a></li>
</ul>
</li>
<li><a href="#section3">三、指数研判</a></li>
<li><a href="#section4">四、个股分析</a></li>
<li><a href="#section5">五、ETF分析</a></li>
<li><a href="#section6">六、分析推理过程</a></li>
<li><a href="#section7">七、参考资料</a></li>
</ul>
</div>

<div class="section" id="section1">
<h2>一、市场数据</h2>

<h3 id="section1-1">1.1 指数数据表</h3>
<table class="data-table">
<thead>
<tr>
<th>指数名称</th><th>指数代码</th><th>当前最新点数</th><th>当前最新点数对应时间戳</th><th>数据来源</th>
</tr>
</thead>
<tbody>
{index_table_csv}
</tbody>
</table>

<h3 id="section1-2">1.2 个股数据表</h3>
{stock_table_csv}

<h3 id="section1-3">1.3 ETF数据表</h3>
{etf_table_csv}
</div>

<div class="section" id="section2">
<h2>二、重大事件分析</h2>

<h3 id="section2-1">2.1 近期已发生的重大事件</h3>

<div class="event-card">
<h4>1. 特朗普宣布无限期延长美伊停火协议，地缘风险暂缓</h4>
<p class="time">发生时间：2026年4月22日（北京时间）</p>
<p><strong>事件概述：</strong>美伊两周临时停火协议原定4月22日北京时间早8点到期，但特朗普宣布将无限期延长停火协议。伊朗否认举行新谈判，指特朗普"又说谎了"，但停火状态得以维持。26艘伊朗商船此前突破美军封锁通航，美军未敢开火升级冲突。</p>
<p><strong>对市场的影响机制：</strong>停火延长消息提振全球风险偏好，美股4月22日大幅反弹（标普500涨1.05%、纳指涨1.64%），但港股因科网股回调仍收跌1.22%。布伦特原油突破100美元/桶后回落至101.90美元/桶。</p>
<p><strong>后续进展预期：</strong>停火虽延长但核心分歧（核问题、海峡管理、制裁解除）仍未解决，冲突随时可能再度升级。英法召开30国军事规划会议推进霍尔木兹海峡恢复通航方案。</p>
<p><strong>对市场的持续影响评估：</strong>地缘风险暂缓为港股提供喘息窗口，但油价中枢上移将重塑市场风格，能源板块持续受益，制造业成本压力加大。</p>
</div>

<div class="event-card">
<h4>2. 港股4月22日收跌1.22%，光通信板块逆势暴涨</h4>
<p class="time">发生时间：2026年4月22日（北京时间）</p>
<p><strong>事件概述：</strong>恒生指数跌324.24点（-1.22%）报26163.24点，恒生科技指数跌1.93%报4963.94点，国企指数跌1.59%报8801.78点。全日成交2283.03亿港元放量。科网股全线回调，但光通信板块逆势暴涨——剑桥科技涨21.08%、长飞光纤光缆涨17.16%创历史新高。南向资金逆势净买入48.91亿港元。</p>
<p><strong>对市场的影响机制：</strong>市场呈现"光通信强、科网弱"的结构性格局，TrendForce预测2026年全球AI专用光模块市场规模将达260亿美元（同比+57.6%），AI算力硬件景气度持续攀升成为最强主线。</p>
<p><strong>后续进展预期：</strong>光通信景气度有望延续，但科网股短期回调提供布局机会，南向资金逆势净买入显示长线资金看好港股。</p>
<p><strong>对市场的持续影响评估：</strong>结构性分化可能持续，AI算力硬件（光通信、半导体）仍是核心主线，建议关注能源+高股息防御配置，同时逢低布局AI科技主线。</p>
</div>

<div class="event-card">
<h4>3. 美股4月22日大幅反弹，纳指涨1.64%创新高</h4>
<p class="time">发生时间：2026年4月22日（美东时间）</p>
<p><strong>事件概述：</strong>道指涨0.69%报49490.03点，标普500涨1.05%报7137.90点，纳指涨1.64%报24657.57点。停火延长提振风险偏好，GE Vernova等重磅财报超预期，Google Cloud Next大会催化AI预期。费半指数14连涨（2014年以来最长）。</p>
<p><strong>对市场的影响机制：</strong>美股反弹对港股形成正面情绪传导，但时差效应导致港股4月23日开盘仅小幅低开（恒指-0.25%），科网股仍承压。</p>
<p><strong>后续进展预期：</strong>特斯拉、IBM等一季报即将披露，若盈利超预期可能进一步提振全球科技股情绪。</p>
<p><strong>对市场的持续影响评估：</strong>美股整体仍处高位，AI算力需求持续推动半导体板块，但地缘风险和美联储鹰派立场限制估值扩张空间。</p>
</div>

<div class="event-card">
<h4>4. 布伦特原油突破100美元/桶，全球通胀预期升温</h4>
<p class="time">发生时间：2026年4月22日（北京时间）</p>
<p><strong>事件概述：</strong>布伦特原油收报101.90美元/桶（+3.48%），WTI原油92.65美元/桶（-0.33%）。霍尔木兹海峡航运过境量下降超95%，全球约三分之一海运化肥贸易受阻，中东颗粒尿素期货离岸价从不到500美元/吨涨至850美元/吨（涨幅超75%）。国内油价4月21日24时下调820元/吨。</p>
<p><strong>对市场的影响机制：</strong>油价中枢上移推升全球通胀预期，美联储降息推迟至2027年。港股能源板块直接受益（中海油、中石油），但制造业和消费板块成本压力加大。</p>
<p><strong>后续进展预期：</strong>若霍尔木兹海峡恢复通航，油价可能回落至80-90美元/桶；若冲突再度升级，油价可能突破130美元/桶。</p>
<p><strong>对市场的持续影响评估：</strong>油价高位运行将重塑市场风格，能源+高股息板块持续受益，成长股估值承压。</p>
</div>

<div class="event-card">
<h4>5. 苹果换帅：库克转任执行董事长，特努斯9月接任CEO</h4>
<p class="time">发生时间：2026年4月20日（美东时间）</p>
<p><strong>事件概述：</strong>苹果公司宣布CEO蒂姆·库克将转任董事会执行董事长，硬件工程高级副总裁约翰·特努斯将于9月1日接任CEO。库克执掌苹果15年间市值增长24倍，年收入突破4000亿美元。</p>
<p><strong>对市场的影响机制：</strong>苹果换帅对全球科技股情绪产生短期扰动，但内部人接班降低不确定性。苹果供应链需关注新CEO战略方向调整。</p>
<p><strong>后续进展预期：</strong>9月正式交接前为过渡期，预计业务连续性强。特努斯作为硬件负责人，可能更注重产品创新和AI硬件整合。</p>
<p><strong>对市场的持续影响评估：</strong>短期影响有限，需关注6月WWDC上新CEO首秀及苹果AI战略推进节奏。</p>
</div>

<div class="event-card">
<h4>6. 中国一季度GDP增长5.0%，进出口同比上涨15%</h4>
<p class="time">发生时间：2026年4月22日（北京时间）</p>
<p><strong>事件概述：</strong>中国一季度GDP同比增长5.0%，进出口同比上涨15%，经济数据表明开局良好。长三角区域进出口总值4.49万亿元创历史同期新高，同比增长15.8%。A股沪指重返4100点，两市成交2.56万亿放量。</p>
<p><strong>对市场的影响机制：</strong>中国经济数据超预期为港股提供基本面支撑，南向资金持续净流入（4月22日净买入48.91亿港元），A股走强对港股形成正面联动。</p>
<p><strong>后续进展预期：</strong>若经济复苏持续超预期，港股盈利端有望上修，特别是内需相关板块。</p>
<p><strong>对市场的持续影响评估：</strong>中国经济温和复苏为港股提供底部支撑，但需关注地产和消费复苏力度。</p>
</div>

<h3 id="section2-2">2.2 未来一周将要发生的重大事件</h3>

<div class="event-card">
<h4>1. 美联储发布经济状况褐皮书（4月23日）</h4>
<p class="time">预计时间：2026年4月23日（美东时间）</p>
<p><strong>事件概述：</strong>美联储将发布经济状况褐皮书，揭示关税政策和地缘冲突对地区经济的实际影响，制造业投入价格指数尤其值得关注。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario base">基准情景（概率50%）：经济温和增长，通胀压力持续但不恶化，市场反应有限</span></p>
<p><span class="scenario optimistic">乐观情景（概率20%）：经济韧性超预期，通胀回落迹象明显，降息预期升温</span></p>
<p><span class="scenario pessimistic">悲观情景（概率30%）：滞胀风险上升，高油价传导至核心通胀，美联储鹰派立场强化</span></p>
</div>

<div class="event-card">
<h4>2. Google Cloud Next大会（4月22日-24日）</h4>
<p class="time">预计时间：2026年4月22日-24日（美东时间）</p>
<p><strong>事件概述：</strong>谷歌举办Google Cloud Next大会，预计发布新一代TPU架构。美满电子已因谷歌商议开发新AI芯片消息涨5.8%，大会可能进一步催化AI算力产业链。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario base">基准情景（概率45%）：TPU架构迭代符合预期，AI算力需求叙事延续，相关个股温和上涨</span></p>
<p><span class="scenario optimistic">乐观情景（概率35%）：新一代TPU性能大幅提升，AI算力投资加速，港股AI概念股大涨</span></p>
<p><span class="scenario pessimistic">悲观情景（概率20%）：发布内容不及预期，AI投资增速放缓担忧升温，科技股回调</span></p>
</div>

<div class="event-card">
<h4>3. 特斯拉、IBM等一季报披露</h4>
<p class="time">预计时间：2026年4月22日-25日（美东时间）</p>
<p><strong>事件概述：</strong>特斯拉、IBM、洛克希德·马丁等公司将披露一季报。目前标普500已公布业绩的公司中近90%利润超预期。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario base">基准情景（概率45%）：特斯拉业绩符合预期，市场反应中性</span></p>
<p><span class="scenario optimistic">乐观情景（概率25%）：特斯拉交付量超预期+AI进展，新能源板块联动上涨</span></p>
<p><span class="scenario pessimistic">悲观情景（概率30%）：特斯拉利润率下滑，新能源车板块承压</span></p>
</div>

<div class="event-card">
<h4>4. 美伊停火后续谈判进展</h4>
<p class="time">预计时间：2026年4月23日-29日</p>
<p><strong>事件概述：</strong>特朗普称未来36至72小时内"可能"与伊朗谈判，伊朗否认举行新谈判。英法召开30国军事规划会议推进霍尔木兹海峡恢复通航方案。停火虽延长但核心分歧仍未解决。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario pessimistic">悲观情景（概率35%）：谈判破裂，冲突再度升级，油价突破130美元/桶，全球股市大幅回调</span></p>
<p><span class="scenario base">基准情景（概率45%）：停火维持但谈判无实质进展，市场震荡加剧，油价在95-110美元/桶区间波动</span></p>
<p><span class="scenario optimistic">乐观情景（概率20%）：双方达成框架协议，地缘溢价快速消退，油价回落至80美元以下，全球风险资产反弹</span></p>
</div>

<div class="event-card">
<h4>5. 美联储4月28-29日议息会议</h4>
<p class="time">预计时间：2026年4月28日-29日（美东时间）</p>
<p><strong>事件概述：</strong>美联储将召开下一次议息会议，维持利率不变概率高达99.5%。市场关注会议声明中对通胀和地缘风险的表述。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario base">基准情景（概率70%）：维持利率3.5%-3.75%不变，声明中性偏鹰，市场反应有限</span></p>
<p><span class="scenario optimistic">乐观情景（概率10%）：声明偏鸽，暗示年内降息可能，风险资产反弹</span></p>
<p><span class="scenario pessimistic">悲观情景（概率20%）：声明超预期鹰派，暗示可能加息，风险资产大幅回调</span></p>
</div>

<h3 id="section2-3">2.3 重点关注领域</h3>

<h4>⭐⭐⭐ 美联储货币政策</h4>
<div class="event-card">
<p><strong>最新立场：</strong>3月FOMC会议维持利率3.5%-3.75%不变。4月28-29日将召开下一次议息会议，维持利率不变概率高达99.5%。</p>
<p><strong>利率路径预期：</strong>德银预计2026年全年维持利率不变。CME数据显示6月降息概率仅4.5%。芝加哥联储主席古尔斯比称若油价长期高企，美联储可能需等到2027年才会降息。圣路易斯联储主席穆萨莱姆称高油价可能使基本通胀率比2%目标高出近一个百分点。</p>
<p><strong>缩表节奏：</strong>缩表仍在持续但节奏已放缓，市场流动性边际改善但整体仍偏紧。</p>
</div>

<h4>⭐⭐⭐ 中东地缘政治危机</h4>
<div class="event-card">
<p><strong>冲突最新动态：</strong>特朗普宣布无限期延长停火协议，但伊朗否认举行新谈判。26艘伊朗商船突破美军封锁。英法召开30国军事规划会议推进海峡通航方案。三支美军航母编队仍在中东海域。</p>
<p><strong>对油价影响：</strong>布伦特原油101.90美元/桶（+3.48%），WTI 92.65美元/桶（-0.33%）。霍尔木兹海峡航运过境量下降超95%。若冲突升级，油价可能突破130美元/桶。</p>
<p><strong>避险情绪传导：</strong>全球避险情绪有所缓解但未消除，资金从成长向价值轮动趋势仍在，港股能源+高股息板块受益，科网股承压。</p>
<p><strong>供应链风险：</strong>霍尔木兹海峡承担全球约30%石油海运，化肥价格暴涨75%显示供应链风险已从能源传导至农业领域。</p>
</div>
</div>

<div class="section" id="section3">
<h2>三、指数研判</h2>

<table class="data-table">
<thead>
<tr>
<th>指数名称</th><th>指数代码</th><th>当前最新点数</th>
<th>未来一个月趋势预判</th>
<th>截止2026年12月31日最高目标点数</th><th>最高目标点数相对当前涨幅</th>
<th>截止2026年12月31日最低目标点数</th><th>最低目标点数相对当前跌幅</th>
<th>未来一个月趋势预判的核心逻辑</th>
</tr>
</thead>
<tbody>
{index_rows}
</tbody>
</table>
</div>

<div class="section" id="section4">
<h2>四、个股分析</h2>

<table class="data-table">
<thead>
<tr>
<th>股票名称</th><th>股票代码</th><th>当前最新价格(HKD)</th>
<th>未来一个月趋势预判</th><th>截止2026年12月31日最高目标价</th><th>最高目标价相对最新价格涨幅</th>
<th>截止2026年12月31日最低目标价</th><th>最低目标价相对最新价格跌幅</th>
<th>当前看多看空观点</th><th>当前仓位调整建议</th>
<th>未来一个月趋势预判的核心逻辑</th>
</tr>
</thead>
<tbody>
{stock_rows}
</tbody>
</table>
</div>

<div class="section" id="section5">
<h2>五、ETF分析</h2>

<table class="data-table">
<thead>
<tr>
<th>ETF名称</th><th>ETF代码</th><th>当前最新价格(HKD)</th>
<th>未来一个月趋势预判</th><th>截止2026年12月31日最高目标价</th><th>最高目标价相对最新价格涨幅</th>
<th>截止2026年12月31日最低目标价</th><th>最低目标价相对最新价格跌幅</th>
<th>当前看多看空观点</th><th>当前仓位调整建议</th>
<th>未来一个月趋势预判的核心逻辑</th>
</tr>
</thead>
<tbody>
{etf_rows}
</tbody>
</table>
</div>

<div class="section" id="section6">
<h2>六、分析推理过程</h2>

<div class="reasoning-chain">
<h4>1. 宏观判断链</h4>
<p><strong>重大事件 → 宏观环境影响 → 市场整体方向</strong></p>
<p>美伊停火协议无限期延长，地缘风险暂缓但核心分歧未解。布伦特原油突破100美元/桶推升全球通胀预期，美联储降息推迟至2027年。中国一季度GDP增长5.0%超预期，为港股提供基本面支撑。苹果换帅增添科技股不确定性。港股呈现"能源强、科技弱"结构性格局，南向资金持续净买入提供底部支撑。A股沪指重返4100点，两市成交2.56万亿放量，对港股形成正面联动。</p>
</div>

<div class="reasoning-chain">
<h4>2. 指数推导链</h4>
<p><strong>宏观判断 → 各指数差异化表现</strong></p>
<p>恒生指数：科网股全线回调拖累，但南向资金逆势净买入48.91亿港元支撑底部，能源+高股息板块抗跌，整体震荡偏弱。</p>
<p>恒生科技指数：科网股普遍回调（腾讯、阿里、美团均跌超2%），AI概念高位获利回吐，但光通信板块暴涨（剑桥科技+21%、长飞光纤+17%）显示AI算力硬件景气度持续，板块内部分化加剧。</p>
<p>国企指数：中字头能源板块受益油价高位领涨，银行高股息防御属性突出，震荡偏强。</p>
<p>美股三大指数：4月22日大幅反弹，停火延长提振风险偏好，费半14连涨显示AI算力需求仍强，但地缘风险和美联储鹰派立场限制估值扩张空间。</p>
</div>

<div class="reasoning-chain">
<h4>3. 个股推导链</h4>
<p><strong>宏观+行业+个股事件 → 个股趋势判断</strong></p>
<p>能源板块（中海油、中石油、中石化、紫金矿业、中国神华）：布伦特突破100美元/桶直接受益，南向资金大幅净买入中海油4.75亿港元居首，量价齐升逻辑最清晰。</p>
<p>AI科技板块（腾讯、百度、中芯国际、华虹半导体）：AI催化持续但内部分化，光通信暴涨带动芯片股情绪，但科网股短期回调提供布局机会。</p>
<p>新能源板块（宁德时代、比亚迪）：宁德时代超级科技日发布新电池但遭获利回吐跌5.03%，比亚迪海外拓展加速，龙头优势明显但短期承压。</p>
<p>银行板块（招行、建行、工行、中行）：高股息防御属性突出，获南向资金持续增持（建行5日+21.21亿元、工行+12.24亿元），但净息差收窄限制上行空间。</p>
<p>创新药板块（信达生物、药明生物）：分化明显，信达管线兑现+GLP-1催化看多，药明受地缘风险压制遭净卖出4.09亿元看空。</p>
</div>

<div class="reasoning-chain">
<h4>4. 关键假设</h4>
<p>① 中东停火协议得以维持，霍尔木兹海峡逐步恢复通航（不确定性：高）</p>
<p>② 美联储2026年维持利率3.5%-3.75%不变（不确定性：中）</p>
<p>③ 中国经济温和复苏，GDP增速4.5%-5.0%（不确定性：低）</p>
<p>④ AI产业资本开支维持30%以上增速（不确定性：低）</p>
<p>⑤ 南向资金日均净流入维持30亿港元以上（不确定性：中）</p>
</div>

<div class="reasoning-chain">
<h4>5. 风险提示</h4>
<p>① <strong>地缘风险再度升级</strong>：若美伊谈判破裂冲突再度升级，油价可能突破130美元/桶，全球股市将面临10%-20%回调。</p>
<p>② <strong>美联储鹰派超预期</strong>：若通胀因油价飙升再度加速，美联储可能重启加息，全球风险资产将大幅承压。</p>
<p>③ <strong>中国经济复苏不及预期</strong>：若内需持续疲弱，港股盈利端将面临下修压力。</p>
<p>④ <strong>AI投资增速放缓</strong>：若科技巨头削减AI资本开支，港股科技板块估值将面临回调。</p>
<p>⑤ <strong>霍尔木兹海峡长期受阻</strong>：若海峡航运持续中断，全球供应链风险将从能源传导至农业和制造业，引发滞胀危机。</p>
</div>

<div class="reasoning-chain">
<h4>6. 与上一份研报的不同之处</h4>
<p><strong>数据更新：</strong>美股指数数据从4月21日收盘更新至4月22日收盘（标普500从7064.01→7137.90，纳指100从26479.47→26937.27，道指从49149.38→49490.03），美股从下跌转为反弹。</p>
<p><strong>事件更新：</strong>美伊停火协议从"即将到期"变为"特朗普宣布无限期延长"，地缘风险从升级概率70%转为暂缓但不确定性仍存。</p>
<p><strong>新增ETF分析：</strong>新增盈富基金、南方恒生科技、恒生中国企业三只ETF的独立分析。</p>
<p><strong>新增个股：</strong>新增香港交易所、友邦保险、中国人寿、中国平安、中国移动、网易、百度集团、理想汽车、小鹏汽车、安踏体育、地平线机器人等11只个股分析。</p>
<p><strong>指数数据来源更新：</strong>index_data.csv中数据来源字段从"Web Search"改为具体网页链接，符合prompt.md要求。</p>
<p><strong>市场格局变化：</strong>从"能源强、科技弱"格局演变为"光通信暴涨+科网回调"的更细化结构性行情，AI算力硬件成为最强主线。</p>
</div>
</div>

<div class="section" id="section7">
<h2>七、参考资料</h2>

<h3>宏观政策类</h3>
<ul class="ref-list">
<li><a href="https://36kr.com/newsflashes/3774347781095940" target="_blank">美联储4月维持利率不变的概率为99.5%</a> — CME美联储观察数据，36氪 (36kr.com)</li>
<li><a href="http://m.toutiao.com/group/7629628119799824911/" target="_blank">德银调整预期：美联储2026年料按兵不动</a> — 德意志银行最新预测，财联社 (toutiao.com)</li>
<li><a href="https://finance.eastmoney.com/a/202604203710365193.html" target="_blank">央行圆桌汇：前景不确定性限制美联储利率指引</a> — 东方财富网 (eastmoney.com)</li>
</ul>

<h3>地缘政治类</h3>
<ul class="ref-list">
<li><a href="http://m.toutiao.com/group/7631029959393329714/" target="_blank">中东：美伊谈判生死局，停火明日到期</a> — 美伊谈判三大死结分析，今日头条 (toutiao.com)</li>
<li><a href="http://m.toutiao.com/group/7631740693873951267/" target="_blank">国际金融要情：特朗普称将无限期延长停火协议</a> — 新浪财经 (toutiao.com)</li>
<li><a href="http://m.toutiao.com/group/7631716966453101119/" target="_blank">财经早餐2026.04.23：中东地缘冲突推高能源与通胀预期</a> — 今日头条 (toutiao.com)</li>
<li><a href="https://m.weibo.cn/detail/5290127752694855" target="_blank">26艘涉伊航运船只突破美军海上封锁</a> — 微博实时战况 (weibo.cn)</li>
</ul>

<h3>行业/公司类</h3>
<ul class="ref-list">
<li><a href="http://m.toutiao.com/group/7631544400241361446/" target="_blank">港股22日收评：恒指回吐324点，光通信板块逆市暴涨</a> — 今日头条 (toutiao.com)</li>
<li><a href="http://www.xinhuanet.com/20260422/32214ffac1bc41839f99608e41ead4fa/c.html" target="_blank">港股22日跌1.22% 收报26163.24点</a> — 新华网 (xinhuanet.com)</li>
<li><a href="http://m.toutiao.com/group/7631762750552670760/" target="_blank">港股开盘：恒指跌0.25%，华勤技术IPO首日开涨超12%</a> — 今日头条 (toutiao.com)</li>
<li><a href="http://m.toutiao.com/group/7631589025953972776/" target="_blank">友邦保险连续15日回购，累计斥资38.22亿港元</a> — 证券时报 (toutiao.com)</li>
<li><a href="https://finance.sina.com.cn/stock/hkstock/ggscyd/2026-04-23/doc-inhvmvzh5051078.shtml" target="_blank">智通港股通持股解析4月23日</a> — 新浪财经 (sina.com.cn)</li>
<li><a href="https://indexes.nasdaq.com/Index/Breakdown/NDX" target="_blank">NASDAQ-100指数数据</a> — 纳斯达克官网 (nasdaq.com)</li>
</ul>

<h3>油价/大宗商品类</h3>
<ul class="ref-list">
<li><a href="http://m.toutiao.com/group/7631020092872016418/" target="_blank">国际油价涨超5.64%，4月21日24时油价或跌820元/吨</a> — 今日头条 (toutiao.com)</li>
<li><a href="https://m.cngold.org/energy/xw10455515.html" target="_blank">今日布伦特原油期货价格最新行情走势</a> — 金投网 (cngold.org)</li>
</ul>

<h3>技术分析类</h3>
<ul class="ref-list">
<li><a href="http://m.toutiao.com/group/7631709000437891625/" target="_blank">2026年4月22日收盘美股三大指数情况</a> — 今日头条 (toutiao.com)</li>
<li><a href="https://apnews.com/article/wall-street-stocks-dow-nasdaq-77e67e3711b7f809005ed4365169b211" target="_blank">How major US stock indexes fared Wednesday 4/22/2026</a> — AP News (apnews.com)</li>
<li><a href="https://www.cfi.net.cn/p20260422000105.html" target="_blank">美股4月22日收盘数据</a> — 中财网 (cfi.net.cn)</li>
</ul>
</div>

<div class="disclaimer">
<strong>免责声明：</strong>本报告仅供参考，不构成任何投资建议。市场有风险，投资需谨慎。报告中的观点和预测基于当前市场信息和分析师判断，可能随市场变化而调整。过往业绩不代表未来表现。
</div>

<div class="footer">
<p>跨市场重大事件与港股龙头策略研判 | 报告生成时间：{now_bj.strftime('%Y-%m-%d %H:%M:%S')}（北京时间）</p>
<p>数据来源：Longport API、新华网、财联社、新浪财经、东方财富网、Nasdaq官网、AP News等</p>
</div>

</div>
</body>
</html>"""

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Report generated: {filepath}")
print(f"Filename: {filename}")
