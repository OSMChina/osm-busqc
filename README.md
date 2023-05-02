# 简易的公交网络检查脚本

featuring:
* 打印全部线路
* 检查线路主线/具体线路缺失
* 检查线名/站名缺失
* 检查首末站

An out-of-box scripts to check local bus network integrity.
* print all routes and stops
* check missing master routes/routes
* check missing names
* check inconsistent terminals name by comparing route[from]/[to] with platform[name]

# Samples

首末站不正:

    主线 2
    2 路: 火车站综合体 -> 塔东路东堤湾
    火车站综合体 波海公园 西江北路中 体育中心西门 体育中心南门 康乐北路 康乐市场 康乐中路 披云楼 北门 豪居路 中心市场 大柑园 工农北路南 友谊路口 和平路中 城东公园北门 前进中路 市公安局 前进南路 塔东路东堤湾 和平路西 华佗医院
    wrong on route 13853854
    AssertionError: inconsistent terminal
    2 路: 塔东路东堤湾 -> 火车站综合体
    塔东路东堤湾 前进南路 市公安局 前进中路 城东公园北门 和平路中 端州公安分局 端州四路东 工农北路 友谊路口 工农北路南 大柑园 中心市场 豪居路 北门 披云楼 康乐中路 康乐市场 康乐北路 体育中心南门 体育中心西门 西江北路中 蕉园 波海公园 火车站综合体

线路缺失:

    主线 5B
    5B 路: 火车站综合体 -> 岭塘村
    火车站综合体 大桥路北 华英名都 惠民居 玑东路南 大鼎路中 一中实验学校 太和南路 端州七路中 睦岗 八中 棠下 肇庆大道西 三榕港 三榕水厂 黄禁 大龙桥 小湘军校 新屋村
    wrong on route 14464670
    AssertionError: inconsistent terminal
    wrong on master 15749944
    AssertionError: inconsistent route count

主线缺失:

    wrong on master 35
    AssertionError: missing master 35
    wrong on master 36
    AssertionError: missing master 36
    wrong on master K01
    AssertionError: missing master K01

# 用法

## 安装

1. 取得程序(clone/download)
2. 安装依赖
   `pip install -r osm_busqc/requirements.`

## 设置

1. 设置 OSM 访问凭据. 复制 `password.sample` 为 `password`, 填入 OSM 的账号密码, 以冒号(:)分隔.
2. 检查和改写 `network_query`, 这是一个 Overpass 检索, 以得到需要检查的主线列表.
   请参照 [Overpass references](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL) 改写和[试验](https://overpass-api.de/query_form.html).
   随附的样例表示查询具有 `network:wikidata=Q111736572` 的公交主线, 即肇庆公交网络.
3. 检查和改写 `masters.lints.py`, 具体参照后文.

## 运行

`python3 -m osm_busqc`
所有操作是只读的, 不会向 OSM 提交修改.

## 多工作区

所有的输入/缓存都位于当前工作目录, 这意味着你可以通过 cd 切换工作环境.
以后会增加 `setup.py`

# masters.lints.py

内容是一个合法的 python dict. 目前没有明确的 schema, 也没有计划规定 schema. 本项目想要专注于为绘图员提供一个趁手的工具, 不希望太复杂. 如果你是 power user, 可以自行编写自己需要的功能.

以下是例子:

```python
{}
```
不规定检查内容. 程序会列出所有的路线/站点, 检查一些基本的问题(如首末站不匹配).


```python
{
  "1": {"route_count":2},
  "2": {"route_count":2},
}
```
检查应有 `1`, `2` 号主线, 各包括两条线路.
