import html
import json
import re
import shutil
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "content" / "site-content.json"
BLOG_DATA_FILE = ROOT / "content" / "blog-posts.json"
BLOG_CONTENT_DIR = ROOT / "content" / "blog"
BLOG_MEDIA_DIR = ROOT / "content" / "blog-media"
OUT_DIR = ROOT / "static-site"
ASSETS_DIR = OUT_DIR / "assets"
DESIGN_DIR = ROOT / "design-system"
LOGO_SOURCE = ROOT / "brand" / "icentech-logo-horizontal.png"
LOGO_ASSET_NAME = "icentech-logo-horizontal.png"

BRAND_TOKENS = {
    "brand_blue_700": "#0c79d6",
    "brand_blue_500": "#0596ef",
    "brand_blue_300": "#8fd0ff",
    "brand_green_600": "#63a60b",
    "brand_green_500": "#78c515",
    "brand_green_200": "#dff3b8",
    "ink": "#11344c",
    "ink_soft": "#33576d",
    "line": "#d4e4ee",
    "mist": "#eef8ff",
    "surface": "#ffffff",
    "surface_alt": "#f6fbfe",
}

THEME_MAP = {
    "home": {"primary": "#0c79d6", "secondary": "#0596ef", "accent": "#78c515", "soft": "#eef8ff"},
    "translation": {"primary": "#0c79d6", "secondary": "#2e8de4", "accent": "#78c515", "soft": "#edf8d8"},
    "dtp": {"primary": "#0a6bbd", "secondary": "#21a3f6", "accent": "#9ed93b", "soft": "#f4fbeb"},
    "engineering": {"primary": "#095ea7", "secondary": "#0d8de5", "accent": "#63a60b", "soft": "#eaf6ff"},
    "testing": {"primary": "#0f6dbe", "secondary": "#31a4ec", "accent": "#7cca1a", "soft": "#eefbf1"},
    "video-production": {"primary": "#0e78ca", "secondary": "#2eaaf7", "accent": "#7fcf29", "soft": "#eef8ff"},
    "interpreting": {"primary": "#0f75c8", "secondary": "#3c9ce7", "accent": "#86c92e", "soft": "#effaf0"},
    "document-localization": {"primary": "#0b78d1", "secondary": "#37a1f2", "accent": "#75bf19", "soft": "#f1f9e8"},
    "website-localization": {"primary": "#0b7bd5", "secondary": "#10a1e7", "accent": "#78c515", "soft": "#eef9ff"},
    "apps-localization": {"primary": "#0d72c8", "secondary": "#2e9ae8", "accent": "#8acd2f", "soft": "#eef9ff"},
    "multimedia-localization": {"primary": "#1176cc", "secondary": "#37a6ef", "accent": "#6fbe14", "soft": "#eefbff"},
    "elearning-localization": {"primary": "#0a70bf", "secondary": "#1da0ec", "accent": "#8bce2c", "soft": "#f1faec"},
    "technology": {"primary": "#0a66b6", "secondary": "#0596ef", "accent": "#78c515", "soft": "#edf8ff"},
    "ai": {"primary": "#0970c3", "secondary": "#14a2ef", "accent": "#8ad128", "soft": "#eefaff"},
    "company": {"primary": "#0f75c8", "secondary": "#2d97e3", "accent": "#6fbe14", "soft": "#f0f9eb"},
    "news-blog": {"primary": "#0b79d1", "secondary": "#2aa2ee", "accent": "#8bce2c", "soft": "#eef9ff"},
    "career": {"primary": "#0b71c3", "secondary": "#0f97e3", "accent": "#7cca1a", "soft": "#eef8ff"},
    "freelance": {"primary": "#0d78cc", "secondary": "#1ca1ea", "accent": "#84ca28", "soft": "#eff9ef"},
}

MENU_GROUPS = [
    {
        "title_en": "HOME",
        "title_zh": "首页",
        "items": [{"en": "Home", "zh": "首页", "slug": ""}],
    },
    {
        "title_en": "SERVICES",
        "title_zh": "服务",
        "items": [
            {"en": "Translation", "zh": "翻译服务", "slug": "translation"},
            {"en": "DTP", "zh": "DTP 排版", "slug": "dtp"},
            {"en": "Engineering", "zh": "国际化工程", "slug": "engineering"},
            {"en": "Testing", "zh": "本地化测试", "slug": "testing"},
            {"en": "Video Production", "zh": "多语视频制作", "slug": "video-production"},
            {"en": "Interpreting", "zh": "口译服务", "slug": "interpreting"},
        ],
    },
    {
        "title_en": "LOCALIZATION",
        "title_zh": "本地化",
        "items": [
            {"en": "Document", "zh": "文档本地化", "slug": "document-localization"},
            {"en": "Website", "zh": "网站本地化", "slug": "website-localization"},
            {"en": "Apps", "zh": "软件与应用本地化", "slug": "apps-localization"},
            {"en": "Multimedia", "zh": "多媒体本地化", "slug": "multimedia-localization"},
            {"en": "eLearning", "zh": "eLearning 本地化", "slug": "elearning-localization"},
        ],
    },
    {
        "title_en": "TECHNOLOGY",
        "title_zh": "技术",
        "items": [
            {"en": "Technology", "zh": "技术能力", "slug": "technology"},
            {"en": "AI", "zh": "AI 语言解决方案", "slug": "ai"},
        ],
    },
    {
        "title_en": "ABOUT US",
        "title_zh": "关于我们",
        "items": [
            {"en": "Company", "zh": "公司介绍", "slug": "company"},
            {"en": "News & Blog", "zh": "新闻与博客", "slug": "news-blog"},
            {"en": "Career", "zh": "加入我们", "slug": "career"},
            {"en": "Freelance", "zh": "自由职业合作", "slug": "freelance"},
        ],
    },
]

PAGE_RELATIONS = {
    "translation": ["dtp", "document-localization", "technology"],
    "dtp": ["translation", "document-localization", "multimedia-localization"],
    "engineering": ["testing", "apps-localization", "technology"],
    "testing": ["engineering", "apps-localization", "website-localization"],
    "video-production": ["multimedia-localization", "elearning-localization", "interpreting"],
    "interpreting": ["video-production", "ai", "company"],
    "document-localization": ["translation", "dtp", "website-localization"],
    "website-localization": ["document-localization", "apps-localization", "testing"],
    "apps-localization": ["engineering", "testing", "ai"],
    "multimedia-localization": ["video-production", "elearning-localization", "translation"],
    "elearning-localization": ["multimedia-localization", "video-production", "document-localization"],
    "technology": ["ai", "engineering", "translation"],
    "ai": ["technology", "translation", "testing"],
    "company": ["technology", "career", "freelance"],
    "news-blog": ["technology", "ai", "company"],
    "career": ["company", "freelance", "technology"],
    "freelance": ["career", "company", "translation"],
}

HOME_SECTIONS = {
    "en": {
        "eyebrow": "One team for multilingual delivery",
        "trust": [
            "Translation, localization, QA, and engineering together",
            "100+ languages supported",
            "Human review with AI support",
        ],
        "stats": [
            {"value": "100+", "label": "Languages supported"},
            {"value": "6", "label": "Core service areas"},
            {"value": "One team", "label": "Single delivery partner"},
            {"value": "AI + Human", "label": "Balanced workflow"},
        ],
        "value_cards": [
            {"title": "Less coordination", "body": "You work with one team instead of multiple vendors."},
            {"title": "Clearer delivery", "body": "Each page explains what you get and when to use it."},
            {"title": "Faster decisions", "body": "Shorter copy helps buyers understand the offer quickly."},
        ],
        "process": ["Share your goal", "Confirm scope and languages", "Produce and review", "Deliver and improve"],
        "ai_ready_title": "ISO 17100 and ISO 18587 certified",
        "ai_ready_body": "Our translation and post-editing workflows follow recognized international standards for quality and consistency.",
        "ai_ready_points": [
            "ISO 17100:2015 for translation services",
            "ISO 18587:2017 for machine translation post-editing",
            "A better fit for projects that need clear process and dependable review",
        ],
        "cta_title": "Need a simpler multilingual workflow?",
        "cta_body": "Start with the service pages below and see which setup fits your next launch.",
    },
    "zh": {
        "eyebrow": "一支团队完成多语言交付",
        "trust": [
            "把翻译、本地化、测试和工程放到一起",
            "支持 100+ 语言",
            "人工把关，AI 提效",
        ],
        "stats": [
            {"value": "100+", "label": "支持语言"},
            {"value": "6", "label": "核心服务方向"},
            {"value": "一个团队", "label": "统一交付窗口"},
            {"value": "AI + 人工", "label": "平衡效率与质量"},
        ],
        "value_cards": [
            {"title": "更少沟通成本", "body": "你不需要同时协调多个供应商。"},
            {"title": "更清楚的交付", "body": "每一页都直接说明能帮你解决什么。"},
            {"title": "更快做决定", "body": "文案更短、更直接，更容易判断是否匹配。"},
        ],
        "process": ["告诉我们目标", "确认范围和语言", "执行与复核", "交付与优化"],
        "ai_ready_title": "通过 ISO 17100 与 ISO 18587 认证",
        "ai_ready_body": "我们的翻译与机器翻译后编辑流程，按照国际通行标准执行，更重视质量、一致性和可追踪交付。",
        "ai_ready_points": [
            "ISO 17100:2015 翻译服务标准",
            "ISO 18587:2017 机器翻译后编辑标准",
            "更适合重视流程规范与复核质量的项目",
        ],
        "cta_title": "想把多语言流程做得更简单？",
        "cta_body": "先从下面的服务页开始，看哪种方式最适合你的项目。",
    },
}

PAGE_DETAILS = {
    "": {
        "theme": "home",
        "en": {
            "intro": "If you need one partner for multilingual content and product delivery, iCentech brings translation, localization, engineering, QA, and AI support together.",
            "highlights": [
                "One team across content and product work",
                "Clear process from request to delivery",
                "Support for ongoing multilingual updates",
            ],
            "workflow": ["Share your goal", "Plan the scope", "Produce and review", "Deliver"],
            "fit": ["Global product teams", "Marketing and content teams", "Companies entering new markets"],
            "outputs": ["Clear service options", "Structured delivery flow", "Reusable multilingual support"],
            "eyebrow": "Global language support",
        },
        "zh": {
            "intro": "如果你希望用一个合作伙伴完成多语言内容和产品交付，iCentech 可以把翻译、本地化、工程、测试和 AI 辅助流程放到一起。",
            "highlights": [
                "一个团队覆盖内容和产品交付",
                "从需求到交付流程更清楚",
                "支持持续更新的多语言项目",
            ],
            "workflow": ["提出需求", "确认范围", "执行与复核", "完成交付"],
            "fit": ["全球化产品团队", "市场与内容团队", "准备进入新市场的企业"],
            "outputs": ["更清楚的服务选择", "结构化交付流程", "可持续的多语言支持"],
            "eyebrow": "全球语言支持",
        },
    },
    "translation": {
        "theme": "translation",
        "en": {
            "intro": "Use this service when you need clear, accurate translation for customer-facing or internal content.",
            "highlights": [
                "Documents, websites, software, and marketing content",
                "Terminology and style consistency",
                "Review and quality control before delivery",
            ],
            "workflow": ["Confirm content", "Translate", "Review", "Deliver"],
            "fit": ["Product content", "Website updates", "Business and legal materials"],
            "outputs": ["Translated files", "Reviewed copy", "Updated terminology assets"],
            "eyebrow": "Clear multilingual content",
        },
        "zh": {
            "intro": "如果你需要把对外或内部内容准确翻成目标语言，这项服务会更适合你。",
            "highlights": [
                "支持文档、网站、软件和营销内容",
                "保证术语和表达一致",
                "交付前做审校和质量检查",
            ],
            "workflow": ["确认内容", "翻译执行", "审校复核", "完成交付"],
            "fit": ["产品内容", "网站更新", "商务和法律材料"],
            "outputs": ["翻译成品文件", "审校后的文案", "更新后的术语资产"],
            "eyebrow": "清楚表达你的内容",
        },
    },
    "dtp": {
        "theme": "dtp",
        "en": {
            "intro": "Use DTP when translated content also needs to look right in layout, typography, and final output.",
            "highlights": [
                "Layout updates for multiple languages",
                "Font, spacing, and overflow handling",
                "Print-ready and digital-ready files",
            ],
            "workflow": ["Check source files", "Adjust layout", "Review visuals", "Deliver"],
            "fit": ["Manuals", "Brochures", "Marketing files"],
            "outputs": ["Updated layouts", "Ready-to-publish files", "Cleaner multilingual visuals"],
            "eyebrow": "Make multilingual layouts work",
        },
        "zh": {
            "intro": "如果翻译后的内容还需要在版式、字体和成品输出上保持专业，这项服务更合适。",
            "highlights": [
                "支持多语言版式调整",
                "处理字体、间距和溢出问题",
                "输出可印刷或可发布文件",
            ],
            "workflow": ["检查源文件", "调整版式", "复核视觉", "完成交付"],
            "fit": ["手册", "宣传册", "营销设计文件"],
            "outputs": ["更新后的版式文件", "可发布成品", "更整洁的多语言视觉"],
            "eyebrow": "让多语言版式更好用",
        },
    },
    "engineering": {
        "theme": "engineering",
        "en": {
            "intro": "Use engineering support when your product needs technical preparation for multiple languages and regions.",
            "highlights": [
                "I18N review and technical fixes",
                "Locale and encoding support",
                "Build and integration support",
            ],
            "workflow": ["Review product", "Prepare resources", "Integrate", "Verify"],
            "fit": ["Apps entering new markets", "Legacy products", "Teams with release pressure"],
            "outputs": ["Prepared resource files", "Localized builds", "Technical recommendations"],
            "eyebrow": "Prepare your product for global release",
        },
        "zh": {
            "intro": "如果你的产品要支持多语言和多地区发布，就需要这类技术准备支持。",
            "highlights": [
                "做国际化检查和技术修正",
                "处理区域和编码兼容问题",
                "支持构建和集成",
            ],
            "workflow": ["评估产品", "整理资源", "完成集成", "验证结果"],
            "fit": ["准备进入新市场的产品", "旧系统改造", "发布周期紧张的团队"],
            "outputs": ["整理后的资源文件", "本地化构建版本", "技术建议"],
            "eyebrow": "为全球发布做好技术准备",
        },
    },
    "testing": {
        "theme": "testing",
        "en": {
            "intro": "Use testing when you want to catch language, UI, and functional issues before release.",
            "highlights": [
                "Check language in real screens and flows",
                "Test locale-sensitive behavior",
                "Support bug reporting and regression",
            ],
            "workflow": ["Plan tests", "Run checks", "Report issues", "Retest"],
            "fit": ["Website launches", "App releases", "Multilingual updates"],
            "outputs": ["Issue reports", "Regression results", "Launch-readiness summary"],
            "eyebrow": "Reduce launch risk",
        },
        "zh": {
            "intro": "如果你想在上线前发现语言、界面和功能问题，这项服务会很有价值。",
            "highlights": [
                "在真实界面和流程里检查语言",
                "验证区域相关功能表现",
                "支持缺陷报告和回归测试",
            ],
            "workflow": ["制定测试计划", "执行检查", "提交问题", "回归验证"],
            "fit": ["网站上线", "应用发布", "多语言版本更新"],
            "outputs": ["问题报告", "回归结果", "上线前总结"],
            "eyebrow": "降低上线风险",
        },
    },
    "video-production": {
        "theme": "video-production",
        "en": {
            "intro": "Use this service when your video content needs subtitles, dubbing, or multilingual editing for new markets.",
            "highlights": [
                "Script, subtitle, and dubbing support",
                "Timing and sync handling",
                "One workflow for multilingual video delivery",
            ],
            "workflow": ["Review content", "Prepare script", "Localize", "Finalize"],
            "fit": ["Product videos", "Training videos", "Campaign videos"],
            "outputs": ["Localized scripts", "Subtitles or voice assets", "Final multilingual video files"],
            "eyebrow": "Make video content travel better",
        },
        "zh": {
            "intro": "如果你的视频需要字幕、配音或多语言版本制作，这项服务更适合。",
            "highlights": [
                "支持脚本、字幕和配音处理",
                "处理时间轴和同步问题",
                "用一套流程完成多语视频交付",
            ],
            "workflow": ["审查内容", "准备脚本", "本地化处理", "完成制作"],
            "fit": ["产品视频", "培训视频", "营销视频"],
            "outputs": ["本地化脚本", "字幕或配音资产", "最终多语视频文件"],
            "eyebrow": "让视频更容易走向海外",
        },
    },
    "interpreting": {
        "theme": "interpreting",
        "en": {
            "intro": "Use interpreting when you need smoother live communication across languages.",
            "highlights": [
                "Remote and onsite interpreting",
                "Match interpreters by meeting type",
                "Support before and during the event",
            ],
            "workflow": ["Confirm meeting", "Match interpreter", "Prepare", "Support live"],
            "fit": ["Business meetings", "Events and webinars", "High-stakes conversations"],
            "outputs": ["Interpreter plan", "Preparation support", "Live language support"],
            "eyebrow": "Support live conversations",
        },
        "zh": {
            "intro": "如果你需要在现场或线上实现更顺畅的跨语言沟通，这项服务会更适合。",
            "highlights": [
                "支持远程和现场口译",
                "按会议类型匹配译员",
                "会前和会中都提供支持",
            ],
            "workflow": ["确认会议需求", "匹配译员", "会前准备", "现场支持"],
            "fit": ["商务会议", "活动和线上研讨会", "关键沟通场景"],
            "outputs": ["译员安排方案", "准备支持", "现场语言支持"],
            "eyebrow": "支持现场沟通",
        },
    },
    "document-localization": {
        "theme": "document-localization",
        "en": {
            "intro": "Use document localization when your manuals, guides, or business files need translation and publishing support together.",
            "highlights": [
                "Translation and DTP in one flow",
                "Better consistency across document sets",
                "Faster publishing for recurring updates",
            ],
            "workflow": ["Review files", "Translate", "Format", "Publish"],
            "fit": ["Manuals", "Guides", "Sales and support documents"],
            "outputs": ["Localized documents", "Final PDFs or source files", "Reusable document assets"],
            "eyebrow": "Get documents ready for market",
        },
        "zh": {
            "intro": "如果你的手册、指南或业务资料既要翻译又要发布支持，这项服务更适合。",
            "highlights": [
                "把翻译和排版放进同一流程",
                "让整套文档更一致",
                "更适合持续更新和发布",
            ],
            "workflow": ["检查文件", "翻译执行", "排版处理", "完成发布"],
            "fit": ["说明书", "操作指南", "销售和支持文档"],
            "outputs": ["本地化文档", "最终 PDF 或源文件", "可复用文档资产"],
            "eyebrow": "让文档更快进入市场",
        },
    },
    "website-localization": {
        "theme": "website-localization",
        "en": {
            "intro": "Use website localization when you want your site to feel clearer and more natural in each target market.",
            "highlights": [
                "Support for static and dynamic websites",
                "Content and UI handled together",
                "QA before multilingual launch",
            ],
            "workflow": ["Review site", "Localize content", "Integrate", "Check before launch"],
            "fit": ["Corporate sites", "Product sites", "Marketing pages"],
            "outputs": ["Localized page content", "Updated multilingual pages", "QA-backed release"],
            "eyebrow": "Adapt your website for new markets",
        },
        "zh": {
            "intro": "如果你希望网站在目标市场里更自然、更容易理解，这项服务会更适合。",
            "highlights": [
                "支持静态和动态网站",
                "页面内容和界面一起处理",
                "上线前完成 QA 检查",
            ],
            "workflow": ["评估网站", "本地化内容", "完成集成", "上线前检查"],
            "fit": ["企业官网", "产品站", "营销页面"],
            "outputs": ["本地化页面内容", "更新后的多语页面", "经 QA 验证的发布结果"],
            "eyebrow": "让网站更适合目标市场",
        },
    },
    "apps-localization": {
        "theme": "apps-localization",
        "en": {
            "intro": "Use app localization when your software needs language, build, and QA support together.",
            "highlights": [
                "Strings, help, and assets in one flow",
                "Build support for multilingual releases",
                "Functional and linguistic checks",
            ],
            "workflow": ["Review app", "Localize resources", "Build", "Validate"],
            "fit": ["Desktop apps", "Mobile apps", "SaaS products"],
            "outputs": ["Localized resources", "Integrated builds", "Release checks"],
            "eyebrow": "Launch apps in more languages",
        },
        "zh": {
            "intro": "如果你的软件需要把语言、构建和测试一起处理，这项服务更合适。",
            "highlights": [
                "把字符串、帮助内容和素材放进同一流程",
                "支持多语言构建发布",
                "做功能和语言双重检查",
            ],
            "workflow": ["评估应用", "本地化资源", "完成构建", "验证结果"],
            "fit": ["桌面软件", "移动应用", "SaaS 产品"],
            "outputs": ["本地化资源", "集成后的构建版本", "发布检查结果"],
            "eyebrow": "让应用支持更多语言",
        },
    },
    "multimedia-localization": {
        "theme": "multimedia-localization",
        "en": {
            "intro": "Use multimedia localization when your audio and video content needs to work naturally in another language.",
            "highlights": [
                "Subtitles, dubbing, and script handling",
                "Support for sync and final review",
                "Better consistency across media assets",
            ],
            "workflow": ["Review assets", "Prepare scripts", "Localize", "Finalize"],
            "fit": ["Campaign media", "Corporate media", "Product demos"],
            "outputs": ["Localized scripts", "Media language assets", "Final reviewed files"],
            "eyebrow": "Adapt media content for local audiences",
        },
        "zh": {
            "intro": "如果你的音视频内容要在另一种语言里自然呈现，这项服务会更适合。",
            "highlights": [
                "支持字幕、配音和脚本处理",
                "支持同步和最终复核",
                "让媒体资产更一致",
            ],
            "workflow": ["检查素材", "准备脚本", "本地化处理", "完成复核"],
            "fit": ["营销素材", "企业传播内容", "产品演示内容"],
            "outputs": ["本地化脚本", "媒体语言资产", "最终复核文件"],
            "eyebrow": "让媒体内容更贴近本地用户",
        },
    },
    "elearning-localization": {
        "theme": "elearning-localization",
        "en": {
            "intro": "Use eLearning localization when training content needs to stay clear and usable in another language.",
            "highlights": [
                "Courses, modules, and assessments",
                "Support for audio and interaction",
                "Consistent learner experience",
            ],
            "workflow": ["Audit content", "Localize", "Integrate", "Check"],
            "fit": ["Internal training", "Customer education", "Interactive courseware"],
            "outputs": ["Localized modules", "Updated learner assets", "Ready-to-deploy packages"],
            "eyebrow": "Make training work in more languages",
        },
        "zh": {
            "intro": "如果培训内容要在另一种语言里保持清楚和易用，这项服务更合适。",
            "highlights": [
                "支持课程、模块和评测",
                "支持音频和交互内容",
                "保持学习体验一致",
            ],
            "workflow": ["审查内容", "本地化处理", "集成更新", "质量检查"],
            "fit": ["内部培训", "客户教育", "交互式课件"],
            "outputs": ["本地化课程模块", "更新后的学习资产", "可部署包"],
            "eyebrow": "让培训内容支持更多语言",
        },
    },
    "technology": {
        "theme": "technology",
        "en": {
            "intro": "Technology helps you get more consistency, more visibility, and less manual work in multilingual delivery.",
            "highlights": [
                "Translation memory and CAT support",
                "QA and file-processing automation",
                "Better workflow visibility",
            ],
            "workflow": ["Assess", "Set up tools", "Run workflow", "Measure"],
            "fit": ["High-volume content teams", "Repeat release programs", "Process-focused operations"],
            "outputs": ["Tool-supported workflows", "Reusable language assets", "Better delivery control"],
            "eyebrow": "Use tools to improve delivery",
        },
        "zh": {
            "intro": "技术能力可以帮你在多语言交付里减少人工工作、提高一致性，也让流程更可见。",
            "highlights": [
                "支持 TM 和 CAT 工具",
                "支持 QA 和文件处理自动化",
                "让流程更容易管理",
            ],
            "workflow": ["评估需求", "配置工具", "执行流程", "查看结果"],
            "fit": ["高内容量团队", "持续发布项目", "重视流程管理的组织"],
            "outputs": ["工具化工作流", "可复用语言资产", "更好的交付控制"],
            "eyebrow": "用技术提升交付效率",
        },
    },
    "ai": {
        "theme": "ai",
        "en": {
            "intro": "Use AI support when you want faster delivery without losing human review where it matters.",
            "highlights": [
                "AI-assisted translation and QA",
                "Human review for important content",
                "Better speed on large-volume work",
            ],
            "workflow": ["Assist with AI", "Review by human", "Check quality", "Deliver"],
            "fit": ["High-volume projects", "Fast-turnaround work", "Teams balancing speed and quality"],
            "outputs": ["Faster drafts", "Reviewed final content", "Clearer workflow data"],
            "eyebrow": "Use AI where it helps",
        },
        "zh": {
            "intro": "如果你希望提升速度，但又不想在关键内容上放弃人工把关，这项服务更适合。",
            "highlights": [
                "支持 AI 辅助翻译和质检",
                "重要内容保留人工复核",
                "更适合大批量项目提速",
            ],
            "workflow": ["AI 辅助", "人工复核", "质量检查", "完成交付"],
            "fit": ["高内容量项目", "时效要求高的任务", "要平衡速度和质量的团队"],
            "outputs": ["更快初稿", "复核后的成品", "更清楚的流程数据"],
            "eyebrow": "在合适的地方用 AI",
        },
    },
    "company": {
        "theme": "company",
        "en": {
            "intro": "If you want to know how iCentech works, this page shows the team, the process, and the delivery style behind the service.",
            "highlights": [
                "One coordinated delivery model",
                "Cross-functional support",
                "Flexible support for ongoing work",
            ],
            "workflow": ["Understand needs", "Build a plan", "Run delivery", "Keep improving"],
            "fit": ["Teams seeking one partner", "Clients with recurring needs", "Projects mixing language and technical work"],
            "outputs": ["Delivery setup", "Team structure", "Longer-term support model"],
            "eyebrow": "How we work with clients",
        },
        "zh": {
            "intro": "如果你想了解 iCentech 是怎么配合客户的，这一页会更清楚地说明团队、流程和交付方式。",
            "highlights": [
                "统一协调的交付模式",
                "跨职能团队支持",
                "适合持续合作的方式",
            ],
            "workflow": ["了解需求", "制定方案", "执行交付", "持续优化"],
            "fit": ["希望找统一合作方的团队", "有持续需求的客户", "语言和技术并重的项目"],
            "outputs": ["交付方式说明", "团队结构说明", "长期支持框架"],
            "eyebrow": "了解我们如何与客户合作",
        },
    },
    "news-blog": {
        "theme": "news-blog",
        "en": {
            "intro": "This blog gives clients one place to read iCentech updates, practical localization ideas, and project stories.",
            "highlights": [
                "Articles publish inside the new website",
                "The repo manages drafting, review, and publishing",
                "Each post is easier to browse, share, and index",
            ],
            "workflow": ["Pick a topic", "Draft", "Review", "Publish"],
            "fit": ["Marketing teams", "Content operations", "Clients following company updates"],
            "outputs": ["Local article archive", "Clearer listing page", "GitHub-based management path"],
            "eyebrow": "Company updates and insights",
        },
        "zh": {
            "intro": "这个博客栏目会把 iCentech 的动态、案例和行业内容真正放进新网站里，方便客户直接阅读。",
            "highlights": [
                "文章直接发布在新站里",
                "用仓库管理写作、审核和发布",
                "更适合浏览、分享和检索",
            ],
            "workflow": ["确定选题", "写稿", "审核", "发布"],
            "fit": ["市场团队", "内容运营团队", "关注公司动态的客户"],
            "outputs": ["站内文章归档", "更清楚的列表页", "基于 GitHub 的管理路径"],
            "eyebrow": "公司动态与行业内容",
        },
    },
    "career": {
        "theme": "career",
        "en": {
            "intro": "Use this page to understand what kinds of roles and team opportunities iCentech may open in the future.",
            "highlights": [
                "Clearer role direction",
                "Space for future openings",
                "A warmer introduction to the team",
            ],
            "workflow": ["Apply", "Review", "Interview", "Join"],
            "fit": ["Project managers", "QA specialists", "Localization engineers"],
            "outputs": ["Role overview", "Future hiring structure", "Clearer applicant path"],
            "eyebrow": "Join the team",
        },
        "zh": {
            "intro": "这一页帮助候选人更快了解 iCentech 未来可能开放的岗位方向和团队机会。",
            "highlights": [
                "岗位方向更清楚",
                "适合后续继续放职位",
                "对团队介绍更友好",
            ],
            "workflow": ["投递", "筛选", "面试", "加入"],
            "fit": ["项目经理", "QA 专员", "本地化工程师"],
            "outputs": ["岗位方向说明", "后续招聘结构", "更清楚的申请路径"],
            "eyebrow": "加入团队",
        },
    },
    "freelance": {
        "theme": "freelance",
        "en": {
            "intro": "Use this page if you want to work with iCentech as a freelance translator, reviewer, voice talent, or specialist partner.",
            "highlights": [
                "Clearer expectations for partners",
                "Better introduction to the collaboration model",
                "Ready for future intake steps",
            ],
            "workflow": ["Submit profile", "Review", "Trial", "Start work"],
            "fit": ["Freelancers", "Voice talent", "Language-tech specialists"],
            "outputs": ["Partnership overview", "Collaboration steps", "Freelancer-facing landing page"],
            "eyebrow": "Work with iCentech",
        },
        "zh": {
            "intro": "如果你想以自由职业者或合作伙伴身份和 iCentech 合作，可以从这里先了解合作方式。",
            "highlights": [
                "让合作预期更清楚",
                "更好介绍合作模式",
                "方便后续继续接入申请流程",
            ],
            "workflow": ["提交资料", "审核", "试项", "开始合作"],
            "fit": ["自由译员", "配音人才", "语言技术合作伙伴"],
            "outputs": ["合作方式说明", "合作步骤", "面向自由职业者的落地页"],
            "eyebrow": "与 iCentech 合作",
        },
    },
}


def page_filename(slug):
    return "index.html" if slug == "" else f"{slug}.html"


def page_asset_basename(slug):
    return "home" if slug == "" else slug


def page_href(lang, slug):
    prefix = "/zh" if lang == "zh" else "/en"
    return f"{prefix}/{page_filename(slug)}"


def get_page_detail(page, lang):
    return PAGE_DETAILS[page["slug"]][lang]


def get_theme(page):
    key = PAGE_DETAILS[page["slug"]]["theme"]
    return THEME_MAP[key]


def build_meta_description(page, lang):
    return page["summary_zh"] if lang == "zh" else page["summary_en"]


def load_blog_posts():
    if not BLOG_DATA_FILE.exists():
        return []
    with open(BLOG_DATA_FILE, "r", encoding="utf-8") as file:
        payload = json.load(file)
    posts = payload.get("posts", [])
    hydrated = []
    for post in posts:
        item = dict(post)
        body_file = item.get("body_file")
        body_path = ROOT / body_file if body_file else None
        if body_path and body_path.exists():
            item["body_html"] = body_path.read_text(encoding="utf-8").strip()
        else:
            item["body_html"] = item.get("body_html", "").strip()

        image = item.get("image", "")
        if image and not image.startswith(("http://", "https://", "/assets/")):
            item["image_url"] = f"/assets/{image.lstrip('/')}"
        else:
            item["image_url"] = image
        excerpt = html.unescape((item.get("excerpt") or "").replace("\xa0", " ")).strip()
        item["excerpt"] = excerpt if excerpt else excerpt_from_body(item["body_html"])
        hydrated.append(item)
    return hydrated


def blog_href(lang, slug):
    prefix = "/zh/blog" if lang == "zh" else "/en/blog"
    return f"{prefix}/{slug}.html"


def excerpt_from_body(body_html):
    text = re.sub(r"<[^>]+>", " ", body_html)
    text = html.unescape(re.sub(r"\s+", " ", text)).strip()
    return text[:156].rstrip() + "…" if len(text) > 156 else text


def detect_language(value):
    return "zh" if re.search(r"[\u4e00-\u9fff]", value or "") else "en"


def get_group_label(page, lang):
    for group in MENU_GROUPS:
        for item in group["items"]:
            if item["slug"] == page["slug"]:
                return group["title_zh"] if lang == "zh" else group["title_en"]
    return None


def render_breadcrumbs(page, lang):
    home_label = "首页" if lang == "zh" else "Home"
    current_label = page["title_zh"] if lang == "zh" else page["title_en"]
    parts = [f'<a href="{page_href(lang, "")}">{html.escape(home_label)}</a>']
    group_label = get_group_label(page, lang)

    if page["slug"] and group_label and group_label != home_label:
        parts.append(f"<span>{html.escape(group_label)}</span>")
    if page["slug"]:
        parts.append(f"<span>{html.escape(current_label)}</span>")
    separator = '<span class="breadcrumb-sep">/</span>'
    return f'<nav class="breadcrumb" aria-label="Breadcrumb">{separator.join(parts)}</nav>'


def render_blog_breadcrumbs(page, post, lang):
    home_label = "首页" if lang == "zh" else "Home"
    group_label = "关于我们" if lang == "zh" else "ABOUT US"
    blog_label = page["title_zh"] if lang == "zh" else page["title_en"]
    separator = '<span class="breadcrumb-sep">/</span>'
    parts = [
        f'<a href="{page_href(lang, "")}">{html.escape(home_label)}</a>',
        f"<span>{html.escape(group_label)}</span>",
        f'<a href="{page_href(lang, "news-blog")}">{html.escape(blog_label)}</a>',
        f"<span>{html.escape(post['title'])}</span>",
    ]
    return f'<nav class="breadcrumb" aria-label="Breadcrumb">{separator.join(parts)}</nav>'


def render_nav(page, lang):
    items = []
    for group in MENU_GROUPS:
        group_title = group["title_zh"] if lang == "zh" else group["title_en"]
        links = []
        for item in group["items"]:
            label = item["zh"] if lang == "zh" else item["en"]
            active = " is-active" if item["slug"] == page["slug"] else ""
            links.append(
                f'<a class="menu-item{active}" href="{page_href(lang, item["slug"])}">{html.escape(label)}</a>'
            )
        items.append(
            f"""
            <div class="menu-group" data-menu-group>
              <button class="menu-title" type="button" aria-expanded="false">{html.escape(group_title)}</button>
              <div class="menu-list" hidden>
                {''.join(links)}
              </div>
            </div>
            """
        )
    return "".join(items)


def render_brand(lang):
    logo_path = ASSETS_DIR / LOGO_ASSET_NAME
    logo_html = (
        f'<img class="brand-logo" src="/assets/{LOGO_ASSET_NAME}" alt="iCentech logo">'
        if logo_path.exists()
        else '<span class="brand-mark brand-mark-fallback" aria-hidden="true">i</span>'
    )
    return f"""
    <a class="brand" href="{page_href(lang, '')}">
      <span class="brand-badge">
        {logo_html}
      </span>
    </a>
    """


def render_switch(page, lang):
    other = "en" if lang == "zh" else "zh"
    label = "English" if lang == "zh" else "中文"
    return f'<a class="lang-switch" href="{page_href(other, page["slug"])}">{label}</a>'


def render_blog_switch(post, lang):
    other = "en" if lang == "zh" else "zh"
    label = "English" if lang == "zh" else "中文"
    return f'<a class="lang-switch" href="{blog_href(other, post["slug"])}">{label}</a>'


def render_theme_toggle(lang):
    return (
        '<button class="theme-toggle" type="button" data-theme-toggle '
        f'data-label-light="{"切换浅色" if lang == "zh" else "Switch To Light"}" '
        f'data-label-dark="{"切换深色" if lang == "zh" else "Switch To Dark"}">'
        f'{"主题" if lang == "zh" else "Theme"}'
        "</button>"
    )


def render_footer_icon(kind):
    icons = {
        "brand": """
        <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
          <circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.8"></circle>
          <path d="M12 3.5c2.7 2.2 4.1 5 4.1 8.5S14.7 18.3 12 20.5C9.3 18.3 7.9 15.5 7.9 12S9.3 5.7 12 3.5Z" fill="none" stroke="currentColor" stroke-width="1.6"></path>
          <path d="M3.8 12h16.4" fill="none" stroke="currentColor" stroke-width="1.6"></path>
        </svg>
        """,
        "pin": """
        <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
          <path d="M12 21s-6-5.7-6-11a6 6 0 1 1 12 0c0 5.3-6 11-6 11Z" fill="none" stroke="currentColor" stroke-width="1.8"></path>
          <circle cx="12" cy="10" r="2.2" fill="currentColor"></circle>
        </svg>
        """,
        "contact": """
        <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
          <rect x="3.5" y="5.5" width="17" height="13" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.8"></rect>
          <path d="m5.5 8 6.5 5 6.5-5" fill="none" stroke="currentColor" stroke-width="1.8"></path>
        </svg>
        """,
        "social": """
        <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
          <circle cx="12" cy="12" r="8.5" fill="none" stroke="currentColor" stroke-width="1.8"></circle>
          <path d="M12 3.5a15.2 15.2 0 0 1 0 17M12 3.5a15.2 15.2 0 0 0 0 17M3.5 12h17" fill="none" stroke="currentColor" stroke-width="1.6"></path>
        </svg>
        """,
        "linkedin": """
        <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
          <rect x="4" y="4" width="16" height="16" rx="4" fill="none" stroke="currentColor" stroke-width="1.8"></rect>
          <path d="M8.3 10.1V16M8.3 8.2h.02M12.1 16v-3.2c0-1.1.6-1.8 1.6-1.8s1.5.7 1.5 1.8V16M12.1 10.1v.8" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8"></path>
        </svg>
        """,
        "facebook": """
        <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
          <circle cx="12" cy="12" r="8.5" fill="none" stroke="currentColor" stroke-width="1.8"></circle>
          <path d="M13.4 8.1H15V6h-1.8c-2 0-3 .9-3 2.9v1.4H8.9v2.1h1.3V18h2.3v-5.6H14l.3-2.1h-1.8V9.2c0-.7.3-1.1.9-1.1Z" fill="currentColor"></path>
        </svg>
        """,
        "x": """
        <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
          <path d="M5 5h3.5l4.1 5.4L17.1 5H19l-5.4 6.2L19.5 19H16l-4.3-5.7L6.8 19H5l5.8-6.6z" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8"></path>
        </svg>
        """,
        "wechat": """
        <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
          <path d="M9.1 6.2c-3.1 0-5.6 2.1-5.6 4.9 0 1.5.8 2.8 2.1 3.7l-.6 2.3 2.5-1.3c.5.1 1 .2 1.6.2 3.1 0 5.6-2.1 5.6-4.9S12.2 6.2 9.1 6.2Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"></path>
          <path d="M15.7 10.1c-2.7 0-4.8 1.8-4.8 4.1 0 1.2.6 2.2 1.7 3l-.5 1.8 2-.9c.5.1 1 .2 1.6.2 2.7 0 4.8-1.8 4.8-4.1s-2.2-4.1-4.8-4.1Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"></path>
          <circle cx="7.4" cy="10.9" r="0.9" fill="currentColor"></circle>
          <circle cx="10.7" cy="10.9" r="0.9" fill="currentColor"></circle>
          <circle cx="14.3" cy="14" r="0.8" fill="currentColor"></circle>
          <circle cx="17.1" cy="14" r="0.8" fill="currentColor"></circle>
        </svg>
        """,
    }
    return icons[kind]


def render_footer_content(lang):
    address_label = "地址" if lang == "zh" else "Addresses"
    contact_label = "联系方式" if lang == "zh" else "Contact"
    social_label = "社交媒体" if lang == "zh" else "Social"
    brand_summary = (
        "让多语言内容、产品与全球交付更清晰、更省心。"
        if lang == "zh"
        else "A clearer way to manage multilingual content, product delivery, and global launch work."
    )
    office_beijing = "北京办公室" if lang == "zh" else "Beijing Office"
    office_hk = "香港办公室" if lang == "zh" else "Hong Kong Office"
    follow_label = "关注 iCentech" if lang == "zh" else "Follow iCentech"
    return f"""
    <div class="footer-grid">
      <div class="footer-block footer-brand-block">
        <div class="footer-heading">
          <span class="footer-heading-icon">{render_footer_icon("brand")}</span>
          <p class="footer-title">iCentech</p>
        </div>
        <p class="footer-lead">{brand_summary}</p>
        <p class="footer-meta">iCentech Limited © 2026</p>
      </div>
      <div class="footer-block">
        <div class="footer-heading">
          <span class="footer-heading-icon">{render_footer_icon("pin")}</span>
          <p class="footer-title">{address_label}</p>
        </div>
        <div class="footer-stack">
          <p class="footer-item-label">{office_beijing}</p>
          <p class="footer-item-copy">wehome110, DoBe WE International Hub, Dongcheng, Beijing, PRC</p>
        </div>
        <div class="footer-stack">
          <p class="footer-item-label">{office_hk}</p>
          <p class="footer-item-copy">2/F, Lee Fung Commercial Building, 32-36 Des Voeux Rd W, Sheung Wan, Hong Kong</p>
        </div>
      </div>
      <div class="footer-block">
        <div class="footer-heading">
          <span class="footer-heading-icon">{render_footer_icon("contact")}</span>
          <p class="footer-title">{contact_label}</p>
        </div>
        <div class="footer-stack">
          <p class="footer-item-label">{'电子邮箱' if lang == 'zh' else 'Email'}</p>
          <p class="footer-item-copy"><a href="mailto:info@icentech.com">info@icentech.com</a></p>
        </div>
        <div class="footer-stack">
          <p class="footer-item-label">{'电话' if lang == 'zh' else 'Phone'}</p>
          <p class="footer-item-copy"><a href="tel:+861067122138">+86 10 67122138</a></p>
          <p class="footer-item-copy"><a href="tel:+85244071920">+852 4407 1920</a></p>
        </div>
      </div>
      <div class="footer-block footer-social-block">
        <div class="footer-heading">
          <span class="footer-heading-icon">{render_footer_icon("social")}</span>
          <p class="footer-title">{social_label}</p>
        </div>
        <p class="footer-meta">{follow_label}</p>
        <div class="social-links" aria-label="{social_label}">
          <a class="social-link" href="http://linkedin.com/company/icentech-limited?trk=fc_badge" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn" title="LinkedIn">
            {render_footer_icon("linkedin")}
            <span class="sr-only">LinkedIn</span>
          </a>
          <a class="social-link" href="http://facebook.com/profile.php?id=100070578788568" target="_blank" rel="noopener noreferrer" aria-label="Facebook" title="Facebook">
            {render_footer_icon("facebook")}
            <span class="sr-only">Facebook</span>
          </a>
          <a class="social-link" href="http://twitter.com/iCentech" target="_blank" rel="noopener noreferrer" aria-label="X" title="X">
            {render_footer_icon("x")}
            <span class="sr-only">X</span>
          </a>
          <a class="social-link" href="https://work.weixin.qq.com/ca/cawcde6ff00b2d1680" target="_blank" rel="noopener noreferrer" aria-label="WeChat" title="WeChat">
            {render_footer_icon("wechat")}
            <span class="sr-only">WeChat</span>
          </a>
        </div>
      </div>
    </div>
    """


def render_service_cards(data, lang):
    cards = []
    for page in data["pages"][1:7]:
        title = page["title_zh"] if lang == "zh" else page["title_en"]
        summary = page["summary_zh"] if lang == "zh" else page["summary_en"]
        cards.append(
            f"""
            <a class="service-card" href="{page_href(lang, page['slug'])}">
              <span class="card-kicker">{'服务模块' if lang == 'zh' else 'Service Area'}</span>
              <h3>{html.escape(title)}</h3>
              <p>{html.escape(summary)}</p>
            </a>
            """
        )
    return "".join(cards)


def render_related_cards(data, page, lang):
    related_slugs = PAGE_RELATIONS.get(page["slug"], [])
    pages_by_slug = {item["slug"]: item for item in data["pages"]}
    cards = []
    for slug in related_slugs:
        related = pages_by_slug.get(slug)
        if not related:
            continue
        title = related["title_zh"] if lang == "zh" else related["title_en"]
        summary = related["summary_zh"] if lang == "zh" else related["summary_en"]
        cards.append(
            f"""
            <a class="service-card related-card" href="{page_href(lang, slug)}">
              <span class="card-kicker">{'关联页面' if lang == 'zh' else 'Related Page'}</span>
              <h3>{html.escape(title)}</h3>
              <p>{html.escape(summary)}</p>
            </a>
            """
        )
    return "".join(cards)


def render_blog_cards(lang, posts):
    cards = []
    for post in posts:
        excerpt = post.get("excerpt") or excerpt_from_body(post.get("body_html", ""))
        language_label = "中文" if detect_language(post["title"]) == "zh" else "English"
        cards.append(
            f"""
            <article class="blog-card">
              <a class="blog-card-media" href="{blog_href(lang, post['slug'])}">
                <img src="{html.escape(post.get('image_url', ''))}" alt="{html.escape(post['title'])}">
              </a>
              <div class="blog-card-body">
                <div class="blog-card-meta">
                  <p class="blog-card-date">{html.escape(post['date'])}</p>
                  <span class="meta-pill">{language_label}</span>
                </div>
                <h3><a href="{blog_href(lang, post['slug'])}">{html.escape(post['title'])}</a></h3>
                <p>{html.escape(excerpt)}</p>
                <a class="text-link" href="{blog_href(lang, post['slug'])}">{'Read article' if lang == 'en' else '阅读文章'}</a>
              </div>
            </article>
            """
        )
    return "".join(cards)


def list_items(items, ordered=False):
    tag = "ol" if ordered else "ul"
    return f"<{tag}>{''.join(f'<li>{html.escape(item)}</li>' for item in items)}</{tag}>"


def render_home(page, lang, data):
    detail = get_page_detail(page, lang)
    home = HOME_SECTIONS[lang]
    title = page["title_zh"] if lang == "zh" else page["title_en"]
    summary = page["summary_zh"] if lang == "zh" else page["summary_en"]
    trust_items = "".join(f"<li>{html.escape(item)}</li>" for item in home["trust"])
    stats_cards = "".join(
        f"""
        <article class="metric-card">
          <strong>{html.escape(item['value'])}</strong>
          <span>{html.escape(item['label'])}</span>
        </article>
        """
        for item in home["stats"]
    )
    value_cards = "".join(
        f"""
        <article class="panel soft-panel">
          <h3>{html.escape(card['title'])}</h3>
          <p>{html.escape(card['body'])}</p>
        </article>
        """
        for card in home["value_cards"]
    )
    process = "".join(
        f"""
        <li>
          <span class="step-index">{index + 1:02d}</span>
          <span>{html.escape(item)}</span>
        </li>
        """
        for index, item in enumerate(home["process"])
    )
    ai_points = "".join(f"<li>{html.escape(item)}</li>" for item in home["ai_ready_points"])
    return f"""
    <section class="hero hero-home">
      <div class="hero-copy">
        <span class="eyebrow">{html.escape(home['eyebrow'])}</span>
        <h1>{html.escape(title)}</h1>
        <p class="lead">{html.escape(summary)}</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="{page_href(lang, 'translation')}">{'查看服务' if lang == 'zh' else 'Explore Services'}</a>
          <a class="btn btn-secondary" href="{page_href(lang, 'company')}">{'了解 iCentech' if lang == 'zh' else 'About iCentech'}</a>
        </div>
        <ul class="trust-pills">{trust_items}</ul>
      </div>
    </section>

    <section class="metrics-grid">{stats_cards}</section>

    <section class="section-shell">
      <div class="section-heading">
        <span class="section-kicker">{'核心服务' if lang == 'zh' else 'Core Services'}</span>
        <h2>{'看看我们可以怎么帮你' if lang == 'zh' else 'See how we can help'}</h2>
      </div>
      <div class="card-grid">{render_service_cards(data, lang)}</div>
    </section>

    <section class="section-shell two-col-shell">
      <article class="panel">
        <span class="section-kicker">{'为什么选择 iCentech' if lang == 'zh' else 'Why iCentech'}</span>
        <h2>{'把多语言项目讲得更清楚，也做得更顺' if lang == 'zh' else 'Make multilingual delivery easier to understand and manage'}</h2>
        <p>{html.escape(detail['intro'])}</p>
        {list_items(detail['highlights'])}
      </article>
      <div class="stack-grid">
        {value_cards}
      </div>
    </section>

    <section class="section-shell two-col-shell">
      <article class="panel">
        <span class="section-kicker">{'工作流程' if lang == 'zh' else 'Workflow'}</span>
        <h2>{'从需求到交付，一步步推进' if lang == 'zh' else 'A simple path from request to delivery'}</h2>
        <ol class="timeline-list">{process}</ol>
      </article>
      <article class="panel ai-panel">
        <span class="section-kicker">{'认证与质量' if lang == 'zh' else 'Certifications'}</span>
        <h2>{html.escape(home['ai_ready_title'])}</h2>
        <p>{html.escape(home['ai_ready_body'])}</p>
        {list_items(home['ai_ready_points'])}
      </article>
    </section>

    <section class="section-shell cta-shell">
      <article class="panel cta-panel">
        <span class="section-kicker">{'下一步' if lang == 'zh' else 'Next Step'}</span>
        <h2>{html.escape(home['cta_title'])}</h2>
        <p>{html.escape(home['cta_body'])}</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="{page_href(lang, 'technology')}">{'查看技术能力' if lang == 'zh' else 'See Technology'}</a>
          <a class="btn btn-secondary" href="{page_href(lang, 'ai')}">{'查看 AI 页面' if lang == 'zh' else 'See AI Page'}</a>
        </div>
      </article>
    </section>
    """


def render_news_blog_page(page, lang):
    detail = get_page_detail(page, lang)
    title = page["title_zh"] if lang == "zh" else page["title_en"]
    summary = page["summary_zh"] if lang == "zh" else page["summary_en"]
    posts = load_blog_posts()
    post_count = str(len(posts))
    latest_date = posts[0]["date"] if posts else ("2026" if lang == "en" else "2026")
    management_cards = [
        {
            "title": "Repo-managed content" if lang == "en" else "仓库内管理内容",
            "body": "Each article now lives in this project with a manifest entry, a local body file, and a local cover image asset."
            if lang == "en" else
            "每篇文章现在都放在这个项目里，包括文章清单、本地正文文件和本地封面图。",
        },
        {
            "title": "GitHub review workflow" if lang == "en" else "GitHub 审核流程",
            "body": "Draft updates in the repo, review with pull requests, and track status with labels or a Project board."
            if lang == "en" else
            "文章草稿进入仓库后通过 Pull Request 审核，再用标签或 Project 面板跟踪状态。",
        },
        {
            "title": "Build and publish from GitHub" if lang == "en" else "从 GitHub 构建和发布",
            "body": "The static generator reads the repo content directly, so blog updates are published as part of the site instead of pointing back to the old platform."
            if lang == "en" else
            "静态站点会直接读取仓库里的文章内容，所以博客更新会成为新站的一部分，而不是再跳回旧平台。",
        },
    ]
    management_html = "".join(
        f"""
        <article class="panel soft-panel">
          <h3>{html.escape(card['title'])}</h3>
          <p>{html.escape(card['body'])}</p>
        </article>
        """
        for card in management_cards
    )
    stats_html = f"""
    <section class="metrics-grid">
      <article class="metric-card">
        <strong>{post_count}</strong>
        <span>{'Local posts in this website' if lang == 'en' else '当前新站内文章数'}</span>
      </article>
      <article class="metric-card">
        <strong>{html.escape(latest_date)}</strong>
        <span>{'Latest article date' if lang == 'en' else '最近文章时间'}</span>
      </article>
      <article class="metric-card">
        <strong>GitHub</strong>
        <span>{'Free editorial workflow ready' if lang == 'en' else '已接入免费内容工作流'}</span>
      </article>
      <article class="metric-card">
        <strong>Local</strong>
        <span>{'Articles and covers are hosted in this project' if lang == 'en' else '文章和封面都托管在本项目中'}</span>
      </article>
    </section>
    """
    return f"""
    <section class="hero hero-page">
      <div class="hero-copy">
        <span class="eyebrow">{html.escape(detail['eyebrow'])}</span>
        <h1>{html.escape(title)}</h1>
        <p class="lead">{html.escape(summary)}</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="#blog-posts">{'查看文章列表' if lang == 'zh' else 'Browse Posts'}</a>
          <a class="btn btn-secondary" href="#blog-management">{'查看管理方式' if lang == 'zh' else 'See Management Setup'}</a>
        </div>
      </div>
    </section>

    {stats_html}

    <section class="section-shell two-col-shell">
      <article class="panel">
        <span class="section-kicker">{'文章中心' if lang == 'zh' else 'Editorial Hub'}</span>
        <h2>{'现在博客已经成为新站的一部分' if lang == 'zh' else 'The blog now lives inside the new site'}</h2>
        <p>{html.escape(detail['intro'])}</p>
        {list_items(detail['highlights'])}
      </article>
      <article class="panel ai-panel" id="blog-management">
        <span class="section-kicker">{'博客管理' if lang == 'zh' else 'Blog Management'}</span>
        <h2>{'用 GitHub 免费能力管理选题、审核和发布' if lang == 'zh' else 'Use GitHub’s free tools for intake, review, and publishing'}</h2>
        <p>{html.escape('后续只要在 GitHub 仓库里新增或更新文章文件，生成器就会把它们编进新网站。'
        if lang == 'zh' else
        'New or updated posts can be managed in the repo, reviewed in pull requests, and compiled directly into this website.')}</p>
        {list_items(detail['workflow'], ordered=True)}
      </article>
    </section>

    <section class="section-shell">
      <div class="section-heading">
        <span class="section-kicker">{'管理结构' if lang == 'zh' else 'Management Setup'}</span>
        <h2>{'后续维护可以直接按这套流程走' if lang == 'zh' else 'A simple setup for ongoing publishing'}</h2>
      </div>
      <div class="stack-grid stack-grid-three">{management_html}</div>
    </section>

    <section class="section-shell" id="blog-posts">
      <div class="section-heading">
        <span class="section-kicker">{'文章' if lang == 'zh' else 'Posts'}</span>
        <h2>{'这些文章现在直接发布在新网站里' if lang == 'zh' else 'These articles now publish directly on the new website'}</h2>
      </div>
      <div class="blog-grid">{render_blog_cards(lang, posts)}</div>
    </section>
    """


def render_blog_post_page(page, post, lang):
    sibling_posts = [item for item in load_blog_posts() if item["slug"] != post["slug"]][:3]
    title = post["title"]
    subtitle = post.get("subtitle", "")
    excerpt = post.get("excerpt") or excerpt_from_body(post.get("body_html", ""))
    tags = "".join(f'<li>{html.escape(tag)}</li>' for tag in post.get("tags", []))
    tag_html = f'<ul class="tag-list">{tags}</ul>' if tags else ""
    related_cards = "".join(
        f"""
        <a class="service-card related-card" href="{blog_href(lang, item['slug'])}">
          <span class="card-kicker">{'最新文章' if lang == 'zh' else 'Latest Post'}</span>
          <h3>{html.escape(item['title'])}</h3>
          <p>{html.escape(item.get('excerpt') or excerpt_from_body(item.get('body_html', '')))}</p>
        </a>
        """
        for item in sibling_posts
    )
    return f"""
    <section class="hero hero-page hero-blog-post">
      <div class="hero-copy">
        <span class="eyebrow">{'博客文章' if lang == 'zh' else 'Blog Article'}</span>
        <h1>{html.escape(title)}</h1>
        <p class="lead">{html.escape(subtitle or excerpt)}</p>
        <div class="hero-meta-strip">
          <span class="meta-pill">{html.escape(post['date'])}</span>
          <span class="meta-pill">{'中文内容' if detect_language(title) == 'zh' else 'English content'}</span>
          <span class="meta-pill">{'新站内发布' if lang == 'zh' else 'Published in this site'}</span>
        </div>
      </div>
    </section>

    <section class="section-shell two-col-shell">
      <article class="panel post-panel">
        <span class="section-kicker">{'正文' if lang == 'zh' else 'Article'}</span>
        <div class="post-content">
          {post.get('body_html', '')}
        </div>
      </article>
      <aside class="stack-grid">
        <article class="panel soft-panel">
          <span class="section-kicker">{'文章信息' if lang == 'zh' else 'Post Info'}</span>
          <h2>{'快速了解这篇文章' if lang == 'zh' else 'Quick context for this article'}</h2>
          <p>{html.escape(excerpt)}</p>
          {tag_html}
        </article>
        <article class="panel ai-panel">
          <span class="section-kicker">{'管理方式' if lang == 'zh' else 'Management'}</span>
          <h2>{'文章已经放进仓库管理' if lang == 'zh' else 'This post is now repo-managed'}</h2>
          <p>{html.escape('正文文件、封面图和文章清单都已经本地化，后续可以直接在 GitHub 里维护。'
          if lang == 'zh' else
          'The body file, cover image, and post manifest now live in the repo, so future edits can happen directly in GitHub.')}</p>
        </article>
      </aside>
    </section>

    <section class="section-shell">
      <div class="section-heading">
        <span class="section-kicker">{'继续阅读' if lang == 'zh' else 'Continue Reading'}</span>
        <h2>{'你还可以看这些文章' if lang == 'zh' else 'You may also want these posts'}</h2>
      </div>
      <div class="card-grid">{related_cards}</div>
    </section>
    """


def render_inner_page(page, lang, data):
    if page["slug"] == "news-blog":
        return render_news_blog_page(page, lang)

    detail = get_page_detail(page, lang)
    title = page["title_zh"] if lang == "zh" else page["title_en"]
    summary = page["summary_zh"] if lang == "zh" else page["summary_en"]
    related = render_related_cards(data, page, lang)
    return f"""
    <section class="hero hero-page">
      <div class="hero-copy">
        <span class="eyebrow">{html.escape(detail['eyebrow'])}</span>
        <h1>{html.escape(title)}</h1>
        <p class="lead">{html.escape(summary)}</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="{page_href(lang, '')}">{'返回首页' if lang == 'zh' else 'Back to Home'}</a>
          <a class="btn btn-secondary" href="{page_href(lang, 'company')}">{'查看公司介绍' if lang == 'zh' else 'See Company'}</a>
        </div>
      </div>
    </section>

    <section class="section-shell two-col-shell">
      <article class="panel">
        <span class="section-kicker">{'服务概览' if lang == 'zh' else 'Overview'}</span>
        <h2>{'这项服务能帮你做什么' if lang == 'zh' else 'What this service helps you do'}</h2>
        <p>{html.escape(detail['intro'])}</p>
      </article>
      <article class="panel soft-panel">
        <span class="section-kicker">{'适用场景' if lang == 'zh' else 'Best Fit'}</span>
        <h2>{'你可以在这些场景里使用它' if lang == 'zh' else 'Use it for situations like these'}</h2>
        {list_items(detail['fit'])}
      </article>
    </section>

    <section class="quick-grid">
      <article class="panel">
        <span class="section-kicker">{'我们处理什么' if lang == 'zh' else 'What We Handle'}</span>
        {list_items(detail['highlights'])}
      </article>
      <article class="panel">
        <span class="section-kicker">{'你会拿到什么' if lang == 'zh' else 'What You Get'}</span>
        {list_items(detail['outputs'])}
      </article>
      <article class="panel ai-panel">
        <span class="section-kicker">{'为什么更好理解' if lang == 'zh' else 'Why It Is Easier To Use'}</span>
        <p>
          {html.escape('这个页面现在按“能做什么、适合什么场景、你会拿到什么、流程怎么走”来组织，更容易快速判断。'
          if lang == 'zh' else
          'This page is now organized around what it does, when to use it, what you get, and how it works, so you can scan it faster.')}
        </p>
      </article>
    </section>

    <section class="section-shell two-col-shell">
      <article class="panel">
        <span class="section-kicker">{'流程' if lang == 'zh' else 'Workflow'}</span>
        <h2>{'这项服务通常怎么推进' if lang == 'zh' else 'How the work usually moves forward'}</h2>
        <ol class="timeline-list">
          {''.join(f'<li><span class="step-index">{index + 1:02d}</span><span>{html.escape(item)}</span></li>' for index, item in enumerate(detail['workflow']))}
        </ol>
      </article>
      <article class="panel">
        <span class="section-kicker">{'你可能还会需要' if lang == 'zh' else 'You May Also Need'}</span>
        <h2>{'这些服务经常会一起使用' if lang == 'zh' else 'These services are often used together'}</h2>
        <div class="card-grid compact-grid">{related}</div>
      </article>
    </section>
    """


def build_schema(page, lang):
    title = page["title_zh"] if lang == "zh" else page["title_en"]
    description = build_meta_description(page, lang)
    service_schema = {
        "@context": "https://schema.org",
        "@type": "Service" if page["slug"] else "Organization",
        "name": title if page["slug"] else "iCentech",
        "description": description,
        "url": f"https://www.icentech.com/{page['slug']}" if page["slug"] else "https://www.icentech.com/",
    }
    if page["slug"]:
        service_schema["provider"] = {"@type": "Organization", "name": "iCentech"}
    return json.dumps(service_schema, ensure_ascii=False)


def build_blog_schema(post):
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": post["title"],
            "description": post.get("excerpt") or excerpt_from_body(post.get("body_html", "")),
            "image": post.get("image_url", ""),
            "datePublished": post.get("date", ""),
            "publisher": {"@type": "Organization", "name": "iCentech"},
        },
        ensure_ascii=False,
    )


def render_page(data, page, lang):
    title = page["title_zh"] if lang == "zh" else page["title_en"]
    description = build_meta_description(page, lang)
    body_content = render_home(page, lang, data) if page["slug"] == "" else render_inner_page(page, lang, data)
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} | iCentech</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
  <meta property="og:title" content="{html.escape(title)} | iCentech">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://www.icentech.com/{page['slug']}">
  <meta property="og:image" content="/assets/{page_asset_basename(page['slug'])}-{lang}.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700;800&family=Noto+Sans+SC:wght@400;500;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/site.css">
  <script>{THEME_INIT_SCRIPT}</script>
  <script type="application/ld+json">{build_schema(page, lang)}</script>
</head>
<body>
  <a class="skip-link" href="#main-content">{'跳到正文' if lang == 'zh' else 'Skip to content'}</a>
  <header class="site-header">
    <div class="header-inner">
      {render_brand(lang)}
      <nav class="menu-panel" aria-label="Primary">
        {render_nav(page, lang)}
      </nav>
      <div class="header-actions">
        {render_theme_toggle(lang)}
        {render_switch(page, lang)}
      </div>
    </div>
  </header>
  <main id="main-content" class="main-shell">
    {render_breadcrumbs(page, lang)}
    {body_content}
  </main>
  <footer class="site-footer">
    <div class="footer-inner">
      {render_footer_content(lang)}
    </div>
  </footer>
  <script>{THEME_SCRIPT}</script>
  <script>{NAV_SCRIPT}</script>
</body>
</html>
"""


def render_blog_detail_document(data, page, post, lang):
    title = post["title"]
    description = post.get("excerpt") or excerpt_from_body(post.get("body_html", ""))
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} | iCentech</title>
  <meta name="description" content="{html.escape(description)}">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
  <meta property="og:title" content="{html.escape(title)} | iCentech">
  <meta property="og:description" content="{html.escape(description)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://www.icentech.com/blog/{post['slug']}">
  <meta property="og:image" content="{html.escape(post.get('image_url', ''))}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700;800&family=Noto+Sans+SC:wght@400;500;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/site.css">
  <script>{THEME_INIT_SCRIPT}</script>
  <script type="application/ld+json">{build_blog_schema(post)}</script>
</head>
<body>
  <a class="skip-link" href="#main-content">{'跳到正文' if lang == 'zh' else 'Skip to content'}</a>
  <header class="site-header">
    <div class="header-inner">
      {render_brand(lang)}
      <nav class="menu-panel" aria-label="Primary">
        {render_nav(page, lang)}
      </nav>
      <div class="header-actions">
        {render_theme_toggle(lang)}
        {render_blog_switch(post, lang)}
      </div>
    </div>
  </header>
  <main id="main-content" class="main-shell">
    {render_blog_breadcrumbs(page, post, lang)}
    {render_blog_post_page(page, post, lang)}
  </main>
  <footer class="site-footer">
    <div class="footer-inner">
      {render_footer_content(lang)}
    </div>
  </footer>
  <script>{THEME_SCRIPT}</script>
  <script>{NAV_SCRIPT}</script>
</body>
</html>
"""


def chip_text(value):
    return value if len(value) <= 22 else value[:21] + "…"


def wrap_text(value, max_chars, max_lines):
    text = value.strip()
    if not text:
        return []

    if " " not in text:
        chunks = [text[index:index + max_chars] for index in range(0, len(text), max_chars)]
    else:
        chunks = []
        current = []
        current_len = 0
        for word in text.split():
            proposed = current_len + len(word) + (1 if current else 0)
            if current and proposed > max_chars:
                chunks.append(" ".join(current))
                current = [word]
                current_len = len(word)
            else:
                current.append(word)
                current_len = proposed
        if current:
            chunks.append(" ".join(current))

    if len(chunks) > max_lines:
        chunks = chunks[:max_lines]
        chunks[-1] = chunks[-1][: max(0, max_chars - 1)].rstrip() + "…"
    return chunks


def render_svg(page, lang):
    theme = get_theme(page)
    return dedent(
        f"""\
        <svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" role="img" aria-hidden="true">
          <defs>
            <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="{theme['soft']}"/>
              <stop offset="55%" stop-color="#ffffff"/>
              <stop offset="100%" stop-color="#f4fbff"/>
            </linearGradient>
            <linearGradient id="panelGlow" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="rgba(255,255,255,0.92)"/>
              <stop offset="100%" stop-color="rgba(255,255,255,0.58)"/>
            </linearGradient>
            <linearGradient id="blueOrb" x1="20%" y1="20%" x2="85%" y2="85%">
              <stop offset="0%" stop-color="{theme['secondary']}"/>
              <stop offset="100%" stop-color="{theme['primary']}"/>
            </linearGradient>
            <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="{theme['accent']}"/>
              <stop offset="100%" stop-color="{BRAND_TOKENS['brand_green_600']}"/>
            </linearGradient>
            <linearGradient id="line" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="{theme['secondary']}"/>
              <stop offset="100%" stop-color="{theme['accent']}"/>
            </linearGradient>
            <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
              <feDropShadow dx="0" dy="24" stdDeviation="24" flood-color="#98b7cc" flood-opacity="0.25"/>
            </filter>
          </defs>
          <rect width="1600" height="900" fill="url(#bg)"/>
          <g opacity="0.55">
            <circle cx="1420" cy="110" r="210" fill="#d8efff"/>
            <circle cx="190" cy="770" r="250" fill="#ebf7da"/>
          </g>
          <g filter="url(#shadow)">
            <rect x="360" y="132" width="880" height="636" rx="40" fill="rgba(255,255,255,0.74)"/>
            <rect x="430" y="204" width="740" height="492" rx="34" fill="rgba(255,255,255,0.58)"/>
          </g>
          <g filter="url(#shadow)">
            <circle cx="800" cy="450" r="176" fill="url(#blueOrb)"/>
            <circle cx="800" cy="450" r="114" fill="rgba(255,255,255,0.92)"/>
            <circle cx="800" cy="450" r="56" fill="url(#accent)"/>
          </g>
          <g filter="url(#shadow)">
            <rect x="520" y="274" width="154" height="92" rx="24" fill="rgba(255,255,255,0.94)"/>
            <rect x="926" y="312" width="164" height="104" rx="24" fill="rgba(255,255,255,0.92)"/>
            <rect x="540" y="540" width="176" height="102" rx="24" fill="rgba(255,255,255,0.9)"/>
            <rect x="886" y="548" width="194" height="118" rx="24" fill="rgba(255,255,255,0.94)"/>
          </g>
          <g fill="none" stroke-linecap="round">
            <path d="M574 320 H628" stroke="url(#line)" stroke-width="12"/>
            <path d="M954 364 H1036" stroke="url(#line)" stroke-width="12"/>
            <path d="M572 592 H650" stroke="url(#line)" stroke-width="12"/>
            <path d="M924 598 H1022" stroke="url(#line)" stroke-width="12"/>
            <path d="M936 634 H998" stroke="{theme['primary']}" stroke-width="10" opacity="0.72"/>
          </g>
          <g opacity="0.7">
            <circle cx="800" cy="450" r="226" fill="none" stroke="rgba(255,255,255,0.46)" stroke-width="2"/>
            <circle cx="800" cy="450" r="266" fill="none" stroke="rgba(5,150,239,0.18)" stroke-width="2"/>
          </g>
        </svg>
        """
    )


NAV_SCRIPT = dedent(
    """
    (() => {
      const groups = Array.from(document.querySelectorAll("[data-menu-group]"));
      if (!groups.length) return;
      const closeTimers = new WeakMap();

      const clearCloseTimer = (group) => {
        const timer = closeTimers.get(group);
        if (timer) {
          window.clearTimeout(timer);
          closeTimers.delete(group);
        }
      };

      const closeGroup = (group) => {
        clearCloseTimer(group);
        group.classList.remove("is-open");
        const button = group.querySelector(".menu-title");
        const list = group.querySelector(".menu-list");
        if (button) button.setAttribute("aria-expanded", "false");
        if (list) list.hidden = true;
      };

      const openGroup = (group) => {
        clearCloseTimer(group);
        groups.forEach((item) => {
          if (item !== group) closeGroup(item);
        });
        group.classList.add("is-open");
        const button = group.querySelector(".menu-title");
        const list = group.querySelector(".menu-list");
        if (button) button.setAttribute("aria-expanded", "true");
        if (list) list.hidden = false;
      };

      const scheduleClose = (group) => {
        clearCloseTimer(group);
        closeTimers.set(group, window.setTimeout(() => closeGroup(group), 180));
      };

      groups.forEach((group) => {
        const button = group.querySelector(".menu-title");
        const list = group.querySelector(".menu-list");
        if (!button) return;

        closeGroup(group);

        group.addEventListener("mouseenter", () => openGroup(group));
        group.addEventListener("mouseleave", () => scheduleClose(group));
        group.addEventListener("focusin", () => openGroup(group));
        group.addEventListener("focusout", () => {
          window.setTimeout(() => {
            if (!group.contains(document.activeElement)) closeGroup(group);
          }, 0);
        });
        if (list) {
          list.addEventListener("mouseenter", () => openGroup(group));
        }
        button.addEventListener("click", (event) => {
          event.stopPropagation();
          if (group.classList.contains("is-open")) {
            closeGroup(group);
          } else {
            openGroup(group);
          }
        });
      });

      document.addEventListener("click", (event) => {
        if (!event.target.closest("[data-menu-group]")) {
          groups.forEach(closeGroup);
        }
      });

      window.addEventListener("resize", () => groups.forEach(closeGroup));
    })();
    """
)


THEME_INIT_SCRIPT = dedent(
    """
    (() => {
      const savedTheme = window.localStorage.getItem("icentech-theme");
      const theme = savedTheme === "light" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", theme);
    })();
    """
)


THEME_SCRIPT = dedent(
    """
    (() => {
      const button = document.querySelector("[data-theme-toggle]");
      if (!button) return;

      const root = document.documentElement;
      const lightLabel = button.getAttribute("data-label-light") || "Switch To Light";
      const darkLabel = button.getAttribute("data-label-dark") || "Switch To Dark";

      const updateButton = () => {
        const theme = root.getAttribute("data-theme") === "light" ? "light" : "dark";
        button.setAttribute("aria-pressed", theme === "light" ? "true" : "false");
        button.textContent = theme === "light" ? darkLabel : lightLabel;
      };

      button.addEventListener("click", () => {
        const nextTheme = root.getAttribute("data-theme") === "light" ? "dark" : "light";
        root.setAttribute("data-theme", nextTheme);
        window.localStorage.setItem("icentech-theme", nextTheme);
        updateButton();
      });

      updateButton();
    })();
    """
)


SITE_CSS = dedent(
    """
    :root {
      --font-body: "Inter", "Noto Sans SC", "Helvetica Neue", Arial, sans-serif;
      --font-heading: "Space Grotesk", "Noto Sans SC", "Helvetica Neue", Arial, sans-serif;
      --font-mono: "IBM Plex Mono", "SFMono-Regular", "Consolas", monospace;
      --brand-blue-700: #0c79d6;
      --brand-blue-500: #0596ef;
      --brand-blue-300: #8fd0ff;
      --brand-green-600: #63a60b;
      --brand-green-500: #78c515;
      --brand-green-200: #dff3b8;
      --bg-950: #061119;
      --bg-900: #0a1824;
      --bg-860: #102334;
      --bg-820: #13293d;
      --ink: #eff8ff;
      --ink-soft: #a8c3d8;
      --line: rgba(143, 208, 255, 0.16);
      --line-strong: rgba(143, 208, 255, 0.26);
      --mist: rgba(143, 208, 255, 0.08);
      --surface: rgba(14, 28, 41, 0.9);
      --surface-alt: rgba(18, 39, 57, 0.8);
      --surface-soft: rgba(16, 35, 52, 0.78);
      --shadow-lg: 0 28px 70px rgba(0, 0, 0, 0.34);
      --shadow-md: 0 18px 38px rgba(0, 0, 0, 0.22);
      --radius-xl: 28px;
      --radius-lg: 22px;
      --radius-md: 16px;
      --radius-pill: 999px;
      --content-width: 1220px;
    }

    * {
      box-sizing: border-box;
    }

    html {
      scroll-behavior: smooth;
    }

    body {
      margin: 0;
      color: var(--ink);
      overflow-x: hidden;
      background:
        radial-gradient(circle at 10% 8%, rgba(5, 150, 239, 0.28), transparent 28%),
        radial-gradient(circle at 88% 10%, rgba(120, 197, 21, 0.22), transparent 18%),
        radial-gradient(circle at 50% 120%, rgba(5, 150, 239, 0.16), transparent 32%),
        linear-gradient(180deg, var(--bg-900) 0%, #0a1621 45%, var(--bg-950) 100%);
      font-family: var(--font-body);
      line-height: 1.65;
    }

    img {
      max-width: 100%;
      display: block;
    }

    a {
      color: inherit;
    }

    h1,
    h2,
    h3,
    p,
    li,
    .menu-item,
    .menu-title,
    .blog-card-body,
    .panel,
    .metric-card {
      min-width: 0;
      overflow-wrap: anywhere;
    }

    .skip-link {
      position: absolute;
      left: 14px;
      top: -44px;
      padding: 10px 14px;
      border-radius: 12px;
      background: white;
      color: #091826;
      text-decoration: none;
      z-index: 99;
    }

    .skip-link:focus {
      top: 14px;
    }

    .site-header {
      position: sticky;
      top: 0;
      z-index: 30;
      backdrop-filter: blur(16px);
      background: rgba(7, 17, 26, 0.76);
      border-bottom: 1px solid rgba(143, 208, 255, 0.08);
    }

    .header-inner,
    .main-shell,
    .footer-inner {
      width: min(var(--content-width), calc(100% - 32px));
      margin: 0 auto;
    }

    .header-inner {
      display: grid;
      grid-template-columns: auto 1fr auto;
      gap: 24px;
      align-items: center;
      padding: 18px 0;
    }

    .brand {
      display: inline-flex;
      align-items: center;
      text-decoration: none;
      min-width: 0;
    }

    .brand-badge {
      display: inline-grid;
      place-items: center;
      width: 156px;
      min-height: 56px;
      padding: 4px 6px;
      border-radius: 22px;
      background: rgba(255, 255, 255, 0.92);
      border: 1px solid rgba(143, 208, 255, 0.14);
      box-shadow: 0 10px 20px rgba(0, 0, 0, 0.14);
    }

    .brand-logo {
      width: 100%;
      max-width: 144px;
      height: auto;
      object-fit: contain;
      object-position: center;
      justify-self: center;
      align-self: center;
      filter: none;
    }

    .brand-mark-fallback {
      display: inline-grid;
      place-items: center;
      width: 62px;
      height: 62px;
      border-radius: 18px;
      font-weight: 800;
      font-size: 28px;
      color: white;
      background: linear-gradient(135deg, var(--brand-blue-700), var(--brand-blue-500));
    }

    .menu-panel {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 12px;
    }

    .menu-group {
      position: relative;
      padding-bottom: 12px;
      margin-bottom: -12px;
    }

    .menu-group::after {
      content: "";
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      height: 14px;
    }

    .menu-title {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 12px 16px;
      border-radius: 999px;
      border: 1px solid rgba(143, 208, 255, 0.1);
      background: rgba(255, 255, 255, 0.04);
      color: var(--ink);
      font-size: 11px;
      font-family: var(--font-mono);
      font-weight: 600;
      letter-spacing: 0.12em;
      cursor: pointer;
      appearance: none;
      transition: all 0.2s ease;
    }

    .menu-title:hover,
    .menu-group.is-open .menu-title,
    .menu-group:focus-within .menu-title {
      border-color: rgba(5, 150, 239, 0.32);
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.08), rgba(5, 150, 239, 0.12));
      box-shadow: 0 16px 26px rgba(0, 0, 0, 0.18);
      transform: translateY(-1px);
    }

    .menu-list {
      position: absolute;
      top: calc(100% + 2px);
      left: 0;
      min-width: 230px;
      padding: 10px;
      display: none;
      gap: 6px;
      background: rgba(12, 26, 39, 0.98);
      border: 1px solid rgba(143, 208, 255, 0.12);
      border-radius: 18px;
      box-shadow: var(--shadow-md);
    }

    .menu-group.is-open .menu-list,
    .menu-group:focus-within .menu-list {
      display: grid;
    }

    .menu-item {
      padding: 10px 12px;
      text-decoration: none;
      color: var(--ink-soft);
      border-radius: 12px;
      transition: all 0.18s ease;
      font-size: 14px;
    }

    .menu-item:hover,
    .menu-item.is-active {
      color: var(--ink);
      background: linear-gradient(135deg, rgba(5, 150, 239, 0.16), rgba(120, 197, 21, 0.16));
    }

    .header-actions {
      display: flex;
      gap: 10px;
      align-items: center;
      justify-content: flex-end;
    }

    .theme-toggle,
    .lang-switch {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      text-decoration: none;
      color: var(--ink);
      padding: 10px 14px;
      border-radius: 999px;
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.08), rgba(143, 208, 255, 0.08));
      border: 1px solid rgba(143, 208, 255, 0.18);
      font-weight: 700;
      font-size: 12px;
      font-family: var(--font-mono);
      letter-spacing: 0.06em;
      min-height: 42px;
    }

    .theme-toggle {
      cursor: pointer;
      appearance: none;
    }

    .main-shell {
      padding: 40px 0 88px;
      display: grid;
      gap: 28px;
    }

    .breadcrumb {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
      padding: 0 2px;
      color: var(--ink-soft);
      font-size: 0.84rem;
      font-family: var(--font-mono);
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }

    .breadcrumb a {
      color: var(--brand-blue-300);
      text-decoration: none;
      font-weight: 700;
    }

    .breadcrumb-sep {
      color: rgba(168, 195, 216, 0.65);
    }

    .hero {
      display: grid;
      grid-template-columns: 1fr;
      gap: 18px;
      align-items: start;
    }

    .hero-copy,
    .hero-visual,
    .panel,
    .metric-card,
    .service-card {
      border: 1px solid var(--line);
      background: var(--surface);
      box-shadow: var(--shadow-md);
      backdrop-filter: blur(12px);
    }

    .hero-copy {
      width: 100%;
      padding: 40px;
      border-radius: var(--radius-xl);
      background:
        linear-gradient(180deg, rgba(255, 255, 255, 0.04), transparent 50%),
        radial-gradient(circle at top left, rgba(120, 197, 21, 0.16), transparent 28%),
        linear-gradient(145deg, rgba(16, 35, 52, 0.96), rgba(10, 24, 36, 0.98));
    }

    .hero-visual {
      width: min(940px, 100%);
      justify-self: center;
      border-radius: var(--radius-xl);
      overflow: hidden;
      min-height: 0;
      padding: 18px;
      background:
        radial-gradient(circle at top right, rgba(120, 197, 21, 0.2), transparent 25%),
        radial-gradient(circle at bottom left, rgba(5, 150, 239, 0.2), transparent 25%),
        linear-gradient(180deg, rgba(16, 35, 52, 0.96), rgba(9, 24, 35, 0.98));
    }

    .hero-image {
      width: 100%;
      height: auto;
      max-height: 100%;
      object-fit: contain;
      border-radius: 18px;
    }

    .eyebrow,
    .section-kicker,
    .card-kicker {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 11px;
      font-family: var(--font-mono);
      font-weight: 600;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: #b8f05f;
    }

    .eyebrow {
      margin-bottom: 18px;
    }

    h1,
    h2,
    h3 {
      margin: 0;
      color: var(--ink);
      font-family: var(--font-heading);
      line-height: 0.98;
    }

    h1 {
      font-size: clamp(2.7rem, 5vw, 5.3rem);
      margin-bottom: 18px;
      max-width: 12ch;
      letter-spacing: -0.04em;
    }

    h2 {
      font-size: clamp(1.9rem, 3.2vw, 3.2rem);
      margin: 10px 0 16px;
      letter-spacing: -0.03em;
    }

    h3 {
      font-size: 1.45rem;
      margin-bottom: 10px;
      letter-spacing: -0.03em;
    }

    p {
      margin: 0;
      color: var(--ink-soft);
      font-size: 1rem;
    }

    .lead {
      font-size: 1.08rem;
      max-width: 62ch;
    }

    .hero-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 24px;
    }

    .hero-meta-strip,
    .blog-card-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 22px;
      align-items: center;
    }

    .meta-pill {
      display: inline-flex;
      align-items: center;
      min-height: 34px;
      padding: 0 12px;
      border-radius: 999px;
      border: 1px solid rgba(143, 208, 255, 0.14);
      background: rgba(255, 255, 255, 0.05);
      color: var(--ink);
      font-size: 0.78rem;
      font-family: var(--font-mono);
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }

    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 48px;
      padding: 0 18px;
      border-radius: 999px;
      text-decoration: none;
      font-weight: 700;
      transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
    }

    .btn:hover {
      transform: translateY(-1px);
      box-shadow: 0 16px 24px rgba(0, 0, 0, 0.2);
    }

    .btn-primary {
      color: white;
      background: linear-gradient(135deg, var(--brand-blue-700), var(--brand-blue-500));
    }

    .btn-secondary {
      color: var(--ink);
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.06), rgba(143, 208, 255, 0.08));
      border: 1px solid rgba(143, 208, 255, 0.12);
    }

    .trust-pills {
      margin: 24px 0 0;
      padding: 0;
      list-style: none;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }

    .trust-pills li {
      padding: 10px 14px;
      border-radius: 999px;
      background: rgba(120, 197, 21, 0.12);
      color: var(--ink);
      font-size: 13px;
      font-weight: 600;
      border: 1px solid rgba(120, 197, 21, 0.12);
    }

    .metrics-grid,
    .quick-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 18px;
    }

    .metric-card {
      padding: 24px;
      border-radius: var(--radius-lg);
      background:
        linear-gradient(180deg, rgba(255, 255, 255, 0.03), transparent 55%),
        linear-gradient(180deg, rgba(18, 39, 57, 0.96), rgba(10, 24, 36, 0.98));
    }

    .metric-card strong {
      display: block;
      font-size: 2rem;
      color: white;
      margin-bottom: 10px;
    }

    .metric-card span {
      color: var(--ink-soft);
      font-size: 0.95rem;
    }

    .section-shell {
      display: grid;
      gap: 18px;
    }

    .section-heading {
      display: grid;
      gap: 8px;
      max-width: 820px;
    }

    .two-col-shell {
      grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
      align-items: start;
    }

    .stack-grid {
      display: grid;
      gap: 16px;
    }

    .stack-grid-three {
      grid-template-columns: repeat(3, minmax(0, 1fr));
    }

    .panel {
      padding: 30px;
      border-radius: var(--radius-lg);
      background: linear-gradient(180deg, rgba(18, 39, 57, 0.92), rgba(10, 24, 36, 0.96));
    }

    .soft-panel {
      background:
        radial-gradient(circle at top left, rgba(120, 197, 21, 0.18), transparent 30%),
        linear-gradient(160deg, rgba(18, 39, 57, 0.95), rgba(12, 28, 39, 0.98));
    }

    .ai-panel {
      background:
        radial-gradient(circle at 90% 8%, rgba(5, 150, 239, 0.24), transparent 26%),
        linear-gradient(160deg, rgba(16, 35, 52, 0.98), rgba(10, 24, 36, 0.98));
    }

    .panel ul,
    .panel ol {
      margin: 18px 0 0;
      padding-left: 20px;
      color: var(--ink);
    }

    .panel li {
      margin-bottom: 10px;
    }

    .card-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 18px;
    }

    .compact-grid {
      grid-template-columns: 1fr;
    }

    .service-card {
      display: grid;
      gap: 12px;
      padding: 24px;
      border-radius: var(--radius-lg);
      text-decoration: none;
      background:
        radial-gradient(circle at top right, rgba(5, 150, 239, 0.14), transparent 28%),
        linear-gradient(180deg, rgba(18, 39, 57, 0.96), rgba(10, 24, 36, 0.98));
      transition: transform 0.18s ease, box-shadow 0.18s ease;
      min-height: 220px;
    }

    .service-card:hover {
      transform: translateY(-3px);
      box-shadow: var(--shadow-lg);
      border-color: rgba(143, 208, 255, 0.28);
    }

    .service-card p {
      font-size: 0.98rem;
    }

    .quick-grid {
      grid-template-columns: repeat(3, minmax(0, 1fr));
    }

    .blog-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 18px;
    }

    .blog-card {
      display: grid;
      grid-template-columns: 200px minmax(0, 1fr);
      gap: 18px;
      padding: 18px;
      border-radius: var(--radius-lg);
      border: 1px solid var(--line);
      background: linear-gradient(180deg, rgba(18, 39, 57, 0.94), rgba(10, 24, 36, 0.98));
      box-shadow: var(--shadow-md);
    }

    .blog-card-media {
      display: block;
      border-radius: 18px;
      overflow: hidden;
      background: var(--surface-alt);
      min-height: 160px;
    }

    .blog-card-media img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .blog-card-body {
      display: grid;
      align-content: start;
      gap: 10px;
      min-width: 0;
    }

    .blog-card-date {
      color: var(--brand-blue-300);
      font-size: 0.82rem;
      font-family: var(--font-mono);
      font-weight: 600;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }

    .blog-card-body h3 {
      font-size: 1.4rem;
    }

    .blog-card-body h3 a,
    .text-link {
      text-decoration: none;
    }

    .text-link {
      color: #d3f895;
      font-weight: 700;
    }

    .timeline-list {
      list-style: none;
      padding: 0;
      margin: 20px 0 0;
      display: grid;
      gap: 12px;
    }

    .timeline-list li {
      display: grid;
      grid-template-columns: 52px 1fr;
      gap: 14px;
      align-items: center;
      padding: 18px 18px;
      border: 1px solid rgba(143, 208, 255, 0.1);
      border-radius: 16px;
      background: rgba(255, 255, 255, 0.03);
      margin: 0;
    }

    .timeline-list li:last-child {
      border-bottom: 1px solid rgba(143, 208, 255, 0.1);
    }

    .step-index {
      display: inline-grid;
      place-items: center;
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: linear-gradient(135deg, rgba(5, 150, 239, 0.2), rgba(120, 197, 21, 0.24));
      color: white;
      font-weight: 800;
      letter-spacing: 0.04em;
      font-family: var(--font-mono);
    }

    .cta-panel {
      padding: 36px;
      background:
        radial-gradient(circle at top right, rgba(120, 197, 21, 0.22), transparent 24%),
        linear-gradient(135deg, rgba(18, 39, 57, 0.98), rgba(10, 24, 36, 0.98));
    }

    .post-content {
      display: grid;
      gap: 16px;
    }

    .post-content h2,
    .post-content h3 {
      margin: 22px 0 8px;
      line-height: 1.06;
    }

    .post-content p,
    .post-content li {
      color: var(--ink-soft);
    }

    .post-content ul,
    .post-content ol {
      padding-left: 20px;
      margin: 6px 0 0;
    }

    .post-content a {
      color: #d3f895;
    }

    .tag-list {
      list-style: none;
      padding: 0;
      margin: 18px 0 0;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }

    .tag-list li {
      margin: 0;
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(143, 208, 255, 0.1);
      font-size: 0.82rem;
      font-family: var(--font-mono);
      color: var(--ink);
    }

    .post-panel {
      min-width: 0;
    }

    .site-footer {
      border-top: 1px solid rgba(143, 208, 255, 0.08);
      background: rgba(7, 17, 26, 0.72);
    }

    html[data-theme="light"] {
      --ink: #153247;
      --ink-soft: #4d6a7d;
      --line: rgba(17, 52, 76, 0.1);
      --line-strong: rgba(17, 52, 76, 0.16);
      --mist: rgba(5, 150, 239, 0.08);
      --surface: rgba(255, 255, 255, 0.94);
      --surface-alt: rgba(246, 251, 254, 0.94);
      --surface-soft: rgba(245, 251, 255, 0.92);
      --shadow-lg: 0 24px 54px rgba(17, 52, 76, 0.12);
      --shadow-md: 0 16px 34px rgba(17, 52, 76, 0.09);
    }

    html[data-theme="light"] body {
      background:
        radial-gradient(circle at 10% 8%, rgba(5, 150, 239, 0.16), transparent 28%),
        radial-gradient(circle at 88% 10%, rgba(120, 197, 21, 0.16), transparent 18%),
        radial-gradient(circle at 50% 120%, rgba(5, 150, 239, 0.1), transparent 32%),
        linear-gradient(180deg, #f4fbff 0%, #ffffff 45%, #f7fbfd 100%);
    }

    html[data-theme="light"] .site-header {
      background: rgba(255, 255, 255, 0.82);
      border-bottom: 1px solid rgba(17, 52, 76, 0.08);
    }

    html[data-theme="light"] .brand-badge {
      background: white;
      border-color: rgba(17, 52, 76, 0.08);
      box-shadow: 0 8px 18px rgba(17, 52, 76, 0.08);
    }

    html[data-theme="light"] .menu-title {
      border-color: rgba(17, 52, 76, 0.08);
      background: rgba(255, 255, 255, 0.78);
      color: var(--ink);
    }

    html[data-theme="light"] .menu-title:hover,
    html[data-theme="light"] .menu-group.is-open .menu-title,
    html[data-theme="light"] .menu-group:focus-within .menu-title {
      border-color: rgba(5, 150, 239, 0.24);
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(238, 248, 255, 0.96));
      box-shadow: 0 14px 24px rgba(17, 52, 76, 0.08);
    }

    html[data-theme="light"] .menu-list {
      background: rgba(255, 255, 255, 0.98);
      border-color: rgba(17, 52, 76, 0.08);
    }

    html[data-theme="light"] .menu-item:hover,
    html[data-theme="light"] .menu-item.is-active {
      background: linear-gradient(135deg, rgba(5, 150, 239, 0.09), rgba(120, 197, 21, 0.12));
    }

    html[data-theme="light"] .theme-toggle,
    html[data-theme="light"] .lang-switch {
      background: linear-gradient(180deg, #ffffff, #eef8ff);
      border-color: rgba(17, 52, 76, 0.12);
      color: var(--ink);
    }

    html[data-theme="light"] .hero-copy,
    html[data-theme="light"] .hero-visual,
    html[data-theme="light"] .panel,
    html[data-theme="light"] .metric-card,
    html[data-theme="light"] .service-card,
    html[data-theme="light"] .blog-card {
      border-color: rgba(17, 52, 76, 0.08);
      background: rgba(255, 255, 255, 0.94);
      box-shadow: var(--shadow-md);
    }

    html[data-theme="light"] .hero-copy {
      background:
        linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(245, 251, 255, 0.96)),
        radial-gradient(circle at top left, rgba(120, 197, 21, 0.12), transparent 28%);
    }

    html[data-theme="light"] .hero-visual {
      background:
        radial-gradient(circle at top right, rgba(120, 197, 21, 0.14), transparent 25%),
        radial-gradient(circle at bottom left, rgba(5, 150, 239, 0.14), transparent 25%),
        linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(238, 248, 255, 0.94));
    }

    html[data-theme="light"] .soft-panel {
      background:
        radial-gradient(circle at top left, rgba(120, 197, 21, 0.12), transparent 30%),
        linear-gradient(160deg, #ffffff, #f6fbfe);
    }

    html[data-theme="light"] .ai-panel {
      background:
        radial-gradient(circle at 90% 8%, rgba(5, 150, 239, 0.14), transparent 26%),
        linear-gradient(160deg, #ffffff, #eff9ff);
    }

    html[data-theme="light"] .service-card {
      background:
        radial-gradient(circle at top right, rgba(5, 150, 239, 0.08), transparent 28%),
        linear-gradient(180deg, #ffffff, #f6fbfe);
    }

    html[data-theme="light"] .metric-card {
      background:
        linear-gradient(180deg, rgba(255, 255, 255, 1), rgba(242, 249, 254, 0.94));
    }

    html[data-theme="light"] .metric-card strong {
      color: var(--brand-blue-700);
    }

    html[data-theme="light"] .trust-pills li,
    html[data-theme="light"] .meta-pill,
    html[data-theme="light"] .tag-list li,
    html[data-theme="light"] .timeline-list li {
      background: rgba(5, 150, 239, 0.06);
      border-color: rgba(17, 52, 76, 0.08);
      color: var(--ink);
    }

    html[data-theme="light"] .btn-secondary {
      background: linear-gradient(180deg, white, #eef8ff);
      border-color: rgba(17, 52, 76, 0.1);
    }

    html[data-theme="light"] .text-link,
    html[data-theme="light"] .post-content a {
      color: var(--brand-blue-700);
    }

    html[data-theme="light"] .site-footer {
      background: rgba(255, 255, 255, 0.86);
      border-top: 1px solid rgba(17, 52, 76, 0.08);
    }

    html[data-theme="light"] .footer-block {
      background: rgba(255, 255, 255, 0.82);
      border-color: rgba(17, 52, 76, 0.08);
      box-shadow: 0 14px 28px rgba(17, 52, 76, 0.06);
    }

    html[data-theme="light"] .footer-brand-block {
      background:
        linear-gradient(180deg, rgba(5, 150, 239, 0.08), rgba(255, 255, 255, 0.94)),
        rgba(255, 255, 255, 0.9);
    }

    html[data-theme="light"] .footer-social-block {
      background:
        linear-gradient(180deg, rgba(120, 197, 21, 0.09), rgba(255, 255, 255, 0.94)),
        rgba(255, 255, 255, 0.9);
    }

    html[data-theme="light"] .footer-heading-icon {
      background: rgba(5, 150, 239, 0.08);
      border-color: rgba(17, 52, 76, 0.08);
      color: var(--brand-blue-700);
    }

    html[data-theme="light"] .footer-meta,
    html[data-theme="light"] .footer-item-label {
      color: color-mix(in srgb, var(--muted) 88%, #11344c 12%);
    }

    html[data-theme="light"] .footer-inner a {
      color: var(--brand-blue-700);
    }

    html[data-theme="light"] .footer-inner a:hover {
      color: var(--brand-blue-800);
    }

    html[data-theme="light"] .social-link {
      color: var(--brand-blue-700);
      background:
        linear-gradient(180deg, #ffffff, #eef8ff),
        rgba(255, 255, 255, 0.9);
      border-color: rgba(17, 52, 76, 0.1);
      box-shadow: 0 12px 24px rgba(17, 52, 76, 0.08);
    }

    html[data-theme="light"] .social-link:hover,
    html[data-theme="light"] .social-link:focus-visible {
      color: var(--brand-blue-800);
      border-color: rgba(120, 197, 21, 0.34);
      background:
        linear-gradient(180deg, rgba(120, 197, 21, 0.14), rgba(5, 150, 239, 0.08)),
        #ffffff;
    }

    .footer-inner {
      padding: 28px 0 40px;
      display: grid;
      gap: 12px;
    }

    .footer-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 18px;
    }

    .footer-block {
      display: grid;
      gap: 12px;
      align-content: start;
      padding: 18px 18px 20px;
      border-radius: 24px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(143, 208, 255, 0.08);
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
    }

    .footer-brand-block {
      background:
        linear-gradient(180deg, rgba(5, 150, 239, 0.08), rgba(5, 150, 239, 0.03)),
        rgba(255, 255, 255, 0.03);
      border-color: rgba(5, 150, 239, 0.14);
    }

    .footer-social-block {
      background:
        linear-gradient(180deg, rgba(120, 197, 21, 0.07), rgba(120, 197, 21, 0.02)),
        rgba(255, 255, 255, 0.03);
      border-color: rgba(120, 197, 21, 0.14);
    }

    .footer-heading {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .footer-heading-icon {
      width: 36px;
      height: 36px;
      border-radius: 12px;
      display: inline-grid;
      place-items: center;
      color: var(--brand-blue-300);
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(143, 208, 255, 0.12);
      flex-shrink: 0;
    }

    .footer-heading-icon svg,
    .social-link svg {
      width: 18px;
      height: 18px;
      display: block;
    }

    .footer-stack {
      display: grid;
      gap: 4px;
    }

    .footer-lead {
      font-size: 0.96rem;
      color: var(--muted);
      max-width: 24ch;
    }

    .footer-meta {
      font-size: 0.8rem;
      color: color-mix(in srgb, var(--muted) 84%, white 16%);
      letter-spacing: 0.03em;
    }

    .footer-item-label {
      font-size: 0.74rem;
      font-family: var(--font-mono);
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: color-mix(in srgb, var(--muted) 74%, white 26%);
    }

    .footer-item-copy {
      font-size: 0.93rem;
      color: var(--ink);
    }

    .footer-title {
      color: var(--ink);
      font-family: var(--font-mono);
      font-size: 0.8rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    .footer-inner p {
      margin: 0;
    }

    .footer-inner a {
      color: color-mix(in srgb, var(--brand-blue-300) 86%, white 14%);
      text-decoration: none;
    }

    .footer-inner a:hover {
      color: white;
    }

    .social-links {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
    }

    .social-link {
      position: relative;
      width: 44px;
      height: 44px;
      border-radius: 999px;
      display: inline-grid;
      place-items: center;
      color: var(--brand-blue-200);
      background:
        linear-gradient(180deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.03)),
        rgba(9, 24, 38, 0.4);
      border: 1px solid rgba(143, 208, 255, 0.16);
      box-shadow: 0 10px 24px rgba(1, 8, 15, 0.22);
      transition: transform 160ms ease, border-color 160ms ease, color 160ms ease, background 160ms ease;
    }

    .social-link:hover,
    .social-link:focus-visible {
      transform: translateY(-1px);
      color: white;
      border-color: rgba(120, 197, 21, 0.34);
      background:
        linear-gradient(180deg, rgba(120, 197, 21, 0.18), rgba(5, 150, 239, 0.14)),
        rgba(9, 24, 38, 0.48);
      outline: none;
    }

    .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }

    @media (max-width: 1100px) {
      .header-inner {
        grid-template-columns: 1fr;
      }

      .menu-panel {
        justify-content: flex-start;
      }

      .header-actions {
        justify-content: flex-start;
      }

      .hero,
      .two-col-shell,
      .metrics-grid,
      .card-grid,
      .quick-grid,
      .blog-grid,
      .stack-grid-three,
      .footer-grid {
        grid-template-columns: 1fr;
      }
    }

    @media (max-width: 780px) {
      .header-inner,
      .main-shell,
      .footer-inner {
        width: min(var(--content-width), calc(100% - 24px));
      }

      .site-header {
        position: static;
      }

      .brand {
        align-items: flex-start;
      }

      .brand-logo {
        width: 100%;
        max-width: 132px;
      }

      .footer-block {
        padding: 16px 16px 18px;
        border-radius: 20px;
      }

      .footer-heading-icon {
        width: 34px;
        height: 34px;
      }

      .social-link {
        width: 42px;
        height: 42px;
      }

      .menu-group {
        width: 100%;
      }

      .menu-title {
        width: 100%;
        justify-content: space-between;
      }

      .menu-list {
        position: static;
        margin-top: 10px;
        min-width: 0;
      }

      .blog-card {
        grid-template-columns: 1fr;
      }

      .hero-copy,
      .panel,
      .service-card,
      .metric-card {
        padding: 22px;
      }

      h1 {
        max-width: none;
      }

      .main-shell {
        padding-top: 20px;
      }

      .breadcrumb {
        font-size: 0.88rem;
      }
    }
    """
)


def write_brand_assets(data):
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / "site.css").write_text(SITE_CSS, encoding="utf-8")

    if LOGO_SOURCE.exists():
        shutil.copy2(LOGO_SOURCE, ASSETS_DIR / LOGO_ASSET_NAME)

    if BLOG_MEDIA_DIR.exists():
        blog_asset_dir = ASSETS_DIR / "blog"
        blog_asset_dir.mkdir(parents=True, exist_ok=True)
        for asset in BLOG_MEDIA_DIR.iterdir():
            if asset.is_file():
                shutil.copy2(asset, blog_asset_dir / asset.name)

    for page in data["pages"]:
        for lang in ("en", "zh"):
            svg_name = f"{page_asset_basename(page['slug'])}-{lang}.svg"
            (ASSETS_DIR / svg_name).write_text(render_svg(page, lang), encoding="utf-8")


def main():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_brand_assets(data)

    en_dir = OUT_DIR / "en"
    zh_dir = OUT_DIR / "zh"
    en_blog_dir = en_dir / "blog"
    zh_blog_dir = zh_dir / "blog"
    en_dir.mkdir(parents=True, exist_ok=True)
    zh_dir.mkdir(parents=True, exist_ok=True)
    en_blog_dir.mkdir(parents=True, exist_ok=True)
    zh_blog_dir.mkdir(parents=True, exist_ok=True)

    for page in data["pages"]:
        filename = page_filename(page["slug"])
        (en_dir / filename).write_text(render_page(data, page, "en"), encoding="utf-8")
        (zh_dir / filename).write_text(render_page(data, page, "zh"), encoding="utf-8")

    blog_page = next((page for page in data["pages"] if page["slug"] == "news-blog"), None)
    if blog_page:
        for post in load_blog_posts():
            (en_blog_dir / f"{post['slug']}.html").write_text(
                render_blog_detail_document(data, blog_page, post, "en"),
                encoding="utf-8",
            )
            (zh_blog_dir / f"{post['slug']}.html").write_text(
                render_blog_detail_document(data, blog_page, post, "zh"),
                encoding="utf-8",
            )

    (OUT_DIR / "index.html").write_text(
        '<!doctype html><html><head><meta http-equiv="refresh" content="0; url=/en/index.html"></head><body></body></html>',
        encoding="utf-8",
    )

    print(f"Generated {len(data['pages']) * 2 + len(load_blog_posts()) * 2 + 1} pages with branded assets in {OUT_DIR}")


if __name__ == "__main__":
    main()
