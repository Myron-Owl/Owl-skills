# 四款参考游戏：借鉴方法与边界

本页判断来自本机安装资源的实际对齐与抽样，采集日期 2026-10-22。它不是四款译文的整体质量排名，也不宣称逐句人工审核了全部语料。中文文本的发布来源以本地语言通道为准；未经额外验证，不推断翻译团队、官方认证或翻译工具。

检索时以 game + variant + key 识别一条记录。完整路径与 SHA-256 在私人 corpus 的 manifest 中。

## Divinity: Original Sin 2 — Definitive Edition / 神界：原罪2 终极版

本机 build 9530355，仅取 DefEd 的英文包与简体中文包，不混入 Classic。
按 contentuid 和性别语境对齐，已配对 92,275 条；英文侧未配对 52 条，中文侧未配对 2 条。只代表所选语言包的覆盖，不代表游戏一切嵌入图片、额外 Mod 或外部文本。

可借鉴：复杂属性、战斗状态及奇幻命名保持概念差异。例如 Physical Armour→物理护甲、Magic Armour→魔法护甲、Action Points→行动点数。对应键：
- `base:h161d5479g06d6g408egade2g37a203e3361f`
- `base:h50eb8e33g82edg412eg9886gec19ca591254`
- `base:h4ef9c467g3c7bg4614g96d0g801b09fcc05c`

不能机械迁移：Source→秘源（`base:h2134d800gfd8eg47d2gb4f7g2cf74f79fc30`）是世界观专名；一般 source 仍可能是来源、源头。Huntsman 同时有“神射技艺”和“猎人”两种实录（`base:h3d3dc89dgd286g418eg8134g2eb65d063514`、`base:h5b7d911eg4de2g4853gbcbcgaec1a107b3c7`），必须先看学派还是身份。Warfare 的“战场技艺”与书名《战争》也不能按原词去重。

本次建议：参考它对机制差异的表达；装备名以目标项目的细分需求为准。例如原译 Mace→锤子不应成为把 mace 与 hammer 合并的理由。

## Wartales / 战争传说

本机 build 25365426；四份语言文件的资源 revision 均为 47880。19,614 条按表名/记录/字段或文本组 ID 精确对齐，双方未配对数为 0。文件内含未必在当前游玩内容中出现的条目，不据此宣布 DLC 已发布或玩家可见。

可借鉴：雇佣兵团、旅行营地、职业、伤病与回合战斗的简短表达。
- Valour points→勇气点数：`export/icon/ActionPoint/text`
- Bleeding→流血：`export/status/Bleeding/name`
- Engaged→交战：`export/status/Engaged/name`
- Blacksmith→铁匠：`export/trait/Blacksmith/name`
- Rations→给养：`export/item/E2Supply/name`

关键反例：
- Guard→防御（`export/attribute/Guard/name`）与 Guard→守卫（`export/groupType/TheGuard/props.tavern.name`）。这是语义差异，不能统一成一个词。
- Pike→梭子鱼（`export/item/Pike/name`）是该游戏实录；其食物语境不能套用武器“长枪”。本页不把这一鱼类中文名称当成自然分类学核验。
- Captain→上尉、Lieutenant→中尉是本作惯例；其他中世纪项目可能应使用队长/副官。
- Gambeson→软铠甲（`export/item/MediumArmorCommonGeneric/name`）可理解，但装备细分项目宜考虑“绗缝甲”并核对美术结构。
- Tavern 在普通地点是“酒馆”，DLC 标题条目是“酒馆开业！”。营销标题不能拿来做一般词典。

## Heads Will Roll: Reforged

本机 build 25676788。普通中文配对 42,742 条，社区中文配对 40,676 条；3 个普通中文块的对白结构不一致、2 个缺英文块及空值被排除，详见 manifest。源脚本含俄语；英文与两套中文分别是翻译通道。中英对照不证明中文经由英文翻译，不能据此推断翻译链或作者。

`chinese` 与 `chinese_community` 必须分开保存，不自动混用。教程块 `windsor_siege_tutorial_ca4ad8ac` 的普通中文使用“送人头”，社区版使用“极难攻陷”；同组 `windsor_siege_tutorial_0e6f1d3e` 的普通中文有“再来一波”，社区版更偏军事叙述。这是已抽样的语域差异，不等于全篇优劣结论。

可借鉴：同一士兵/围城场景的两套处理，可用于选择军中口语强度；社区版更适合作为这些具体教程的沉稳表达参考。技能默认保留直白语气，不主动加入当代网游俚语。英文教程本身也可能较繁复，不能把“像参考”误解为复制句法。

另一个实际一致性问题：同一 Gambeson 在普通中文的无格式条目译“夹棉甲”，首字装饰条目却译“护臂甲”；社区版两条均为“武装衣”。对应 string 键分别为 d801a93ce727d364d43d114943e1e719a6692fea25a9b9f7f47153e5c65d1f9f 与 9aa3608869c26dc0224c9e6a446e2ecf354ba186f56b91eaa062471d9aea5185。应同时检查菜单短名与装饰标题，不从单条命中推断全作一致。

准确配对方式：translate block ID 与原始 old 字符串；行号只是定位资料。遇到英文或中文缺项、重复冲突必须保留记录，不按临近句猜配。

## Stoneshard / 紫色晶石

本机 build 24780451。已从编译程序内的 28 个语言表头对应的多语言行中提取 16,398 对，按完整中英文本去重为 15,005 对。原始 ID 加字节偏移组成版本内唯一键；偏移不是跨版本稳定 ID。范围不含运行时拼句、图片文字或压缩文本，非汉字目标列另存。

参考时保持损伤、疼痛、出血、疲劳等不同概念，不把生存状态都压成泛化的“虚弱”。名称需要和实际物件形制、属性说明互相验证；这是本次翻译使用原则，不能把原则写成某游戏逐句采用的事实。


可核对的借鉴实例：
- Gambeson→夹棉软铠（`table_equipment/Gambeson@06615320`）、Mail Coif→链甲头套（`table_equipment/Mail Coif@06610080`）：通过器物结构形成可辨识名称。
- Bleeding→出血（`table_effects/o_db_bleed@06406300`）与其他两作的“流血”都是来源实录，不能跨项目混用两套状态名。
- Pain Shock→疼痛休克（`table_effects/o_db_pain3@06407ba0`）：与疼痛、剧痛分级，保留机制差别。
- 同一租房功能，Jorgrim 的 "I need a bunk."→“还有床没有？”（`table_lines/custom_rent_room@06774400`）；Arna 的 "I'd like to stay for the night."→“我想在这儿过夜。”（`table_lines/custom_rent_room@06774700`）；Mahir 的 "Is there a bed for a weary traveler?"→“旅途劳累，可有床位歇息？”（`table_lines/custom_rent_room@06775ba0`）。此处省略相同的存档提示，演示的是角色语气差异。

原译也有可查问题：`table_skills/Constrict@060073a0` 的中文将 `/*Crushing_Damage*/` 换成 `/*Piercing_Damage*/`。因此用它学习结构和口吻，同时独立检查变量。本作 Stun→硬直、Daze→眩晕的命名也不能直接套到另一套状态机制。

## 资料级别

1. 目标项目已确认的词表与世界观。
2. 同版本、稳定 ID/同表语言列对齐的游戏实录。
3. 清楚标识来源和版本的社区译文。
4. 编者给目标项目的建议译法。

第 2/3 级供比较，不自动压过目标项目。自动抽取的短条目属于候选词表，只有经过语境确认后才能成为批准词条。
