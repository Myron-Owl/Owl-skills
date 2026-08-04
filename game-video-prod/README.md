# game-video-prod

**游戏评测视频全流程生产**（李三两Owl 视频号）

脚本 → 标题 → 封面方案 → HyperFrames 合成 → 成片 MP4。兼容 **Claude Code 与 Codex**（`agents/openai.yaml` 提供 Codex 元数据，安装脚本自动同步到 `~/.codex/skills/`）。

## 用途
- 输入：`video-projects/<游戏名>/raw/` 下的游戏录屏 + 用户口述观点/笔记
- 产出：成片 MP4（1080P，16:9 或 9:16）+ 脚本 + 标题 3 备选 + 封面方案

## 能力范围
- 深度评测脚本（8-12 分钟结构、策划视角）
- 标题 3 备选（5 种公式）
- 封面方案（元素决策：游戏画面✅/游戏名✅/美女限定使用）
- HyperFrames 合成与渲染

## 配套
- 选题：Hermes 的 `game-videos` 技能 + steam-game-sourcing cron（每周四推送候选）
- 本技能专注：拿到选题和素材后的**创作 + 生产**

## 安装
```bash
bash install.sh   # 安装到 ~/.claude/skills/ 和 ~/.codex/skills/
```

## 依赖
Node.js 18+、FFmpeg、HyperFrames（`npx hyperframes`）
