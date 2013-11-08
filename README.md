## 比特币交易预警与止损项目（btc-proj） ##
_小拿_

_<Justinli.LJT@gmail.com>_

_2013-11-08_

### 目的 ###

随着四月份国际__比特币(BTC)__价格的持续攀升，国内涌现了大量比特币交易市场，本项目正是基于[比特币中国](https://vip.btcchina.com "BTC China")提供的接口所开发的。

比特币的市场前景不明朗，仍旧具有很大的不确定性，比特币价格攀升是价值的回归，还是又一个庞氏骗局，谁也说不清楚。正如[比特币中国](https://vip.btcchina.com "BTC China")的风险提示：

    风险提示：比特币的交易有极高的风险，它没有像中国股市那样的涨跌停限制，同时交易是24小时开放的。比特币由于筹码较少，价格易受到庄家控制，有可能出现一天价格涨几倍的情况，同时也可能出现一天内价格跌去一半的情况！入市须谨慎，一定注意控制好风险！

尽管存在如此高的风险，鉴于其价格攀升的迅猛，还是吸引了大批的投资/投机分子（我也是其中之一，哈哈）。为了能够有效地控制投资风险，确保收益最大化，开发了此项目。

### 功能 ###

* 实时交易价格的查询与存储（SQLite）
* 价格监控预警：当满足某一止损策略时，系统自动发送短信进行预警提示
* 自动止损卖空：当满足某一止损策略时，系统自动以略低于当前价格卖空所有比特币
* 止损策略
    * 均值策略
    * 首次低于某阀值策略（未开发）
* 最大化收益策略（未开发）

### 目录及文件 ###

*  __config.py__: 配置文件
*  __api_sqlite3.py__: 数据库接口文件
*  __api_sms.py__: 短信接口文件
*  __api_trans_btcchina.py__: BTCChina交易接口类
*  __api_account_btcchina.py__: BTCChina封装交易接口
*  __api_price_btcchina.py__: BTCChina价格抓取类
*  __run_update_price.py__: 价格更新脚本
*  __run_monitor_trend.py__: 价格预警脚本

### 使用说明 ###

1. 设定 config.py 相关配置项，特别是访问密钥

        ACCESS_KEY="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
        SECRET_KEY="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
        ACCOUNT_ID='XXXXXXXX'

2. 启动价格更新脚本

        nohup python run_update_price.py 1>/dev/null 2>&1 &


3. 启动价格预警脚本

        nohup python run_monitor_trend.py 1>/dev/null 2>&1 &
        

### 其他 ###

* 鉴于急用，程序中还存在大量问题，有问题可随时与<Justinli.LJT@gmail.com>联系

___

_本文档在__[Mou](http://mouapp.com/ “Mou, web developers' Markdown editor for Mac OS X.”)__协助下完成_









