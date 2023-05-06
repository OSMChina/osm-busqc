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
   `pip install -r osm_busqc/requirements.txt`

## 设置

1. 设置 OSM 访问凭据. 复制 `password.sample` 为 `password`, 填入 OSM 的账号密码, 以冒号(:)分隔.
2. 检查和改写 `network_query`, 这是一个 Overpass 检索, 以得到需要检查的主线列表.  
   请参照 [Overpass QL references](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL) 改写和[试验](https://overpass-api.de/query_form.html).  
   随附的样例表示查询具有 `network:wikidata=Q111736572` 的公交主线, 即肇庆公交网络.
3. 检查和改写 `masters.lints.py`, 参考 [man/masters.lints.py](./man/masters.lints.py.md).  

## 运行

`python3 -m osm_busqc`  
`python3 -m osm_busqc [OPTIONS]`  

### 命令行参数:
* `--cache_exp CACHE_EXP`
  ISO 时间字符串, 缓存过期时间, 早于此时间的主线/路线/站点缓存被认为过期, 并从 OSM 下载对象.  
  例如, 可以 `--cache_exp \`date -d "-1 day" -Is\`` 指定过期时间为昨天.
  参考 [man date(1)](https://man7.org/linux/man-pages/man1/date.1.html)
* `--lint_file LINT_FILE`
  覆写默认的检查文件路径 `./masters.lints.py`
* `--masters_list_file MASTERS_LIST_FILE`
  使用存储的主线列表, 而非以 Overpass 查询.  
  指定的路径应当是一个文本文件, 每行包括一个主线的 `id`, 不能有空行和注释.  

所有操作是只读的, 不会向 OSM 提交修改.

## 多工作区

所有的输入/缓存都位于当前工作目录, 这意味着你可以通过 cd 切换工作环境.
以后会增加 `setup.py`


