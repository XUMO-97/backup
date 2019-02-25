# HyperDragons+Rocket Protocol 开启区块链游戏 2.0 时代

> @author Nep.Yan 2018-08-21

## 0x01 区块链游戏的痛点与希望

从 2017 年底开始掀起的区块链游戏浪潮，如今已快满一年。然而受限于主流公链（以太坊）当前的性能瓶颈，至今没有一款真正意义上核心玩法去中心化并且还能保持足够体验的游戏诞生。

HyperDragons 作为一款核心玩法运行在以太坊智能合约上且常年维持在各大 DApp 排行榜前 5 的真游戏，在探索去中心化游戏玩法的同时，深切感受到了当前技术的瓶颈对游戏体验的限制。这个限制通常可以总结为 2 个字：慢、贵。无论是缓慢的确认时间还是每笔操作都需要支付 Gas 费，都让用户体验变得非常糟糕。

![image](http://mix-workstation.oss-cn-hangzhou.aliyuncs.com/nep.yan/hd.png)

**HyperDragons 的理想是让 DApp 跟 App 一样好玩。**

我们可以看到行业内众多的技术力量都在为了扩展以太坊的能力而进行努力，如：Sharding、State Channels、Plasma、Truebit。这其中无论是第一层还是第二层解决方案，看起来离真正落地还尚需时间。**而我们等不及了**。我们迫切地想要带给玩家更高质量的游戏体验，于是我们自己动手了。HyperDragons 团队携手中美区块链工程师共同打造了完全为区块链游戏而设计的 Layer2 解决方案：Rocket Protocol。

有了 Rocket Protocol，游戏逻辑在链下飞速执行，且每笔操作无需支付任何费用。但同时又能通过加密经济的机制，保障了数字资产在链上链下的转移，游戏逻辑的公平、公开、透明。简单说就是 App 的体验 + DApp 的去中心化精神。

## 0x02 什么是 Rocket Protocol

Rocket Protocol 是以太坊 Layer2 解决方案，一个加密经济解决方案。Rocket Protocol 系统可以将链上的数字资产（如：ERC20、ERC721）进行锁定，然后在链下的游戏逻辑中快速的使用或改变，而游戏执行的结果（数据）则可以安全的保存回链上。我们设计了一整套完整的激励机制与技术结合，通过一个验证人网络来确保这一点。

> Rocket Protocol 的特点

#### 1. 💰 低成本

由于游戏逻辑完全在链下执行，玩家和开发团队不再需要支付高昂的手续费。对于开发团队来说，可以不再受到合约的 Gas 上限限制，开发出更高复杂度的游戏逻辑、战斗逻辑，尽情发挥他们的创意。

#### 2. ⚡️ 快速响应

不用再等待链上缓慢的区块确认，玩家的任何操作都可以与传统游戏媲美的速度被响应和确认。

#### 3. 🚀 抗拥堵

相信大部分 DApp 玩家和开发团队都遇到过以太坊拥堵的情况，在那些拥堵的日子里，几乎所有 DApp 都陷入了日活接近 0 的窘迫境地。
而 Rocket Protocol 将极大的避免这种情况的发生，除了链上链下锁定和解锁的过程，游戏逻辑的执行，丝毫不受主链拥堵的影响。

#### 4. 💡 开发语言友好

开发者的福音！相比于其他 Layer2 解决方案，Rocket Protocol 的最大特色是方案本身并不限制游戏逻辑的开发语言，只需要满足一定的规则，开发者可以用任意自己擅长的开发语言和架构来完成游戏逻辑的开发。这大大降低了游戏开发者的门槛，同时也让历史悠久的游戏开发经验可以快速的转移到区块链游戏中。

> Rocket Protocol 的组成

Rocket Protocol 主要由以下几部分组成：

![Rocket](http://mix-workstation.oss-cn-hangzhou.aliyuncs.com/nep.yan/RocketArchitecture.jpg)

#### Part.0 ERC20 Token

Rocket Protocol 是一个加密经济解决方案，因此要求每个 Rocket Protocol 系统需要发行一个通证（ERC20），用于激励和惩罚机制。

#### Part.1 Smart Contracts

> Bridge

智能合约，用于锁定解锁、更新数字资产。
举例：当玩家决定玩一个游戏（如云斗龙的竞技场、龙堡战争）时，需要将 NFT 在 Bridge 合约中锁定，然后可以在链下的玩法中尽情使用。当玩家想要退出游戏时，从 Bridge 合约取回 NFT，同时如果该 NFT 有属性变化，则会更新到 NFT 合约中。

> State Registry

智能合约，基于代币精选注册表（TCR）扩展而来，用于安全的存储游戏在链下执行的状态（数据）。
任何人都可以申请将链下游戏中计算出来的数据写回链上，但后文讲述的验证人网络会保障正确的数据才会被存储到合约中。
当玩家解锁拿回自己数字资产的时候，通过读取 State Registry 中的数据来进行更新。

当任何人申请将数据写入 State Registry 时需要质押一定的 Token 并同时进入一个等待期，如果验证人网络发现有人写入错误的数据，将发起挑战。随后将进入投票阶段，验证人网络中的节点或 Token 持有者将对结果进行投票。投票结束后，胜利者将拿走失败者质押的 Token。

#### Part.2 Game Server & State Machine

Rocket Protocol 的一个特色是：游戏开发者可以用传统的技术去编写游戏服务端逻辑，比如：C++，Java，JavaScript，Go 等等。

唯一的要求是：游戏逻辑必须写在一个状态机中，游戏逻辑的推动需要 GameServer 将游戏事件传入到状态机中。同时这个状态机必须保证接收同样的消息序列的情况下，最终输出的状态结果是一致的。如此一来，验证人网络中的每一个节点就可以计算出相同的结果，来验算上链保存的状态是否正确（跟链下一样）。

同时状态机代码存储在 IPFS，任何人都可以下载阅读其源码，运行其程序。

值得注意的是，GameServer 只是一个服务于玩家的 Operator 角色，并不是中心化的控制者。在 Rocket Protocol 系统最终的版本中，Operator 是可以被玩家投票替换的，这切实保障了玩家的利益（不怕开发商跑路），也实践了去中心化的精神。

#### Part.3 Validators Network

这是一个自动运行软件，任何人可以运行这个软件来监控和确保状态机中的游戏状态正确的更新到了链上（State Registry）。

软件会自动从 IPFS 下载并运行一份状态机的程序拷贝。同时通过一个可信赖的 P2P 网络接收游戏消息事件，运行和验算游戏当前的状态。当有人将错误的数据写入链上时，软件会自动发起挑战，拿走恶意者质押的代币。

P2P 网络使用[Secure Scuttlebutt](https://ssbc.github.io/secure-scuttlebutt/)的协议。这个协议的特点是由一个人发送事件（Operator），其他人只能监听事件（Validators）。该协议确保了 Operator 发出的事件是有序的、安全的、可靠的。

> Rocket Protocol 的激励机制

Rocket Protocol 的激励机制分为三部分：

1. 通过挑战错误写入 State Registry 的申请获得其质押的 Token
2. 通过参与投票获胜获取申请/挑战失败者质押的 Token
3. Token 发行方定期故意引入错误上链申请，让验证人网络中的节点通过方式 1 和 2 获取 Token

## 0x03 区块链游戏 2.0 时代

Rocket Protocol 是一个通用的解决方案，State Registry + Validators Network + State Machine 规范定义了通用的框架。

游戏开发商在这基础之上只需实现两样内容便能快速的享受 Rocket Protocol 带来的优势：

1. 锁定和解锁数字资产的 Bridge 合约
2. 提供 Game Server 并在 State Machine 实现游戏逻辑

随着 HyperDragons+Rocket Protocol 将 Layer2 解决方案落地，给区块链游戏插上了更快和更便宜的翅膀。作为第一个范本，HyperDragons 的竞技场玩法将基于 Rocket Protocol 进行改造，除了带给玩家更优质的体验，也期望带给区块链游戏开发者更多的启示。

让我们一起携手走进区块链 2.0 时代！

## 0x04 写在最后

本文讲述了 HyperDragons 在解决行业痛点上的进展，阐述了 Layer2 解决方案 Rocket Protocol 的技术概况。更多的技术细节将在后续文章中逐步披露，敬请期待和指正。
