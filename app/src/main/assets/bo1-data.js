window.BO1_DATA={
bo1_nacht:{name:"亡者之夜",english:"Nacht der Untoten",quest:"生存图 / 无传统主线",difficulty:"入门",time:"不限",source:"BO1 社区资料交叉核对 · 2026-09",requirements:["无电源","无特长","无武器强化机","核心目标是生存回合"],recorder:[{key:"round",label:"当前最高回合",placeholder:"例如 25"}],steps:[
{title:"开局控点",place:"出生房",action:"先用手枪点射配合刀击赚分，按需要开楼梯或 HELP 房路线。",success:"有足够点数买墙枪/开区域。",tips:"这张图没有主彩蛋，不要把无线电、箱子点位当成主线。"},
{title:"拿稳定武器",place:"楼上 / HELP 房 / 神秘箱",action:"优先拿一把稳定清怪武器；箱子位置固定在 HELP 房一侧体系。",success:"能稳定处理当前回合。",tips:"没有强化机，后期靠走位、陷阱式绕圈与弹药管理。"},
{title:"选刷怪点",place:"楼上或出生房",action:"选自己熟悉的路线训练僵尸，避免同时打开会破坏刷怪节奏的路线。",success:"怪群能被稳定聚拢并循环击杀。",tips:"纯生存图，目标就是尽可能高回合。"}]},
bo1_verruckt:{name:"疯人院",english:"Verrückt",quest:"生存图 / 无传统主线",difficulty:"中等",time:"不限",source:"BO1 社区资料交叉核对 · 2026-09",requirements:["双出生区联机时会分开","开启电源后两侧区域贯通","有特长，无武器强化机"],recorder:[{key:"round",label:"最高回合",placeholder:"例如 30"}],steps:[
{title:"推进到电源",place:"两侧出生区 → 后方电源房",action:"沿任一侧开门向后推进，到电源房拉闸。",success:"全图供电，特长机工作，两条路线连通。",tips:"联机出生在不同侧时，开电后才能完整会合。"},
{title:"补齐生存配置",place:"全图",action:"根据路线购买 Juggernog、Speed Cola 等特长，准备稳定墙枪。",success:"能持续补弹并承受失误。",tips:"没有 Pack-a-Punch，不要浪费时间找强化机。"},
{title:"利用电击陷阱控场",place:"长走廊/电网区域",action:"高回合用电击陷阱和绕圈路线清理密集怪群。",success:"回合推进稳定。",tips:"陷阱启动前确认自己有退路。"}]},
bo1_shi:{name:"死亡沼泽",english:"Shi No Numa",quest:"生存图 / 无传统主线",difficulty:"中等",time:"不限",source:"BO1 社区资料交叉核对 · 2026-09",requirements:["四间小屋的特长位置每局随机分配","无传统主线彩蛋","无 Pack-a-Punch"],recorder:[{key:"perks",label:"本局四小屋特长",placeholder:"医生/储物/通讯/钓鱼分别是什么"}],steps:[
{title:"打开中央区与小屋",place:"主建筑 → 沼泽四方向",action:"按需要打开四条木栈道和小屋，确认本局各特长位置。",success:"核心区域与补给路线可用。",tips:"每局特长分配会变化，建议记下来。"},
{title:"准备 Wunderwaffe / 稳定主武器",place:"神秘箱",action:"按生存需求抽取 Wunderwaffe DG-2 或稳定高伤害武器。",success:"有能快速处理高密度怪群的武器。",tips:"这张图没有强化机，Wonder Weapon 价值更高。"},
{title:"利用 Flogger 与沼泽路线",place:"主建筑外侧",action:"高回合以开阔区训练怪群，必要时使用 Flogger 陷阱清场。",success:"回合持续推进。",tips:"沼泽减速明显，别在狭窄木栈道被夹。"}]},
bo1_der:{name:"巨人",english:"Der Riese",quest:"生存 + Fly Trap 支线",difficulty:"中等",time:"不限",source:"BO1 社区资料交叉核对 · 2026-09",requirements:["先开电","连接3台传送器可解锁 Pack-a-Punch","Fly Trap 属于支线，不是主线结局"],recorder:[{key:"tele",label:"已连接传送器",placeholder:"A / B / C"}],steps:[
{title:"开启电源",place:"中央电源区",action:"开门推进到主电闸并启动。",success:"地图供电，陷阱/特长等系统工作。",tips:"开电会改变刷怪路线，提前留好撤退方向。"},
{title:"连接3台传送器",place:"Teleporter A / B / C → 主机",action:"逐台在传送器端启动倒计时，再在时间内跑回出生主机互动完成连接。",success:"三盏连接灯全部亮。",tips:"联机可分工，一人守主机附近更省时间。"},
{title:"解锁武器强化机",place:"出生主机后方",action:"三台传送器全部链接后，Pack-a-Punch 门打开。",success:"可以升级武器。",tips:"高回合优先升级一把能持续补弹的武器。"},
{title:"Fly Trap 支线",place:"地图外控制面板 → 三个玩具",action:"用强化后的武器射击地图外 Fly Trap 控制面板，听到提示后依次寻找并射击/命中三件隐藏玩具。",success:"三件玩具全部触发，听到 Samantha 的反馈。",tips:"这是支线彩蛋，不影响生存和 Pack-a-Punch。"}]},
bo1_kino:{name:"剧院",english:"Kino der Toten",quest:"生存图 / 无传统主线",difficulty:"入门",time:"不限",source:"BO1 社区资料交叉核对 · 2026-09",requirements:["开电后可使用舞台传送器","连接传送器后可进入放映室强化武器"],recorder:[{key:"round",label:"最高回合",placeholder:"例如 35"}],steps:[
{title:"一路推进到舞台",place:"大厅 → 更衣区/巷道 → 舞台",action:"按任一路线开门到舞台并拉下电源。",success:"剧院灯亮，幕布打开，特长机工作。",tips:"开电后爬行怪会开始参与普通回合。"},
{title:"连接传送器",place:"舞台传送器 → 大厅出生点",action:"先在舞台启动传送器，再跑到出生大厅的链接面板完成配对。",success:"传送器显示可用。",tips:"每次使用后要等冷却并重新链接。"},
{title:"传送到放映室强化",place:"舞台 → 放映室",action:"进入已链接传送器，传送到放映室，用 Pack-a-Punch 升级武器。",success:"武器完成强化并被送回地图。",tips:"放映室停留时间有限。"},
{title:"高回合路线",place:"舞台 / 巷道",action:"在开阔区训练怪群，配合 Thundergun 和舞台陷阱清场。",success:"稳定推进回合。",tips:"这张图没有传统主线结局。"}]},
bo1_five:{name:"五角大楼",english:"Five",quest:"生存图 / 无传统主线",difficulty:"困难",time:"不限",source:"BO1 社区资料交叉核对 · 2026-09",requirements:["开启地下电源","DEFCON 系统可临时打开 Pack-a-Punch 区域","Pentagon Thief 会偷玩家武器"],recorder:[{key:"round",label:"最高回合",placeholder:"例如 25"}],steps:[
{title:"进入地下并开电",place:"办公层 → 战情室 → 实验室",action:"通过电梯一路下到实验室，找到主电源并开启。",success:"特长、传送器与 DEFCON 系统开始工作。",tips:"路线窄，开电前留一把近距离救命武器。"},
{title:"启动5个 DEFCON 开关",place:"战情室两层",action:"依次把 DEFCON 状态从 1 推到 5。",success:"传送门通往总统紧急会议室，Pack-a-Punch 可使用。",tips:"DEFCON 会在一段时间后恢复，需要重新启动。"},
{title:"应对 Pentagon Thief",place:"偷窃者回合",action:"小偷出现后会锁定一名玩家并尝试偷走当前手持武器；集中火力在他得手前击杀。",success:"保住武器；快速击杀可获得额外奖励。",tips:"别在小偷贴脸时切出最关键的武器。"},
{title:"高回合训练",place:"战情室/电梯路线",action:"利用开阔环形区域和电梯拉开距离，持续训练清怪。",success:"稳定推进回合。",tips:"Five 没有传统主彩蛋。"}]},
bo1_ascension:{name:"升天",english:"Ascension",quest:"Casimir Mechanism",difficulty:"中等",time:"约45–90分钟",source:"COD Zombies Guides · 2026-07-07",requirements:["必须4人","已开电","Gersh Device","强化 Thundergun（Zeus Cannon）","Matryoshka Dolls","强化 Ray Gun"],recorder:[{key:"luna",label:"LUNA 进度",placeholder:"L/U/N/A"}],steps:[
{title:"Gersh 吸走发电机并启动电脑",place:"PHD/Widow 路线 rubble → Stamin-Up 月球着陆器",action:"把 Gersh Device 扔到废墟后的小型发电机旁把它吸走，再到 Stamin-Up 着陆器角落互动亮屏电脑。",success:"电脑显示符号，任务正式推进。",tips:"Gersh 扔偏会失败，听到 Samantha 笑声就要重来。"},
{title:"猴子回合四人同时按按钮",place:"Jug / Speed / Stamin-Up / PHD(Widow) 附近",action:"等 Space Monkey 回合，四名玩家分别守四个按钮并同时按下。",success:"听到成功提示，任务装置增加一盏灯。",tips:"必须同一时间按，不能逐个。"},
{title:"强化机门口压力板站满2分钟",place:"火箭发射后的 Pack-a-Punch 房外",action:"先发射火箭打开强化机区域，四人一起站在墙钟前的大压力板上整整2分钟。",success:"核爆结束当前回合，装置第三盏灯亮。",tips:"任何人离开压力板都会重置计时。"},
{title:"乘月球着陆器拼出 LUNA",place:"Spawn / Stamin-Up / Speed-Cola-Sickle",action:"按路线乘坐着陆器收集空中字母：出生→Stamin-Up 得L；Stamin-Up→出生得U；出生→Speed/Sickle 得N；Speed/Sickle→Stamin-Up 得A。",success:"空中拼成 LUNA，装置四灯全亮。",tips:"每段都要有人站在着陆器里。"},
{title:"白色光球最终充能",place:"Stamin-Up 附近装置",action:"在发光白球处扔 Gersh Device，并在 Gersh 持续时间内用强化 Ray Gun、Zeus Cannon 和 Matryoshka 集中输出。",success:"白球飞向天空，Gersh 道谢。",tips:"火力不足就先补弹和重抽所需道具。"}]},
bo1_cotd:{name:"亡者的召唤",english:"Call of the Dead",quest:"Stand-in（单人）/ Ensemble Cast（联机）",difficulty:"中等",time:"约60–120分钟",source:"COD Zombies Guides + 社区攻略 · 2026-09",requirements:["开电","V-R11","爆炸物","联机完整路线需2人以上"],recorder:[{key:"route",label:"本局路线",placeholder:"单人 Stand-in / 联机 Ensemble Cast"}],steps:[
{title:"开启电源并找到 Ultimis 门",place:"船上电源 → PHD 下方锁门",action:"开电后到锁门处近战触发门内 Ultimis 对话。",success:"开始索要保险丝。",tips:"单人和联机到这里相同。"},
{title:"装上保险丝",place:"锁门附近房间",action:"在附近候选桌面找到 Fuse，拿回锁门旁的电箱安装。",success:"门内继续对话并要求处理发电机。",tips:"保险丝位置是固定候选范围，不在全图乱找。"},
{title:"炸掉4台红色发电机",place:"地图四处红灯发电机",action:"用手雷、Semtex、Scavenger 等爆炸伤害破坏四台红色发电机。",success:"四台全部熄灭。",tips:"普通子弹无效。"},
{title:"联机额外：Vodka + 四台无线电",place:"船体与地图多处",action:"如果是 Ensemble Cast：两人配合拿 Vodka（一人打落，一人接住）并放入门旁管道；之后严格按顺序互动4台无线电。单人 Stand-in 跳过这一整步。",success:"联机路线获得后续线索。",tips:"别把联机专属步骤硬塞进单人流程。"},
{title:"调整舰桥方向盘与拉杆",place:"船桥驾驶室",action:"把方向盘转到棕色把手大约5点方向；左侧拉杆操作1次，最右拉杆操作3次。",success:"灯塔出现绿色光束。",tips:"这是单人和联机都会用到的关键步骤。"},
{title:"联机额外：雾笛与灯塔转盘",place:"灯塔外围 / 灯塔内部",action:"Ensemble Cast 按正确顺序操作4个雾笛，再把灯塔四层数字转盘从上到下设为 2-7-4-6。单人跳过。",success:"联机路线准备好灯塔光束。",tips:"四人/多人先分站位再动机关。"},
{title:"V-R11 把僵尸变成人并送进绿光",place:"灯塔底部绿光",action:"用 V-R11 射一只僵尸让其变成人，让他进入绿色光束并向上漂；在到顶前击杀他。",success:"Golden Rod / Vril Device 掉落。",tips:"如果人类走偏，重新做一只。"},
{title:"把 Golden Rod 交给 Ultimis",place:"锁门旁管道",action:"拾取 Golden Rod 放进门边装置，等待对话/充能结束。",success:"Ultimis 准备离开。",tips:"耐心等语音完整跑完。"},
{title:"修复保险丝箱结束任务",place:"锁门旁保险丝箱",action:"按提示近战/互动保险丝箱完成最后修复。",success:"Ultimis 传送离开，单人/联机对应成就完成。",tips:"这一步后任务结束。"}]},
bo1_shang:{name:"香格里拉",english:"Shangri-La",quest:"Time Travel Will Tell",difficulty:"困难",time:"约90–120分钟",source:"COD Zombies Guides · 2026-07-07",requirements:["必须4人","开电","31-79 JGb215（后续需强化为 Fractalizer）","Spikemores","爆炸物","Napalm Zombie"],recorder:[{key:"panels",label:"符号/机关记录",placeholder:"需要时记符号或站位"}],steps:[
{title:"四人同时按出生区石按钮进入 Eclipse",place:"出生区四块石按钮",action:"四名玩家同时站/按对应按钮进入日食状态。",success:"天空变暗，任务场景进入 Eclipse。",tips:"后续多步失败后要重新触发 Eclipse。"},
{title:"匹配神庙地砖符号",place:"地图两侧地砖区域",action:"两组玩家分别观察地砖图案，踩出互相匹配的符号对。",success:"全部符号配对完成。",tips:"一次只确认一对，踩错会重置。"},
{title:"完成水滑梯/压力机关",place:"水滑梯终点与相关压力板",action:"按社区固定流程让玩家从滑梯通过并配合站位触发机关。",success:"听到下一段 Brock/Gary 对话。",tips:"四人站位是硬要求。"},
{title:"缩小并移动水晶",place:"洞穴/水晶机关",action:"用 31-79 JGb215 缩小指定水晶/障碍，并按机关路线推进。",success:"水晶进入正确位置。",tips:"baby gun 弹药珍贵，别误射普通怪。"},
{title:"Napalm 点燃4处煤气泄漏",place:"地下隧道",action:"把一只 Napalm Zombie 引过4处煤气泄漏，让它们全部点燃，再在安全位置处理掉 Napalm。",success:"四处火焰全部点亮。",tips:"不要提前把 Napalm 打爆。"},
{title:"Spikemore 封住4个墙洞",place:"隧道墙面",action:"用 Spikemore 的爆炸效果把四个指定墙洞全部处理。",success:"四洞完成。",tips:"BO3 版对应改用 Trip Mine。"},
{title:"近战12块符文板并破坏陷阱",place:"地图多处",action:"找到12块隐藏/分布的符文板并按要求近战，再处理指定绊索/陷阱。",success:"机关给出后续音效。",tips:"建议四人分区数数量，防漏。"},
{title:"设置轮盘/无线电密码",place:"泥浆区轮盘与无线电",action:"按固定组合输入 16、1、3、4 的机关信息，完成对应无线电/轮盘步骤。",success:"进入锣与水晶阶段。",tips:"不要把数字顺序倒过来。"},
{title:"找4个正确的锣",place:"全图8个锣",action:"逐个测试锣，确认4个发出正确反馈的锣并全部敲响。",success:"水晶机关准备完成。",tips:"错误锣不会推进。"},
{title:"Fractalizer 射水晶取得炸药",place:"水晶区域",action:"把 baby gun 强化为 The Fractalizer，按流程射击水晶，让能量移动并最终掉出炸药。",success:"拿到 Dynamite。",tips:"必须是强化后的 Fractalizer。"},
{title:"缩小115陨石并炸墙拿 Focusing Stone",place:"最终神庙区域",action:"用 Fractalizer 缩小115陨石，放置炸药炸开最终墙体，取得 Focusing Stone。",success:"Time Travel Will Tell 完成。",tips:"只有一名玩家实际获得石头，但任务算全队完成。"}]},
bo1_moon:{name:"月球",english:"Moon",quest:"Richtofen's Grand Scheme",difficulty:"困难",time:"约45–120分钟",source:"COD Zombies Guides · 2026-07-07",requirements:["BO1 需2人以上","必须有 Richtofen","至少一名玩家此前完成 Call of the Dead + Shangri-La 主任务","开电","Wave Gun","Hacker","QED","Gersh Device"],recorder:[{key:"simon",label:"Simon Says 顺序",placeholder:"红绿蓝黄…"}],steps:[
{title:"Simon Says 第一轮",place:"Receiving Bay 外 Tunnel 6 前四台电脑",action:"按电脑闪烁的颜色顺序复现，共5轮，序列会逐步变长。",success:"四台电脑最后熄灭。",tips:"从左到右对应红、绿、蓝、黄。"},
{title:"实验室 Hacker 60秒小游戏",place:"实验室二楼按钮墙 + 8个白面板",action:"先用 Hacker 黑入按钮墙任一按钮；60秒内在实验室三层范围找到4个亮绿灯白面板并黑入，随后快速按亮按钮墙的4个按钮。",success:"4个墙按钮全部发光。",tips:"失败可再花500点重新开始。"},
{title:"等 Excavator Pi 挖穿 Tunnel 6 并复位",place:"Tunnel 6 / 接收区控制台",action:"等 Excavator Pi 破坏 Tunnel 6，再用 Hacker 在对应控制台把它移开。",success:"Tunnel 6 可重新进入并出现 Vril Sphere。",tips:"必须是 Pi，不是另外两台挖掘机。"},
{title:"护送 Vril Sphere 到 MPD",place:"Tunnel 6 → 出生上方卫星 → Stamin-Up 房 → MPD",action:"近战球让它移动；卡在出生上方卫星时用 Wave Gun 射；卡在 Stamin-Up 房顶时用枪/爆炸物打落，直到它进入 MPD 的 Vril Interface。",success:"球卡入 MPD 中央接口。",tips:"沿路提前开门。"},
{title:"25魂打开 MPD",place:"MPD 右侧灵魂罐",action:"在出现的玻璃罐附近击杀25只僵尸，满后拉右侧开关打开 MPD。",success:"Samantha 出现，完成 Cryogenic Slumber Party 阶段。",tips:"这还不是完整任务终点。"},
{title:"取得六角板与S形电缆",place:"Area 51 + Laboratory",action:"Area 51 用爆炸物打落传送器右侧架子上的两块六角板，用 Gersh 把板送到传送垫并带回月球，再用 QED 让它们落到出生电脑旁机器上；同时在实验室寻找S形电缆并连接。",success:"电脑、六角板机器和电缆全部就位。",tips:"S形电缆有多个实验室候选点。"},
{title:"给 Golden Rod / Vril Device 充能",place:"出生电脑",action:"Richtofen 把 Golden Rod 放在两块六角板中间，连续互动电脑直到键盘声和对话结束。",success:"Golden Rod 发紫光，可取回。",tips:"BO1 必须是 Richtofen 操作。"},
{title:"四个灵魂罐各填25魂并交换灵魂",place:"MPD 四角",action:"在4个新灵魂罐旁分别杀25只僵尸，全部装满后把已充能 Vril Device 放回正面接口。",success:"Richtofen 与 Samantha 交换灵魂，Richtofen 获得永久全特长。",tips:"四罐都要满。"},
{title:"QED → Simon Says 第二轮 → Gersh",place:"MPD / Tunnel 6 前电脑",action:"先对 MPD 前的 Vril Sphere 扔 QED；回四台电脑完成更难的 Simon Says；成功后在电脑右侧地面 Vril Sphere 附近扔 Gersh Device。",success:"火箭倒计时启动。",tips:"QED 与 Gersh 顺序不要反。"},
{title:"见证地球毁灭",place:"Receiving Bay 外",action:"等待3枚火箭发射并击中地球。",success:"Big Bang Theory / 完整 Moon 主任务完成。",tips:"BO3 版本需求不同，单独看 COD12→Moon。"}]}
};
window.BO1_ORDER=["bo1_nacht","bo1_verruckt","bo1_shi","bo1_der","bo1_kino","bo1_five","bo1_ascension","bo1_cotd","bo1_shang","bo1_moon"];