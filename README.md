# code_siy

Sentaurus TCAD 器件仿真代码仓库。

## 项目说明

基于 Sentaurus V-2023.12 的 GaN 功率器件仿真，包括结构建模（SDE）、
电学特性仿真（sdevice）和数据分析。

## 文件结构

```
├── sde/              # SDE 结构生成脚本
├── sdevice/          # sdevice 仿真脚本
├── results/          # 仿真结果
└── README.md         # 本文件
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

## 更新日志

- 2026-07-15：初始化仓库
