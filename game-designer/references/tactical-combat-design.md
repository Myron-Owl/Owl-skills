# 战棋设计专项

适用于战棋、回合制小队战术、SRPG / TRPG、网格或自由移动的战术战斗，以及桌面战棋启发的战斗设计。由原 `tactical-wargame-design` 合并而来，统一通过 `game-designer` 使用。

## 使用方式与范围

- 先明确战斗承诺：玩家反复享受哪一种战术决策？再确认移动形式、确定性 / 概率、单角色 / 小队、PvE / PvP、永久损失 / 消耗恢复，以及单场战斗 / 战役。
- 以位置、时机、风险、资源和目标进度之间的可读权衡评估规则；输出具体规则调整、反馈需求、单位职责、遭遇战示例或测试问题。
- 聚焦问题只读相关原则，不强制输出完整矩阵或三个遭遇战。完整设计和评审时再按下列检查项展开。
- 通用循环、机制规格、数值依据、待测试标记和测试记录沿用《游戏设计师实务》。CC战棋正式文档继续遵循主技能 5.7 节与现行项目规范，不把本参考建议直接视为项目已确定规则。

## 战斗评审检查项

通常先看信息与行动经济，再看局面变化；按本次问题选择检查项，不将次序作为所有设计的硬性流程。

| 检查项 | 要回答的问题 |
|---|---|
| 信息清晰度 | 在行动前能否判断威胁、地形、范围、行动顺序、目标和后果？信息隐藏是否有侦察与恢复手段？ |
| 行动经济 | 移动、攻击、技能、防御、等待、警戒、反应和道具是否有清楚的机会成本？ |
| 位置价值 | 地图几何是否改变正确行动，还是仅在平地交换数值？ |
| 目标压力 | 任务目标是否改变单位价值、行动优先级或路线，而不只是追加清敌步骤？ |
| 反制与恢复 | 出错后是否能通过防御、控制、牺牲或节奏恢复，而非只有读档？ |
| 单位职责 | 每种职责是否解决独特问题，同时保留弱点，避免每张图都必须携带？ |
| 随机性 | 不确定性是否有边界、可理解、可管理，并允许合理预案？ |
| 成长 | 成长是否增加战术动作、交互和约束，而非只提高数字？ |

## 交付与测试

完整评审通常交付：战斗承诺诊断、优先风险、具体规则或反馈调整、用于评估的遭遇战示例、试玩检查。新战斗系统交付：战斗承诺与循环、行动经济、单位职责矩阵、地形 / 目标词汇、随机性与信息政策，以及围绕关键假设的最小测试战斗。示例效果仍需试玩，不规定每次都产出相同数量的风险或地图。

战术不足时，先排查信息、行动经济、目标与地形，再考虑增加数值、技能或地图长度。隐藏关键威胁应服务已确定的迷雾、侦察或伏击玩法，并提供反制。任务目标应形成不同的决策压力，按游戏的战斗承诺选用，不要求每张地图更换胜利条件。

平衡评估除胜率外，关注决策多样性、回合压力、职责使用、重开原因、空转回合和支配策略；下列原则提供具体模型与测试问题。

## 保留的设计原则与资料来源

以下完整保留原参考的 12 项设计原则、模型、示例与出处。它们是设计讨论的综合笔记，不作为已核实的大师言论或项目定论；原出处链接未在本次合并中重新核查。按具体战斗承诺选择适用建议。

## 1. Start from the combat promise

Define the repeated pleasure before choosing mechanics:

- Chesslike certainty: players solve visible board states with deterministic rules.
- Command under uncertainty: players scout, hedge, and reserve actions because not all threats are known.
- Character-drama tactics: attachment, injury, and growth make each move emotionally costly.
- Puzzle tactics: each encounter is a compact rules problem with minimal randomness.
- Campaign attrition: victory quality matters because units, supplies, wounds, or territory persist.

Reject mechanics that do not serve the chosen promise.

## 2. Preserve game-state clarity

Players need enough information to make non-arbitrary decisions. Show or make easily inspectable:

- Movement ranges, attack ranges, line of sight, area of effect, facing, cover, elevation, hazards, and zone control.
- Turn order, initiative changes, reinforcement timing, enemy intent, status durations, and objective timers.
- Damage previews, hit modifiers, crit rules, push/pull paths, death/injury consequences, and expected counterattacks.

Fog of war and ambush can work, but only if the game provides scouting tools, tells, fallback plans, and costs for overextension.

## 3. Make action economy the spine

Action economy is the real currency of tactics. Decide what one turn means before tuning stats.

Common models:

- Move plus one main action: readable, good for SRPGs, can become solved if movement has no opportunity cost.
- Shared action points: flexible, supports tradeoffs, but UI must preview costs and leftover value clearly.
- Alternating activations: reduces alpha strike and creates tempo play.
- Team phase: simple and dramatic, but needs enemy pressure, reactions, or anti-focus-fire tools to avoid first-turn deletion.
- Reaction systems: add counterplay, but must be predictable enough that players can plan around them.

Ask: What does the player give up by attacking now? What does waiting, defending, repositioning, scouting, or supporting buy?

## 4. Design terrain as verbs, not decoration

Terrain should change what actions are correct. Useful terrain verbs include:

- Block, reveal, slow, funnel, split, elevate, expose, protect, push, burn, freeze, collapse, electrify, drown, conceal, and amplify.
- Chokepoints should help one side while creating flank, area damage, timer, or objective risks.
- High ground, cover, facing, and line of sight should produce distinct choices, not duplicate the same defense bonus.

A good map can be described as a tactical sentence: "Cross exposed bridges under artillery while deciding whether to split for side objectives."

## 5. Vary objectives to vary correct play

If every map is "kill all enemies," optimal play collapses toward damage, healing, and focus fire. Rotate objective pressure:

- Capture, hold, extract, escort, rescue, delay, survive, sabotage, intercept, protect civilians, split forces, retreat under pressure, defeat commander, or escape with loot.
- Put objectives in spatial tension: safe route vs fast route, treasure vs survival, boss damage vs crowd control.
- Give support, mobility, control, tanking, scouting, and terrain manipulation roles real objective value.

## 6. Bound randomness and make it strategic

Randomness should create risk management, not invalidate planning.

Prefer:

- Visible odds and modifiers.
- Damage bands instead of huge binary swings when failure is unrecoverable.
- Mitigation tools: aim setup, advantage, guaranteed chip damage, overwatch, guard, shields, retries with cost, or resource spending.
- Random inputs before commitment when possible; random outcomes after commitment need recovery options.

If a 75% hit chance misses and the player loses the mission immediately, the system probably lacks contingency design.

## 7. Build units around battlefield jobs

Define roles by problem solved, not class fantasy alone:

- Anchor: holds zones, soaks pressure, controls lanes.
- Striker: converts openings into kills or boss progress.
- Skirmisher: probes, flanks, escapes, pressures objectives.
- Controller: moves enemies, denies areas, changes turn order, applies statuses.
- Support: restores tempo, grants actions, shields, reveals, repairs, or enables combos.
- Specialist: solves rare map constraints such as armor, terrain, stealth, or machines.

A unit is healthy when it is sometimes best, sometimes wrong, and often useful with tradeoffs.

## 8. Control alpha strike and dominant strategies

Tactics collapse when the best answer is always focus-fire first, turtle forever, kite indefinitely, or restart after one bad roll.

Use counters:

- Alternating activation, initiative costs, armor gates, shields, morale, suppression, reinforcement timers, objectives, enemy reactions, positioning exposure, and overkill waste.
- Enemies that punish clustering, punish isolation, contest objectives, force movement, or change priorities.
- Reward clean play, but leave room for controlled recovery after mistakes.

## 9. Design enemies as pressure patterns

Enemies do not need full player-like complexity. They need readable pressure.

Give each enemy type:

- One threat shape: rush, pin, flank, artillery, guard, pull, explode, heal, mark, summon, or deny area.
- One counterplay cue: range, wind-up, line of sight, armor type, weak side, cooldown, morale, terrain vulnerability.
- One composition role: opener, finisher, screen, objective runner, disruptor, boss support, or timer.

Encounter depth usually comes from enemy combinations and map pressure, not from every enemy having many skills.

## 10. Progression should add verbs and constraints

Good progression expands tactical expression:

- New movement modes, reactions, formation effects, status interactions, terrain manipulation, scouting, command resources, and build-defining tradeoffs.
- Avoid pure stat inflation that makes old maps trivial and forces enemies into larger numbers.
- Preserve weakness. A promoted unit should gain new agency but still care about positioning, counters, resources, and mission objectives.

## 11. Prototype with battle questions

Create prototype encounters as questions:

- Can the player understand threat ranges and survive the first contact?
- Can mobility beat damage in an extraction map?
- Can control beat raw offense in a holdout?
- Can scouting prevent an ambush without making fog irrelevant?
- Can a wounded squad win by objective play instead of grinding every enemy?

Each test map should isolate one question. Do not tune the whole campaign from one mixed encounter.

## 12. Playtest metrics

Track:

- Turn count distribution, resets, deaths, damage taken, objective failures, unused skills, ignored classes, dominant openers, enemy types skipped by focus-fire, dead turns, UI misreads, and player explanations after losses.
- Ask players what they thought would happen before showing them what happened. Misprediction often indicates unclear UI or hidden rules.

## Source Synthesis

These notes synthesize public design discussions and articles, especially:

- Michael Burnam-Fink, "Pillars of Tactical RPG Design" (Medium): https://medium.com/mbf-data-science/pillars-of-tactical-rpg-design-a85f7393b271
- RPG.net forum thread, "Pillars of Tactical RPG Design": https://forum.rpg.net/index.php?threads/pillars-of-tactical-rpg-design.890517/
- Game Developer, "Building an RPG Battle System - Part 1": https://www.gamedeveloper.com/design/building-an-rpg-battle-system---part-1
- Campaign Mastery, "Combat System Design and Understanding The Rules": https://www.campaignmastery.com/blog/combat-system-design/
- Game Industry Conference talk, "Understanding modern turn based tactical design": https://www.youtube.com/watch?v=HcBU8iyu4U0
- Tales from Elsewhere, "Designing Tactical RPGs | Design Discussions": https://www.youtube.com/watch?v=vq8g8AI-AEg
