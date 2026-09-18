"""Targeted draft corrections only; article-level review status remains unreviewed."""
from pathlib import Path
import json,re,hashlib,collections

# Each key is exact archived prose (quotation marks may surround it). These are
# explicitly translated units, not substitutions inferred from game mechanics.
FIXES={
'So much death, so quickly, like Eastern Front all over again!':'这么多人转眼就死了，简直像东线战场重演！',
"Look, I just made a new pet. I'll take it for a walk for about 5 minutes while the rest of you dick around.":'看，我刚弄了只新宠物。你们继续瞎折腾吧，我带它散个步，大概5分钟。',
'Good, that fucking song was driving me nuts!':'好极了，那首该死的歌都快把我逼疯了！',
'Ha Ha, you just got fucked by a monkey!!':'哈哈，你刚被一只猴子干翻了！！',
'You fall like drunkards on way home.':'你们倒下的样子就像醉鬼在回家路上摔倒。',
'Those should be mine, you Japanese pig!':'那些应该是我的，你这头日本猪！',
'Ah, the same weapon I used to kill my third wife! She was bitch!':'啊，这就是我杀第三任妻子时用的武器！她是个贱人！',
'— After getting a M1897 Trench Gun or Double-Barreled shotgun':'— 获得M1897战壕霰弹枪或双管霰弹枪后。',
'Death is inevitable, like hangovers, I know.':'死亡无法避免，就像宿醉，这个我懂。',
'Same weapon I used to kill my second wife. It was accident!... She talked too much.':'这就是我杀第二任妻子时用的武器。那是意外！……她话太多了。',
'I had more powerful weapons on my pig farm!':'我养猪场里的武器都比这更有威力！',
'This will hurt like syphilis. Believe me, I know.':'这会像梅毒一样折磨你。信我，这个我懂。',
'Someone is not sharing their ammo...':'有人不肯分享弹药……',
'How come you always get the good guns, and I get the Colt?':'为什么你们总能拿到好枪，我却拿到柯尔特？',
'I end you!':'我来终结你！',
'Wunderbar!! Wunderwaffe, WUNDERBAR!!':'太棒了！！奇迹武器，太棒了！！',
'Shi-Ne!':'去死吧！',
'Shi-ne!':'去死吧！',
'Larger magazine and more ammo, more range and bigger radius':'弹匣更大、备弹更多，射程更远、作用半径更大。',
'Suspended outside of a window of a lab, to the right when entering the labs from the power room (requires the window to be destroyed first)':'悬在一间实验室的窗外。从电力室进入实验室时位于右侧（需要先打碎窗户）。',
'Near the power switch on the left side, leaning on the power conduits':'在电源开关附近的左侧，靠着供电管道。',
'In the corner of the air lock between the power room and the labs':'在电力室与实验室之间气闸的角落里。',
'On a desk in the first room of Tunnel 11':'在11号隧道第一个房间的桌子上。',
'In the last room in Tunnel 11, to the right of the window next to some large computer components':'在11号隧道最后一个房间，窗户右侧、一些大型计算机部件旁。',
'We have other ways. This power is too intense for my purpose, I cannot communicate while it is...':'我们还有别的办法。这股能量过强，无法满足我的目的；在它……的时候，我无法与你们沟通……',
'— Said when the spire is active (cut quote)':'— 尖塔处于激活状态时说出（被删减的对白）。',
'Please keep the doorway clear of hands and feet.':'请勿将手脚放在车门处。',
'All passengers must remain behind the yellow line at all times.':'所有乘客必须始终站在黄线后方。',
'Thank you for riding Consolidated Coach Corporation Bus Lines.':'感谢乘坐联合客车公司的公交线路。',
'Livingstone Mine and Calico, Namibe, Angola':'安哥拉纳米贝的利文斯通矿场与卡利科镇。',
'The four survivors look off into the distance. It is daytime, Meteors fall to the ground, and there is a noticeable glowing.':'四名幸存者望向远方。此时是白天，陨石坠向地面，并能看见明显的光芒。',
'*whistles* Patience is a virtue... That I DO. NOT. HAVE!':'＊吹口哨＊耐心是一种美德……而我，完！全！没！有！',
'WHERE IS HE, that foul, stinking ROTTEN GERMAN! He was here, now he is gone. He will pay for what he has done, mark my words.':'他在哪儿，那个肮脏、恶臭、烂透了的德国佬！他刚才还在，现在却不见了。他会为自己的所作所为付出代价，记住我的话。',
'Curse this confusion! I must remember my mission. Why am I here? The enemy war machine must be destroyed.':'该死，我怎么这么混乱！我必须想起自己的任务。我为什么在这里？必须摧毁敌人的战争机器。',
'I must find a way to survive this nightmare. Perhaps these machines will help me fend off the wretched hordes.':'我必须设法从这场噩梦中活下来。也许这些机器能帮我抵御那群可憎的怪物。',
'Ha, this aiming thing actually works!':'哈，瞄准这招还真管用！',
'I am magician! I made his head disappear!':'我是魔术师！我把他的脑袋变没了！',
'What are you, fucking Rasputin? Stay dead this time!':'你他妈是什么，拉斯普京吗？这次死了就别再起来！',
'Hey, hell pigs, can you attack someone else for a while?':'喂，地狱猪，你们能不能先去攻击别人一会儿？',
"Is this another one of the German's twisted experiments?":'这又是那个德国佬的变态实验之一吗？',
'Somehow, I knew my patience would have been suitably rewarded.':'不知为何，我早就知道自己的耐心会得到应有的回报。',
'Only fool would drink such awful beverage!':'只有傻子才会喝这么难喝的饮料！',
'Who could enjoy such a foul concoction? Eugh!':'谁会喜欢这么恶心的混合饮料？呃！',
'Is this what Western children eat? No wonder they are so skinny.':'西方孩子就吃这个吗？难怪他们那么瘦。',
'Though flavor is strong, I still have stench of blood in my nostrils.':'味道虽重，我鼻孔里仍然满是血腥味。',
'You dishonor your lineage German! Do you not care for the shame you bring upon your ancestors?!':'德国佬，你让自己的血脉蒙羞！你难道不在乎自己给祖先带来的耻辱吗？！',
"For so long, I've feared the Emperor's displeasure. I know not where he is, yet I remain loyal. This, I must never forget!":'长久以来，我一直惧怕天皇的不满。我不知道他身在何处，却依然忠诚。这一点，我绝不能忘记！',
'My dreams are haunted by spirits. I fear they are not those of my ancestors.':'我的梦里有亡魂纠缠。我担心它们并不是祖先的亡魂。',
'Long-range solution to nearby problems.':'用远程手段解决近处的问题。',
"I... I killed him. I-I didn't want to but I-I... I kinda sorta ha-ha-had to.":'我……我杀了他。我、我并不想，可我、我……我有点儿、有点儿不得不这么做。',
"This may be the most elaborate egg cup I've ever seen! It seems there's a place for everything. Even a giant, interdimensional egg!":'这可能是我见过最精巧的蛋杯！似乎什么东西都有适合它的位置，就连一颗巨大的跨维度蛋也不例外！',
'Just as I thought, it fits like a glove.':'和我想的一样，严丝合缝。',
'— In response to Shadow Man , at the beginning of a match after Shadow Man finishes speaking':'— 一局开始时，在暗影人说完话后回应暗影人。',
"Wha- You mean to tell me that these corpses are actually the real people of the city? Fuck 'em.":'什——你是说，这些尸体原本真是这座城里的人？去他们的。',
"Look, I killed a lot of people. Bad guys. You're gonna have to be a lot more specific there, pal.":'听着，我杀过不少人。都是坏人。你得说得更具体一点，伙计。',
'I think I used just the right amount of force.':'我觉得这次用力恰到好处。',
"You gotta be shittin' me. I thought I had more rounds than this.":'你他妈一定是在逗我。我以为自己的子弹不止这些。',
"In a moment this weapon is going to be about as useful as Magic Man's wand.":'再过一会儿，这把武器就会和魔术师的魔杖一样没用了。',
"Hey, I'm gonna need some more slugs real soon!":'喂，我马上就得补些子弹了！',
"Give up? I'm Jack fuckin' Vincent! I don't give up now, not never!":'放弃？老子可是杰克·文森特！我现在不会放弃，永远不会！',
"I get a feeling Jacky V's about to put a hurt on the next freak I see!":'我有种感觉，杰克V马上就要把下一个撞见的怪物痛扁一顿！',
"I'd give you all a final warning, but I think I'd rather just put you down!":'本来可以给你们最后一次警告，不过我想还是直接干掉你们吧！',
'Bye bye click click! Hello bam bam!':'再见，咔哒咔哒！你好，砰砰砰！',
'Let the bloodbath begin!':'让血战开始吧！',
'Time to get gobbled, gum.':'泡泡糖，该把你吞下去了。',
'Strange gum brings magic benefits.':'奇怪的泡泡糖带来神奇的效果。',
'I look forward to harvest time.':'我期待收获的时刻。',
'Well, now I feel empowered!':'好了，现在我感到力量充沛！',
"Oh, look! It's the little man gun!":'哦，看！是给小个子用的小手枪！',
'— Receiving a pistol from the box.':'— 从神秘箱抽到手枪时。',
"I'm going to die!":'我要死了！',
'— Getting the Teddy Bear .':'— 抽到泰迪熊时。',
'— Getting the Teddy Bear.':'— 抽到泰迪熊时。',
'— Running low on ammo.':'— 弹药不足时。',
'Hello?? Anyone have ammo?!':'喂？？有人有弹药吗？！',
'Bullets? Who needs bullets? I DO!':'子弹？谁需要子弹？我需要！',
"I'M DOOMED!":'我死定了！',
'I HAVE NOTHING LEFT TO SHOOT!':'我已经没子弹可打了！',
'Sehr gut! Just what the Doctor ordered!':'很好！正是医生开的方子！',
"I don't like stabbing! I LOVE STABBING!":'我不是喜欢捅人！我是爱死捅人了！',
'Stab, stab, stabbity-stab-stab!':'捅，捅，捅捅捅捅捅！',
'The doctor is IN!!':'医生来接诊了！！',
'OHHH, could you FEEL it going in?':'哦——你能感觉到它捅进去吗？',
'STOP IT!':'住手！',
'How dare you even TOUCH the doctor?':'你竟敢碰医生？',
"You're very insistent, aren't you?":'你还真是不依不饶，是吧？',
"Don't touch without asking! It's not nice!":'没问过就别碰！这不礼貌！',
'Once with a normal weapon.':'用普通武器攻击一次。',
'Once with a lethal grenade, Wraith Fire is the most effective':'用致命投掷物攻击一次，幽灵之火最有效。',
'Once with a shield bash.':'用盾击攻击一次。',
'Scarlett turns towards Diego, Shaw and Bruno.':'斯嘉丽转向迭戈、肖和布鲁诺。',
'Diego picks up a torch and the three enter the secret passage while Scarlett opens the other bonds with the key.':'迭戈拿起火把，三人走进秘密通道；斯嘉丽则用钥匙打开其余束缚。',
'Diego, Shaw and Bruno arrive in a chamber.':'迭戈、肖和布鲁诺来到一间密室。',
'The eyes of the Oracle turn yellow and she stares at Scarlett.':'神谕者的双眼变成黄色，她盯着斯嘉丽。',
'— Upon being attacked enough times.':'— 遭到足够次数的攻击时。',
"Bored? Try backgammon! The game your grandmother loved that you still don't fully understand! Backgammon: A game that exists!":'无聊？试试西洋双陆棋！你祖母钟爱的游戏，你到现在都还没完全弄懂！西洋双陆棋：确实存在的一种游戏！',
'Hmm, kinda minty...kinda fishy.':'嗯，有点薄荷味……又有点鱼腥味。',
'Well that went *strained groaning* straight to my nervous system.':'好吧，这玩意儿＊吃力地呻吟＊直接冲进我的神经系统了。',
"That'll put some hair on your chest!":'这东西能让你胸口都长出毛来！',
'Yeah! Thats kickin\' in right away.':'好！这就开始起效了。',
"I don't know if these drinks are habit forming, but staying alive sure is.":'不知道这些饮料会不会让人上瘾，但活着肯定会。',
'*Chokes* Ooh ahh...I think my tongue just died.':'＊呛住＊哦，啊……我觉得舌头刚才死掉了。',
"Woah...hearts beatin' a hundred miles an hour!":'哇……心脏简直以每小时一百英里的速度狂跳！',
"Ohh good thing Big Pharma doesn't exist anymore or that thing woulda cost ten times more!":'哦，幸好大药企已经不存在了，不然这东西得贵十倍！',
'*Chuckles* Ooo-hoo! That is like a lightning bolt!':'＊轻笑＊呜呼！这感觉就像一道闪电！',
'Agh, okay. *Coughs* That was just straight-up mouthwash...Fine. I can take a hint.':'啊，好吧。＊咳嗽＊这根本就是漱口水……行，我懂这个暗示了。',
"¡Vete pa'l carajo!":'滚你妈的！',
'¡Muérase! ¡Los perros del infierno!':'去死吧！地狱来的狗！',
'¡Perro travieso!':'该死的坏狗！',
'Eenie, meenie, miney, mo...':'点兵点将，点到谁就是谁……',
'The MP40! Wunderbar!':'MP40！太棒了！',
'Ultimis ( BO & BOIII )':'终始小队（黑色行动1与黑色行动3）',
'Der Meisterbogenschuetze':'弓术大师（Der Meisterbogenschuetze）',
'Ground Control':'地面管制（Ground Control）',
'Space Dog':'太空狗（Space Dog）',
'BowieKnife BOCW':'鲍伊猎刀／黑色行动冷战',
'The V-R11.':'V-R11的外观。',
'The V-R11 .':'V-R11的外观。',
'The VR11':'V-R11的外观',
'The Wunderwaffe DG-3 JZ.':'DG-3 JZ奇迹武器的外观。',
'Firebase Z':'Firebase Z（Z战区）',
'How To Pack A Punch Tutorial Shangri La Zombies Annihilation Map Pack':'香格里拉武器强化教程／僵尸模式Annihilation地图包'
}

def norm(s):return s.strip().strip('"“”').strip()
def main():
    root=Path('.drafts');records=[];matched=collections.Counter();url_checks=[]
    for p in sorted(root.glob('drafts/*.json')):
        d=json.loads(p.read_text());pid=d['pageid'];a=Path('app/src/main/assets/faithful')/f'p{pid}.js';s=a.read_text();doc=json.loads(s[s.index('(')+1:s.rfind(')')]);assert d['sourceSha256']==[hashlib.sha256(u['en'].encode()).hexdigest() for u in doc['units']]
        for i,u in enumerate(doc['units']):
            en=u['en'];before=d['translationsInUnitOrder'][i];zh=before;k=norm(en)
            if k in FIXES:
                zh=FIXES[k]
                if en.strip().startswith(('"','“')):zh='“'+zh+'”'
                matched[k]+=1
            if re.search(r'\bzombies?\b',en,re.I) and not re.search('mosquito',en,re.I):zh=zh.replace('蚊子','僵尸')
            # Literal URLs must never be run through a language glossary or translation.
            source_urls=list(re.finditer(r'https?://\S+',en));target_urls=list(re.finditer(r'https?://\S+',zh))
            if source_urls:
                if re.fullmatch(r'[\s↑\d.\[\]]*https?://\S+(?:\s+https?://\S+)*',en):zh=en
                elif re.fullmatch(r'(?:https?://\S+\s*)+',en[source_urls[0].start():]) and target_urls:
                    zh=zh[:target_urls[0].start()]+en[source_urls[0].start():]
                elif len(source_urls)==len(target_urls):
                    for x,y in reversed(list(zip(source_urls,target_urls))):zh=zh[:y.start()]+x.group()+zh[y.end():]
                else:url_checks.append({'pageid':pid,'unit':u['id'],'issue':'URL alignment requires review','en':en,'zh':zh})
            if zh!=before:
                d['translationsInUnitOrder'][i]=zh;d['methodsInUnitOrder'][i]='targeted-source-bound-qa'
                records.append({'pageid':pid,'unit':u['id'],'sourceSha256':d['sourceSha256'][i],'before':before,'after':zh})
        p.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')))
    report={'articleLevelReviewUnchanged':True,'correctedUnits':len(records),'exactProseTranslationsUsed':len(matched),'urlChecks':url_checks,'records':records}
    (root/'targeted-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print('Targeted draft QA',len(records),'units;',len(matched),'exact prose translations; unresolved URL rows',len(url_checks))
    assert not url_checks,'A source URL alignment needs manual handling before packaging'
if __name__=='__main__':main()
