直接启动主网：

​	`ontology`
测试网络：

​	`ontology --networkid 2`
测试模式：

​	`ontology --testmode`

​	`ontology --testmode --gasprice 0`	不需要gas

​	测试模式必须要在ontology.exe的根目录下有一个wallet.dat钱包文件，否则无法运行

创建钱包：

​	`ontology account add -d`	输入密码后，就会在根目录下生成钱包文件

查询可提取ong数量：

​	`ontology asset unboundong 1`

发送ont：

​	`ontology asset transfer --from 1 --to 2 --amount 100000000`

发送ong：

​	`ontology asset transfer --from 1 --to AVGm37tygZkpa4q9z9YUg2EAhb5q69ACmK --amount 1000000 --asset ong`

查询账户余额：

​	`ontology asset balance 1`

提取ong：

​	`ontology asset withdrawong 1`

ont cli的更多参数指令：

​	https://github.com/ontio/ontology/blob/master/docs/specifications/cli_user_guide_CN.md

