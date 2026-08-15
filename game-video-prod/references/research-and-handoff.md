# 多源预研与剪辑交接

## 目录

1. 来源分工
2. 玩法建模
3. 证据矩阵
4. 预研稿与录制清单
5. 配音驱动剪辑
6. Premiere 交接

## 来源分工

不同来源回答不同问题，不把信息数量当成可信度。

| 来源 | 主要用途 | 不能单独证明 |
|---|---|---|
| 自己的完整实机 | 操作感、节奏、门槛、重复性、性能、购买建议 | 未体验到的后期或分支 |
| 第三方实机视频 | 发现动作、界面、系统、阶段和待验证问题 | 操作手感、真实节奏、长期体验 |
| 官方页面/开发日志 | 规则、定位、平台、版本、商业信息 | 是否好玩、是否重复、实际完成度 |
| 补丁说明 | 当前机制和版本变化 | 改动后的实际体验质量 |
| 评测/玩家评价 | 常见痛点、分歧、长期反馈线索 | 对当前用户必然成立的结论 |

来源优先级不固定。事实规则优先官方和游戏内说明；体验判断优先一手实机；长期问题可由多位玩家反馈提出，再由实机尽量验证。

## 玩法建模

先回答以下问题，再写一句玩法总结：

1. 玩家扮演谁，追求什么可见目标？
2. 每 30 秒到 2 分钟反复执行哪些“动词 + 对象”？
3. 动作消耗什么资源，产生什么结果和反馈？
4. 结果怎样回流到下一轮行动？
5. 成长、失败、压力和关键选择从哪里出现？
6. 它与同类的差异是规则差异、内容差异，还是表现差异？

玩法骨架格式：

`身份/目标 → 核心动作链 → 资源与反馈 → 成长/失败 → 差异机制`

视频只显示结果而未显示原因时，原因必须标为假设。剪辑视频跳过等待、失败和重复操作时，不据此判断真实游戏节奏。

## 证据矩阵

`research/evidence_matrix.csv` 使用以下字段：

```csv
claim_id,claim,type,source_level,source_id,version,observed_fact,interpretation,conflict,confidence,needs_playtest,raw_clip,status
C01,核心循环是采集-建造-防守,gameplay,C,VID01|OFF01,1.2,视频出现三段连续操作,这些操作构成主要循环,,medium,yes,,provisional
```

要求：

- `observed_fact` 只写看见或读到的事实，`interpretation` 单独写解释。
- 一个结论可关联多个来源；来源之间必须尽量独立。
- `confidence` 使用 `high/medium/low`，但最终评测的核心体验判断必须有 `A-一手确认`。
- `status` 使用 `provisional/confirmed/rejected/conflicted`。
- 来源发生版本冲突时填写 `conflict`，不要静默覆盖旧信息。

`research/source_inventory.md` 至少记录：来源 ID、标题、作者/发布方、URL/本地路径、发布日期、访问日期、游戏版本、来源类型、用途和授权备注。

## 预研稿与录制清单

预研稿中每个段落使用：

```markdown
### 论点 C01：基地扩张会主动放大防守压力

- 文稿：从目前公开实机看，每次扩张似乎都会扩大需要防守的区域。
- 证据：VID01 03:12；DEV02“威胁范围”说明
- 等级/置信度：C / medium
- 待验证：不扩张是否也会随时间提高压力？
- 预期画面：扩张前后防区范围与敌人路径对比
```

`edit/first_capture_shotlist.csv` 字段：

```csv
shot_id,claim_id,question,setup,action,expected_result,counterexample,priority,captured,clip_path,notes
S01,C01,扩张是否提高防守压力,保持难度与时间相近,扩大可建区域,敌人路径或威胁范围变化,不扩张时压力同样增长,P0,no,,
```

优先级：`P0` 决定核心结论，`P1` 支撑正文，`P2` 用于补画面。先录反例与失败条件，再录漂亮结果，降低确认偏误。

## 配音驱动剪辑

最终稿锁定后录正式配音。保留无降噪原始录音和处理后的交付音轨；项目统一使用 48 kHz WAV。转写后生成：

- `script/timed_script.md`：段落级时间码、口播、论点 ID、情绪/停顿提示。
- `script/voiceover.srt`：字幕与基础时间轴。
- 可选词级 JSON：需要逐词字幕或精确动画时使用。
- `edit/capture_shotlist.csv`：按声音时间线组织最终镜头。

当用户提供确定版本的配音、但明确要在 Premiere 等软件中后期手动合并时：

- 配音仅作为锁定时间轴和口播内容的参考，不进入自动剪辑成片，也不再次生成旁白。
- 每个实机镜头必须同步保留原素材对应区间的游戏音频；禁止只裁画面、不裁原声。
- HyperFrames 中视频仍使用 `muted playsinline`，素材原声作为独立 `<audio>` 轨按同一源入点与时长挂载；也可在画面渲染后无损封装原声轨。
- “不要合并音频/字幕”若语境指用户后期合并配音，应解释为“不嵌入旁白、不烧录字幕”，不能自行扩大为“删除所有音频”。有歧义时优先保留素材原声，并在交付说明中写清音轨内容。
- 交付验证必须读取媒体流：应有视频流和素材原声音频流，不应有旁白轨；至少抽查三个时间点确认不是整轨静音。

最终录制清单字段：

```csv
shot_id,vo_in,vo_out,narration,claim_id,visual_requirement,evidence_target,priority,min_duration,status,clip_path,clip_in,clip_out,notes
V001,00:00:00.000,00:00:02.400,你每扩一块地...,C01,扩张前后同屏对比,显示防区扩大与威胁变化,P0,2.4,needed,,,,
```

前 20 秒一句一个镜头目标。正文允许一个完整因果镜头覆盖多句，但必须看清操作、反馈和结果。泛用风景不能替代机制证据。

## Premiere 交接

优先交付兼容媒介，不把 `.prproj` 作为默认自动生成目标。建议目录：

```text
handoff/
  01_video/
  02_voiceover/
  03_music_sfx/
  04_graphics/
  05_captions/
  edit_decision_list.csv
  assets_manifest.csv
  timeline.fcpxml
  rough_cut.mp4
```

统一要求：

- 序列帧率与自录主素材一致，默认分辨率 1920x1080；不要混用 29.97 与 30 fps。
- 音频统一 48 kHz；交接前检查峰值、静音和声画同步。
- 文件锁定后不改名；`assets_manifest.csv` 记录资产 ID、相对路径、类型、时长、帧率/采样率、来源和授权。
- `edit_decision_list.csv` 记录轨道、时间线入出点、素材路径、源入出点、用途和论点 ID。
- XML/FCPXML 必须在 Premiere 中实际导入验证；未经验证时只交付 EDL CSV、素材清单和参考粗剪，并明确需要人工建序列。
- HyperFrames 动画若无法转换为可编辑图层，导出带透明通道或独立成片作为上层素材，同时保留 HTML/CSS 源文件。
