# Travel Roadbook Builder

一个面向 Codex 的旅游攻略 Skill：先核验并确认路线和交通，再按选择生成可以真正执行、可以分享、可以打印的旅行路书。

它适合自驾、高铁、飞机或混合交通旅行，能够处理逐日行程、景点游玩方法、预约日历、租车取还、住宿餐饮、安全提醒、单文件 HTML 和完整彩色 PDF。

![云南 8 天 7 晚攻略效果图](docs/preview.png)

> 效果图来自本 Skill 工作流生成的真实旅行攻略 PDF 首页。

## 完整示例

仓库提供一套由本 Skill 工作流生成的云南 8 天 7 晚完整成品，可用于查看信息深度、视觉设计和文件交付效果：

- [可分享单文件 HTML](examples/yunnan-8d7n-roadbook.html)：实景图片已嵌入，不依赖发送者电脑上的本地路径
- [完整彩色 PDF](examples/yunnan-8d7n-roadbook.pdf)：包含路线、逐日时间轴、预约、住宿、美食、装备和风险预案

示例中的班次、票价、预约、住宿和道路信息具有时效性。规划新旅行时应重新核验，不要直接把示例数据当作当前事实。

## 能做什么

- 比较自驾、高铁、飞机和包车的门到门时间、费用与疲劳程度
- 区分“规划 → 已确认 → 生成”三个状态；只有行程事实一致并获确认后才制作最终文件
- 在确认行程后明确提供“路书、路书+PDF、继续修改”三种交付选择
- 持续记录固定日期、必去体验、驾驶上限和已经否决的方案，避免多轮修改后漂移
- 区分普通转场与“公路本身就是景点”的景观自驾，不会为缩短时间擅自删掉核心体验
- 解释两份路线里程或驾驶时间为何不同，统一起终点、途经点和计时口径后再修改
- 明确每座城市采用什么交通方式
- 规划租车城市、门店区域、取还车日期以及异地还车核验
- 生成日期、住宿晚数、车票和预约相互一致的逐日行程
- 展开每个景点的入口、停车、接驳、游览顺序和退出路线
- 整理门票预约渠道、放票时间、证件、退改规则与 Plan B
- 推荐住宿区域、具体酒店，并为每个在店用餐餐次给出具体分店主选、1–2 家备选、推荐菜、理由与当天动线
- 默认综合小红书近期真实体验，交叉验证独立笔记、识别营销、区分体验可信度与营业事实
- 补充天气、高原、山路、夜间驾驶、行李与安全提醒
- 生成响应式动画 HTML、可分享单文件 HTML 和完整彩色 PDF
- 自动检查重复 ID、丢失图片、未嵌入资源、错误天数/晚数和 HTML/PDF 残留旧路线

## 安装

把整个目录复制到个人 Codex Skill 目录：

```bash
mkdir -p ~/.codex/skills
cp -R travel-roadbook-builder ~/.codex/skills/
```

新建一个 Codex 任务后，即可通过 `$travel-roadbook-builder` 调用。

## 使用示例

```text
使用 $travel-roadbook-builder：

我计划 9 月 24 日凌晨抵达昆明，10 月 1 日从昆明返回。
想去大理、丽江、香格里拉和德钦，在德钦看日照金山。
请比较每段使用高铁还是自驾，并明确在哪个城市取车、还车。
每天尽量不要驾驶超过 5 小时。

请生成：
1. 推荐路线和轻松备选路线
2. 8 天 7 晚逐日时间轴
3. 景点具体游玩方法和预约日历
4. 酒店、餐厅、装备和安全提醒
5. 可分享的单文件 HTML
6. 保留完整背景和图片的彩色 PDF
```

上例已指定期望产物，因此不会在确认后重复询问交付形式；但 Skill 仍会先补齐会影响路线的事实，并等待你确认完整行程后再生成文件。

也可以要求它修改已有攻略：

```text
使用 $travel-roadbook-builder 检查这份路线。
重点核对日期、住宿晚数、租车取还、每天真实驾驶时间，
并把取消的城市从景点、餐厅、预算和预约表中全部清除。
```

## 工作方式

```mermaid
flowchart LR
    A[确认日期与偏好] --> B[核验实时资料]
    B --> C[比较交通与路线]
    C --> D[锁定逐日主表]
    D --> E[按景点补齐预约住宿美食]
    E --> F[确认完整行程]
    F --> G[选择路书/PDF]
    G --> H[生成所选产物]
    H --> I[嵌入图片、导出并逐页检查 PDF]
    I --> J[一致性校验与交付]
```

资料优先级：

1. 官方及实时信息，包括景区、政府、交通、天气和经营方信息
2. 当前地图与导航，用于位置、分店、路线和交通核验
3. 小红书近期独立亲历笔记与有实质内容的评论
4. 其他攻略、旅行报告和预订平台的推荐内容

实际预订库存与交易条件仍以官方或对应预订系统为准。社区内容用于发现餐厅、排队、停车、摄影机位和驾驶体验；封路、天气、开放规则与班次以适用日期的官方/实时信息为准。

### 小红书能力与降级

本 Skill 提供搜索与核验规则，不附带或自动安装小红书 MCP。若环境中有 `xhs-search` / `xhs-explore` 或等价搜索、详情工具，会按实际工具说明调用；没有时尝试公开网页搜索，明确披露全文或评论无法读取的限制。搜索摘要不等于已验证笔记，不编造收藏数或阅读记录。

按本次目的地动态生成搜索主题，不预设固定地区。日出、雪山观景等体验结合有效天气预报；超预报范围采用条件性方案与复核节点。具体规则见 [小红书旅行与美食搜索](references/xiaohongshu-travel-and-food.md)。

## 交付范围

提供旅行规划、按天路线安排、地图信息核验、可分享 HTML 路书与可选 PDF。不生成导航链接、平台行程分享入口、KML/GPX 导入文件，也不为路书交付要求地图账号登录或手机镜像。

## 目录结构

```text
travel-roadbook-builder/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── roadbook-template.html
├── docs/
│   └── preview.png
├── examples/
│   ├── yunnan-8d7n-roadbook.html
│   └── yunnan-8d7n-roadbook.pdf
├── references/
│   ├── deliverable-spec.md
│   ├── intake-and-research.md
│   ├── maps-and-transport.md
│   ├── xiaohongshu-integration.md
│   ├── plan-data-model.md
│   ├── provenance.md
│   ├── xiaohongshu-travel-and-food.md
│   ├── revision-and-route-audit.md
│   └── quality-checklist.md
├── scripts/
│   ├── embed_html_images.py
│   └── validate_roadbook.py
└── tests/
    └── test_*.py
```

## 工具脚本

### 嵌入本地图片

把 HTML 中的本地图片和 CSS 背景图转换为 Base64，生成可以直接发给别人的单文件版本：

```bash
python3 scripts/embed_html_images.py \
  source.html \
  shareable.html
```

远程链接仍会保留，但分享版不应再依赖本机图片路径。本地资源默认必须位于源 HTML 所在目录内；使用 `--base-dir` 时，该目录就是明确的可信资源根目录，脚本会拒绝 `../`、目录外绝对路径和越界符号链接。

### 校验攻略

```bash
python3 scripts/validate_roadbook.py \
  --html source.html \
  --bundle shareable.html \
  --pdf guide.pdf \
  --expected-days 8 \
  --expected-nights 7 \
  --expected-revision "YOUR-REVISION-ID" \
  --must-contain "德钦" \
  --forbid "已取消目的地" \
  --strict-pdf-text
```

校验内容包括：

- 重复 HTML ID
- 无效页内链接
- 未替换的模板占位符
- 丢失或未嵌入的普通图片、Hero 图和 CSS 背景资源
- `data-day` 天数、顺序和 `data-sleep` 住宿晚数错误
- 源 HTML 与分享版 revision 不一致
- HTML、分享版和 PDF 中必须存在或禁止残留的文本
- PDF 是否能打开、是否加密以及严格文本回归检查

PDF 最终仍需逐页渲染为图片，检查背景、字体、表格、分页和裁切。

上面的 revision、关键词和文件名是调用示例，请替换成当前路书的真实值。

## 设计原则

- 不编造班次、票价、预约规则、道路开放状态或异地还车费用
- 不因追求最短车程擅自删除用户明确要求的景观公路或体验
- 不使用不同起终点、途经点或计时口径比较驾驶里程
- 不用单纯导航时间掩盖真实驾驶疲劳
- 不让视觉效果遮住高反、山路、天气和误机风险
- 不把小红书等社区内容当作安全规则的唯一来源
- 不交付仍引用本机路径的“单文件”HTML
- 不交付未经逐页渲染检查的 PDF

## 环境要求

- Codex
- Python 3.10+
- 生成 PDF 时建议使用 Chromium 打印引擎或 Codex PDF 工具
- PDF 检查建议安装 Poppler 和 `pypdf`

基础的 HTML 图片嵌入只使用 Python 标准库。

## License

当前仓库未附加开源许可证。公开分发或接受外部贡献前，请根据需要添加合适的 `LICENSE`。
