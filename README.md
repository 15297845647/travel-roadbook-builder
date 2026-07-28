# Travel Roadbook Builder

一个面向 Codex 的旅游攻略 Skill：先核验路线和交通，再生成可以真正执行、可以分享、可以打印的完整旅行路书。

它适合自驾、高铁、飞机或混合交通旅行，能够处理逐日行程、景点游玩方法、预约日历、租车取还、住宿餐饮、安全提醒、单文件 HTML 和完整彩色 PDF。

![云南 8 天 7 晚攻略效果图](docs/preview.png)

> 效果图来自本 Skill 工作流生成的真实旅行攻略 PDF 首页。

## 能做什么

- 比较自驾、高铁、飞机和包车的门到门时间、费用与疲劳程度
- 明确每座城市采用什么交通方式
- 规划租车城市、门店区域、取还车日期以及异地还车核验
- 生成日期、住宿晚数、车票和预约相互一致的逐日行程
- 展开每个景点的入口、停车、接驳、游览顺序和退出路线
- 整理门票预约渠道、放票时间、证件、退改规则与 Plan B
- 推荐住宿区域、具体酒店、餐厅、招牌菜和备选店铺
- 补充天气、高原、山路、夜间驾驶、行李与安全提醒
- 生成响应式动画 HTML、可分享单文件 HTML 和完整彩色 PDF
- 自动检查重复 ID、丢失图片、未嵌入资源、错误天数和残留旧路线

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
    D --> E[补充预约住宿美食]
    E --> F[生成动画 HTML]
    F --> G[嵌入图片成为单文件]
    G --> H[导出并逐页检查 PDF]
    H --> I[一致性校验与交付]
```

资料优先级：

1. 官方景区、政府、铁路、航空和租车信息
2. 官方酒店、餐厅页面和当前地图信息
3. 成熟预订平台
4. 小红书、马蜂窝等近期实地经验作为补充

社区内容用于发现排队、停车、摄影机位和真实体验；门票、道路、班次和安全规则仍需权威来源确认。

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
├── references/
│   ├── deliverable-spec.md
│   ├── intake-and-research.md
│   └── quality-checklist.md
└── scripts/
    ├── embed_html_images.py
    └── validate_roadbook.py
```

## 工具脚本

### 嵌入本地图片

把 HTML 中的本地图片转换为 Base64，生成可以直接发给别人的单文件版本：

```bash
python3 scripts/embed_html_images.py \
  source.html \
  shareable.html
```

远程链接仍会保留，但分享版不应再依赖本机图片路径。

### 校验攻略

```bash
python3 scripts/validate_roadbook.py \
  --html source.html \
  --bundle shareable.html \
  --pdf guide.pdf \
  --expected-days 8 \
  --must-contain "德钦" \
  --forbid "已取消目的地"
```

校验内容包括：

- 重复 HTML ID
- 无效页内链接
- 未替换的模板占位符
- 丢失或未嵌入的图片
- `data-day` 天数错误
- 必须存在或禁止残留的文本
- PDF 是否能打开、是否加密以及基础文本检查

PDF 最终仍需逐页渲染为图片，检查背景、字体、表格、分页和裁切。

## 设计原则

- 不编造班次、票价、预约规则、道路开放状态或异地还车费用
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
