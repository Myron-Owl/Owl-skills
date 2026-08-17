---
name: godot-shader
description: Godot 4.x shader 中文手册（gdbook「肖老师的Godot实验室」22章）。写/改 Godot shader、查 2D/3D 特效配方、确认内置变量与 render_mode 时使用。
metadata:
  created: 2026-08-17
  updated: 2026-08-17
  version: "1.0"
---

# Godot Shader 手册

来源：<https://gdbook.kidsgame.top/shader-book/>（肖老师的Godot实验室，中文，Godot 4.X）
22 章，从 GPU 基础讲到 3D 水体/描边。面向「会搭场景但怕 shader 代码」的开发者。

## When to Use

- 写新 shader 或改现有 shader（2D 或 3D）
- 查特效配方：描边、水体、溶解、后处理、顶点动画、卡通光照、故障艺术……
- 确认内置变量 / render_mode / 坐标空间 / 数据通道用法

## 快速索引（按需求定位章节）

| 需求 | 章节 | 参考文件 |
|------|------|----------|
| shader 骨架/内置变量/数据通道 | ch04 | `references/ch04.md` |
| 周期动画/呼吸发光/波形 | ch05 | `references/ch05.md` |
| 遮罩/平滑过渡/扩散圆环 | ch06 | `references/ch06.md` |
| 噪声（值噪声/Perlin/FBM/草地变色） | ch07 | `references/ch07.md` |
| 距离场 SDF（圆/环/矩形/雷达 HUD） | ch08 | `references/ch08.md` |
| 纹理采样/UV 变换/Parallax 星空 | ch09 | `references/ch09.md` |
| 屏幕空间（模糊/热浪/放大镜） | ch10 | `references/ch10.md` |
| 预处理器/include/工程化 | ch11 | `references/ch11.md` |
| 2D 顶点动画（旗帜/草丛/果冻） | ch12 | `references/ch12.md` |
| 颜色处理 HSV（闪白/中毒/彩虹/调色板） | ch13 | `references/ch13.md` |
| 遮罩驱动特效（溶解/隐身斗篷/扫描线） | ch14 | `references/ch14.md` |
| 2D 描边与轮廓 | ch15 | `references/ch15.md` |
| 复古后处理（像素化/色差/CRT/VHS/Glitch） | ch16 | `references/ch16.md` |
| 2D 水体/云层 | ch17 | `references/ch17.md` |
| 3D 顶点动画（地形/冲击波/植被/Billboard） | ch18 | `references/ch18.md` |
| PBR 材质属性（ALBEDO/ROUGHNESS/METALLIC…） | ch19 | `references/ch19.md` |
| 自定义光照 light()（Lambert/Blinn-Phong/Fresnel/Toon） | ch20 | `references/ch20.md` |
| 3D 水体（低成本/Toon/写实 Gerstner） | ch21 | `references/ch21.md` |
| 3D 描边（倒壳/Stencil/屏幕空间） | ch22 | `references/ch22.md` |
| 图形学数学（向量/矩阵/点积/叉积） | ch02 | `references/ch02.md` |
| 坐标空间（Model→World→View→Clip→NDC→Screen） | ch03 | `references/ch03.md` |
| GPU 基础概念（为什么 shader 这样设计） | ch01 | `references/ch01.md` |

## 速查：shader 骨架

```gdshader
shader_type canvas_item;   // canvas_item=2D / spatial=3D / particles / sky / fog
render_mode ...;           // 渲染规则（可选）
uniform ...;               // CPU→GPU 参数通道
void vertex()   { ... }    // 顶点处理器：改 VERTEX（2D 是 vec2，3D 是 vec3）
void fragment() { ... }    // 像素处理器：2D 写 COLOR(vec4)，3D 写 ALBEDO(vec3) 等
void light()    { ... }    // 光照处理器：每像素×每光源执行
```

**数据通道**：`uniform`（GDScript→GPU，`material.set_shader_parameter("name", value)`）；`varying`（vertex→fragment 自动插值）。内置变量直接用：`COLOR`、`VERTEX`、`UV`、`TEXTURE`、`TIME`、`NORMAL`（2D 系）；`ALBEDO`、`ROUGHNESS`、`METALLIC`、`EMISSION`、`NORMAL_MAP`（3D 系）。

## 速查：2D vs 3D 对照

|  | canvas_item | spatial |
|---|---|---|
| 身份声明 | `shader_type canvas_item;` | `shader_type spatial;` |
| 主要输出 | `COLOR` (vec4) | `ALBEDO` (vec3) + ROUGHNESS/METALLIC/EMISSION/AO |
| VERTEX | vec2 | vec3 |
| 矩阵 | MODEL / CANVAS / SCREEN | MODEL / VIEW / PROJECTION 全系列 |
| 光照 | 2D light() 或 unshaded | PBR 或自定义 light() 或 unshaded |

## 速查：核心公式与函数

- **周期动画**：`sin(TIME * ω) * A + B`（ω=频率、A=振幅、B=偏置；抬到 [0,1] 用 `*0.5+0.5`）
- **有机波动**：多频叠加 `sin(t*f1)*a1 + sin(t*f2)*a2 + sin(t*f3)*a3`，f 用非整数倍、振幅递减（0.6/0.3/0.1），最后归一化
- **线性循环**：`fract(TIME * speed)`（匀速、瞬间复位）；`mod(UV.x, size)` 做空间重复
- **塑形**：`step(edge,x)` 硬边界 / `smoothstep(a,b,x)` 平滑过渡 / `mix(a,b,t)` 插值 / `clamp(x,lo,hi)` 限幅
- **距离场**：`distance(UV, center)` 当尺子；`min`=并集、`max(-a,b)`=差集、`max`=交集
- **噪声**：hash → 值噪声 → Perlin；快速路径用 `NoiseTexture2D` 传 `uniform sampler2D`；FBM=多层噪声叠加
- **屏幕后处理**：`uniform sampler2D screen_texture : hint_screen_texture;` + `SCREEN_UV`/`FRAGCOORD`/`SCREEN_PIXEL_SIZE`；多效果用 `BackBufferCopy` 串联
- **颜色**：rgb2hsv/hsv2rgb 放 `.gdshaderinc`；受伤闪白=提 V 降 S；中毒=h+0.3；彩虹=fract(TIME*speed) 滚 Hue
- **遮罩通用公式**：`noise → smoothstep(amount, amount+edge, noise) → mask`，再分支控制 alpha（溶解）/纹理（斗篷）/颜色（扫描线）

## 速查：常用 render_mode

- 2D：`blend_mix`(默认) / `blend_add`(发光) / `blend_sub` / `blend_mul` / `blend_premul_alpha`(粒子) / `unshaded`
- 3D：`cull_back`(默认) / `cull_disabled`(叶片布料) / `unshaded` / `shadows_disabled`

## 常见坑

- `COLOR.a=0.5` 但 rgb 没预乘 → 半透明粒子边缘暗晕，用 `blend_premul_alpha` 并手动 `rgb *= alpha`
- `blend_add` 叠加在亮白背景上会"消失"（被 clamp 到白）
- canvas_item 里写 `ALBEDO` 编译报错——那是 spatial 专属变量
- `TIME` 无法暂停/倒放/按事件触发 → 需要玩家控制时用 GDScript uniform 驱动
- sin 负值直接进颜色会被钳黑 → 先 `*A+B` 抬到正值区
- 3D 水体用 `SCREEN_TEXTURE`/`DEPTH_TEXTURE` 需要 Forward+ 或 Mobile 渲染器

## 文件组织

- `references/ch01.md` ~ `references/ch22.md`：各章完整内容（概念讲解 + 全部代码 + 练习）
- 需要某类效果：先按上表定位章节 → 读取 `references/chXX.md`
- 代码基于 Godot 4.X，部分调试功能（shader 逐行变量预览）需 4.7+
