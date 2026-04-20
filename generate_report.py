import os
import pandas as pd
from datetime import datetime
import pytz

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

bj_tz = pytz.timezone('Asia/Shanghai')
now_bj = datetime.now(bj_tz)
report_date = now_bj.strftime('%Y年%m月%d日')
timestamp_str = now_bj.strftime('%Y%m%d%H%M%S')
filename = f"YB{timestamp_str}.html"
filepath = os.path.join(OUTPUT_DIR, filename)

df_index = pd.read_csv(os.path.join(OUTPUT_DIR, 'index_data.csv'))
df_stock = pd.read_csv(os.path.join(OUTPUT_DIR, 'stock_data.csv'))
df_cbbc = pd.read_csv(os.path.join(OUTPUT_DIR, 'cbbc_stock_data.csv'))

hsi = 26361.07
hstech = 5065.63
hscei = 8899.06
ndx = 26672.43
spx = 7126.06
dji = 49447.43

stocks_data = {
    "腾讯控股": {"code": "00700.HK", "price": 522.50},
    "阿里巴巴": {"code": "09988.HK", "price": 137.00},
    "小米": {"code": "01810.HK", "price": 32.32},
    "快手": {"code": "01024.HK", "price": 46.98},
    "京东": {"code": "09618.HK", "price": 122.40},
    "美团": {"code": "03690.HK", "price": 85.15},
    "紫金矿业": {"code": "02899.HK", "price": 37.12},
    "中芯国际": {"code": "00981.HK", "price": 59.80},
    "华虹半导体": {"code": "01347.HK", "price": 94.45},
    "泡泡玛特": {"code": "09992.HK", "price": 160.90},
    "中国神华": {"code": "01088.HK", "price": 45.18},
    "宁德时代": {"code": "03750.HK", "price": 702.50},
    "赣锋锂业": {"code": "01772.HK", "price": 80.60},
    "昆仑能源": {"code": "00135.HK", "price": 7.53},
    "中国石油化工股份": {"code": "00386.HK", "price": 4.54},
    "国泰君安国际": {"code": "01788.HK", "price": 2.67},
    "中国宏桥": {"code": "01378.HK", "price": 37.30},
    "招商银行": {"code": "03968.HK", "price": 51.10},
    "建设银行": {"code": "00939.HK", "price": 8.88},
    "中国银行": {"code": "03988.HK", "price": 5.21},
    "汇丰控股": {"code": "00005.HK", "price": 142.20},
    "信达生物": {"code": "01801.HK", "price": 91.10},
    "药明生物": {"code": "02269.HK", "price": 35.58},
    "中国海洋石油": {"code": "00883.HK", "price": 26.32},
    "中国石油股份": {"code": "00857.HK", "price": 10.34},
    "工商银行": {"code": "01398.HK", "price": 7.19},
    "比亚迪股份": {"code": "01211.HK", "price": 110.00},
}

cbbc_stocks_data = {
    "新鸿基地产": {"code": "00016.HK", "price": 135.60},
    "恒基地产": {"code": "00012.HK", "price": 30.18},
    "新世界发展": {"code": "00017.HK", "price": 8.55},
    "长实集团": {"code": "01113.HK", "price": 47.66},
    "香港交易所": {"code": "00388.HK", "price": 411.60},
    "友邦保险": {"code": "01299.HK", "price": 83.50},
    "中国人寿": {"code": "02628.HK", "price": 27.62},
    "中国平安": {"code": "02318.HK", "price": 61.50},
    "中国移动": {"code": "00941.HK", "price": 81.80},
    "中国联通": {"code": "00762.HK", "price": 7.36},
    "中国电信": {"code": "00728.HK", "price": 4.95},
    "网易": {"code": "09999.HK", "price": 183.80},
    "百度集团": {"code": "09888.HK", "price": 122.80},
    "哔哩哔哩": {"code": "09626.HK", "price": 195.40},
    "蔚来": {"code": "09866.HK", "price": 53.25},
    "理想汽车": {"code": "02015.HK", "price": 73.30},
    "小鹏汽车": {"code": "09868.HK", "price": 69.40},
    "海尔智家": {"code": "06690.HK", "price": 21.14},
    "李宁": {"code": "02331.HK", "price": 21.34},
    "安踏体育": {"code": "02020.HK", "price": 85.65},
}

def calc_rise(current, target):
    return round((target - current) / current * 100, 2)

def calc_fall(current, target):
    return round((target - current) / current * 100, 2)

def make_index_row(name, code, current, high_target, low_target):
    high_rise = calc_rise(current, high_target)
    low_fall = calc_fall(current, low_target)
    return f"""<tr>
<td>{name}</td><td>{code}</td><td>{current:,.2f}</td>
<td>{high_target:,.2f}</td><td>{high_rise}%</td>
<td>{low_target:,.2f}</td><td>{low_fall}%</td>
</tr>"""

def make_stock_row(name, code, price, trend, high, low, advice, position, events, logic):
    high_rise = calc_rise(price, high)
    low_fall = calc_fall(price, low)
    return f"""<tr>
<td>{name}</td><td>{code}</td><td>{price:.2f}</td>
<td>{trend}</td><td>{high:.2f}</td><td>{high_rise}%</td>
<td>{low:.2f}</td><td>{low_fall}%</td>
<td>{advice}</td><td>{position}</td>
<td>{events}</td><td>{logic}</td>
</tr>"""

index_analysis = [
    {"name": "恒生指数", "code": "HSI", "current": hsi, "trend": "震荡偏强", "high": 28500, "low": 24000,
     "logic": "中东局势短期扰动但停火预期仍存，南向资金持续流入，AI与新能源板块轮动支撑指数，但油价飙升对通胀构成压力，限制上行空间。"},
    {"name": "恒生科技指数", "code": "HSTECH", "current": hstech, "trend": "震荡上行", "high": 5800, "low": 4400,
     "logic": "AI应用端持续催化，科技巨头业绩预期向好，外资回流港股科技板块，但估值修复已过半程，需警惕高位回调风险。"},
    {"name": "国企指数", "code": "HSCEI", "current": hscei, "trend": "震荡偏强", "high": 9800, "low": 8000,
     "logic": "中字头板块受益于国企改革预期和分红提升，银行能源板块估值仍具吸引力，但地缘风险和油价波动构成短期压力。"},
    {"name": "纳斯达克100指数", "code": ".NDX", "current": ndx, "trend": "震荡偏强", "high": 30000, "low": 24000,
     "logic": "纳指13连涨后技术面超买，AI算力需求持续推动科技股盈利，但美联储维持高利率和地缘风险可能触发获利回吐。"},
    {"name": "标普500指数", "code": ".SPX", "current": spx, "trend": "震荡偏强", "high": 7800, "low": 6500,
     "logic": "美股屡创新高，企业盈利韧性支撑市场，但通胀粘性和美联储鹰派立场可能限制进一步上行，需关注经济数据边际变化。"},
    {"name": "道琼斯指数", "code": ".DJI", "current": dji, "trend": "震荡偏强", "high": 53000, "low": 45000,
     "logic": "道指受传统行业盈利改善推动，但油价飙升对运输和制造业成本端构成压力，美联储维持高利率环境下大盘蓝筹估值承压。"},
]

stock_analysis = [
    {"name": "腾讯控股", "code": "00700.HK", "price": 522.50, "trend": "震荡上行", "high": 620, "low": 450, "advice": "做多", "position": "持有",
     "events": "微信AI搜索功能上线，游戏版号持续获批，回购计划推进", "logic": "AI赋能核心业务提升变现效率，游戏出海加速，估值仍有修复空间。"},
    {"name": "阿里巴巴", "code": "09988.HK", "price": 137.00, "trend": "震荡上行", "high": 180, "low": 110, "advice": "做多", "position": "加仓",
     "events": "云业务AI收入快速增长，菜鸟分拆上市推进中", "logic": "电商基本盘稳固，云业务AI转型加速，估值处于历史低位具备安全边际。"},
    {"name": "小米", "code": "01810.HK", "price": 32.32, "trend": "震荡上行", "high": 42, "low": 26, "advice": "做多", "position": "加仓",
     "events": "小米汽车SU7交付量持续攀升，IoT生态扩张", "logic": "汽车业务放量带动估值重估，手机高端化战略见效，生态协同效应增强。"},
    {"name": "快手", "code": "01024.HK", "price": 46.98, "trend": "震荡偏强", "high": 58, "low": 38, "advice": "做多", "position": "持有",
     "events": "短剧和电商GMV增长超预期，海外业务减亏", "logic": "商业化效率持续提升，盈利拐点确认，但需关注用户增长天花板。"},
    {"name": "京东", "code": "09618.HK", "price": 122.40, "trend": "震荡偏弱", "high": 150, "low": 100, "advice": "观望", "position": "平仓",
     "events": "京东物流整合推进，百亿补贴效果待验证", "logic": "电商竞争加剧挤压利润率，物流优势难以完全转化为盈利，短期缺乏催化。"},
    {"name": "美团", "code": "03690.HK", "price": 85.15, "trend": "震荡偏强", "high": 105, "low": 68, "advice": "做多", "position": "持有",
     "events": "即时零售业务扩张，到店业务竞争趋缓", "logic": "本地生活壁垒稳固，新业务减亏趋势明确，盈利能力持续改善。"},
    {"name": "紫金矿业", "code": "02899.HK", "price": 37.12, "trend": "震荡上行", "high": 48, "low": 30, "advice": "做多", "position": "加仓",
     "events": "黄金价格屡创新高，铜矿产能扩张", "logic": "金价受益于地缘避险和降息预期，铜价受AI算力需求拉动，量价齐升逻辑清晰。"},
    {"name": "中芯国际", "code": "00981.HK", "price": 59.80, "trend": "震荡偏强", "high": 75, "low": 48, "advice": "做多", "position": "持有",
     "events": "成熟制程产能利用率回升，国产替代加速", "logic": "半导体国产化长期逻辑不变，成熟制程需求稳健，但先进制程突破仍需时间。"},
    {"name": "华虹半导体", "code": "01347.HK", "price": 94.45, "trend": "震荡偏弱", "high": 115, "low": 75, "advice": "观望", "position": "平仓",
     "events": "功率半导体需求分化，产能利用率恢复缓慢", "logic": "成熟制程竞争加剧，价格压力较大，需等待需求端明确改善信号。"},
    {"name": "泡泡玛特", "code": "09992.HK", "price": 160.90, "trend": "震荡偏强", "high": 200, "low": 130, "advice": "做多", "position": "持有",
     "events": "海外市场快速扩张，新IP持续孵化", "logic": "出海逻辑验证中，IP矩阵丰富度提升，但高估值需要业绩持续超预期支撑。"},
    {"name": "中国神华", "code": "01088.HK", "price": 45.18, "trend": "震荡偏强", "high": 52, "low": 38, "advice": "做多", "position": "持有",
     "events": "煤炭长协价格稳定，分红率维持高位", "logic": "高股息防御属性突出，煤价中枢上移利好盈利，但需关注新能源替代长期影响。"},
    {"name": "宁德时代", "code": "03750.HK", "price": 702.50, "trend": "震荡上行", "high": 880, "low": 580, "advice": "做多", "position": "加仓",
     "events": "固态电池技术突破，海外建厂加速", "logic": "全球动力电池龙头地位稳固，储能业务高增长，技术壁垒持续加深。"},
    {"name": "赣锋锂业", "code": "01772.HK", "price": 80.60, "trend": "震荡偏弱", "high": 100, "low": 60, "advice": "观望", "position": "平仓",
     "events": "锂价低位震荡，产能扩张与需求恢复错配", "logic": "锂价底部确认但反弹力度有限，行业供给过剩格局未根本改变。"},
    {"name": "昆仑能源", "code": "00135.HK", "price": 7.53, "trend": "震荡偏强", "high": 9.0, "low": 6.5, "advice": "做多", "position": "持有",
     "events": "天然气销售量增长，管道资产注入预期", "logic": "天然气消费量稳步增长，中石油体系内资源协同优势明显，估值偏低。"},
    {"name": "中国石油化工股份", "code": "00386.HK", "price": 4.54, "trend": "震荡偏强", "high": 5.5, "low": 3.8, "advice": "做多", "position": "持有",
     "events": "炼化盈利改善，新能源材料布局加速", "logic": "油价高位利好上游，炼化价差修复，高股息特征在震荡市中具备吸引力。"},
    {"name": "国泰君安国际", "code": "01788.HK", "price": 2.67, "trend": "震荡偏强", "high": 3.3, "low": 2.2, "advice": "做多", "position": "持有",
     "events": "港股成交额回升利好经纪业务，跨境理财通扩容", "logic": "港股市场活跃度提升直接受益，财富管理转型推进，估值处于历史低位。"},
    {"name": "中国宏桥", "code": "01378.HK", "price": 37.30, "trend": "震荡上行", "high": 46, "low": 30, "advice": "做多", "position": "加仓",
     "events": "铝价受地缘冲突支撑上涨，产能优化推进", "logic": "电解铝供给刚性约束，油价推升能源成本但铝价传导顺畅，盈利弹性大。"},
    {"name": "招商银行", "code": "03968.HK", "price": 51.10, "trend": "震荡偏强", "high": 62, "low": 43, "advice": "做多", "position": "持有",
     "events": "零售银行龙头地位稳固，财富管理业务恢复增长", "logic": "资产质量优于同业，零售业务护城河深厚，估值修复空间较大。"},
    {"name": "建设银行", "code": "00939.HK", "price": 8.88, "trend": "震荡偏强", "high": 10.5, "low": 7.5, "advice": "做多", "position": "持有",
     "events": "信贷投放稳健，分红率维持30%以上", "logic": "国有大行估值极低，股息率超7%具备配置价值，但净息差收窄压力持续。"},
    {"name": "中国银行", "code": "03988.HK", "price": 5.21, "trend": "震荡偏强", "high": 6.2, "low": 4.4, "advice": "做多", "position": "持有",
     "events": "国际化业务优势突出，跨境人民币结算量增长", "logic": "外汇业务和跨境金融优势明显，高股息低估值特征突出。"},
    {"name": "汇丰控股", "code": "00005.HK", "price": 142.20, "trend": "震荡偏强", "high": 168, "low": 125, "advice": "做多", "position": "持有",
     "events": "利率维持高位利好净息差，回购计划持续推进", "logic": "高利率环境直接受益，亚洲业务增长强劲，股东回报力度大。"},
    {"name": "信达生物", "code": "01801.HK", "price": 91.10, "trend": "震荡上行", "high": 120, "low": 70, "advice": "做多", "position": "加仓",
     "events": "PD-1海外授权推进，减重药物临床进展积极", "logic": "创新药管线持续兑现，商业化能力提升，GLP-1赛道布局具备想象空间。"},
    {"name": "药明生物", "code": "02269.HK", "price": 35.58, "trend": "震荡偏弱", "high": 45, "low": 25, "advice": "观望", "position": "平仓",
     "events": "美国生物安全法案影响持续，海外订单恢复缓慢", "logic": "地缘政治风险压制估值，短期订单恢复不确定性大，需等待政策面明朗。"},
    {"name": "中国海洋石油", "code": "00883.HK", "price": 26.32, "trend": "震荡上行", "high": 34, "low": 22, "advice": "做多", "position": "加仓",
     "events": "油价飙升直接受益，深海油气勘探突破", "logic": "地缘冲突推升油价，桶油成本行业最低，高股息+高盈利弹性双击。"},
    {"name": "中国石油股份", "code": "00857.HK", "price": 10.34, "trend": "震荡上行", "high": 13.5, "low": 8.5, "advice": "做多", "position": "加仓",
     "events": "油价高位运行利好上游，天然气业务快速增长", "logic": "油价每涨10美元增厚利润约200亿，地缘溢价直接受益，估值仍偏低。"},
    {"name": "工商银行", "code": "01398.HK", "price": 7.19, "trend": "震荡偏强", "high": 8.5, "low": 6.0, "advice": "做多", "position": "持有",
     "events": "信贷规模稳健增长，不良率持续下降", "logic": "宇宙行估值极低，股息率超8%，防御配置价值突出。"},
    {"name": "比亚迪股份", "code": "01211.HK", "price": 110.00, "trend": "震荡上行", "high": 145, "low": 88, "advice": "做多", "position": "加仓",
     "events": "海外市场拓展加速，智能驾驶技术突破", "logic": "新能源车全球销量龙头，海外放量打开第二增长曲线，智能化升级提升产品力。"},
]

cbbc_stock_analysis = [
    {"name": "新鸿基地产", "code": "00016.HK", "price": 135.60, "trend": "震荡偏弱", "high": 155, "low": 115, "advice": "观望", "position": "平仓",
     "events": "香港楼市成交回暖但价格承压，利率维持高位增加融资成本", "logic": "高利率环境压制地产估值，楼市复苏力度不及预期，短期缺乏催化。"},
    {"name": "恒基地产", "code": "00012.HK", "price": 30.18, "trend": "震荡偏弱", "high": 35, "low": 25, "advice": "观望", "position": "平仓",
     "events": "农地转换进展缓慢，楼市去化压力仍存", "logic": "地产板块整体承压，利率高位增加持有成本，需等待楼市政策进一步放松。"},
    {"name": "新世界发展", "code": "00017.HK", "price": 8.55, "trend": "震荡下行", "high": 10, "low": 6.5, "advice": "做空", "position": "根据当前预设，做空无仓位调整建议",
     "events": "债务压力较大，出售资产回笼资金", "logic": "财务杠杆过高，降杠杆过程压制估值，地产业务恢复缓慢。"},
    {"name": "长实集团", "code": "01113.HK", "price": 47.66, "trend": "震荡偏弱", "high": 55, "low": 40, "advice": "观望", "position": "平仓",
     "events": "飞机租赁业务稳健，地产销售承压", "logic": "多元化业务提供一定防御，但地产核心业务仍受高利率压制。"},
    {"name": "香港交易所", "code": "00388.HK", "price": 411.60, "trend": "震荡偏强", "high": 480, "low": 360, "advice": "做多", "position": "持有",
     "events": "港股成交额回升，IPO市场回暖", "logic": "市场活跃度提升直接受益，垄断地位不可替代，但需关注地缘风险对资金流向的影响。"},
    {"name": "友邦保险", "code": "01299.HK", "price": 83.50, "trend": "震荡偏强", "high": 98, "low": 70, "advice": "做多", "position": "持有",
     "events": "新业务价值增长稳健，内地访客需求强劲", "logic": "亚太寿险龙头地位稳固，利率高位利好投资收益，估值处于合理区间。"},
    {"name": "中国人寿", "code": "02628.HK", "price": 27.62, "trend": "震荡偏强", "high": 34, "low": 22, "advice": "做多", "position": "持有",
     "events": "保费收入增长，投资收益改善", "logic": "寿险行业景气度回升，权益市场回暖利好投资端，估值修复空间较大。"},
    {"name": "中国平安", "code": "02318.HK", "price": 61.50, "trend": "震荡偏强", "high": 75, "low": 50, "advice": "做多", "position": "持有",
     "events": "综合金融生态协同增强，科技赋能降本增效", "logic": "金融+科技双轮驱动，寿险改革成效显现，估值处于历史低位。"},
    {"name": "中国移动", "code": "00941.HK", "price": 81.80, "trend": "震荡偏强", "high": 95, "low": 70, "advice": "做多", "position": "持有",
     "events": "5G用户渗透率提升，算力网络建设加速", "logic": "高股息+稳增长特征突出，AI算力需求拉动云业务增长，防御价值显著。"},
    {"name": "中国联通", "code": "00762.HK", "price": 7.36, "trend": "震荡偏强", "high": 8.8, "low": 6.2, "advice": "做多", "position": "持有",
     "events": "产业互联网收入占比提升，大数据业务增长", "logic": "数字化转型加速，产业互联网打开增长空间，估值偏低具备安全边际。"},
    {"name": "中国电信", "code": "00728.HK", "price": 4.95, "trend": "震荡偏强", "high": 6.0, "low": 4.2, "advice": "做多", "position": "持有",
     "events": "天翼云收入高速增长，AI大模型落地应用", "logic": "云业务增速行业领先，AI+通信融合催化，高股息率具备配置吸引力。"},
    {"name": "网易", "code": "09999.HK", "price": 183.80, "trend": "震荡偏强", "high": 220, "low": 155, "advice": "做多", "position": "持有",
     "events": "新游戏上线表现优异，AI赋能游戏研发提效", "logic": "游戏管线丰富，AI降本增效逻辑清晰，海外市场拓展顺利。"},
    {"name": "百度集团", "code": "09888.HK", "price": 122.80, "trend": "震荡上行", "high": 155, "low": 100, "advice": "做多", "position": "加仓",
     "events": "文心大模型持续迭代，自动驾驶商业化推进", "logic": "AI搜索和大模型商业化加速，自动驾驶Robotaxi落地，估值修复空间大。"},
    {"name": "哔哩哔哩", "code": "09626.HK", "price": 195.40, "trend": "震荡偏强", "high": 240, "low": 160, "advice": "做多", "position": "持有",
     "events": "广告和增值服务收入高增长，首次实现季度盈利", "logic": "盈利拐点确认，社区生态变现效率提升，但估值偏高需业绩持续验证。"},
    {"name": "蔚来", "code": "09866.HK", "price": 53.25, "trend": "震荡偏弱", "high": 65, "low": 38, "advice": "观望", "position": "平仓",
     "events": "换电网络扩张，但交付量增长放缓", "logic": "换电模式差异化但资本开支大，销量增速落后竞品，盈利时点不确定。"},
    {"name": "理想汽车", "code": "02015.HK", "price": 73.30, "trend": "震荡偏强", "high": 92, "low": 58, "advice": "做多", "position": "持有",
     "events": "纯电车型上市，智驾技术迭代", "logic": "产品矩阵完善，家庭用车定位精准，但纯电转型效果待验证。"},
    {"name": "小鹏汽车", "code": "09868.HK", "price": 69.40, "trend": "震荡偏强", "high": 88, "low": 52, "advice": "做多", "position": "持有",
     "events": "MONA系列销量超预期，智驾技术领先", "logic": "智驾技术护城河加深，大众合作推进，但盈利能力仍需改善。"},
    {"name": "海尔智家", "code": "06690.HK", "price": 21.14, "trend": "震荡偏强", "high": 26, "low": 18, "advice": "做多", "position": "持有",
     "events": "海外市场盈利改善，高端品牌卡萨帝增长", "logic": "全球化布局成效显现，高端化战略提升盈利能力，估值合理。"},
    {"name": "李宁", "code": "02331.HK", "price": 21.34, "trend": "震荡偏弱", "high": 26, "low": 16, "advice": "观望", "position": "平仓",
     "events": "国潮热度退减，库存去化进行中", "logic": "运动服饰竞争加剧，品牌力边际减弱，需等待渠道改革和产品创新见效。"},
    {"name": "安踏体育", "code": "02020.HK", "price": 85.65, "trend": "震荡偏强", "high": 105, "low": 70, "advice": "做多", "position": "持有",
     "events": "亚玛芬体育整合顺利，多品牌战略成效显著", "logic": "多品牌矩阵覆盖各细分市场，全球化进程加速，经营效率行业领先。"},
]

index_rows = ""
for ia in index_analysis:
    index_rows += make_index_row(ia["name"], ia["code"], ia["current"], ia["high"], ia["low"])

stock_rows = ""
for sa in stock_analysis:
    stock_rows += make_stock_row(sa["name"], sa["code"], sa["price"], sa["trend"], sa["high"], sa["low"], sa["advice"], sa["position"], sa["events"], sa["logic"])

cbbc_rows = ""
for ca in cbbc_stock_analysis:
    cbbc_rows += make_stock_row(ca["name"], ca["code"], ca["price"], ca["trend"], ca["high"], ca["low"], ca["advice"], ca["position"], ca["events"], ca["logic"])

index_table_csv = df_index.to_html(index=False, classes="data-table", border=0, escape=False)
stock_table_csv = df_stock.to_html(index=False, classes="data-table", border=0, escape=False)
cbbc_table_csv = df_cbbc.to_html(index=False, classes="data-table", border=0, escape=False)

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
.highlight {{ background: #fff9c4; padding: 2px 5px; border-radius: 3px; }}
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
<li><a href="#section1-2">1.2 指定个股数据表</a></li>
<li><a href="#section1-3">1.3 拥有可交易牛熊证的额外港股个股数据表</a></li>
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
<li><a href="#section4">四、个股分析</a>
<ul class="sub">
<li><a href="#section4-1">4.1 指定个股分析</a></li>
<li><a href="#section4-2">4.2 当前存在可交易牛熊证的个股分析</a></li>
</ul>
</li>
<li><a href="#section5">五、分析推理过程</a></li>
<li><a href="#section6">六、参考资料</a></li>
</ul>
</div>

<div class="section" id="section1">
<h2>一、市场数据</h2>

<h3 id="section1-1">1.1 指数数据表</h3>
{index_table_csv}

<h3 id="section1-2">1.2 指定个股数据表</h3>
{stock_table_csv}

<h3 id="section1-3">1.3 拥有可交易牛熊证的额外港股个股数据表</h3>
{cbbc_table_csv}
</div>

<div class="section" id="section2">
<h2>二、重大事件分析</h2>

<h3 id="section2-1">2.1 近期已发生的重大事件</h3>

<div class="event-card">
<h4>1. 美伊临时停火协议即将到期，中东局势急剧恶化</h4>
<p class="time">发生时间：2026年4月17日-20日</p>
<p><strong>事件概述：</strong>美伊此前为期两周的临时停火协议将于4月21日深夜到期，双方谈判彻底破裂。4月20日美军在阿曼湾向伊朗商船开火并强行登船扣押，伊朗定性为"海盗行径"誓言强硬报复。霍尔木兹海峡航运受阻，约3200艘船舶滞留海湾。</p>
<p><strong>对市场的影响机制：</strong>地缘冲突升级直接推升国际油价（WTI涨至约89美元/桶，布伦特涨至约96美元/桶），避险情绪传导至全球股市，港股受南向资金对冲需求支撑但波动加剧。</p>
<p><strong>后续进展预期：</strong>若停火协议到期后冲突进一步升级，油价可能突破100美元/桶；若巴基斯坦斡旋成功重启谈判，地缘溢价将快速消退。</p>
<p><strong>对市场的持续影响评估：</strong>高油价将推升全球通胀预期，延缓美联储降息时点，对港股能源板块构成利好，但对科技和消费板块形成压制。</p>
</div>

<div class="event-card">
<h4>2. 美股三大指数创历史新高，纳指13连涨</h4>
<p class="time">发生时间：2026年4月17日（美东时间）</p>
<p><strong>事件概述：</strong>标普500指数收报7126.06点涨1.20%，道指收报49447.43点涨1.79%，纳指收报24468.48点涨1.52%。纳指连续13个交易日上涨，追平1992年以来最长连涨纪录。</p>
<p><strong>对市场的影响机制：</strong>美股强势对全球风险偏好形成正向传导，港股科技股联动上涨，但需警惕连涨后的技术性回调风险。</p>
<p><strong>后续进展预期：</strong>若美联储4月28-29日议息会议释放偏鹰信号，美股可能面临获利回吐压力。</p>
<p><strong>对市场的持续影响评估：</strong>美股高位运行对港股形成情绪支撑，但估值分化加剧，需关注资金轮动方向。</p>
</div>

<div class="event-card">
<h4>3. 恒生科技指数重返5000点，港股AI板块领涨</h4>
<p class="time">发生时间：2026年4月16日-20日</p>
<p><strong>事件概述：</strong>受美伊停火消息提振，4月16日恒生科技指数大涨3.67%至5092.08点，收复5000点整数关口。科网股普涨，百度涨超7%，阿里巴巴领涨。4月20日恒指收报26361.07点涨0.77%。</p>
<p><strong>对市场的影响机制：</strong>AI应用端催化持续，外资回流港股科技板块，南向资金同步加仓，形成资金共振。</p>
<p><strong>后续进展预期：</strong>AI算力需求持续增长，Google Cloud Next大会（4月22-24日）可能发布新一代TPU，进一步催化AI产业链。</p>
<p><strong>对市场的持续影响评估：</strong>AI主题仍是港股核心主线，但估值修复已过半程，需关注业绩兑现能力。</p>
</div>

<div class="event-card">
<h4>4. 美联储3月会议纪要显示利率维持3.5%-3.75%不变</h4>
<p class="time">发生时间：2026年4月8日（美东时间）</p>
<p><strong>事件概述：</strong>美联储3月17-18日FOMC会议纪要显示，维持联邦基金利率目标区间3.5%-3.75%不变，为连续第二次按兵不动。德意志银行预计美联储2026年将维持利率不变。</p>
<p><strong>对市场的影响机制：</strong>高利率环境延续对港股估值形成压制，但市场已充分定价，边际影响减弱。油价飙升可能进一步推迟降息预期。</p>
<p><strong>后续进展预期：</strong>4月28-29日议息会议大概率维持利率不变（概率99.5%），6月降息概率仅4.5%。</p>
<p><strong>对市场的持续影响评估：</strong>利率高位延长将压制港股估值修复节奏，但南向资金对冲效应增强。</p>
</div>

<div class="event-card">
<h4>5. 国际油价飙升，WTI突破89美元/桶</h4>
<p class="time">发生时间：2026年4月20日</p>
<p><strong>事件概述：</strong>受中东局势恶化影响，WTI原油涨至约89.49美元/桶（涨幅6.72%），布伦特原油涨至约95.52美元/桶（涨幅5.68%）。国内成品油调价窗口将于4月21日24时开启。</p>
<p><strong>对市场的影响机制：</strong>油价飙升直接利好港股能源板块（中海油、中石油、中石化），但推升通胀预期，对制造业和消费板块构成成本压力。</p>
<p><strong>后续进展预期：</strong>若霍尔木兹海峡持续受阻，油价可能突破100美元/桶；若局势缓和，地缘溢价将快速消退。</p>
<p><strong>对市场的持续影响评估：</strong>油价中枢上移将重塑市场风格，能源板块超额收益可期，但整体市场风险偏好受压。</p>
</div>

<h3 id="section2-2">2.2 未来一周将要发生的重大事件</h3>

<div class="event-card">
<h4>1. 美伊临时停火协议到期（4月21日深夜）</h4>
<p class="time">预计时间：2026年4月21日深夜（北京时间4月22日早8点）</p>
<p><strong>事件概述：</strong>美伊两周临时停火协议到期，双方谈判已破裂，军事冲突风险显著上升。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario base">基准情景（概率45%）：停火协议到期后双方维持低烈度对峙，油价短期冲高后回落，全球股市震荡加剧</span></p>
<p><span class="scenario optimistic">乐观情景（概率20%）：巴基斯坦斡旋成功，双方同意延长停火或重启谈判，地缘溢价快速消退，油价回落至80美元以下，全球风险资产反弹</span></p>
<p><span class="scenario pessimistic">悲观情景（概率35%）：冲突全面升级，霍尔木兹海峡长期受阻，油价突破100美元/桶，全球股市大幅回调，避险资产暴涨</span></p>
</div>

<div class="event-card">
<h4>2. 美联储主席候选人沃什参议院听证会（4月21日）</h4>
<p class="time">预计时间：2026年4月21日</p>
<p><strong>事件概述：</strong>美联储主席候选人凯文·沃什将出席参议院听证会，其货币政策立场将影响市场对未来利率路径的预期。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario base">基准情景（概率50%）：沃什表态偏中性，强调数据依赖，市场反应温和</span></p>
<p><span class="scenario optimistic">乐观情景（概率25%）：沃什释放偏鸽信号，暗示若通胀回落将支持降息，美股和港股科技股上涨</span></p>
<p><span class="scenario pessimistic">悲观情景（概率25%）：沃什表态偏鹰，强调通胀风险，市场降息预期进一步推迟，风险资产承压</span></p>
</div>

<div class="event-card">
<h4>3. Google Cloud Next大会（4月22日-24日）</h4>
<p class="time">预计时间：2026年4月22日-24日</p>
<p><strong>事件概述：</strong>谷歌将举办Google Cloud Next大会，预计发布新一代TPU架构，并披露内存池化和光路交换机（OCS）等技术进展，对AI算力产业链可能产生重要影响。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario base">基准情景（概率45%）：TPU架构迭代符合预期，AI算力需求叙事延续，相关个股温和上涨</span></p>
<p><span class="scenario optimistic">乐观情景（概率35%）：新一代TPU性能大幅提升，AI算力投资加速，港股AI概念股（中芯国际、华虹半导体等）大涨</span></p>
<p><span class="scenario pessimistic">悲观情景（概率20%）：发布内容不及预期，AI投资增速放缓担忧升温，科技股回调</span></p>
</div>

<div class="event-card">
<h4>4. 全球6G技术与产业生态大会（4月21日-23日）</h4>
<p class="time">预计时间：2026年4月21日-23日，南京</p>
<p><strong>事件概述：</strong>2026全球6G技术与产业生态大会将推动6G从概念走向产业生态，对通信产业链形成催化。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario base">基准情景（概率55%）：6G技术路线图进一步明确，通信板块温和反应</span></p>
<p><span class="scenario optimistic">乐观情景（概率30%）：6G标准推进超预期，运营商和设备商估值重估，中国移动、中国电信等上涨</span></p>
<p><span class="scenario pessimistic">悲观情景（概率15%）：6G商业化时间表推迟，市场反应平淡</span></p>
</div>

<div class="event-card">
<h4>5. 特斯拉、贵州茅台等一季报披露</h4>
<p class="time">预计时间：2026年4月21日-25日</p>
<p><strong>事件概述：</strong>特斯拉、贵州茅台、新易盛等重点公司将披露一季报，业绩表现将影响相关板块情绪。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario base">基准情景（概率45%）：特斯拉业绩符合预期，茅台稳健增长，市场反应中性</span></p>
<p><span class="scenario optimistic">乐观情景（概率25%）：特斯拉交付量超预期+AI进展，茅台增速超预期，消费和新能源板块联动上涨</span></p>
<p><span class="scenario pessimistic">悲观情景（概率30%）：特斯拉利润率下滑，茅台增速放缓，相关板块承压</span></p>
</div>

<div class="event-card">
<h4>6. 美联储发布经济状况褐皮书（4月23日）</h4>
<p class="time">预计时间：2026年4月23日（美东时间）</p>
<p><strong>事件概述：</strong>美联储将发布经济状况褐皮书，揭示不确定性与关税政策对地区经济的实际影响，制造业投入价格指数尤其值得关注。</p>
<p><strong>可能的市场影响情景分析：</strong></p>
<p><span class="scenario base">基准情景（概率50%）：经济温和增长，通胀压力持续但不恶化，市场反应有限</span></p>
<p><span class="scenario optimistic">乐观情景（概率20%）：经济韧性超预期，通胀回落迹象明显，降息预期升温</span></p>
<p><span class="scenario pessimistic">悲观情景（概率30%）：滞胀风险上升，高油价传导至核心通胀，美联储鹰派立场强化</span></p>
</div>

<h3 id="section2-3">2.3 重点关注领域</h3>

<h4>⭐⭐⭐ 美联储货币政策</h4>
<div class="event-card">
<p><strong>最新立场：</strong>3月FOMC会议维持利率3.5%-3.75%不变，连续第二次按兵不动。4月28-29日将召开下一次议息会议，维持利率不变概率高达99.5%。</p>
<p><strong>利率路径预期：</strong>德意志银行预计2026年全年维持利率不变。CME数据显示6月降息概率仅4.5%，加息概率0.5%。芝加哥联储主席古尔斯比称若油价长期高企，美联储可能需等到2027年才会降息。</p>
<p><strong>缩表节奏：</strong>缩表仍在持续，但节奏已放缓。市场流动性边际改善但整体仍偏紧。</p>
<p><strong>官员近期表态：</strong>圣路易斯联储主席穆萨莱姆称高油价可能使基本通胀率比2%目标高出近一个百分点，美联储可能需要维持利率不变。整体基调偏鹰。</p>
</div>

<h4>⭐⭐⭐ 中东地缘政治危机</h4>
<div class="event-card">
<p><strong>冲突最新动态：</strong>美伊临时停火协议4月21日深夜到期，谈判已破裂。4月20日美军在阿曼湾向伊朗商船开火，霍尔木兹海峡航运受阻，3200艘船舶滞留。三支美军航母编队压境。</p>
<p><strong>对油价影响：</strong>WTI原油涨至约89.49美元/桶（+6.72%），布伦特原油涨至约95.52美元/桶（+5.68%）。若冲突升级，油价可能突破100美元/桶。</p>
<p><strong>避险情绪传导：</strong>全球避险情绪升温，黄金和美元走强，港股受南向资金对冲支撑但波动加剧。</p>
<p><strong>供应链风险：</strong>霍尔木兹海峡承担全球约30%石油海运，若长期受阻将严重冲击全球供应链，推升制造业成本。</p>
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
<tr>
<td>恒生指数</td><td>HSI</td><td>{hsi:,.2f}</td>
<td><span class="tag strong">震荡偏强</span></td>
<td>28,500.00</td><td>{calc_rise(hsi, 28500)}%</td>
<td>24,000.00</td><td>{calc_fall(hsi, 24000)}%</td>
<td>中东局势短期扰动但停火预期仍存，南向资金持续流入，AI与新能源板块轮动支撑指数，但油价飙升对通胀构成压力限制上行空间。</td>
</tr>
<tr>
<td>恒生科技指数</td><td>HSTECH</td><td>{hstech:,.2f}</td>
<td><span class="tag up">震荡上行</span></td>
<td>5,800.00</td><td>{calc_rise(hstech, 5800)}%</td>
<td>4,400.00</td><td>{calc_fall(hstech, 4400)}%</td>
<td>AI应用端持续催化，科技巨头业绩预期向好，外资回流港股科技板块，但估值修复已过半程需警惕高位回调风险。</td>
</tr>
<tr>
<td>国企指数</td><td>HSCEI</td><td>{hscei:,.2f}</td>
<td><span class="tag strong">震荡偏强</span></td>
<td>9,800.00</td><td>{calc_rise(hscei, 9800)}%</td>
<td>8,000.00</td><td>{calc_fall(hscei, 8000)}%</td>
<td>中字头板块受益于国企改革预期和分红提升，银行能源板块估值仍具吸引力，但地缘风险和油价波动构成短期压力。</td>
</tr>
<tr>
<td>纳斯达克100指数</td><td>.NDX</td><td>{ndx:,.2f}</td>
<td><span class="tag strong">震荡偏强</span></td>
<td>30,000.00</td><td>{calc_rise(ndx, 30000)}%</td>
<td>24,000.00</td><td>{calc_fall(ndx, 24000)}%</td>
<td>纳指13连涨后技术面超买，AI算力需求持续推动科技股盈利，但美联储维持高利率和地缘风险可能触发获利回吐。</td>
</tr>
<tr>
<td>标普500指数</td><td>.SPX</td><td>{spx:,.2f}</td>
<td><span class="tag strong">震荡偏强</span></td>
<td>7,800.00</td><td>{calc_rise(spx, 7800)}%</td>
<td>6,500.00</td><td>{calc_fall(spx, 6500)}%</td>
<td>美股屡创新高企业盈利韧性支撑市场，但通胀粘性和美联储鹰派立场可能限制进一步上行，需关注经济数据边际变化。</td>
</tr>
<tr>
<td>道琼斯指数</td><td>.DJI</td><td>{dji:,.2f}</td>
<td><span class="tag strong">震荡偏强</span></td>
<td>53,000.00</td><td>{calc_rise(dji, 53000)}%</td>
<td>45,000.00</td><td>{calc_fall(dji, 45000)}%</td>
<td>道指受传统行业盈利改善推动，但油价飙升对运输和制造业成本端构成压力，美联储维持高利率环境下大盘蓝筹估值承压。</td>
</tr>
</tbody>
</table>
</div>

<div class="section" id="section4">
<h2>四、个股分析</h2>

<h3 id="section4-1">4.1 指定个股分析</h3>

<table class="data-table">
<thead>
<tr>
<th>股票名称</th><th>股票代码</th><th>当前最新价格(HKD)</th>
<th>未来一个月趋势预判</th>
<th>截止2026年12月31日最高目标价</th><th>最高目标价相对最新价格涨幅</th>
<th>截止2026年12月31日最低目标价</th><th>最低目标价相对最新价格跌幅</th>
<th>当前做多做空建议</th><th>当前仓位调整建议</th>
<th>近期个股自身重大事件</th><th>未来一个月趋势预判的核心逻辑</th>
</tr>
</thead>
<tbody>
{stock_rows}
</tbody>
</table>

<h3 id="section4-2">4.2 当前存在可交易牛熊证的个股分析</h3>

<table class="data-table">
<thead>
<tr>
<th>股票名称</th><th>股票代码</th><th>当前最新价格(HKD)</th>
<th>未来一个月趋势预判</th>
<th>截止2026年12月31日最高目标价</th><th>最高目标价相对最新价格涨幅</th>
<th>截止2026年12月31日最低目标价</th><th>最低目标价相对最新价格跌幅</th>
<th>当前做多做空建议</th><th>当前仓位调整建议</th>
<th>近期个股自身重大事件</th><th>未来一个月趋势预判的核心逻辑</th>
</tr>
</thead>
<tbody>
{cbbc_rows}
</tbody>
</table>
</div>

<div class="section" id="section5">
<h2>五、分析推理过程</h2>

<div class="reasoning-chain">
<h4>1. 宏观判断链</h4>
<p><strong>重大事件 → 宏观环境影响 → 市场整体方向</strong></p>
<p>中东冲突升级（美伊停火破裂、霍尔木兹海峡受阻）→ 油价飙升（WTI约89美元、布伦特约96美元）→ 全球通胀预期上修 → 美联储降息预期推迟至2027年 → 全球流动性维持偏紧 → 风险资产估值承压但盈利端分化。同时，AI产业趋势持续强化（Google Cloud Next催化），结构性机会依然存在。港股受南向资金对冲需求支撑，整体呈现"上有顶、下有底"格局。</p>
</div>

<div class="reasoning-chain">
<h4>2. 指数推导链</h4>
<p><strong>宏观判断 → 各指数差异化表现</strong></p>
<p>恒生指数：能源+银行板块高股息支撑底部，科技板块AI催化提供弹性，但油价飙升压制消费和制造端，整体震荡偏强。</p>
<p>恒生科技指数：AI应用端催化最强，外资回流+南向加仓形成资金共振，但估值修复过半后上行斜率放缓，震荡上行。</p>
<p>国企指数：中字头分红+能源板块受益油价，但银行净息差收窄压力持续，震荡偏强。</p>
<p>美股三大指数：纳指13连涨后超买，AI算力需求支撑盈利但高利率压制估值，震荡偏强。道指受油价成本端压力更大，标普居中。</p>
</div>

<div class="reasoning-chain">
<h4>3. 个股推导链</h4>
<p><strong>宏观+行业+个股事件 → 个股趋势判断</strong></p>
<p>能源板块（中海油、中石油、中石化、紫金矿业）：油价飙升直接受益，量价齐升逻辑清晰，目标价上行空间最大。</p>
<p>AI科技板块（腾讯、百度、中芯国际）：AI催化持续，但需区分业绩兑现能力，腾讯和百度确定性最高。</p>
<p>新能源车板块（比亚迪、理想、小鹏）：国内销量稳健+海外拓展，比亚迪龙头优势最大。</p>
<p>银行板块（招行、建行、工行、中行）：高股息防御属性突出，但净息差收窄限制上行空间。</p>
<p>地产板块（新鸿基、恒基、新世界）：高利率环境持续压制，短期缺乏催化，建议观望或做空。</p>
<p>创新药板块（信达生物、药明生物）：分化明显，信达管线兑现+GLP-1催化看多，药明受地缘风险压制观望。</p>
</div>

<div class="reasoning-chain">
<h4>4. 关键假设</h4>
<p>① 中东冲突不会演变为全面战争，霍尔木兹海峡受阻时间不超过2周（不确定性：高）</p>
<p>② 美联储2026年维持利率3.5%-3.75%不变（不确定性：中）</p>
<p>③ 中国经济温和复苏，GDP增速4.5%-5.0%（不确定性：中）</p>
<p>④ AI产业资本开支维持30%以上增速（不确定性：低）</p>
<p>⑤ 南向资金日均净流入维持50亿港元以上（不确定性：中）</p>
</div>

<div class="reasoning-chain">
<h4>5. 风险提示</h4>
<p>① <strong>地缘风险超预期升级</strong>：若中东冲突演变为全面战争，油价可能突破120美元/桶，全球股市将面临10%-20%回调。</p>
<p>② <strong>美联储鹰派超预期</strong>：若通胀因油价飙升再度加速，美联储可能重启加息，全球风险资产将大幅承压。</p>
<p>③ <strong>中国经济复苏不及预期</strong>：若内需持续疲弱，港股盈利端将面临下修压力。</p>
<p>④ <strong>AI投资增速放缓</strong>：若科技巨头削减AI资本开支，港股科技板块估值将面临回调。</p>
<p>⑤ <strong>流动性风险</strong>：若南向资金流入放缓或外资大幅流出，港股可能面临流动性冲击。</p>
</div>
</div>

<div class="section" id="section6">
<h2>六、参考资料</h2>

<h3>宏观政策类</h3>
<ul class="ref-list">
<li><a href="https://36kr.com/newsflashes/3774347781095940" target="_blank">美联储4月维持利率不变的概率为99.5%</a> — CME美联储观察数据，36氪 (36kr.com)</li>
<li><a href="http://m.toutiao.com/group/7626715012748280363/" target="_blank">美联储3月FOMC会议纪要：维持利率3.5%-3.75%不变</a> — 3月17-18日会议纪要，今日头条 (toutiao.com)</li>
<li><a href="https://finance.eastmoney.com/a/202604203710365193.html" target="_blank">央行圆桌汇：前景不确定性限制美联储利率指引</a> — 东方财富网 (eastmoney.com)</li>
<li><a href="http://m.toutiao.com/group/7629628119799824911/" target="_blank">德银调整预期：美联储2026年料按兵不动</a> — 德意志银行最新预测，财联社 (toutiao.com)</li>
</ul>

<h3>地缘政治类</h3>
<ul class="ref-list">
<li><a href="http://m.toutiao.com/group/7630731934590714377/" target="_blank">2026年4月下旬国际局势：中东战火一触即发</a> — 美伊停火破裂与军事冲突分析，今日头条 (toutiao.com)</li>
<li><a href="http://m.toutiao.com/group/7630749110064218659/" target="_blank">中东48小时巨变：霍尔木兹海峡断航全球命脉告急</a> — 海峡航运受阻与油价影响，今日头条 (toutiao.com)</li>
<li><a href="http://m.toutiao.com/group/7630755214777205294/" target="_blank">白宫放狠话"经济狂怒"：美伊博弈进入"死局"</a> — 美国对伊制裁升级，今日头条 (toutiao.com)</li>
<li><a href="http://m.toutiao.com/group/7630687238212403712/" target="_blank">战与和反复拉锯：美伊多轨博弈进入新阶段</a> — 巴基斯坦斡旋外交，央视新闻 (toutiao.com)</li>
</ul>

<h3>行业/公司类</h3>
<ul class="ref-list">
<li><a href="https://finance.eastmoney.com/a/202604203710698228.html" target="_blank">恒生指数上涨0.77% 恒生科技指数上涨0.46%</a> — 港股4月20日收盘数据，东方财富网 (eastmoney.com)</li>
<li><a href="http://m.toutiao.com/group/7629645148204319282/" target="_blank">港股收盘：本周三大指数集体震荡上行 AI算力与新能源领涨</a> — 本周港股行情总结，财联社 (toutiao.com)</li>
<li><a href="http://m.toutiao.com/group/7630291106327970367/" target="_blank">每周热点集锦(2026年4月13日至19日)</a> — 港股科技板块反弹与AI催化，今日头条 (toutiao.com)</li>
<li><a href="http://m.toutiao.com/group/7629467526610649652/" target="_blank">美股：标普500与纳斯达克100指数续创新高</a> — 美股连涨分析，新浪财经 (toutiao.com)</li>
<li><a href="https://indexes.nasdaq.com/Index/Breakdown/NDX" target="_blank">NASDAQ-100指数数据</a> — 纳斯达克100指数官方数据，Nasdaq (nasdaq.com)</li>
</ul>

<h3>技术分析类</h3>
<ul class="ref-list">
<li><a href="http://m.toutiao.com/group/7629593073999184420/" target="_blank">港股大跌A股遇压：后市会怎么走？</a> — 技术面回调分析，今日头条 (toutiao.com)</li>
<li><a href="http://m.toutiao.com/group/7630639844066099727/" target="_blank">美伊临时停火将到期：一周前瞻</a> — 本周重大事件日历，21世纪经济报道 (toutiao.com)</li>
<li><a href="http://m.toutiao.com/group/7630427830769254953/" target="_blank">一周重磅日程：沃什听证会、美伊停火到期</a> — 本周市场前瞻，华尔街见闻 (toutiao.com)</li>
</ul>
</div>

<div class="disclaimer">
<strong>免责声明：</strong>本报告仅供参考，不构成任何投资建议。市场有风险，投资需谨慎。报告中的观点和预测基于当前市场信息和分析师判断，可能随市场变化而调整。过往业绩不代表未来表现。
</div>

<div class="footer">
<p>跨市场重大事件与港股龙头策略研判 | 报告生成时间：{now_bj.strftime('%Y-%m-%d %H:%M:%S')}（北京时间）</p>
<p>数据来源：Longport API、AKShare API、东方财富网、Nasdaq官网、中财网等</p>
</div>

</div>
</body>
</html>"""

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Report generated: {filepath}")
print(f"Filename: {filename}")
