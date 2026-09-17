window.BO2_DATA={
bo2_bus:{name:"公交车站",english:"Bus Depot Survival",quest:"生存图 / 无传统主线",difficulty:"入门",time:"不限",source:"BO2 社区资料交叉核对 · 2026-09",requirements:["纯生存小图","无电源","无特长","无武器强化机"],recorder:[{key:"round",label:"最高回合",placeholder:"例如 20"}],steps:[
{title:"开局攒分",place:"公交车站",action:"低回合优先点射+刀击攒分，尽快拿稳定墙枪。",success:"有足够点数维持弹药。",tips:"这里没有主彩蛋，也没有强化机。"},
{title:"控制刷怪口",place:"站内/站外",action:"根据人数选择站内守窗或站外绕圈，避免多人互相堵路线。",success:"怪群可持续被聚拢并清掉。",tips:"纯生存图，后期武器伤害衰减明显。"}]},
bo2_farm:{name:"农场",english:"Farm Survival",quest:"生存图 / 无传统主线",difficulty:"入门",time:"不限",source:"BO2 社区资料交叉核对 · 2026-09",requirements:["有部分特长","无 Pack-a-Punch","无主彩蛋"],recorder:[{key:"round",label:"最高回合",placeholder:"例如 30"}],steps:[
{title:"开区域并拿核心特长",place:"农舍/谷仓",action:"先拿 Juggernog，再按武器与人数补 Speed Cola、Double Tap 等。",success:"基础生存配置成型。",tips:"不要在狭窄楼梯长期守点。"},
{title:"在开阔区训练",place:"农场外场",action:"利用开阔地拉怪，集中清掉后再补弹。",success:"稳定推进回合。",tips:"没有强化机，弹药经济比击杀速度更重要。"}]},
bo2_town:{name:"小镇",english:"Town Survival",quest:"生存图 / 无传统主线",difficulty:"中等",time:"不限",source:"BO2 社区资料交叉核对 · 2026-09",requirements:["有特长","有 Pack-a-Punch","地面岩浆持续造成危险"],recorder:[{key:"round",label:"最高回合",placeholder:"例如 40"}],steps:[
{title:"拿 Juggernog 并控制岩浆路线",place:"小镇主街",action:"优先买 Juggernog，熟悉两栋建筑与街道之间的跳跃/绕圈路线。",success:"能稳定通过岩浆区不被堵死。",tips:"着火僵尸死亡会爆炸，贴脸击杀要留血量。"},
{title:"强化主武器",place:"镇中心 Pack-a-Punch",action:"攒够点数后强化一把主武器，保留另一把可补墙弹的枪。",success:"中高回合输出稳定。",tips:"强化机暴露在开阔区，先清场再操作。"},
{title:"外场训练",place:"主街/酒吧外",action:"大范围绕圈聚怪后集中清理。",success:"回合稳定推进。",tips:"这张图没有主彩蛋。"}]},
bo2_nuketown:{name:"核弹镇僵尸",english:"Nuketown Zombies",quest:"生存图 / 随机空投机制",difficulty:"中等",time:"不限",source:"BO2 社区资料交叉核对 · 2026-09",requirements:["电源与特长机会随回合从天而降","没有传统主线彩蛋"],recorder:[{key:"drops",label:"本局空投顺序",placeholder:"电源/Jug/Speed/Double Tap/PaP…"}],steps:[
{title:"先确认本局空投",place:"两栋房屋/后院",action:"随着回合推进听警报并观察从天而降的机器，记录本局电源、特长和 Pack-a-Punch 到达顺序。",success:"知道当前能买什么。",tips:"顺序每局随机，不能照固定攻略硬等某一回合。"},
{title:"电源落地后开启",place:"电源机空投点",action:"找到落地的电源装置并开启。",success:"已落地的特长/系统开始可用。",tips:"如果 Jug 还没落地就只能继续等。"},
{title:"拿生存配置并强化",place:"对应空投点",action:"Juggernog 与 Pack-a-Punch 出现后尽快完成核心配置。",success:"能进入高回合。",tips:"纯生存图，没有传统主任务结局。"}]},
bo2_tranzit:{name:"迁徙",english:"Tranzit",quest:"Tower of Babble",difficulty:"中等",time:"约60–150分钟",source:"COD Zombies Guides · 2026-07-12",requirements:["Maxis 路线至少2人且任务阶段电源必须关闭","Richtofen 路线任意人数；单人必须是 Stuhlinger 且电源开启","Maxis：EMP、2个 Turbine","Richtofen：Jet Gun、EMP、爆炸物"],recorder:[{key:"branch",label:"选择路线",placeholder:"Maxis / Richtofen"},{key:"lamps",label:"路灯/涡轮站位",placeholder:"记录玩家负责路灯"}],steps:[
{title:"选择阵营并准备道具",place:"全图",action:"先决定做 Maxis 还是 Richtofen。两条路线电源状态相反，不能混做。",success:"队伍明确同一条路线并准备对应道具。",tips:"官方时间线采用 Maxis 结局。"},
{title:"[Maxis] 开电释放 Avogadro 后关闭电源",place:"Power Station",action:"组装并打开电源，等 Maxis/地图反馈确认 Avogadro 条件已建立，然后重新把电源关掉。",success:"任务阶段处于断电状态。",tips:"Maxis 后续必须保持断电。"},
{title:"[Maxis] 玉米地 Pylon：两台 Turbine + EMP Avogadro",place:"Cornfield Pylon",action:"两名玩家把 Turbine 放在 Pylon 下方指定位置，等闪电条件与 Avogadro 出现，把它引到塔下后用 EMP 消灭；EMP 不要同时炸坏两台 Turbine。",success:"Maxis 确认塔已获得能量。",tips:"先把 Avogadro 拉准再扔 EMP。"},
{title:"[Maxis] 两盏路灯完成最终供能",place:"绿色路灯传送点",action:"按人数方案把 Turbine 放在两处正确路灯下，使两点同时有供能。",success:"Tower of Babble 的 Maxis 路线完成。",tips:"两人做时按社区的轮换方法处理 Turbine，别提前收走。"},
{title:"[Richtofen] 开电并用 Jet Gun 加热 Pylon",place:"Cornfield Pylon",action:"保持电源开启，在塔下持续使用 Jet Gun，直到过热并最终碎裂/被任务接受。",success:"Richtofen 给出下一阶段语音。",tips:"单人必须是 Stuhlinger 才能听到 Richtofen。"},
{title:"[Richtofen] 塔下累计爆炸击杀",place:"Cornfield Pylon",action:"在 Pylon 下用爆炸伤害累计击杀约25只僵尸，直到 Richtofen 确认。",success:"塔的能量阶段完成。",tips:"不要把击杀拉离塔太远。"},
{title:"[Richtofen] EMP 四盏绿色路灯",place:"4个传送路灯",action:"让四盏绿色路灯在任务窗口中都被 EMP 命中。四人可一人一处；少人需要利用 Denizen 传送与时机技巧。",success:"四盏灯都被关闭并触发任务完成。",tips:"单人理论可做但操作非常苛刻，建议联机。"}]},
bo2_dierise:{name:"大厦",english:"Die Rise",quest:"High Maintenance",difficulty:"困难",time:"约60–120分钟",source:"COD Zombies Guides · 2026-07-07",requirements:["必须4人","开电","建好 Nav Card Table","中途选择 Maxis 或 Richtofen","最终需要 Galvaknuckles"],recorder:[{key:"branch",label:"选择路线",placeholder:"Maxis / Richtofen"},{key:"floor",label:"地板符号顺序",placeholder:"记录试出的4符号顺序"},{key:"mahjong",label:"麻将牌配对",placeholder:"颜色→方向→数字"}],steps:[
{title:"四人同时站电梯顶部金色符号",place:"4个电梯顶",action:"四名玩家分别站到电梯顶部的金色符号上并保持同时激活。",success:"听到确认音效，符号阶段推进。",tips:"电梯会上下移动，先分配好位置。"},
{title:"试出4个地面符号的随机顺序",place:"地图4个金色地面符号",action:"四人按试错法依次踩符号，找出当局正确的完整顺序。",success:"四个符号全部锁定/获得任务反馈。",tips:"顺序每局随机，记事区直接记录。"},
{title:"狙击龙嘴里的两颗球",place:"屋顶龙雕像",action:"用狙击步枪射击两座龙雕像嘴里的球，让它们脱落并进入任务流程。",success:"两颗球进入下一阶段。",tips:"SVU 墙枪可直接使用。"},
{title:"[Maxis] Buddha 房连续15杀",place:"Buddha Room 一层",action:"确保任务期间所有击杀都发生在 Buddha Room 一层，连续击杀15只。",success:"Maxis 说“Reincarnation will reveal the way forward”。",tips:"有人在房外误杀会重置。"},
{title:"[Maxis] 强化 Ballistic Knife 步骤",place:"Buddha Room",action:"让一名还没买 Bowie/Galvaknuckles 的玩家拿 Ballistic Knife 并 Pack-a-Punch，在 Buddha Room 按任务要求射击/击杀。",success:"Maxis 给出后续确认。",tips:"提前买了近战升级的玩家不要承担这一步。"},
{title:"[Maxis] 四个 Trample Steam 对准狮子符号",place:"四处狮子/符号点",action:"四人把 Trample Steam 摆在对应狮子符号方向，并把两颗任务球按 Maxis 路线送入/激活。",success:"Maxis 路线进入最终麻将步骤。",tips:"装置朝向很关键。"},
{title:"[Richtofen] Sliquifier 旋转两颗龙球",place:"龙球位置",action:"用 Sliquifier 持续射击两颗球，让它们按要求旋转/充能。",success:"Richtofen 给出确认。",tips:"不要在 Maxis 路线做这步。"},
{title:"[Richtofen] 四个 Trample Steam 对准金色僵尸符号",place:"四个任务点",action:"四人按金色僵尸符号摆好 Trample Steam 并激活。",success:"Richtofen 路线进入最终麻将步骤。",tips:"四台装置要全部正确。"},
{title:"麻将牌推导 Pylon 四面顺序",place:"全图11候选点 → Pylon",action:"找出8块麻将牌，按颜色配成4对，利用方向与数字推导四个方位的击打顺序。",success:"得到唯一四方向顺序。",tips:"牌位每局变化，别照搬别人的数字。"},
{title:"按顺序 Galvaknuckle Pylon 四面",place:"Pylon",action:"四人按推导出的顺序用 Galvaknuckles 近战 Pylon 四面。",success:"塔体出现对应阵营颜色电流，全员获得奖励，High Maintenance 完成。",tips:"每回合只能正式尝试一次，错了要翻回合。"}]},
bo2_mob:{name:"监狱",english:"Mob of the Dead",quest:"Pop Goes the Weasel",difficulty:"中等",time:"约45–90分钟",source:"COD Zombies Guides · 2026-07-12",requirements:["至少2人","必须有一名 Weasel","Warden's Key","Hell's Retriever"],recorder:[{key:"flights",label:"已完成桥梁往返",placeholder:"0 / 1 / 2 / 3"}],steps:[
{title:"拿典狱长钥匙",place:"典狱长办公室外或食堂/淋浴区域上方候选点",action:"用 Afterlife 给装置通电/处理钥匙机关，拿到 Warden's Key。",success:"钥匙进入团队道具栏。",tips:"钥匙每局在两个主要候选区域之一。"},
{title:"收集5个飞机零件并组装",place:"监狱全图 → 屋顶",action:"依次处理洗衣房、码头、医务/典狱长相关区域等机关，收齐5个 Icarus 飞机部件，在屋顶工作台组装。",success:"屋顶飞机完整可乘坐。",tips:"多数零件都和 Afterlife / Warden's Key 交互有关。"},
{title:"第一次飞金门大桥",place:"屋顶 → Golden Gate Bridge",action:"全员登机飞往桥上。",success:"到达桥梁区域。",tips:"想做完整主任务，后续还要重复往返。"},
{title:"喂满3个狗头拿 Hell's Retriever",place:"New Industries / Cell Block / Docks",action:"分别在三个 Cerberus 狗头附近击杀僵尸直到狗头消失，再从地下快速移动路线经过的武器点拾取 Hell's Retriever。",success:"投掷物变为 Hell's Retriever。",tips:"这是主任务硬前置。"},
{title:"累计完成3次桥梁往返",place:"Alcatraz ↔ Golden Gate Bridge",action:"修复飞机并完成总计3次去桥/返回的循环。",success:"主任务最后阶段解锁。",tips:"不是只飞一次。"},
{title:"Citadel Afterlife 输入4组数字",place:"Citadel Tunnels",action:"在 Afterlife 状态依次输入 101、872、386、481。",success:"开始播放/开放通往屋顶的最终语音路线。",tips:"四组是固定值。"},
{title:"沿路收集5段音频记录",place:"Citadel → 屋顶路线",action:"沿最终路线逐个触发5个音频日志/耳机提示，直到到达屋顶。",success:"飞机变为最终幽灵状态。",tips:"漏一个会卡最终登机。"},
{title:"全员 Afterlife 登最终飞机",place:"屋顶",action:"所有玩家都进入 Afterlife，再登上幽灵飞机飞往金门大桥。",success:"桥上出现各自的肉身。",tips:"必须全队同步推进。"},
{title:"复活肉身并进行 Weasel 对决",place:"Golden Gate Bridge",action:"各自复活肉身后，Weasel 与其他囚犯进入最终对决。",success:"Weasel 杀死其他人=打破循环（正史）；其他人杀 Weasel=继续循环。",tips:"如果你只是想看正史结局，让 Weasel 获胜。"}]},
bo2_buried:{name:"埋葬",english:"Buried",quest:"Mined Games",difficulty:"困难",time:"约45–120分钟",source:"COD Zombies Guides · 2026-07-07",requirements:["推荐4人；最终理论可3人但很难","Paralyzer","Time Bomb","Galvaknuckles 或 Bowie Knife","Richtofen 路线需要 Vulture Aid"],recorder:[{key:"branch",label:"选择路线",placeholder:"Maxis / Richtofen"},{key:"maze",label:"迷宫开关顺序",placeholder:"红/绿/蓝/黄顺序"},{key:"signs",label:"Richtofen 三个牌子",placeholder:"记录3个解码地点"}],steps:[
{title:"给4颗任务球供能",place:"糖果店-酒吧间 / 教堂左墓地 / Lunger Undermines / 女巫宅后",action:"两条路线共同前置：用 Paralyzer 持续加热每颗球直到变白并“叮”一声，或用 Subsurface Resonator 摧毁。",success:"四颗球全部完成。",tips:"完成后必须选择 Maxis 或 Richtofen，不要混线。"},
{title:"[Richtofen] 组装 Guillotine",place:"指定工作点",action:"收齐卫星盘、线缆、水晶、天线四个零件并装到 Guillotine。",success:"Guillotine 完整。",tips:"Vulture Aid 后面会用于看任务痕迹。"},
{title:"[Richtofen] 打落并充满幽灵灯笼",place:"幽灵宅/小镇",action:"用爆炸物把空中的 Ghost Lantern 打落，捡起后通过击杀女巫给灯笼充能，再把充满的灯笼放到 Gunsmith 屋顶指定位置。",success:"墙上出现密码/符号线索。",tips:"灯笼没充满放不上去。"},
{title:"[Richtofen] 解三块牌子并护送 Wisp",place:"小镇三处线索 → Guillotine",action:"解出3个符号/牌子地点并近战激活；随后利用 Vulture Aid 看见 Wisp，沿路线保护它回到 Guillotine，并用发光僵尸击杀给装置充能。",success:"Guillotine 获得足够能量。",tips:"Wisp 被打断就要重做。"},
{title:"[Richtofen] Round Infinity 找开关",place:"Guillotine",action:"先把 Time Bomb 放在 Guillotine 附近再启动装置，进入 Round Infinity；在地图寻找 Victis 尸体并取得任务开关，然后回到正常时间安装。",success:"开关安装完成。",tips:"Time Bomb 放置顺序不要错。"},
{title:"[Maxis] 组装 Gallows 并充 Ghost Lantern",place:"Gallows / 女巫宅",action:"走 Maxis 路线时改为收集并组装 Gallows 所需部件；按 Maxis 规则把 Ghost Lantern 充能并安装。",success:"Maxis 给出下一步提示。",tips:"这条和 Guillotine 路线互斥。"},
{title:"[Maxis] Wisp 与 Bell 步骤",place:"小镇 → 女巫宅/建筑铃铛",action:"按 Maxis 路线处理 Wisp，并根据线索让队员在对应建筑敲响正确铃铛/完成同步机关。",success:"Maxis 路线进入迷宫阶段。",tips:"建议一人读线索，其他人站铃铛位置。"},
{title:"迷宫四个彩色开关试出顺序",place:"女巫宅后迷宫",action:"找到迷宫中的4个彩色开关，通过试错确定当局正确顺序并全部按下。",success:"四开关顺序被接受。",tips:"顺序每局随机，立刻记录。"},
{title:"最终 Sharpshooter 靶场",place:"小镇多个射击位置",action:"全队站到规定射击点，同时开始最终靶场挑战，快速打掉自己负责区域的所有目标。",success:"所有目标在同一次尝试中全部命中，Mined Games 完成并锁定所选阵营结局。",tips:"这是最吃配合的一步，先分区练熟再正式触发。"}]},
bo2_origins:{name:"起源",english:"Origins",quest:"Little Lost Girl",difficulty:"极难",time:"约90–180分钟",source:"COD Zombies Guides · 2026-07-07",requirements:["可单人完成","4把元素 Staff 及升级","G-Strike","Maxis Drone","One-Inch Punch"],recorder:[{key:"staffs",label:"Staff 进度",placeholder:"风/冰/火/雷：制作/升级"},{key:"robots",label:"机器人站位",placeholder:"需要时记脚/Staff"}],steps:[
{title:"制作并升级四把 Staff",place:"全图 / Crazy Place",action:"收集风、冰、火、雷四把 Staff 的唱片、零件和水晶并制作；分别完成各自升级谜题，把4把全部升级。",success:"四把 Ultimate Staff 全部可用。",tips:"多人可分工；单人要规划好拿枪顺序。"},
{title:"准备 G-Strike、Maxis Drone、One-Inch Punch",place:"全图",action:"完成石板净化拿 G-Strike；收集3个 Maxis Drone 零件并制作；用4个发电机附近灵魂箱完成 One-Inch Punch。",success:"三项前置都到手。",tips:"这些不是可选道具，主任务后面都会用到。"},
{title:"Secure the Keys：把 Staff 放入对应机关",place:"三台机器人 + Excavation Site",action:"按版本对应规则把升级 Staff 放到三台巨型机器人内部基座与挖掘场底部基座。",success:"任务进入 Rain Fire。",tips:"BO2 与 BO3 的部分 Staff 放置逻辑存在版本差异，以当前游戏版本反馈为准。"},
{title:"Rain Fire：机器人内按钮 + G-Strike 炸封印",place:"中间机器人 / Generator 5 附近封印",action:"进入正确机器人脚内按红色按钮，地面队友/单人快速向封印位置投 G-Strike，让导弹轰开地面封印。",success:"封印炸开。",tips:"时间窗很短，提前站好投掷点。"},
{title:"Unleash the Horde：击杀 Panzer 群",place:"地图中部",action:"封印打开后会刷大量 Panzer Soldat，集中火力全部击杀。",success:"Panzer 波清空。",tips:"雷 Staff、冰 Staff 或强力强化枪都能提高容错。"},
{title:"Skewer the Winged Beast",place:"教堂上空 → Excavation/地图指定点",action:"进入 Zombie Blood，射下天空中发光的隐形飞机，再在 Zombie Blood 状态找到并击杀只能此时看见的白色特殊僵尸。",success:"获得任务物品/推进语音。",tips:"先把飞机打下来，再找地面目标。"},
{title:"Wield a Fist of Iron：升级铁拳",place:"四个 Staff 基座/地下区域",action:"用 One-Inch Punch 击杀带白色烟雾的特殊圣殿骑士，把拳套升级为 Iron Fist。",success:"近战拳套升级完成。",tips:"只打任务指定的白烟骑士。"},
{title:"Raise Hell：四 Staff 回 Crazy Place 收魂",place:"Crazy Place",action:"把四把 Staff 放回各自 Crazy Place 基座，在中央区域持续击杀僵尸给能量充魂。",success:"上方能量/传送光束完成。",tips:"完成前别把 Staff 乱拔。"},
{title:"Freedom：Maxis Drone 进入光束",place:"Crazy Place 中央",action:"把 Maxis Drone 放入中央上方光束/传送区域。",success:"Samantha 被释放，Little Lost Girl 完成。",tips:"想继续打可以不立即结束；按版本交互触发最终动画。"}]}
};
window.BO2_ORDER=["bo2_bus","bo2_farm","bo2_town","bo2_nuketown","bo2_tranzit","bo2_dierise","bo2_mob","bo2_buried","bo2_origins"];