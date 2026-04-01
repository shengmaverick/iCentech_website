# iCentech Color System

这份文件把新版网站的颜色正式定稿下来，后续页面、插画、博客封面和框架重建都以这里为准。

## Core Brand Colors

### Brand Blue 700
- Hex: `#0C79D6`
- Role: primary actions, headline emphasis, key gradients
- 用法：主按钮、主视觉强调、核心标题重点

### Brand Blue 500
- Hex: `#0596EF`
- Role: secondary blue highlight, active states, glow accents
- 用法：次级亮蓝、激活状态、发光层和辅助强调

### Brand Blue 300
- Hex: `#8FD0FF`
- Role: light outline, breadcrumb links, soft emphasis
- 用法：浅描边、路径导航链接、轻强调

### Brand Green 600
- Hex: `#63A60B`
- Role: accent emphasis, category labels, success cues
- 用法：强调色、栏目标签、正向提示

### Brand Green 500
- Hex: `#78C515`
- Role: supporting glow, pills, secondary highlight
- 用法：标签、辅助渐变、次级强调

### Brand Green 200
- Hex: `#DFF3B8`
- Role: soft green wash, low-pressure backgrounds
- 用法：浅绿背景层、弱提示区块

## Editorial Dark Base

### Background 950
- Hex: `#061119`
- Role: global page background

### Background 900
- Hex: `#0A1824`
- Role: main layout base

### Background 860
- Hex: `#102334`
- Role: raised surfaces

### Background 820
- Hex: `#13293D`
- Role: cards, content panels, dropdowns

## Text And UI Support

### Ink
- Hex: `#EFF8FF`
- Role: primary text on dark surfaces

### Ink Soft
- Hex: `#A8C3D8`
- Role: secondary copy, paragraph text, metadata

### Line
- Hex: `rgba(143, 208, 255, 0.16)`
- Role: default borders and separators

### Line Strong
- Hex: `rgba(143, 208, 255, 0.26)`
- Role: hover borders, stronger panel outlines

### Surface
- Hex: `rgba(14, 28, 41, 0.90)`
- Role: main card and panel background

### Surface Alt
- Hex: `rgba(18, 39, 57, 0.80)`
- Role: image blocks and alternative panels

## Usage Rules

- Blue remains the main action color. Green is an accent, not the main field color.
- Large surfaces should use the deep editorial navy base instead of flat white.
- Use green mainly on labels, supporting glow, and “go forward” cues.
- Use bright blue for links, buttons, active borders, and important interface states.
- Keep copy on dark surfaces in `Ink` or `Ink Soft`; do not switch back to low-contrast gray.
- Gradients should be directional and restrained: hero panels, CTA buttons, and illustration accents.

## Recommended Combinations

- Primary CTA: `Brand Blue 700 -> Brand Blue 500`
- Accent glow: `Brand Green 500` with transparent fade
- Dark panel: `Background 860` + `Surface`
- Link on dark: `Brand Blue 300`
- Kicker / label: `Brand Green 500` or `Brand Green 600`

## Theme Modes

- Dark mode: the current editorial version, used as the default experience
- Light mode: a white-base version for visitors who prefer a brighter interface
- Both themes use the same brand blue and green accents
- The theme switch should stay visible in the header across home, service, and blog pages

## Do Not

- 不要大面积把绿色当主背景。
- 不要在同一个区块里同时堆太多蓝绿渐变。
- 不要用纯黑替代深蓝底色。
- 不要回到旧站那种发灰、层级不明确的浅色布局。

## Implementation Files

- Tokens: `design-system/tokens.css`
- Generator source: `tools/generate_static_site.py`
- Generated site CSS: `static-site/assets/site.css`
