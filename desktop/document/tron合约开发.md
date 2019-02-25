## 一.环境配置及工具安装（`windows10`）

1. 环境配置

   - `tron`参考开发文档地址：https://cn.developers.tron.network/

   - 安装`docker`

     参考[官网](https://docs.docker.com/docker-for-windows/install/)

   - 安装`Node.js`

     参考[官网](https://nodejs.org/en/download/)

2. 工具安装

   - 安装`tronbox`

     命令行输入`npm install -g tronbox`全局安装`tronbox`开发工具

     `tronbox`命令参考：

     | 命令                            | 用法                                                         |
     | ------------------------------- | ------------------------------------------------------------ |
     | tronbox compile                 | 编译所有智能合约。结果进入 ./build/contracts。它只会编译自上次编译以来被修改的文件。 |
     | tronbox compile --compile-all   | 重新编译一切。                                               |
     | tronbox migrate                 | 部署你的合同。它只会在上次成功迁移后进行迁移。               |
     | tronbox migrate --reset         | 重新迁移一切。                                               |
     | tronbox test [test_script_path] | 运行所有测试脚本。定义测试文件名是可选的。它也可以使用 --reset 标志运行。 |
     | tronbox console                 | 控制台支持 `tronbox` 命令。例如，您可以在控制台中调用 “migrate --reset”。结果与在命令中调用`tronbox migrate --reset` 相同。 |

   - 安装`ide`

     `tron`与`eth`相似，主要使用`solidity`语言进行合约开发

     可以使用`vscode`，安装`solidity`插件，支持最新`solidity-5.0.0`版本

     ![1548399665088](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\1548399665088.png)

   - 安装`tronlink`钱包

     类似`metamask`的`chrome`插件钱包，在插件商店搜索安装

     使用水龙头：https://www.trongrid.io/shasta/#request

     贴入自己钱包地址就可以获取测试币

## 二.合约的开发、部署与交互

1. 开启测试节点

   开发者文档中提供了使用`tron docker`快速开启本地测试节点的方法

   命令行中输入：

   ```
   docker run -it -p 8091:8091 -p 8092:8092 -p 8090:8090 -p 50051:50051 -p 50052:50052 --rm --name tron trontools/quickstart:latest
   ```

   会自动拉取并开启`tron`节点，提供十个拥有`10000trx`的私钥账户

   如果无法获取，可以在`docker`的`Settings-Daemon-Registry mirrors`中添加阿里云镜像：

   ```
   https://zy6uz231.mirror.aliyuncs.com
   ```

   或者使用`tron-cli`命令行工具来启动节点：

   ```
   python3 -m venv venv    // Optional step
   
   cd venv/Scripts   // Optional step
   
   activate   // Optional step
   
   pip install troncli
   
   python tron-cli quick
   ```

2. 编写合约

   参考`solidity`文档：https://solidity.readthedocs.io/en/v0.5.3/

3. 使用`tronbox`创建项目

   以`metacoin`为例，创建项目：

   ```
   mkdir metacoin
   cd metacion
   tronbox unbox metacoin
   ```

4. 配置项目

   ①删除目录内的`tronbox.js`文件，否则会在编译时一直跳转打开这个文件（具体原因并未仔细研究）

   ②编辑`tronbox-config.js`文件，以测试网为例

   ```js
   module.exports = {
     networks: {
       shasta: {
         privateKey: 'your private key',
         userFeePercentage: 50,
         feeLimit: 1e8,
         fullHost: "https://api.shasta.trongrid.io",
         network_id: "2"
       }
     }
   }
   ```

   ③在目录下`npm install`安装依赖，注意需要修改`npm`默认使用`python2.7`否则会报错

5. 编译项目

   `tronbox deploy`

   编译成功后会在目录下生成`build`文件夹包含带有接口的合约`json`文件

   注意：似乎无法使用library合约（未发现原因）

6. 部署项目

   `tronbox migrate`

   成功后会在测试网部署合约

7. 合约交互

   ①在测试网部署完合约后，可以在目录下用`npm run dev`打开服务端，通过`http://localhost:3000/`前端界面与合约交互，前端`api`有类似`web3`的`tron-web`可以使用

   ![1549850733601](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\1549850733601.png)

   ②官方文档中提供了`Tron-Studio`，[下载地址](https://cn.developers.tron.network/docs/download-the-code)

   ③`python-sdk`还非常简陋，源码中缺少一些文件，无法正常使用
