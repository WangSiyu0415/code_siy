# code_siy

Sentaurus TCAD 器件仿真代码仓库。

## 项目说明

基于 Sentaurus V-2023.12 的 GaN 功率器件仿真，包括结构建模（SDE）、
电学特性仿真（sdevice）和数据分析。

## 文件结构

```
├── scripts/           # 数据分析/处理脚本
│   ├── parse_*.py     # 数据解析
│   ├── plot_*.py      # 绘图
│   └── compare_*.py   # 数据对比
│
├── sde/               # SDE 结构生成脚本
├── sdevice/           # sdevice 仿真脚本
├── figures/           # 仿真结果图
└── README.md          # 本文件
```

## 仿真内容

- [ ] p-GaN HEMT 结构建模
- [ ] 输出特性 (Id-Vd)
- [ ] 转移特性 (Id-Vg)
- [ ] 击穿特性 (BV)
- [ ] 热击穿分析

## 使用环境

- 远程服务器：`58.199.136.91`
- 用户：`klren`
- 工作路径：`/home/klren/Sentaurus/STDB/wangsiyu/sentaurus-work/`

## 本地目录结构

```
D:\a_experiment\sentauruse\sentaurus_data\
├── projects/          # 仿真项目
├── scripts/           # 脚本（与仓库同步）
├── figures/           # 生成的图片
└── ...
```

## 更新日志

- 2026-07-15：初始化仓库，添加数据分析脚本
