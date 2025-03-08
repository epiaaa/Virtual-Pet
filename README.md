# VirtualPet

## 目录

* [简介](#简介)
  * [写在最前](#写在最前)
  * [关于本仓库](#关于本仓库)
  * [关于版本号](#关于版本号)
* [环境依赖](#环境依赖)
* [目录结构描述](#目录结构描述)
* [更新日志](#更新日志)

## 简介
### 写在最前...
### 关于本仓库

一个简单的桌面宠物，仅自己用于娱乐

### 关于版本号
基本结构`Vx.y.z`，如`V0.1.0_beta20250304`

命名规则如下：
- **第一位：版本前缀(<span style="color:red;background-color:yellow">V</span>0.1.0.20250304_beta)**
V(version)英文版本的缩写
- **第二位：版本前缀(V<span style="color:red;background-color:yellow">0</span>.1.0.20250304_beta)**
功能发生较大变化，如增加模块或整体架构发生变化
- **第三位：版本前缀(V0.<span style="color:red;background-color:yellow">1</span>.0.20250304_beta)**
功能有一定的变化，如增加自定义视图等
- **第四位：版本前缀(V0.1.<span style="color:red;background-color:yellow">0</span>.20250304_beta)**
一般是Bug修复或小变动
- **第五位：版本前缀(V0.1.0.<span style="color:red;background-color:yellow">20250304</span>_beta)**
用于记录修改的日期
- **第六位：版本前缀(V0.1.0.20250304_<span style="color:red;background-color:yellow">beta</span>)**
分为**base、alpha、beta、RC、release**

## 环境依赖

语言：Python

## 目录结构描述

## 更新日志
<details>
<summary>点击展开</summary>

> V0.2.0.20250307_base
> - 目前功能与存在问题 
>  - 1. 挂机系统：每1分钟获得1经验
>  - 2. 可以使用文件喂养宠物 `Bug: 文件夹喂养会出现报错`
>  - 3. 可以读取上次关闭的地方，下次启动从此处启动 `Bug: 需要正常关闭，强制关闭无法保存数据`
>  - 4. <span style="color:red;background-color:yellow">鼠标悬停宠物可以显示状态条，离开时渐变消失</span> `Bug: 有时无法正常显示`
>  - 5. 目前可以显示gif宠物 `Sug: 使用的别人的图，需要自己再做一个`
> - 未来计划
>  - 1. 增加经验系统，学习系统，打工系统
>  - 2. 接入AI
>  - 3. 增加小游戏
>
>
> V0.2.0.20250306_base
> - <span style="color:red;background-color:yellow">更改代码模式，使用MVP（Model-View-Presenter）设置模式，将UI与数据分离。</span>
> - <span style="color:red;background-color:yellow">整理了部分学习科目、工作和娱乐项目，设定他们的需求、精力和消耗。</span>
> - 目前功能与存在问题
>  - 1. 可以使用文件喂养宠物 `Bug: 文件夹喂养会出现报错`
>  - 2. 退出记忆上次位置 `Bug: 需要正常关闭，强制关闭无法保存数据`
>  - 3. 挂机系统：每1分钟获得1经验 <span style="color:red;background-color:yellow">~~`Bug: 运行挂机系统会立马获得1经验`~~</span>
>  - 4. 可以显示状态条，`Sug: 可以改成消失的时候渐变`
>  - 5. 目前可以显示gif宠物 `Sug: 使用的别人的图，需要自己再做一个`
> - 未来计划
>  - 1. 增加经验系统，学习系统，打工系统
>  - 2. 接入AI
>  - 3. 增加小游戏
>
>
> V0.1.1.20250305_base
> - 目前功能与存在问题
>  - 1. 可以使用文件喂养宠物 `Bug: 文件夹喂养会出现报错`
>  - 2. 可以读取上次关闭的地方，下次启动从此处启动 `Bug: 需要正常关闭，强制关闭无法保存数据`
>  - 3. <span style="color:red;background-color:yellow">挂机系统：每1分钟获得1经验</span> `Bug: 运行挂机系统会立马获得1经验`
>  - 4. 可以显示状态条，`Sug: 可以改成消失的时候渐变`
>  - 5. 目前可以显示gif宠物 `Sug: 使用的别人的图，需要自己再做一个`
> - 未来计划
>  - 1. 增加经验系统，学习系统，打工系统
>  - 2. 接入AI
>  - 3. 增加小游戏
>
>
> V0.1.0.20250304_base
> - 目前功能与存在问题
>  - 1. 可以使用文件喂养宠物，`bug:文件夹喂养会出现报错`
>  - 2. 可以读取上次关闭的地方，下次启动从此处启动，`bug: 需要正常关闭，强制关闭无法保存数据`
>  - 3. 可以显示状态条，`sug: 可以改成消失的时候渐变`
>  - 4. 目前可以显示gif宠物，`sug: 使用的别人的图，需要自己再做一个`
> - 未来计划
>  - 1. 增加经验系统，学习系统，打工系统
>  - 2. 接入AI
>  - 3. 增加小游戏
>
>
