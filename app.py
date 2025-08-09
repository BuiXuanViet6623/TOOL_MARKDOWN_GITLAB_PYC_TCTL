import os
import re
import datetime
import random
import traceback
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import zipfile
import io

app = Flask(__name__)
CORS(app)

FIXED_APPS = [
    "91视频", "台湾Swag", "Porn高清", "Pornbest", "Pornhub", "tiktok成人版",
    "50度灰", "黄瓜视频", "香蕉视频", "樱桃视频", "蜜桃视频", "幸福宝",
    "中国X站", "果冻传媒", "麻豆传媒", "天美传媒", "精东传媒", "大象传媒",
]

FIXED_URLS = [
    "最新在线地址", "入口地址发布页", "当前可用地址", "永久地址", "官方最新地址",
    "在线观看入口", "免费观看入口", "不用付费观看", "无广告在线播放", "高清视频免费看",
]

# DANH SÁCH TỪ KHÓA CHÍNH (PRIMARY_KEYWORDS) bạn đưa
PRIMARY_KEYWORDS = [
    "欧美18VIDEOSEX极品",
    "JAPANESEXXXⅩHD乱",
    "BDSMVIDEOS极端变态",
    "(NP、高H、纯肉)高H高辣",
    "疯狂揉小泬到失禁高潮漫画",
    "男男少年乖H调教跪趴SM主人",
    "调教家政妇",
    "饥渴放荡受NP公车",
    "顶级肉欲(军高H)1V1",
    "高H小月被几个老头调教",
    "《床戏替身(NP)》",
    "日本大尺度做爰呻吟",
    "性取向测试",
    "荷兰最开放表演女性的节目",
    "XXXXX性女HD性爽",
    "双性传奇",
    "海蒂性学报告",
    "挤奶油进去PLAY高污",
    "总裁是条骚狗(完结 番外)笔趣...",
    "吻戏高潮",
    "两个女了互添下身自慰",
    "双男主刺激战场",
    "同性男同",
    "同性",
    "一个吃我乳房一个吃我B",
    "女同性恋网",
    "善良的馊孑高潮5",
    "伦理《裸体肉欲》",
    "《黑人性奴》无删减版",
    "船开得猛的双男主剧",
    "妻情六欲",
    "《欲女春潮》美国伦理",
    "FREE性张柏芝",
    "欧州女人高潮喷水AⅤ片",
    "欧美色少妇高潮4444",
    "殴美熟妇XXOO高潮痉挛",
    "公翁太涨公欲息肉婷",
    "性别意识淡化的世界幼儿寒玉",
    "扒开双腿吃奶呻吟做受",
    "(巨肉高H)文少妇交换",
    "淑婷在公室被躁到高潮观看",
    "欢欲榨干(苏欢 高H)",
    "放荡闺蜜高H苏桃H",
    "(巨肉高H)文闺蜜",
    "娇妻被邻居脔到高潮H",
    "唔嗯啊野战H呻吟男男",
    "和尚伦流澡到高潮H",
    "性生交大片免费观看A片动态图",
    "厨房肉欲(H)冰块",
    "合欢椅H调教玉势玉珠",
    "1V1.H圆房调教H",
    "调教所",
    "双性喂奶给室友八人攻",
    "双性花唇大开开宫口",
    "全彩调教本子H里番全彩无码",
    "色欲XXOO久久久精产国品",
    "久久AV无码AV高潮AV喷",
    "任你躁X7X7X7AV在线",
    "性色AV夜夜嗨AV浪潮牛牛",
    "男主开会桌下被C得合不拢H",
    "双性少年挨脔日常H惩罚",
    "吻胸摸激情床激烈",
    "床戏裸交120秒",
    "我在野性做爰中截取了一个段落",
    "公车上拨开少妇内裤进入青少年号",
    "宝贝乖～胸罩脱了让我揉你的胸",
    "同桌上课解我胸罩玩我下面",
    "摸进她的内裤里疯狂揉她",
    "双男主做酱酱酿酿大全真人版",
    "不许穿内裤来我办公室调教",
    "少妇脱了内裤在客厅被",
    "男朋友说我的骚B只能给他日",
    "撕开奶罩揉吮奶头玩大胸",
    "韩国咬住奶头的乳三级",
    "人体艺术乳头",
    "学长含着我的乳奶晃来晃去",
    "办公室秘书胸罩太薄胸凸出来",
    "宝贝～把内裤和胸罩脱了",
    "《老师喂我乳我掀奶罩》",
    "男人揉女人的爆乳",
    "帮老师解开蕾丝奶罩吸乳网站",
    "女朋友主动拿胸给我吃",
    "清冷神明初次承欢双男主",
    "前列腺高潮",
    "攻被保镖狂C呻吟爆汁BL",
    "自慰被室友看见强行嗯啊男男",
    "男男做爰猛烈叫床XXXⅩ图片",
    "通感插头(BY金银花)",
    "拍裸戏时被C了H辣文NP动漫",
    "床戏指导(高H)",
    "少爷们的床奴NP高H",
    "男男被各种姿势C到高潮高H漫画",
    "啊顶撞潮双H龙椅榨汁NP",
    "贞操裤",
    "捆绑",
    "天奴",
    "虐之恋",
    "《办公室高潮秘书2》",
    "《艳乳欲乱2》免费观看",
    "欲望监禁",
    "成人性教育",
    "被捆绑",
    "久久久久精品国产乱码78M",
    "女主魂穿多夫洞房BY",
    "性饥渴老太XXXXXHD",
    "性VIDEOSTV另类极品",
    "疯狂三人交性欧美",
    "床戏(巨肉高H)",
    "调教刑奴",
    "调教系",
    "双男主刺激战场高清",
    "苏桃的骚乱文肉NP",
    "巨爆乳中文字幕巨爆区巨爆乳",
    "巨胸爆乳女教师奶",
    "调教超级YIN荡护士H",
    "脱警花警服露大白乳",
    "老师揉捏爆乳巨胸挤奶",
    "护士爆乳洗澡自慰流出白色液体",
    "办公室玩弄爆乳女秘HD",
    "一区二区三区SM重味",
    "小受内裤勒到中间打屁股羞耻作文",
    "荡货夹的这么紧欠C调教",
    "她扒下内裤让我爽了一夜A片",
    "精品亚洲AV无码高潮男人带套",
    "免费高H肉肉在线观看",
    "性展览",
    "裸体旅馆",
    "性公园",
    "裸体花园",
    "裸骑",
    "女裸全身无奶胸罩内裤图片",
    "裸女",
    "裸奔",
    "裸睡",
    "裸体挑战",
    "裸祭节",
    "裸穿",
    "裸晒",
    "裸贷图片",
    "女大学生裸贷",
    "淫日尽欢(H)(青卿)TX",
    "高H喷水荡肉欲文〈奴〉",
    "乳香诱人(高H)全文免费阅读",
    "高H喷水荡肉欲文〈男男〉",
    "高H粗口调教羞辱SM文女王动画",
    "JAPANESE BDSM T...",
    "主人",
    "小骚包娇喘抽搐喷潮H",
    "高H秘书不许穿内裤1V1",
    "调教小奴高潮惩罚PLAY道具",
    "蜜欲【高H】(完结)",
    "(NP、高H、纯肉)",
    "两个夫君一起满足妻主",
    "乳尖春药H糙汉",
    "古代全肉高H春药",
    "1章 饱满的乳峰喷奶水",
    "被体育老师抱着C到高潮",
    "肉欲伦JIAN",
    "磨到高潮(H)1V1",
    "做哭边走边肉楼梯PLAY",
    "男男浴室PLAY18肉车R",
    "欧美肉体裸交做爰XXXⅩ",
    "巜豪妇荡乳2做爰",
    "双性大胸产奶受H",
    "美味的双性室友",
    "双性少年的假期(H)",
    "用玉器养大的皇子双男主",
    "美人双性受H多人运动NP",
    "男男顶撞喘嗯啊H双性",
    "双性男国师被C得合不拢腿H漫画",
    "床戏指导(高H)总攻",
    "三攻一受4P巨肉寝室",
    "男倌受呻吟双腿大开H漫画",
    "男男互攻互受H啪肉NP文",
    "双性帝王受含玉势珠子",
    "双性疯狂宫交H辣粗猛",
    "日本折磨另类SM",
    "调教小游戏",
    "挤公交忘穿内裤被挺进",
    "被继夫添乳尖HD",
    "被强壮公H粗暴C高H",
    "强壮公让我高潮八次",
    "公让我达到了舒服高潮",
    "调教侵犯小男生(H)",
    "男男GAY互吃鸣巴自慰出精文",
    "双男主真人素材外网直接看",
    "办公自慰PLAY男男",
    "男性生殖生理学图",
    "两个男同用一根双头自慰器问医生",
    "美少年高潮H跪趴扩张调教喷水",
    "后宅淫事H(香艳)",
    "公主的腿间舌奴们NP肉",
    "乳尖春药H糙汉共妻",
    "公主被大臣扒开腿狂躁漫画",
    "暗卫含着她的乳尖H御书屋",
    "玉瑶公主H文H",
    "和亲公主荒淫史(H)",
    "解开她的扣子伸进她的胸罩",
    "男朋友解开内衣揉我胸",
    "大乳秘书被CAO到哭H"
]

TEMPLATES = [
    """# {title}

🎉 欢迎来到 {app}{url} 官方导航页！

尊敬的用户您好！为了让您能够轻松、快速地找到 {app} 的最新地址，我们特地建立了本官方导航页面。无论您是首次访问，还是长期使用我们的老用户，都能在这里第一时间获取最新、最稳定的访问链接。

关键词：{keywords_text}  
更新时间：{date}  

以下是您当前可用的访问入口，强烈建议收藏多个备用链接，以防主链路出现故障：

- [主站入口]({domain})  
- [备用链接一]({domain})  
- [备用链接二]({domain})  

📌 我们的优势：
- 实时监测所有链接状态，确保每条链接均可正常访问，杜绝失效情况。
- 支持各种设备，包括手机、平板和电脑，跨平台无缝体验。
- 无需注册，无需登录，完全免费，保护用户隐私安全。
- 提供简洁清爽的界面，无任何弹窗和广告打扰。

⚙️ 遇到访问问题怎么办？
- 首先尝试刷新页面或关闭浏览器缓存，清除旧数据。
- 尝试切换不同浏览器访问，比如 Chrome、Firefox 或 Edge。
- 使用浏览器隐身模式，避免浏览器扩展或缓存干扰访问。
- 如果网络环境有限制，建议使用 VPN 或代理服务，突破地理屏蔽。
- 确认您的网络连接正常，必要时切换至数据流量或其他网络环境。

✨ 我们一直致力于为用户打造安全稳定的访问环境，您的支持是我们前进的动力。请务必收藏本页面，以便随时找到最新链接。如有任何疑问或建议，欢迎通过官方联系方式反馈，我们将竭诚为您服务。

感谢您的信赖，祝您访问顺利，使用愉快！
""",

    """# {title}

🔥 {app} - {url} 最新可用地址合集！

随着网络限制日益增多，保证稳定访问优质内容成为我们最重要的目标。为此，我们精心整理并持续更新本页面，确保您可以第一时间获得 {app} 的最新可用地址。

关键词：{keywords_text}  
页面更新日期：{date}  

🔗 当前可访问地址：
- [主入口]({domain})  
- [备用入口一]({domain})  
- [备用入口二]({domain})  

为什么选择我们？
- 多线路保障，确保任一线路出现故障时能迅速切换，不影响您的观看体验。
- 采用先进的服务器集群技术，极大提升访问速度和稳定性。
- 定期更新内容，保证资源丰富多样，满足不同用户需求。
- 严格无广告政策，杜绝一切骚扰弹窗和弹广告，专注提升用户体验。
- 完全匿名访问，绝不收集任何个人信息，保护您的隐私安全。

🌟 使用技巧：
- 请尽量收藏多个链接，预防主链接偶尔因维护或封锁而暂时无法访问。
- 遇到无法访问或加载缓慢时，可尝试清理浏览器缓存或切换网络环境。
- 推荐使用最新版主流浏览器，如 Chrome、Firefox 以获得最佳性能。
- 若您身处网络受限区域，建议配合 VPN 使用，保障访问畅通。

💬 用户支持：
如您遇到任何问题或需要协助，请通过我们的官方反馈渠道联系我们。我们拥有专业的技术团队，致力于快速响应并解决访问相关问题。

感谢您一直以来的支持和理解，愿您有一个愉快的浏览体验！
""",

    """# {title}

🚀 {app} 官方跳转入口说明 - {url}

您好，欢迎访问由我们精心维护的 {app} 官方导航页面。本页面专门提供当前最新、最安全、最稳定的访问入口，确保您能顺畅浏览所有内容。

关键词聚合：{keywords_text}  
日期：{date}  

🌍 可用地址一览：
- [主站点]({domain})  
- [备用站点A]({domain})  
- [备用站点B]({domain})  

📢 访问建议：
- 移动设备推荐使用 Chrome 或 Safari 浏览器，获得最佳兼容性和体验。
- 如果您在 WiFi 网络下遇到访问障碍，建议切换到 4G/5G 移动网络或使用 VPN。
- 浏览时开启无痕/隐身模式，避免浏览器缓存对页面加载造成影响。
- 遇到页面显示异常或链接无法访问，尝试清理浏览器缓存和 Cookie。

⚙️ 技术保障：
- 本导航页面为唯一官方入口，所有链接均经过严格检测，杜绝失效和安全隐患。
- 绝无任何弹窗、广告或恶意插件，确保用户安全无忧。
- 我们每日对链接状态进行检测并及时更新，保障链接实时有效。
- 任何访问问题均可通过官方渠道反馈，获得快速专业支持。

❤️ 用户隐私：
我们尊重您的隐私，绝不追踪任何访问行为，所有访问均匿名处理。

请务必收藏本页面，确保每次访问都能快速找到有效链接。感谢您的支持和信任！
""",

    """# {title}

🌟 {app} 永久导航页 - {url}

感谢您长期以来对 {app} 的信赖与支持。由于域名被封、访问限制频发，我们特别打造本永久导航页面，集中发布每日最新、稳定可用的访问地址，确保您畅享无忧。

关键词：{keywords_text}  
最后更新：{date}  

🔗 推荐访问链接：
- [主域名]({domain})  
- [备用1]({domain})  
- [备用2]({domain})  

技术说明：
- 我们采用先进的自动监控系统，实时检测所有链接可用状态。
- 一旦发现链接失效，立即替换为最新有效地址，完全无需用户操作。
- 支持多节点服务器，保障访问速度和稳定性。

用户体验：
- 本页面无任何广告和弹窗，界面简洁清爽。
- 访问无需注册或下载安装任何软件，直接打开即可使用。
- 完全匿名访问，保障用户隐私安全。

友情提示：
- 建议您将多个备用链接收藏，以便在某条线路出现问题时，快速切换。
- 保持浏览器更新，确保兼容性。
- 若遇访问困难，可尝试使用 VPN 或切换网络环境。

感谢您的支持与配合，我们会持续优化服务，带给您更加流畅的使用体验！
""",

    """# {title}

📘 {app} - {url} 全新访问指南

网络限制日益加剧，想要稳定访问 {app} 优质内容，必须掌握正确的访问方法。本页面将为您详细介绍最有效的访问策略及资源获取渠道。

关键词聚焦：{keywords_text}  
更新时间：{date}  

推荐收藏的访问链接：
- [主入口地址]({domain})
- [备用镜像1]({domain})
- [备用镜像2]({domain})

访问受限时的解决方案：
1. 首先刷新页面或尝试更换不同的主流浏览器。
2. 检查是否启用了代理工具，尝试关闭后重新访问。
3. 切换至手机数据流量，有时运营商网络会更通畅。
4. 使用稳定的 VPN 服务，突破地域限制。

访问小贴士：
- 我们每日检测更新所有链接，确保99.99%的可用率。
- 本站不存储任何用户数据，保护您的隐私安全。
- 提供超清播放体验，兼顾流畅和清晰度。

技术支持：
如您在访问过程中遇到任何问题，请及时反馈给我们。我们拥有专门的技术团队，保障您的访问畅通无阻。

感谢您选择我们的服务，祝您体验愉快！
""",

    """# {title}

🌐 {app} 多线路访问保障 - {url}

为了满足不同地区和网络环境的访问需求，我们特意准备了多条线路供您自由选择，确保您在任何时间都能顺畅访问 {app}。

关键词：{keywords_text}  
更新日期：{date}  

访问优势：
- 多线路切换，避免单点故障，保障访问连续性。
- 支持各种设备及主流浏览器，无论电脑还是手机均适用。
- 免注册登录，无任何广告干扰，尊重您的隐私。

实用建议：
- 收藏所有推荐链接，遇到访问异常时及时切换。
- 尽量使用最新版本浏览器，提升兼容性和安全性。
- 定期清理浏览器缓存，减少访问异常。
- 若网络受限严重，建议搭配 VPN 进行访问。

问题反馈：
如发现任何异常或疑问，请通过官方渠道联系我们。我们将第一时间协助解决，保障您的正常访问。
""",

    """# {title}

📢 {app} 官方推荐访问方式 - {url}

为了确保每位用户都能享受高效稳定的访问体验，我们提供了多个官方认证的访问入口，随时满足您的访问需求。

关键词汇总：{keywords_text}  
最后更新时间：{date}  

访问链接：
- [主入口]({domain})
- [备用入口1]({domain})
- [备用入口2]({domain})

选择我们的理由：
- 高速服务器，支持全天候无间断访问。
- 节点遍布多地，提升访问速度和稳定性。
- 访问免安装，打开即用，操作简单。

访问提示：
- 推荐使用隐身模式访问，避免缓存导致访问失败。
- 遇到加载缓慢或无法访问时，尝试更换线路或刷新页面。
- 网络不佳时，可切换至移动数据流量，提高访问成功率。

您的满意是我们的动力，感谢您的支持与信任！
""",

    """# {title}

🔗 {app} 最佳访问导航 - {url}

欢迎来到官方导航页面！为了让您畅享 {app} 的所有精彩内容，我们每日更新多个有效访问链接，保障您的使用无忧。

关键词：{keywords_text}  
更新日期：{date}  

主要访问入口：
- [主链接]({domain})
- [备用链接一]({domain})
- [备用链接二]({domain})

平台特色：
- 访问稳定安全，杜绝病毒和广告骚扰。
- 支持多设备多浏览器，跨平台无障碍。
- 全免费使用，零门槛零限制。

访问建议：
- 访问时遇到问题，建议先清理浏览器缓存或切换链接。
- 保持浏览器版本更新，提升兼容性。
- 定期关注导航页面更新信息，确保链接有效。

感谢您的选择与支持，祝您浏览愉快！
""",

    """# {title}

🛠️ {app} 用户访问指南 - {url}

为了让您顺畅访问平台，我们精心整理了详细的访问说明和常见问题解答，助您无忧使用。

关键词汇总：{keywords_text}  
更新日期：{date}  

访问方法：
- 直接使用本页面提供的主入口或备用入口访问。
- 推荐使用 Chrome、Firefox 等主流浏览器，确保兼容性。
- 建议开启浏览器隐私/无痕模式，避免缓存影响。

常见问题解决：
- 页面加载慢或无法访问时，尝试刷新页面或切换网络环境。
- 链接失效时，优先尝试备用链接。
- 网络限制严重时，使用 VPN 是有效手段。

请务必收藏本页面，保证每次访问都顺畅无阻。

感谢您的支持，我们会持续优化，提供最优质的服务体验！
"""
]
OUTPUT_FOLDER = "generated_markdown_files"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def log_error(msg):
    with open("error.log", "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def sanitize_filename(text):
    return re.sub(r'[\\/*?:"<>|]', "_", text)

# Chỉnh sửa hàm generate_md_content để thêm primary_keyword đầu title
def generate_md_content(app, url, keyword_list, suffix, primary_keyword=None):
    if primary_keyword is None:
        primary_keyword = random.choice(PRIMARY_KEYWORDS)

    title = f"{primary_keyword} - {app} - {url} - {'-'.join(keyword_list)} - {suffix}"
    date_now = datetime.datetime.now().strftime("%Y-%m-%d")
    keywords_text = "，".join(keyword_list)
    subdomain = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=3))
    domain_link = f"https://{subdomain}.zaixianyule.top/"

    template = random.choice(TEMPLATES)
    content = template.format(
        title=title,
        app=app,
        url=url,
        keywords_text=keywords_text,
        suffix=suffix,
        date=date_now,
        domain=domain_link
    )
    return content

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"msg": "pong"})

@app.route("/", methods=["GET"])
def root_home():
    return jsonify({"msg": "Welcome to the Flask API. Use /ping to test or /generate to create markdown files."}), 200

@app.route("/generate", methods=["POST"])
def generate_markdown_files():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON body"}), 400

        keywords = data.get("keywords")
        cy = data.get("cy")

        if not keywords or not isinstance(keywords, list) or not all(isinstance(k, str) for k in keywords):
            return jsonify({"error": "Invalid or missing 'keywords' list"}), 400
        if not cy or not isinstance(cy, str):
            return jsonify({"error": "Invalid or missing 'cy' string"}), 400

        today_str = datetime.datetime.now().strftime("%m%d")
        suffix = f"{today_str}{cy}|881比鸭"

        used_filenames = set()
        created_files = []

        app_fixed = random.choice(FIXED_APPS)
        url_fixed = random.choice(FIXED_URLS)

        # Lấy 1 từ khóa chính random cho tất cả các file lần này
        primary_keyword = random.choice(PRIMARY_KEYWORDS)

        selected_keywords = keywords

        memory_zip = io.BytesIO()
        with zipfile.ZipFile(memory_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for keyword in selected_keywords:
                safe_keyword = sanitize_filename(keyword)
                filename = f"{safe_keyword}.md"

                # Tránh trùng tên file
                original_filename = filename
                count = 1
                while filename in used_filenames:
                    filename = f"{safe_keyword}_{count}.md"
                    count += 1
                used_filenames.add(filename)

                other_keywords = random.sample(keywords, min(2, len(keywords)))
                if keyword not in other_keywords:
                    keyword_list = [keyword] + other_keywords
                else:
                    keyword_list = other_keywords

                content = generate_md_content(app_fixed, url_fixed, keyword_list, suffix, primary_keyword=primary_keyword)
                zf.writestr(filename, content)
                created_files.append(filename)

        memory_zip.seek(0)
        zip_filename = f"Tool-MARKDOWN-TCTL-PYC-{datetime.datetime.now().strftime('%Y-%m-%d')}.zip"

        return send_file(
            memory_zip,
            as_attachment=True,
            download_name=zip_filename,
            mimetype="application/zip"
        )

    except Exception as e:
        err = f"Error: {e}\n{traceback.format_exc()}"
        log_error(err)
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Server running on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
