# Ontology 学习笔记

## 一.了解[Ontology Smart Contract](https://github.com/ontio/ontology-smartcontract) 

Version V0.7.0

### 1.什么是智能合约？

智能合约是一套以数字形式定义的承诺，包括合约参与方可以在上面执行这些承诺的协议。

区块链技术给我们带来了一个去中心化的，不可篡改的，高可靠性的系统，在这种环境下，智能合约才大有用武之地。

智能合约是区块链最重要的特性之一，也是区块链能够被称为颠覆性技术的主要原因。

### 2.Ont智能合约的特点

Ont智能合约具有确定性、高性能、扩展性的特性，包括两大模块：**交互服务**和**虚拟机**。

交互服务提供了**虚拟机和区块链账本之间的交互**。

虚拟机提供了**智能合约的运行环境**。

交互服务包括**原生服务**，**Neo虚拟机服务**，和**Wasm虚拟机服务**。

原生服务提供了**基础链上特殊智能合约的实现**，这种合约能被快速方便地使用。

Neo虚拟机服务提供了**外部访问Neo虚拟机的API**, 它能增强智能合约的调用功能。

Wasm虚拟机服务提供了**访问外部虚拟机的Wasm虚拟机的API**。

虚拟机包括**Neo虚拟机**和**Wasm虚拟机**。

Neo虚拟机是一种轻量级的虚拟机，已被证明在公链上运行良好。

Wasm虚拟机是一种高效能的通用虚拟机。

本体智能合约也支持在不同的虚拟机上调用合约。

开发者可以通过本体智能合约方便地构建项目。

思维导图：

![Ont智能合约模块](C:\Users\18402\Desktop\onchain-ont\思维导图\Ont智能合约模块.jpg)

### 3.支持的语言

当前支持的语言有：

C#, VB.Net, F#

Java, Kotlin

Python

C, C++

我们计划支持的语言有：

Rust

Golang

JavaScript

### 4.如何开发智能合约

我们已经开发了一个在线工具[Smartx](http://smartx.ont.io/)，来帮助应用开发者。

SmartX是一个可用于编译，部署和调用智能合约的一站式IDE。它提供了丰富的智能合约模板以及强大的在线编辑器。基于SmartX这个工具，智能合约的需求方可以参考和使用模板合约，或者委托社区开发人员定制开发所需的合约。未来，智能合约的开发人员可以交易自己编写的智能合约，或者协作多人开发智能合约，利用自己的专业知识获得收益。

本体智能合约支持了**Native智能合约**、**NeoVm智能合约**、**WASM智能合约**等多种合约类型，目前，Smartx支持基于NeoVM的C＃和Python两种语言，未来还会支持WASM在线编译功能及更多主流开发语言，包括Java、Rust、Go、JavaScript等。

下一步，我们将像类似GitHub等分布式软件项目代码托管平台一样，支持多人共同参与、分享一份复杂的合约；并同时实施一套的经济激励措施，融入公正的治理政策，反映每一个参与者的贡献，使智能合约编写、智能合约交易、协作、社区建设等相结合，形成一个良好的智能合约开发生态。

下面介绍了使用Smartx来创建智能合约的主要流程。

#### 第一步 - 编写&编译智能合约

目前，我们支持运行于**NEO虚拟机**和**WASM虚拟机**的智能合约。

- **对于NEO虚拟机**，我们提供了[>>Smartx](http://smartx.ont.io/)来帮助你编写和编译智能合约。
- **对于WASM虚拟机**, 请查阅 [>>WASM智能合约](https://github.com/ontio/ontology-smartcontract/blob/master/smart-contract-tutorial/README_wasm.md)文档。

首先你需要创建一个项目并选择你喜欢的语言，开始编写智能合约。

![Select language](https://camo.githubusercontent.com/abe1420009f110add915751a9197afe89583782e/68747470733a2f2f73312e617831782e636f6d2f323031382f30332f32342f3962784a59522e706e67)

然后进入项目编辑页面。

中间主要部分是合约的编辑器。

右侧是操作面板。

中间下部打印操作的输出结果。

![Compile contract](https://camo.githubusercontent.com/0ea3d469c471efa89061e5718c1ef03973122ebe/68747470733a2f2f73312e617831782e636f6d2f323031382f30342f30342f4370496470522e706e67)

#### 编写智能合约

接下里你可以开始编写你的智能合约。我们提供众多实用的模板供你参考。

[>>> 更多具体实例](https://github.com/ontio/ontology-smartcontract/blob/master/smart-contract-tutorial/examples)

#### 编译智能合约

在你完成编写合约之后，你可以点击操作面板上的**编译**按钮，编译你的合约。

如果你的合约语法正确，将会被编译出相应的ABI文件和AVM文件，并展示在右侧。

#### 第二步 - 部署合约

接下来，你可以将合约部署到区块链上。当选择的网络是测试网时，这一步不需要消耗gas。点击**部署**按钮来部署合约。部署的结果将会打印在输出框里。你可以拷贝结果里的交易hash到本体的[区块链浏览器](https://explorer.ont.io/)上，进一步确认部署是否成功。

除了Smartx外，你还可以使用本体的SDK来部署合约。更多信息请查阅相关文档。

[>> Java SDK](https://ontio.github.io/documentation/ontology_java_sdk_smartcontract_zh.html)

[>> TS SDK](https://ontio.github.io/documentation/ontology_ts_sdk_smartcontract_zh.html)

[![Deploy contract](https://camo.githubusercontent.com/765ddf30a5f84905182f0ddb0dd06b0e663b399f/68747470733a2f2f73312e617831782e636f6d2f323031382f30342f30342f4370496341652e706e67)](https://camo.githubusercontent.com/765ddf30a5f84905182f0ddb0dd06b0e663b399f/68747470733a2f2f73312e617831782e636f6d2f323031382f30342f30342f4370496341652e706e67)

#### 第三步 - 调用智能合约

最后，你可以运行合约中的方法。你可以选择想要运行的方法，输入正确的参数值，点击**运行**按钮，调用智能合约。调用的结果将会打印在输出框里。

[![Invoke smart contract](https://camo.githubusercontent.com/9dbae63f90e86e0d29efb34d544fc9f61b4107aa/68747470733a2f2f73312e617831782e636f6d2f323031382f30342f30342f43706f4345462e706e67)](https://camo.githubusercontent.com/9dbae63f90e86e0d29efb34d544fc9f61b4107aa/68747470733a2f2f73312e617831782e636f6d2f323031382f30342f30342f43706f4345462e706e67)

除了Smartx，你还可以使用本体的SDK来调用智能合约。更多信息请查阅相关文档。

[>> Java SDK](https://ontio.github.io/documentation/ontology_java_sdk_smartcontract_zh.html)

[>> TS SDK](https://ontio.github.io/documentation/ontology_ts_sdk_smartcontract_zh.html)



## 二.[Ontology 本地环境搭建与节点启动](https://github.com/ontio/ontology)

### 1.构建开发环境

成功编译ontology需要以下准备：

- Golang版本在1.9及以上(已有)
- 安装第三方包管理工具glide(需要安装)
- 正确的Go语言开发环境(已有)
- Golang所支持的操作系统(已有)

安装[glide](https://github.com/Masterminds/glide):

根据github的内容在ubuntu中使用adp-get来安装:

```
sudo add-apt-repository ppa:masterminds/glide && sudo apt-get update
sudo apt-get install glide
```

安装成功后就可以直接使用glide

### 2.获取ontology

因为节点不太好用导致git clone或者go get比较慢,所以直接在github上download了zip然后解压缩

解压到 **$GOPATH/src/github.com/ontio** 目录

接着用第三方包管理工具glide拉取依赖库

```
$ cd $GOPATH/src/github.com/ontio/ontology
$ glide install
```

用make编译源码

```
$ make all
```

成功编译后会生成两个可以执行程序

- `ontology`: 节点程序/以命令行方式提供的节点控制程序
- `tools/sigsvr`: (可选)签名服务 - sigsvr是一个签名服务的server以满足一些特殊的需求。详细的文档可以在[这里](https://github.com/ontio/ontology/blob/master/docs/specifications/sigsvr_CN.md)参考

编译成功后,为了使用方便,在/etc/environment中添加了一个全局变量/home/xumo/gocode/src/github.com/ontio/ontology

这样就不用cd,可以直接在终端中快捷地调用了

windows中直接下载最新的releases使用

### 3.运行ontology

#### 主网同步节点

直接启动Ontology

```
 ontology
```

可以连接上主网了。

#### 公开测试网Polaris同步节点

直接启动Ontology

```
 ontology --networkid 2
```

可以连接上公共测试网了。

#### 测试模式

在单机上创建一个目录，在目录下存放以下文件：

- 节点程序`ontology`
- 钱包文件`wallet.dat` （注：`wallet.dat`可通过`./ontology account add -d`生成）

使用命令 `$ ./ontology --testmode` 即可启动单机版的测试网络。

单机配置的例子如下：

- 目录结构

  ```
  $ tree
  └── node
      ├── ontology
      └── wallet.dat
  ```

对于docker的使用不太熟悉所以就不测试了

由于github上的示例较为简单,所以查阅[ontlogy的文档](https://ontio.github.io/documentation/tutorial_for_developer_zh.html#%E6%9C%AC%E4%BD%93%E8%8A%82%E7%82%B9%E4%BB%8B%E7%BB%8D)进行测试

### 4.使用ontology

①按照[连接到本体网络](https://ontio.github.io/documentation/tutorial_for_developer_zh.html#%E8%BF%9E%E6%8E%A5%E5%88%B0%E6%9C%AC%E4%BD%93%E7%BD%91%E7%BB%9C)所述，建议使用单机环境下的测试模式。当然，你也可以选择连接到本体的公共测试网络Polaris。 接下来的步骤将以单机环境下的测试模式为例进行。

②使用命令`./ontology --rest --ws --localrpc --gaslimit 20000 --gasprice 0 --testmode --networkid 3`启动测试网络，输入对应的钱包里的账户的密码。

--rest:Enable restful api server

--ws:Enable web socket server

--localrpc:Enable local rpc server

--gaslimit:Min gas limit <value> of transaction to be accepted by tx pool. (default: 20000)

--gasprice:Min gas price <value> of transaction to be accepted by tx pool. (default: 500)

--testmode:Single node network for testing. In test mode, will start rpc, rest, web socket server, and set default gasprice to 0

--networkid 3:Network id <number>. 1=ontology main net, 2=polaris test net, 3=testmode, and other for custom network (default: 1)

③使用rest接口查询初始账户（solo模式下的记账人）的余额。

- 在浏览器中输入`http://localhost:20334/api/v1/balance/APrkensMwPiaqg5rfz54Qa62hDWwtFAnkh`。其中`localhost`是节点的ip，`20334`是默认的rest端口，这个端口也可以自己指定，命令为 `--rest --restport 20339`；`api/v1/balance/`为rest接口的url 路径，后接的`APrkensMwPiaqg5rfz54Qa62hDWwtFAnkh`为初始记账人的地址。这整个URL构成了余额查询的rest接口调用方式。
- 浏览器返回响应`{"Action":"getbalance","Desc":"SUCCESS","Error":0,"Result":{"ont":"1000000000","ong":"0"},"Version":"1.0.0"}`，这是一段json格式的响应字符串，可以看到该账户的ont 数量为十亿，ong数量为0。

④在本体网络中，几乎所有的操作都需要消耗gas，即ong，在本例中，启动时使用了`--gasprice 0`参数将gas消耗置位0，所以后续的操作不消耗gas，但仍可以支付gas。这一步将演示如何给账户提取ong。

- ong是ont的伴生燃料，随ONT逐步释放，但是需要手动提取到自己的账户里；

- 使用`./ontology asset unboundong 1`查询默认钱包里第一个账户可提取的ONG数量，可以使用`./ontology asset --help`了解命令的详细信息；

  ```
    Unbound ONG:
    Account:APrkensMwPiaqg5rfz54Qa62hDWwtFAnkh
    ONG:0
  ```

- 此时可提取的ong数量为零，是因为此账户还未激活ONG的释放，可以使用转账方式来激活；

- 使用`./ontology account add -d`创建另一个ontology账户，地址为`AGrJQhb7bZsy57MoQk6YDt3hDP7zRioHia`，使用`./ontology account list`查询默认钱包的账户情况；

  ```
    Index:1    Address:APrkensMwPiaqg5rfz54Qa62hDWwtFAnkh  Label: (default)
    Index:2    Address:AGrJQhb7bZsy57MoQk6YDt3hDP7zRioHia  Label:
  ```

- 使用`./ontology asset transfer --from 1 --to 2 --amount 100000000`命令，从账户1向账户2转入一亿个ont，输入账户1的密码后，转入成功；

  ```
    Transfer ONT
    From:APrkensMwPiaqg5rfz54Qa62hDWwtFAnkh
    To:AGrJQhb7bZsy57MoQk6YDt3hDP7zRioHia
    Amount:100000000
    TxHash:73a3d24b7dfd0d96b23f93fd38afe4638b70f921c278202443d0dd29a036236f
      
    Tip:
       Using './ontology info status 73a3d24b7dfd0d96b23f93fd38afe4638b70f921c278202443d0dd29a036236f' to query transaction status
  ```

- 查询账户1和账户2的余额，这次使用命令行的方式查询，命令为`./ontology asset balance 1`和`./ontology asset balance 2`：

  ```
    BalanceOf:APrkensMwPiaqg5rfz54Qa62hDWwtFAnkh
    ONT:900000000
    ONG:0
         
    BalanceOf:AGrJQhb7bZsy57MoQk6YDt3hDP7zRioHia
    ONT:100000000
    ONG:0
  ```

- 再次使用`./ontology asset unboundong 1`查询账户1可提取的ong数量，可以发现可提取的数量大于0（实际执行过程中，这个数额受区块高度和转出的数额影响）：

  ```
    Unbound ONG:
    Account:APrkensMwPiaqg5rfz54Qa62hDWwtFAnkh
    ONG:5242930
  ```

- 使用`./ontology asset withdrawong 1`命令，输入账户1的密码后提取账户1的ong：

  ```
    Withdraw ONG:
    Account:APrkensMwPiaqg5rfz54Qa62hDWwtFAnkh
    Amount:5242930
    TxHash:6e10592e52cb7a3645eecd987c0161a8811f25ed5e183614d0e9cd9c58ab8a33
      
    Tip:
      Using './ontology info status 6e10592e52cb7a3645eecd987c0161a8811f25ed5e183614d0e9cd9c58ab8a33' to query transaction status
  ```

- 使用命令行方式查询账户1的余额，可以看到，该账户里已经有ong了：

  ```
    BalanceOf:APrkensMwPiaqg5rfz54Qa62hDWwtFAnkh
    ONT:900000000
    ONG:5242930
  ```

好像是在进行转账后,遇到了error

2018/11/10 22:50:58.460976 [INFO ] GID 76, increment validator block height -1 != ledger block height 35
2018/11/10 22:50:58.461173 [INFO ] GID 76, current block height 35, increment validator block cache range: [0, 0)
2018/11/10 22:50:58.462257 [ERROR] GID 76, Ledger AddBlock BlockHeight:36 BlockHash:c9da1ecbee7eeb7442548037f972e6f9d46552243d52a6c1c5f8d812e898a0ee error:verifyHeader error block timestamp is incorrect
2018/11/10 22:50:58.462428 [ERROR] GID 76, Solo genBlock error genBlock DefLedgerPid.RequestFuture Height:36 error:verifyHeader error block timestamp is incorrect
2018/11/10 22:50:58.466100 [INFO ] GID 56, CurrentBlockHeight = 35

应该是在创建新块的时候出错了,区块时间戳方面的错误,可以看到之后没有创建出新块,而是一直停留在35的高度

使用ontology --testmode 还是会报上述的错

发现是环境变量的锅,直接在根目录进行testmode时,有一些文件无法读取出来,因为config源代码使用./来调用那些文件,而Golang的相对路径是相对于执行命令时的目录,所以在根目录执行时,直接调用了根目录,无法获取相应的文件,就无法正常运行,或许可以通过更改源码来解决

多次尝试后,终于发现了一个简单的解决方案如下:

修改源码中/common/config/config.go

由于const无法赋予字符串,所以把定义调用文件地址的常量改为变量来定义

```go
var (
    //先调用出ontology项目的绝对路径再在下面进行拼接
   dir = os.Getenv("GOPATH") + "/src/github.com/ontio/ontology"
   DEFAULT_DATA_DIR      = dir + "/Chain"
   DEFAULT_RESERVED_FILE = dir + "/peers.rsv"
   DEFAULT_CONFIG_FILE_NAME = dir + "/config.json"
   DEFAULT_WALLET_FILE_NAME = dir + "/wallet.dat"
)
```

修改之后,主网测试网和testmode都可以正常使用



## 三.[Ontology Cli使用教程](https://github.com/ontio/ontology/blob/master/docs/specifications/cli_user_guide_CN.md)

主要内容在二中都有涉及到,更详细的一些操作指令可以直接查阅文档

## 四.[SmartX使用教程](https://ontio.github.io/documentation/SmartX_Tutorial_en.html)

### 1.什么是 SmartX

SmartX是一个可用于编译，部署和调用智能合约的一站式IDE。它提供了丰富的智能合约模板以及强大的在线编辑器。基于SmartX这个工具，智能合约的需求方可以参考和使用模板合约，或者委托社区开发人员定制开发所需的合约。未来，智能合约的开发人员可以交易自己编写的智能合约，或者协作多人开发智能合约，利用自己的专业知识获得收益。

下一步，我们将像类似GitHub等分布式软件项目代码托管平台一样，支持多人共同参与、分享一份复杂的合约；并同时实施一套的经济激励措施，融入公正的治理政策，反映每一个参与者的贡献，使智能合约编写、智能合约交易、协作、社区建设等相结合，形成一个良好的智能合约开发生态。

### 2.注册与登录

smartX上的ONT ID似乎没有开放注册,OntId中的[快速开发指南](https://github.com/ontio/ontology-DID/blob/master/docs/cn/get_started_cn.html)是404,看来只能绑定github登录

### 3.第一步 - 编写&编译智能合约

- **对于NEO虚拟机**, 我们提供了[SmartX](http://smartx.ont.io/) 来帮助您编写，编译，调用智能合约。

首先你需要创建一个项目并选择你喜欢的语言，开始编写智能合约。

先选择python,新建一个Hello World合约模板,名称也是Hello World

提供的Hello Worldmob模板为:

```python
from boa.interop.System.Runtime import Log

def Main(operation, args):
    if operation == 'Hello':
        msg = args[0]
        return Hello(msg)

    return False


def Hello(msg):
    Log(msg)
    return True
```

此处调用的是python编译器而不是neo-boa

先尝试使用cyano wallet完成编译:

在谷歌商店下载并安装插件cyano wallet,然后导入了wallet.dat文件中的钱包

接着在打开终端,运行ontology --testmode

使用cyano wallet连接本地私链,发现地址处填写localhost:20334并不能连接上,改用本机ip地址127.0.0.1后成功连接

发现使用python 的Hello World 总是会报错The transaction timed out:

Your transaction has not completed in time. This does not mean it has failed, please check the blockchain to confirm. (Note: Make sure you have 0.01 claimed ONG to pay the network transaction fee)

而C#的不会

询问过后,解决方法是更换使用的函数

```python
from boa.interop.System.Runtime import Notify

def Main(operation, args):
    if operation == 'hello':
        msg = args[0]
        return hello(msg)

    return False


def hello(msg):
    Notify(msg)
    return True
```

编译智能合约：

在完成编写合约之后，可以点击操作面板上的编译按钮，编译合约。

如果合约语法正确，将会被编译出相应的ABI文件和AVM文件，并展示在操作面板上。

### 4.第二步 - 部署智能合约

接下来，可以将合约部署到区块链上。当选择的网络是测试网时，这一步不需要消耗gas。点击部署按钮来部署合约。部署的结果将会打印在输出框里。可以拷贝结果里的交易hash到本体的[区块链浏览器](https://explorer.ont.io/)上，进一步确认部署是否成功。

除了SmartX外，还可以使用本体的SDK来部署合约。更多信息请查阅相关文档。

[» Java SDK](https://ontio.github.io/documentation/ontology_java_sdk_smartcontract_en.html)

[» TS SDK](https://ontio.github.io/documentation/ontology_ts_sdk_smartcontract_en.html)

### 5.第三步 - 调用智能合约

最后，可以运行合约中的方法。可以选择想要运行的方法，输入正确的参数值，点击运行按钮，调用智能合约。调用的结果将会打印在输出框里。

除了Smartx，还可以使用本体的SDK来调用智能合约。更多信息请查阅相关文档。

[» Java SDK](https://ontio.github.io/documentation/ontology_java_sdk_smartcontract_en.html)

[» TS SDK](https://ontio.github.io/documentation/ontology_ts_sdk_smartcontract_en.html)



## 五.合约编译

### 1.通过smartX编译

在smartX中将代码输入后，点击编译就能直接编译

会生成一个.json的ABI文件，和一个AVM文件，可以下载，ABI文件中带有合约的哈希值。

### 2.通过本地编译器编译

```python
from boa.interop.System.Runtime import Notify

def Main(operation, args):
    if operation == 'hello':
        msg = args[0]
        return hello(msg)

    return False


def hello(msg):
    Notify(msg)
    return True
```

使用的是[python编译器](https://github.com/ontio/ontology-python-compiler)

编译步骤：

①将python编译器[ontology-python-compiler](https://github.com/ontio/ontology-python-compiler)项目下载并解压。

②使用命令`python -m venv venv`创建一个venv虚拟环境，可以让每个python项目单独使用一个环境，就不会影响系统环境，也不会影响其他项目的环境。

③cd到创建好的venv环境中，Scripts目录下，执行activate.bat，就能够在命令行中启用venv环境。

④使用命令`pip install -r requirements.txt`安装依赖包

⑤在编译器项目的目录下，使用命令`setup.py install`就能将编译器配置到环境中。

⑥使用命令`run.py -n helloworld.py -m 1`就可以将helloworld.py文件成功编译，在相应目录下生成abi与avm文件。

也可以使用[智能合约模版](https://github.com/ONT-Avocados/python-template)中的[compile_contract.py](https://github.com/ONT-Avocados/python-template/blob/master/compile_contract.py)来编译合约，但是该模板中使用的都是neo-boa编译器，如果使用的是引用python编译器来编写的合约，需要修改一下compile_conteact.py文件的内容，就是把`from boa.compiler import Compiler`改为`from ontology.compiler import Compiler`。

## 六.合约部署

### 1.可以通过SmartX,连上cyano wallet(ONT的cyano wallet是一种chrome plugin，可以用Ethereum的MetaMask来类比)指定网络(与IP地址)，可将合约布署到本地网、或测试网、或主网。

部署helloworld步骤：

①首先需要安装好cyano wallet，再chrome商店中就能够完成安装。

②先在本地网络测试，所以使用./ontology --testmode来打开本地私链。

③将cyano wallet选择为PRIVATE-NET，地址为本机ip：127.0.0.1。

④向cyano wallet导入本地的钱包文件wallet.dat，创建好测试用的钱包。

⑤在smartX中编译好合约后，点击部署，通过cyano wallet支付gas之后，就能够成功部署。

### 2.在启动节点的情况下，可以通过Cli，将合约布署到本地、测试网或主网。

可以参考[Ontology Cli使用教程](https://github.com/ontio/ontology/blob/master/docs/specifications/cli_user_guide_CN.md)中的智能合约一栏。

使用命令`ontology contract deploy --code h.avm --name 'Hello' --version '1.0' --author 'xumo' --email '1@1.com' --desc 'helloworld' --needstore --gaslimit=100000000`就能在本地部署合约。

部署失败，报错：

[ERROR] DeployContract error:hex.DecodeString error:encoding/hex: odd length hex string。

多次尝试后发现，无论是使用neo或者python编译器编译出的avm文件，还是从smartX下载的avm文件，都不能正常使用，只能在smartX中编译后，复制出avm字节码，保存到文件中修改后缀名为avm，才可以成功部署。

可能是编译器编译出的avm文件的问题：

用python编译器或boa编译器编译出的helloworld.avm打开来为一串乱码，而helloworld.avm.str则为正确的avm字节码

![img](file:///C:\Users\18402\Documents\Tencent Files\184026603\Image\C2C\~%YR~GFA}WEZZ4P[C42A$OH.png)

使用smartX编译后的avm文件，下载之后尝试部署也失败，报错：

[ERROR] DeployContract error:hex.DecodeString error:encoding/hex: invalid byte: U+0022 '"'

打开下载来的avm文件，发现avm字节码的前后有两个双引号，去掉就能正常部署了，应该是编译器的问题。



## 七.合约测试

### 1.SmartX上可以进行运行、调试合约内的函数。

在运行栏，选择运行函数为hello，输入一个string的Hello World，点击运行，就能在下方的日志得到一个返回：

Invoke: {"result":["48656c6c6f20576f726c64"],"transaction":"2785e1830d607abf5bfd4dc957fec94a2ff3189fcd5b086ac0f8f84bd0b0e6a0"}

其中的result即为返回的结果，将48656c6c6f20576f726c64十六进制转字符串，就为Hello World。

### 2.可以通过Cli运行、调试合约函数。

在命令行工具中使用命令

`ontology contract invoke --address 39f3fb644842c808828817bd73da0946d99f237f --params string:Hello,[string:tester] --gaslimit 200000`

`--params string:Hello,[string:tester]`指定调用合约传入的参数，这里传入了两个参数，分别是`string:Hello`和`[string:Hello World]`，这些参数即是传入到合约代码中Main函数执行的参数。

输入后返回

   TxHash:a4efb7019ec609a77d107e921dadb37bc7f29aced7669cf20efe9d29cc31898e

Tips:
  Using './ontology info status a4efb7019ec609a77d107e921dadb37bc7f29aced7669cf20efe9d29cc31898e' to query transaction status.

根据提示使用命令`ontology info status a4efb7019ec609a77d107e921dadb37bc7f29aced7669cf20efe9d29cc31898e`查询交易情况

返回

Transaction states:
{
   "TxHash": "a4efb7019ec609a77d107e921dadb37bc7f29aced7669cf20efe9d29cc31898e",
   "State": 1,
   "GasConsumed": 0,
   "Notify": [
​      {
​         "ContractAddress": "39f3fb644842c808828817bd73da0946d99f237f",
​         "States": "746573746572"
​      }
   ]
}

746573746572十六进制转字符换即为tester。

### 3.我们也有Python测试框架，可测试合约功能，建议：在上述内容有了大致了解之后，再去接触测试框架。

在下面研究测试框架的内容。



## 八.python测试框架

感兴趣且有时间的话，也可以看一下我们的Dapp开发框架[punica-python](https://github.com/ontio-community/punica-python), 类型于Ethereum的truffle工具。

看github主页，似乎该项目转移到了[punicasuite](https://github.com/punicasuite/punica-python)。

### 1.概述

punica的特性：

- Punica-Cli 支持智能合约的编译，部署，调用，测试以及单行命令。
- Punica-Cli 为使用不同语言的开发者实现了Python和TypeScript版本。
- Punica网站提供了丰富的文档资料与合约模板。
- Solo chain 有一个带有UI的测试节点，用于轻松地查看区块，交易，合约，合约通知等。
- 能够自动地生成dApp项目目录，提供各种类型的盒子，轻松地开发基于Punica-Boxes的dApp。
- 与SmartX中的合约测试配置和测试功能使用相同的标准。
- 提供了智能合约包管理工具。

punica的help文档：

```
punica
Usage: punica [OPTIONS] COMMAND [ARGS]...

Options:
  -p, --project PATH  Specify a punica project directory.
  -v, --version       Show the version and exit.
  -h, --help          Show this message and exit.

Commands:
  compile  Compile the specified contracts to avm and...
  deploy   Deploys the specified contracts to specified...
  init     Initialize new and empty Ontology DApp...
  invoke   Invoke the function list in default-config or...
  node     Ontology Blockchain private net in test mode.
  scpm     Smart contract package manager，support...
  smartx   Ontology smart contract IDE,SmartX...
  test     Unit test with specified smart contract
  unbox    Download a Punica Box, a pre-built Ontology...
  wallet   Manager your ontid, account, asset.
```

### 2.搭建开发环境

需要git和python3.7，已经有了。

### 3.安装punica

```
pip install punica
```

or

```
python setup.py install
```

### 4.快速启动

大多数的punica命令，都需要在一个punica项目中运行。

#### 4.1创建一个项目

##### 4.1.1初始化一个新项目

没有智能合约也能创建punica项目。

使用命令`punica init`。

完成初始化后，会在当前文件夹下创建好一个如下的项目结构：

- `contracts/`: 本体智能合约的目录。
- `src/`: DApp源文件的目录。
- `test/`: 测试程序与合约文件的目录。
- `wallet/`: 保存本体钱包的目录。

注意：如果不是在项目的根目录中运行punica cli，则需要使用-p或者--project来指定DAp'p项目的路径。

##### 4.1.2创建一个盒子中的项目

可以使用Punica Boxes，其中拥有许多示例应用和项目模板。

接下来使用[ontology-tutorialtoken box](https://github.com/wdx7266/ontology-tutorialtoken)，来创建一个OPE4标准的token，它可以在账户之间进行传输：

- 为Punica Project创建一个新目录：

```
mkdir tutorialtoken
cd tutorialtoken
```

- 使用命令unbox来下载项目：

```
punica unbox tutorialtoken
punica unbox --help
Usage: punica unbox [OPTIONS] BOX_NAME

  Download a Punica Box, a pre-built Ontology DApp project.

Options:
  -h, --help  Show this message and exit.
```

#### 4.2编译项目

可以用下面这个命令来编译智能合约：

```
punica compile
```

成功编译之后，在contracts/build目录下会出现avm和abi文件。

```
contacts
    ├─build
    │      contract.avm
    │      contract_abi.json
```

但是报错：

File "c:\users\18402\appdata\local\programs\python\python37\lib\site-packages\punica\compile\contract_compile.py", line 212, in update_invoke_config
​    all_func_name_list.append(func_information['name'])
KeyError: 'name'

对比了环境中的contract_compile.py与github上源码上的contract_compile.py，发现此处的name与下面一处的name应该为operation，可能是pip install取得的版本有问题。

所以改为从源码安装punica之后，能够成功编译。

#### 4.3部署项目

在项目部署之前，可以优化两个配置文件，用于配置使用的区块链网络的punica-config.json，用于配置合约信息的default-config.json。

使用下面这个命令来部署合约：

```
 punica deploy
```

返回了：

```
Using network 'privateNet'.

Running deployment: oep4_token.avm
        Deploying...
        Deploy to: cb9f3b7c6fb1cf2c13a40637c189bdd066a272b4
Deploy successful to network...
         Contract address is cb9f3b7c6fb1cf2c13a40637c189bdd066a272b4
         Txhash is 2380f8fca5be5202fcb7bb59a98134e4c2421504fc80a39be9e4ef551d2aa6e3
```

注意：

- 如果bin（build？）目录中有多个avm文件，则需要使用--avm选择指定合约来部署。
- 如果wallet目录中有多个钱包文件，可以用--wallet来指定使用的钱包，否则将会随机使用钱包文件。

#### 4.4调用

如果要在已部署的合约中调用功能列表，可以使用`invoke`命令，在使用invoke命令之前，应该先配置好default-config.json文件。

查看可以调用的函数的指令：

`punica invoke list`

会返回所有可以调用的函数名：

```
All Functions:
         init
         name
         symbol
         decimals
         totalSupply
         balanceOf
         transfer
         transferMulti
         allowance
         transferFrom
         approve
```

调用所有list中的函数，可以直接使用指令：

`punica invoke`

会直接执行所有的函数：

```
Using network 'privateNet'.

Running invocation: oep4_token_abi.json
Unlock default payer account...
Invoking  init
Invoke successful
txHash: 0x5e63e563a59b1491a180a9e4c572b4dfaf75d8b51ec48c43bea53b86b666f094
Invoking  name
Invoke successful
Invoke result: 4458546f6b656e
Invoking  symbol
Invoke successful
Invoke result: 4458
Invoking  decimals
Invoke successful
Invoke result: 0a
Invoking  totalSupply
Invoke successful
Invoke result: 0000e8890423c78a00
Invoking  balanceOf
Invoke successful
Invoke result:
Invoking  transfer
Unlock signers account...
Invoke successful
txHash: 0x89e545495963d41d36da08242e0037b8a6c70868141aaf08819e23c69299405a
Invoking  transferMulti
Unlock signers account...
txHash: 0xd3175ee9ef4a021ffafa4dfce14fbdba6e4151ecc33a919224310c65c4e2bf50
        Invoke failed, [NeoVmService] vm execute state fault!
Invoking  allowance
Unlock signers account...
Invoke successful
txHash: 0x1bdf4e04eba5b2dbb03a829d1baf1db9782cf6efa618120ef800bece263f9cd9
Invoking  transferFrom
Unlock signers account...
Invoke successful
txHash: 0xda03feb070d7bd38a1aa92876762a9e96a3f94b92528cc06a4f818ab0e81e49a
Invoking  approve
Unlock signers account...
Invoke successful
txHash: 0x9eb53f175c397d12e97511d0755946385e32f25d3acbe388e241ec59f521880b
```

#### 4.5节点

```
$ punica node
Usage: punica node [OPTIONS]

   Ontology Blockchain private net in test mode. please download from
   https://github.com/punicasuite/solo-chain/releases

Options:
   -h, --help  Show this message and exit.
```

#### 4.6智能合约包管理

```
$ punica scpm
Usage: punica scpm [OPTIONS]

   smart contract package manager，support download and publish.

Options:
   -h, --help  Show this message and exit.
```

#### 4.7smartX

```

```

#### 4.8测试

```
$ punica test -h
Usage: punica test [OPTIONS] COMMAND [ARGS]...

  Unit test with specified smart contract

Options:
  --file TEXT  Specify which test file will be used.
  -h, --help   Show this message and exit.

Commands:
  template  generate test template file
```

#### 4.9钱包

```
$ punica wallet
Usage: punica wallet [OPTIONS] COMMAND [ARGS]...

   Manager your asset, ontid, account.

Options:
   -h, --help  Show this message and exit.

Commands:
   account  Manager your account.
   asset    Manager your asset, transfer, balance,...
   ontid    Manager your ont_id, list or add.
```

