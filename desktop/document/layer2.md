### `Registry`合约

#### 主要接口说明

1. 部署合约，需要先部署以下几个合约

+ `EIP20`(可选，如果已有可以直接使用)
+ `Parameterizer`
+ `PLCRVoting`

部署流程：

+ 部署一个`oep4 token`
+ 部署`PLCRVoting`
+ 部署`Parameterizer`
+ 最后部署`Registry`

2. `apply`接口

接口特点:
+ 申请新的`listing`
+ 保证`listing`不为空（已被使用后空闲的状态），即不能重复创建同一个`listing`
+ 保证`listing`不处于`appilication`状态(正在被使用)
+ 保证`listing`中设定的参数`minDeposit`大于`parameterizer`中的设定,即最小限定的存款(质押值)
+ 接口会使用`_listingHash`创建一个`listing`结构体
+ `listing`的`applyStageLen`参数设定为`parameterizer`中的设定,即这个`listing`最长的存活时间,超出时间将会被置为`white`
+ `listing`的`applicationExpiry`参数,设定为区块当前的时间加上`applyStageLen`
+ 将传入的`_data`存储进`listing`结构体中
+ `listing`的`unstakedDeposit`参数设置为`_amount`即`listing`中的所有存款数量
+ 将`_amount`数量的`token`传入合约,进行质押

需要测试的重点:
- [ ] 合约开头的三个`require`能否正常工作
- [ ] 超过`applicationExpiry`的`listing`是否有被置为`white`以及时间是否正确
- [ ] `_data`是否有被储存
- [ ] `token`是否已经质押进合约

3. `deposit`接口

接口特点:
+ 保证`listing`的`owner`为`deposit`的交易发起者
+ `listing`的`unstakedDeposit`参数增加`_amount`的数量
+ 将`_amount`数量的`token`传入合约,进行质押
  
需要测试的重点:
- [ ] `token`是否已经质押进合约
- [ ] `listing`的`unstakedDeposit`参数是否有增加

4. `withdraw`接口

接口特点:
+ 保证`listing`的`owner`为`withdraw`的交易发起者
+ 保证转出的数量`_amount`小于`listing`的`unstakedDeposit`参数
+ 保证`listing`的`unstakedDeposit`在转出`_amount`后,仍大于`minDeposit`,即保证`listing`中始终有大于`minDeposit`的`token`处于质押状态

需要测试的重点:
- [ ] 三个`require`
- [ ] `token`是否已经质押进合约

5. `exit`接口

接口特点:
+ 只有`listing`的`owner`才能关闭它
+ 保证`listing`处于`white`状态
+ 保证`listing`中没有`challengeID`(没有被`challenge`),或它的`chalklenge`已经被解决(被`challenge`过)
+ 调用`resetListing`接口

需要测试的重点:
- [ ] 三个`require`
- [ ] `resetListing`接口可以正常调用

6. `resetListing`接口

接口特点:
+ 如果`listing`处于`white`状态,调用事件反馈`_ListingRemoved`
+ 如果`listing`不处于`white`状态,调用事件反馈`_ApplicationRemoved`
+ 将`listing`的`map`中该`_listingHash`对应的`listing`删除
+ 将`listing`中质押的所有`token`发送给`owner`

需要测试的重点:
- [ ] `listing`在`white`状态下调用`_ListingRemoved`是否正常
- [ ] `listing`不在`white`状态下调用`_ApplicationRemoved`是否正常
- [ ] `map`中的该`listing`是否被删除
- [ ] `listing`中质押的所有`token`是否已发送给`owner`

7. `challenge`接口

接口特点:
+ 保证`listing`处于`application`状态或`white`状态
+ 保证`listing`中没有`challengeID`(没有被`challenge`),或它的`chalklenge`已经被解决(被`challenge`过)
+ 如果`listing`不处于`white`状态,需要保证现在的时间大于:`listing`被`apply`的时间再加上一个小于等于`applyStageLen`的随机时间,实现的功能为:每个用户对于某个`listing`都会有一个随机的`barrier`,只有时间超过了这个`barrier`才可以对该`listing`发起挑战(是为了防止`application`刚开始时出现大量挑战,从而浪费`gas`)
+ 如果`listing`的`unstakedDeposit`小于`minDeposit`,会调用`resetListing`接口将该`listing`删除,实现了自动摘除余额不足的`listing`
+ 调用`voting`创建一个民意投票
+ 根据投票的`pollID`在`challenges map`中创建一个新的`challenge`,赋予奖励池为100减去`dispensationPct`,`dispensationPct`为失败方的质押金分配给胜利方的比例,假如`dispensationPct`设定为50,那么失败方所质押资金的50%将会奖励给胜利方
+ 设置`challenge`的股份`stake`为`minDeposit`    ????有什么用处????
+ 设置`challenge`的`resoved`参数为`false`
+ 设置`challenge`的`totalTokens`为0             ????有什么用处????
+ 在`listing`中设置`challengeID`即为投票的`pollID`
+ `listing`中的`unstakedDeposit`数量减去`minDeposit`即在挑战期间锁定`listing`中`minDeposit`数量的质押金
+ 挑战者将`minDeposit`数量的质押金发送给合约
+ 从`voting`合约中根据`pollID`调取`commitEndDate`与`revealEndDate`参数

需要测试的重点:
- [ ] 前面的两个`require`
- [ ] `barrier`能否正常工作,可以先设置为10秒,便于检测
- [ ] 如果`listing`中的`unstakedDeposit`不足,能否自动删除`listing`
- [ ] `voting`是否有成功调用,创建出一个`poll`
- [ ] `challenge`是否有被成功创建
- [ ] `listing`中的`unstakedDeposit`是否有减去锁定的值
- [ ] `token`是否有传送到合约中
- [ ] `pollMap`中的两个参数是否有调取出来

8. `updateStatus`接口

接口特点:
+ 用于更新`listing`的状态
+ 调用`canBeWhitelisted`,如果返回`true`,就将该`listing`置为`white`
+ 调用`challengeCanBeResolved`,如果返回`true`,就将`listing`中的`challenge`置为`resolve`状态
+ 对于上述两点,测试时需注意,需要先将`listing`状态改为能够被置为`white`或完成`challenge`后,才能用该接口改变`listing`的状态

需要测试的重点:
- [ ] 能否将`listing`置为`white`
- [ ] 能否将`listing`的`challenge`置为`resolve`

9. `canBeWhitelisted`接口

接口特点:
+ 保证`listing`已处于`application`状态
+ 现在的时间并没有超出`listing`的`applicationExpiry`
+ 保证`listing`不处于`white`状态
+ 保证`listing`中没有`challengeID`(没有被`challenge`),或它的`chalklenge`已经被解决(被`challenge`过)
+ 同时满足以上四点,才可以返回true

需要测试的重点:
- [ ] 能够对四个特点进行检验

10.`challengeCanBeResolved`接口

接口特点:
+ 调用`challengeExists`接口保证该`listing`的`challengeID`存在且`challenge map`中对应的该`challenge`处于`resolved`状态
+ 调用`voting`合约的`pollEnded`接口来确认投票已经结束

需要测试的重点:
- [ ] 能否调用`voting`中的接口成功结束投票

11.`resolveChallenge`接口

接口特点:
+ 调用`determineReward`接口计算出胜者方的奖励数值`reward`
+ 将`challenge`置为`resolved`状态
+ 调用`voting`合约的`getTotalNumberOfTokensForWinningOption`接口获取胜方在投票中花费的所有`token`数量,并将这个值储存在`totalTokens`中
+ 通过`voting`的`isPassed`接口判断挑战是否成功
+ 如果挑战失败,将`listing`置为`white`状态,在`unstakedDeposit`中添加`reward`的量,即将挑战者失败后需要付出的,作为胜者的`owner`奖励的资金添加进`listing`拥有者的余额中
+ 如果挑战成功,调用`resetListing`接口删除该`listing`并将剩下的余额返还给`owner`,同时将挑战者的奖励`reward`值的`token`发送给挑战者

需要测试的重点:
- [ ] `reward`奖励,`resetListing`返还的余额,`totalTokens`的数值是否正常
- [ ] 挑战失败后是否有为`listing`的`owner`添加余额
- [ ] 挑战成功后能够正常拿到奖励,`listing`是否被删除,`owner`是否有收回余额

12.`determineReward`接口

接口特点:
+ 保证`challenge`处于`resolved`状态并且投票已经结束
+ 如果`voting`的`getTotalNumberOfTokensForWinningOption`调取出的值为0(无人投票),就返回两倍的`challenge`的`stake`值(即所有的token)
+ 否则就返回两倍`stake`减去`challenge`中的`rewardPool`值

需要测试的重点:
- [ ] 能够获取正确的`reward`值

13.`claimReward`接口

接口特点:
+ 保证`challenge`的`tokenClaims`对交易发起者为`false`
+ 保证`challenge`处于`resolved`状态
+ 调用`voting`的`getNumPassingTokens`获取在本次投票中使用的所有`token`数量????
+ 计算出投票者的奖励数值`reward`为(在投票中的token总数 * `challenge`的奖励池 / `challenge`中的所有`token`数量)
+ 将发起者的`tokenClaims`状态置为`true`保证无法重复索取奖励
+ 发送`token`

需要测试的重点:
- [ ] 计算获取奖励数量的逻辑是否正确实现,获取的奖励数量都正常
- [ ] 无法重复索取奖励

#### 测试思路:

`owner-address1`
`challenger-address2`

+ 用`owner`部署合约
  + 部署流程:
    1. 部署`oep4 token`
    2. `owner`调用`token init`
    3. `owner`给`challenger`发送足够用的`token`
    4. 部署`Parameterizer`
    5. 部署`Registry`

+ challenge测试:
  + 无人投票-挑战者成功
    1. `owner`调用`apply`接口,传入`1*minDeposit`
    2. `owner`调用`deposit`接口,传入`1*minDeposit`
    3. `challenger`调用`challenge`接口
    4. 等待投票时间结束
    5. `challenger`调用`updateStatus`接口结束挑战
    + `listing`将被删除,所有`token`会被发放
    + `challenger`会获得`2*minDeposit`,`owner`会得到返还的`1*minDeposit`
  + 有人投票-挑战者成功
    1. `owner`调用`apply`接口
    2. `challenger`调用`chanllenge`接口
    3. `challenger`调用`commitVote`接口,传入`200 token`(试试投一样数量)
    4. `owner`调用`commitVote`接口,传入`100 token`
    5. 等待投票时间结束
    6. `challenger`调用`updateStatus`接口结束挑战
    + `listing`将被删除,所有`token`会被发放
    + `challenger`会获得`minDeposit*(100+dispensationPct)%`
    + `challenger`还可获得`voterReward`的`minDeposit*(100-dispensationPct)%`
  + 有人投票-挑战者失败
    1. `owner`调用`apply`接口
    2. `challenger`调用`challenge`接口
    3. `owner`调用`commitVote`接口
    4. 等待投票时间结束
    5. `challenger`调用`updateStatus`接口结束挑战
    + `listing`将被删除,所有`token`会被发放
    + `listing`的`unstakedDeposit`会增加`minDeposit * (100+dispensationPct)%`