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

TEMPLATES = [
    # Template 1
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
- 实时监测所有链接状态，确保每条链接均可正常访问，杜绝失效情况，为您的浏览体验提供最强保障。
- 支持各种设备，包括手机、平板和电脑，跨平台无缝体验，不受硬件限制。
- 无需注册，无需登录，完全免费，保护用户隐私安全，做到真正的零门槛访问。
- 提供简洁清爽的界面设计，没有任何干扰弹窗，让您专注于内容本身。
- 海量优质资源实时更新，确保内容丰富多样，满足不同用户的需求。
- 系统采用先进的 CDN 加速技术，让您在全球任何地区都能快速加载页面。
- 所有链接均通过加密传输，保障您的数据和隐私安全。

⚙️ 遇到访问问题怎么办？
- 尝试刷新页面或关闭浏览器缓存，避免旧数据影响加载速度。
- 切换不同浏览器访问，比如 Chrome、Firefox 或 Edge，以提高兼容性。
- 使用隐身模式，减少浏览器插件或缓存干扰。
- 如果网络环境有限制，可以使用高质量 VPN 或代理服务突破封锁。
- 检查网络连接是否稳定，必要时切换至移动数据网络。
- 如果多个备用入口都不可用，请等待我们更新最新链接，或联系技术支持团队获取帮助。

✨ 我们致力于为用户打造安全稳定的访问环境，请务必收藏本页面，确保您随时都能找到最新的访问入口。""",

    # Template 2
    """# {title}

🔥 {app} - {url} 最新可用地址合集！

随着网络环境不断变化，稳定访问高质量内容变得至关重要。为此，我们为您打造了这一官方导航页，持续更新最新可用链接，让您无论何时何地都能顺利进入 {app}。

关键词：{keywords_text}  
页面更新日期：{date}  

🔗 当前可访问地址：
- [主站入口]({domain})
- [备用链接一]({domain})
- [备用链接二]({domain})

💎 为什么选择我们？
- 多线路保障技术，确保任何线路出现问题时，您都能即时切换，保持流畅体验。
- 后端采用分布式服务器架构，大幅提升访问速度和页面加载效率。
- 所有资源持续更新，涵盖多种类型与主题，满足各类用户需求。
- 严格执行无广告策略，保证浏览过程纯净无干扰。
- 支持匿名访问，避免个人数据被收集和追踪。
- 采用高强度加密技术，确保您的访问数据和账户安全。

🌟 使用技巧：
- 收藏本页面，确保在主链接不可用时可以快速找到备用入口。
- 遇到访问缓慢可尝试清理缓存，或切换至不同网络环境。
- 推荐使用最新版 Chrome、Firefox、Edge 等浏览器。
- 在网络受限地区，建议搭配 VPN 工具，提升连接成功率。
- 如果遇到 DNS 污染问题，可以尝试修改 DNS 至 8.8.8.8 或 1.1.1.1。

💬 用户支持：
如遇到问题，请通过官方反馈通道联系技术团队，我们将快速响应，为您解决访问困难。""",

    # Template 3
    """# {title}

🚀 {app} 官方跳转入口说明 - {url}

欢迎访问由我们官方维护的 {app} 导航页面！本页面专为您提供最新、最安全的访问入口，不论您是日常使用还是临时需要，都能第一时间获取有效链接。

关键词：{keywords_text}  
日期：{date}  

🌍 可用地址一览：
- [主站入口]({domain})
- [备用链接一]({domain})
- [备用链接二]({domain})

📢 使用建议：
- 移动端用户建议使用 Chrome 或 Safari，以确保最佳兼容性和速度。
- WiFi 网络受限时，可切换至 4G/5G 移动网络，或使用优质 VPN 服务。
- 开启浏览器隐私模式，避免缓存和插件影响访问。
- 出现页面异常时，及时清理浏览器缓存与 Cookie。
- 若遇到页面无法加载，请更换不同设备进行测试。

⚙️ 技术保障：
- 全部链接均通过严格检测，确保无病毒、无恶意代码。
- 全天候监控链接可用性，保证实时有效。
- 无广告、无弹窗，为用户提供纯净安全的体验。
- 分布式服务器架构，在不同地区都有快速节点。

❤️ 用户隐私：
我们尊重每位用户的隐私，不追踪访问行为，所有数据均匿名处理，请放心使用。""",

    # Template 4
    """# {title}

🌟 {app} 永久导航页 - {url}

感谢您对 {app} 的支持！由于网络封锁和访问限制频繁，我们特别建立此永久导航页，每日发布最新可用的访问入口，让您无障碍使用平台功能。

关键词：{keywords_text}  
最后更新：{date}  

🔗 推荐访问链接：
- [主站入口]({domain})
- [备用链接一]({domain})
- [备用链接二]({domain})

🔒 技术说明：
- 采用自动监控系统，实时检测链接状态并自动替换失效地址。
- 全球多节点加速，确保不同地区均可高速访问。
- 服务器加密传输数据，防止中间人攻击和隐私泄露。
- 数据中心拥有多重防护机制，保障平台安全运行。

💡 用户体验：
- 无需注册，直接访问，省去繁琐步骤。
- 界面简洁干净，无广告打扰，提升使用舒适度。
- 支持多种设备和系统，兼容性极强。
- 保证所有内容持续更新，满足长期使用需求。

📌 温馨提示：
- 收藏备用链接，避免因单一入口失效而无法访问。
- 保持浏览器更新至最新版本，减少兼容性问题。
- 遇到限制严重时，建议搭配 VPN 工具使用。
- 如果多条线路同时失效，请及时关注我们的公告频道。""",
  # Template 6
    """# {title}

🌐 **{app} 多线路访问保障 - {url}**

尊敬的用户，欢迎来到 {app} 官方多线路访问保障页面！我们深知，在当今复杂多变的网络环境下，保持平台稳定畅通对于您的使用体验至关重要。为了让全球各地的用户无论何时何地都能顺利访问，我们建立了这一页面，并为您准备了多条经过严格检测的访问线路。

关键词：{keywords_text}  
更新日期：{date}  

## 🌍 为什么需要多线路访问？
互联网的开放性带来了无限可能，但也不可避免地面临地区封锁、网络波动、运营商限制等问题。这些因素可能导致您访问平台时出现延迟、卡顿甚至无法打开页面的情况。为了最大限度降低风险，我们为您提供了多条备用访问通道，并实时监控这些通道的可用性。

## 📡 访问链接：
- [主站入口]({domain})
- [备用链接一]({domain})
- [备用链接二]({domain})

## 💪 访问优势：
- **多线路自由切换**：当某条线路出现延迟或中断时，您可以立即切换至备用线路，确保访问不中断。
- **全平台兼容**：无论您使用的是 Windows、Mac、Android、iOS 还是 Linux 系统，均可顺畅访问。
- **加密传输**：我们采用 TLS/SSL 加密技术保护您的数据安全，防止被窃取或篡改。
- **全球加速节点**：智能选择离您最近的节点，大幅度缩短响应时间，减少延迟。

## 💡 使用建议：
1. **收藏所有推荐链接**：以防某一入口暂时不可用时，您仍有替代方案。
2. **定期清理浏览器缓存**：避免缓存的过期数据影响加载速度。
3. **更新浏览器版本**：保持兼容性和安全性。
4. **使用隐身模式**：减少插件干扰，提升访问稳定性。
5. **网络受限地区建议使用 VPN**：优质的 VPN 可绕过限制，提升访问速度。

## ❓ 常见问题解答：
- **Q：链接打不开怎么办？**  
  A：尝试切换备用链接或刷新页面，并清除浏览器缓存。
- **Q：访问速度慢怎么办？**  
  A：切换到其他线路，或尝试使用移动数据网络。
- **Q：使用 VPN 是否安全？**  
  A：选择可靠的付费 VPN 服务，避免免费 VPN 可能带来的隐私风险。

## 🛠 技术支持：
我们拥有 24 小时在线监控系统和响应机制，一旦发现主入口不可用，会立即切换为备用线路，并在此页面更新最新信息。请务必收藏本页面，确保您随时掌握最新的访问方式。

---

""",

    # Template 7
    """# {title}

📢 **{app} 官方推荐访问方式 - {url}**

欢迎您访问 {app} 官方推荐访问页面！在当前网络环境下，访问速度和稳定性不仅仅取决于您的网络质量，还受服务器位置、传输协议、安全防护等多方面因素影响。为了保障用户的最佳体验，我们在此集中发布最优质的访问方式与通道。

关键词：{keywords_text}  
最后更新时间：{date}  

## 🔗 访问链接：
- [主站入口]({domain})
- [备用链接一]({domain})
- [备用链接二]({domain})

## 🚀 我们的优势：
- **高速服务器集群**：采用分布式架构，确保即使访问高峰期也不会拥堵。
- **多地加速节点**：无论您身在何处，系统都会自动为您选择最快的线路。
- **稳定性保障**：全天候 7x24 监控，故障秒级切换，最大限度降低中断风险。
- **简单易用**：不需要下载任何客户端，打开链接即可使用。
- **隐私保护**：严格遵循数据保护法规，不记录、不追踪用户行为。

## 💡 使用提示：
1. **使用隐身模式或无痕浏览**：避免插件缓存造成的加载失败。
2. **切换不同网络环境**：如从 Wi-Fi 改用 4G/5G 移动数据。
3. **尝试不同浏览器**：Chrome、Firefox、Edge 等浏览器对现代加密协议支持更佳。
4. **收藏本页面**：在主入口不可用时可第一时间使用备用通道。

## ❓ 常见问题：
- **为什么有多个链接？**  
  因为不同线路可能受不同网络策略影响，备用线路是为了防止访问中断。
- **是否需要付费才能使用？**  
  不需要，所有访问链接均为官方免费提供。
- **VPN 一定要用吗？**  
  如果您所在地区限制严格，使用 VPN 可以提升成功率，但大多数情况下无需额外工具。

## 🙏 致用户：
您的支持与反馈是我们持续优化的动力，我们将不断提升平台的安全性与易用性，确保您在任何情况下都能顺利访问。""",

    # Template 8
    """# {title}

🔗 **{app} 最佳访问导航 - {url}**

感谢您访问 {app} 官方最佳访问导航页面！我们深知在当下网络环境中，保持平台的可访问性至关重要。此页面为您提供每日更新的最新可用入口，让您不论身处何地都能流畅体验平台服务。

关键词：{keywords_text}  
更新日期：{date}  

## 🌟 主要访问入口：
- [主站入口]({domain})
- [备用链接一]({domain})
- [备用链接二]({domain})

## 💎 平台特色：
- **高度安全的访问环境**：采用全程加密传输，确保信息不会被窃听。
- **多平台兼容**：支持电脑、手机、平板等所有主流设备。
- **无广告干扰**：页面简洁清爽，加载速度快。
- **智能线路分配**：系统会根据您的位置自动匹配最佳访问路径。

## 💡 使用建议：
1. 收藏本导航页面，方便快速获取最新入口。
2. 出现访问异常时，先尝试备用链接。
3. 定期清理浏览器缓存，避免因旧数据导致加载缓慢。
4. 在网络限制较严的环境中，使用 VPN 或代理服务。

## ❓ 常见问题：
- **为什么有时速度变慢？**  
  网络拥堵、线路负载高都会影响速度，切换备用线路通常能解决问题。
- **备用链接安全吗？**  
  所有链接均为官方提供，经过安全检测，请放心使用。
- **是否会收集用户信息？**  
  我们承诺不收集任何个人数据，所有访问均为匿名状态。

""",

    # Template 9
    """# {title}

🛠️ **{app} 用户访问指南 - {url}**

为了帮助广大用户在任何情况下都能顺利访问 {app}，我们特别整理了这份详细的用户访问指南，包含最新的入口地址、使用技巧以及常见问题的解决方案。

关键词：{keywords_text}  
更新日期：{date}  

## 📍 访问方法：
- [主站入口]({domain})
- [备用链接一]({domain})
- [备用链接二]({domain})

## 💡 使用技巧：
1. **收藏全部入口**：这样即使一个入口暂时无法访问，您也能迅速切换。
2. **切换网络环境**：Wi-Fi 不佳时可以使用 4G/5G，反之亦然。
3. **更新浏览器**：确保支持最新的加密协议和技术。
4. **使用隐私模式**：防止缓存数据影响访问。

## ❓ 常见问题解决：
- **页面加载慢**：清理缓存或切换备用链接。
- **链接不可用**：检查是否有防火墙或安全软件拦截。
- **无法播放内容**：尝试更换浏览器或升级版本。

""",

    # Template 10
    """# {title}

🌈 **{app} 高速稳定访问页 - {url}**

本页面专为热爱 {app} 的用户准备，旨在确保无论您身处何地，都能高速、稳定、无障碍地访问平台内容。

关键词：{keywords_text}  
更新日期：{date}  

## 🌍 高速访问链接：
- [主站入口]({domain})
- [备用链接一]({domain})
- [备用链接二]({domain})

## 💪 平台优势：
- **全天候服务器监控**：保证平台高可用性，故障即时修复。
- **分布式加速节点**：优化各地区访问速度，减少延迟。
- **安全纯净**：无广告、无恶意插件。

## 💡 使用建议：
1. 收藏多个入口，防止临时封锁影响使用。
2. 使用最新版浏览器提升加载体验。
3. 网络不佳时，可使用 VPN 确保稳定连接。
  
]

OUTPUT_FOLDER = "generated_markdown_files"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def log_error(msg):
    with open("error.log", "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def sanitize_filename(text):
    return re.sub(r'[\\/*?:"<>|]', "_", text)

def generate_md_content(app, url, keyword_list, suffix):
    title = f"{app}-{url}-{'-'.join(keyword_list)}-{suffix}"
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

        # Lấy toàn bộ từ khóa, tạo 1 bài cho mỗi từ khóa
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

                content = generate_md_content(app_fixed, url_fixed, keyword_list, suffix)
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

