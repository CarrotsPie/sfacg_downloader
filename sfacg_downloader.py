import time
import requests
import re
import hashlib
import json
import uuid
import html
from ebooklib import epub

# 加载字典（特殊字符替换）
SPECIAL_CHARS = '宦缺泛洁槛掳马杉傲冷衡弗害烬遗刨饵韵动味碳骄寥凹汁姚也鼎勒痈慕来诊箔迅沁羞僚休儿唾摆窘厌椿母残貌盔弦沉恃棒菱沂巳釜没工溃春肢焦占遥浴轩儡栗梦陨嘴荤梢宇钮捆争土枣盛渝信茵厕忆士急败茁徘吁莉旋腆踪钩捂超峙蒙瘦差应漳沥瑚横阅文缸吱滨变形霉霹僻终愧甥券拽盘预奖鸟透真椅取堕舱票厂彩扯时宋檄瘫峨题楼搭报瘴础勤梨宠古坯忠鲍层癌键肠足荒秃认菏百涣坑投滥谚草坞太桨拓剧宾栋奉老上似丈避侥烯准种壁峦臻谴卤隆垂番协愚划鸦攻藏曾对痔跺墓根撰聂闯察咋发衅撵寡竣茶宏议亨艇务狗裤宣鹃逼饱宅孔诲遣警亿贤鄙沮译龟膀蹭絮伙触锌庚吹命躬圣追炯霞叫裴底族疟痴熊闸臆撂访午茨柿巡米鞍邹逃兑绎犀椎己控篡室劈巍参苦瞬冠摩凭胰甫讯否绅汉诛仙扁活醚挎荷篆黍捕汝吊蕊虱抓从略诞惶逆脉塔歧镶衰撮伍片阶凑松九菊固娄姻委惮酷封澎牙在翰裁南挫沾赏赫厅韩葵介鸡编欧捐能炉挠杀勘浦者粤杖幂琢焉刁爱如惫府武找佯捣锈灰茫铸肛敬阿可属沙创概廊墨乳湛咖级蚂淋反豁旺岭星琉凌嗜目侠迄喇靶福矾丹拔绥觉孟沫霖袭帕驼镁泰啊极孙实经趟当歼斗柑嗽录贡雍稽阜损铬尿痒醒岗渡宗莆捧筑岸井燎搐负粕励爵啮庄涌卢蝶垄仍脂操哉句热耽乓拐苍团斌掩孩沃堆眠闻毛歹齐辖育芳榜其蝇侩杰胞魄粱姬蜕淹轧甚寸舌播霓硒啥钎馅力皇擅染寂相熬必羹期腕跌租僵虏矫恿笨元物历砧噎犬帜舰柞腊定洽剐蕉惨摔珠着烘朋咎某丧酉友郡痹俘啦师蔑涅绒侨官戊锡泌误棘嗡顽谱懂捌潮员豢焰岁丽炕缘搁庐叁崭羔龙崩哩体酗穆猎餐机欺悉蔫寿髓庸焚洲技缠绰傍浅泄此嘶祸肪凶锣雪厢摧粗刷乙脯枪稿寝螟席扎杂第漠檀魂品籽氛越芥呕做滴债缕帛及募悬彰酌堑艘煤癣口售津耀冈涪蝗予攀棚木新泡猖宽躁阁健霍揍铰陕非樟问颠话缴况矽吗昂披努疵滩执拟鼓枷摄湃亚昏旁塑含阑荣安掐宁苞监放施辣浙主遍邀告枯释灾啪驭全断缩晌藐孵折据辕设离病呀解汲援娜幻辩很盆毡铆敢粳蔼榨游掉皑挽呈擦舀麦咏唁专肝伯章脸氖揪枚戏惠萍卧隶庙量啄贞烙响柒熙违泪娶吨矢艺培降迁映丙硬碾蠕囚怪删支适佑搽淆蜒判奄想障袄跑窜燕广登停嚷户铡挚要瘁猿甭韦嘿檬瘸烈招铅眶蜘火洛姐圾分雇阳剑练皋凝劳建脓一俏苔严洗睹耗茎国漾辆疲篱煽走歌亥诽藉狞径菠雁言审碰双慰森揣钠世芝炙蜗针奋曹鉴遁冬扫偶赐陶酚束砷兽噬揽永汤庇脖挣泣蓟本润饺常偏垛教悄芭琳计偷詹夏帝韭擂卵吧暗拆插忌橱搅条曲糖恳宙贯甲稼撇鳞鸭臭臀迂回磁淤统羽三功伏烹札杭暑凰弄祭币皿懦店萝眺瘤产菇勾笼引漏惭堡鹊闽恫宿累谰曙厩莽蔡杆烛镜碗费惧碑啡枫慧沧颊恕揭簇材握留伟灼墟噶恨俺腻赌娃蚊膨婴闺碟陵连晕扑递蜡勇沸这玻挑兜耙疫舶乃羌瓷进胖俐基卓谆企边眷独潭毅牢蛆砍而丫唆诺舟殖陈浇勉捡饮完托更腑瞎减幌我吟滑算钱枉睦妊冶红救贴忍旧刊淡依喘共斥侗先峡香紊候肺袒拄猫跳砖剂窑渔假果色挟界名逛膘蘑酪吃翟研翻频提忿饼腾倚疮脆婚甘赠鹰带摘匆锥瑟睛领钵柄祥烩蛮稗矗濒卫溜制扭藻吾赂拙辛肄轰哭哑凛羡窖筷俄姆楔缝兄民表痉舆膊捷岂蓖卡限肿倪好炬淑助且颤斋蔬莹又忻瞩二畜总坤心鸵眨挡戴榔页缨恍几胁帐传迭临锹煌典特沏向尼谷哇状溪胜衣养丛斟萤柠恼讳朱楷肆防禹烃零若醋夕倘铲岿茧薯牌罗妥距苏规瞳赘铜钒奇奸疆魁矿蛤澈呛父详丘叼路吼驮端凳床涕瓤仆撼腺亭禾乐白侯抵诧失铱慷铭识迪哨巴使涝巨棺碱奎芹掸颇浆悦激侣长埃禄袋踢舍侧舜寺盐叭鸿面局私贷比容掀搔藩览吞态左布素侵侮咀憾郸现娥记淀咯馆仿黎敖少寄匣贮脐看亩趴歉样斧酣奠旭筋狂筐蚜最聋遵酶晒擒妒拖窿鸥示抛娘县台导矮窒顺女邑慌齿蔷蜜字数竭瑶谨抒乌耕霸泥兵号亏匈侄猩褒琶署静住饿碉桂抬庆匙扬慈牟倾媚矣搀锤拇构吵嫩讹焊郁漫守贱拌效例弊灭桅尾道供葱狈垃壮筹栈扮躇疤骆揩露莫孰敏订购潍顷盈转胯撞居鞘摇周幽魔镍蚌水树戍谐飞梯豪添业晓挪柴袁烫苟怔冤念决初碎立臣纳陇异喉葬驯确死桌雾嘱臂沟殴歇丝造坛蚤围拴延自芋祟巷猜恭毒辟湖牧傅惺磐瞻砾壕踞疼尝骂咆同症耿呢敝穷饲钨块每耐巧王躯姑藕泳颈肃崖役犹辱您棕满锅垫措深忙酞讽化场馈赞节拒矛宴蛇乞杨赣咬均中邢蛛瞪睁韶悼鞋滇雄站骗于阂茅阀煎斜渴季哼跃暖签耻躲写宫剔叙载尊怒蒋翅请函贝姥穴驰盾势纵瓦罢存冲血龋脑敌瞧营仁扰刻狐啸珍荆知晤乍榴鲁冻咱竹今融烂咕喜踌赴财氏靡右琐忽贺汞赵躺垮瞒拥屏虐蒲邮壤颖破斯既棠誊彤铝蝉止案佐捞童椭凤贩那塘湿陷清圭诣须义萎梧箍蛙息入勃另锚棋舅筒卿收尽骑脏毋屡蔓胆痊膳钙并敞傀秘奶卯谭给峰远瞥禽卉傻掇冗器货悯咨剁维讲子药纲腮和嫡麓诚故些闭档选箕樱气幅酥赊辑虞怀蛊弧抢价俊跪斡雌甩绘罩忘晚驻龚斩靠涂螺锑雷步绚智组骸仅庭涸琴骚络旬乏杯灸呜椽斤寒输阉斑辐烟刑平涯般倒榷湘公氢嚎疚启乡茸芒巩鹿景甄誓秒炼杏绞剿葫筏翱骋管蓝蔗稚网君腥掺臼遇继脊瑰流磨瞅寨鸳送宝拷击汕圈蓬尉磕田疏妄绵畦仑竖刺硕渭棍试悲污豆箩云暴东憨让哈芽妖黔耍栖欠狠秆讶叉狡敷砌暮宪廉鞭彬炭嘘么首账践趣史迟瘪岳谅豺单拨拳船社厄厉天弃寇尤保摹佬尘炒苑夯匪扔顿毁雀窟熔洱湍究献姨蛔治蔽袖姜虹缀盗漱狰嚣哆豫虽煮削滚爸巫峪惕锐脱屑压泼纸荡证模院伞霄混砰谎彦糕奴派夷彻串忱耸酬致滞类郭撑樊辈哎抱缎妈艰绢朵荚颗摸事邱综冒菩稍婆轨库携懈鹏至思蹈滋痢酱论珐蜀咐窃军还强归肥爬秉莲注妓充垒瓶丢绍坊惰测柔炳榆埂掠掌董恶戳禁打菲坍开阻嚼灶逻额罐肯胶凋肤朽只匠腰蛹喊棵潘验倍柱卖裂喂粮贿门鳃勋笆迫蛾笛醛礼称奢纹卞陆趁蝴与升胺贫卸随党镐劲诫轿镊魏伎街缮估囊策屠泊舵皂疑集拼祁俯灿舷范佃征展出侈厦驴缓刀喝厚抿六港希糙才堰苹批辞聚舔缅蹄隔捍蕴弟柳州帖欢佣快桩慑生瓢椰翘骇鬃说阐蚁山瓮氮听殿渍辊办各济坠蹦联屯习月鼻植砚沿嫂区佰唉怕艳始校剥括雕祈旅置徽诈浪轴已邦裙碍窍哄撤哮部匀摊兼蓑潦橙关科绷嘻嘉妨搜值棉惩蟹倦驶税芯泻密运涧仇珊涨昌男琵渺正光呻硅有傣逐袜净吠缔溯将婶钡电迹股昧卜低无嘲兆诌沦恋溺糯钢宰饥悸夫版胃笋牡咒箭把泞虑易纤唐梅咳郑需象玉大譬崔晶洼赦弱丁馋四挂磊硝昆痰撒调蔚胳它抗猪幼镭秸谁恒印诀厨芍显恐猾冀司廷坚篮酵撕锰履位澳市汐哀辨则萧溢秦奈城隧叹茬政责炔铺掣赤兔撩蹬铃馒爪钥震凄畅移是辅讼翼栓瀑搪醉獭懒陌臃毫弛裳祷列毙岛浚遂澜盏郎贾扦酒呐境早余评作坎罚环窥狱炊淌郊怜书外册贰剪际滤油迎渊桶媒付担肌郴盂整袍就坏邻皮用谩瑞采栽吮雹烦克患轮探咸拈墅椒但恬愁裔肘峻敦件枕匿恤散谜央诵链绳讥捶烤薛直栏垣弓睬汀栅刚职畴敲扣读纱搂晰凡痞赃雏徊兴糟篇粒海复郝八赚之冯酸侍漓糜渠惋乎们晨垦吕乾千亡芜项的逸铂池僳往买搞车诬焙辗利妹富你查朝跋砸氦旷娠搓怎澡危氯契押曼帧纬受讨壹愈胚昨柬驱轻勿桓靖锭赖彼袱喧捏靴涩虚薪矩割末恩唱革幢日催五屁线情挖苯哲犊讣盟地十落去伶个苗间闹谋骏唬沼糠迈殉绊罕肖邪晋闷窗鱼嫁狭紫改炮浮灯迸锨孤诡汾抉孺甸增套灵著寞赡梭循疗弯京补乱重灌朔空粉桥演婉即昭鸽泵妆燥过彝具阴错匝人劝描亢抚张金犁氟耪板逮墙拜服喳阔址刽拿匹壶箱赔葛赎画贸帆辫沈射惊训绪沪久扼蹿叛埋劫钦爹庞绕淮颜缉悟楚叶波默颓簧擞蠢背竟驳鼠滔啃祖屿爷氰飘会苫哦雅酋堪篷邵咽伦仕伐秩柏获承屎蜂浩愉竿仗芦琼盎慨林干玄凉滦她李畏挥吝捻毕被胡崇膝馁宜踊指簿疽瘩抖皱侦掘呆巾农咙胎赛跟别剩普菜溅感权钞楞副虾膏鸯肉橡仪俗玩烽赶申万拦坷钉坦糊汛醇戈因望夹行蒸成觅钳绿资乘捎邯座险择钧为嚏述帅护笑炽讫毗不洋眩氓德花烷汪意渣浑许秀曝腿谦稻鹤蛰消雨寅玲壬嘛萄欲代由刘搬缆聘粟泉荧球寻亮村家省扛帽陀谬羊稠爽籍亲舒吭点乒衷晃振熏短汰诸烧梆惹坐屹桑丑肋速次喷理饭谊赋拭彭逝玫起骡贼了瓣谤疥退银娩黑授促河眯砒菌锗薄加圆锯辉睫褐泽或奥抠园伺揉墒刮猛兢埠年替朗玛锁微未艾呵吉琅排炎碘眉逾式趾浓卒尚客械啤帮优却沛腹胀队嵌镣谓怖垢冕叠叮像仔笔渐掷蹋笺令撬蚀接镑铣厘竞众呼痪肾愿桔孝峭疯岔黄橇隙邓媳褥该举弘川洞扒俱潜呸缄豹酝镇筛塞尧西锋脾头摈律检任翔青芬戎吐洪麻鳖诅窝声耶杜交尔拎盲盯姓隅丰伴续霜涟衙帘除标癸辰寓磋龄俞纯拢截鞠配姿郧逢爆英幕盒窄堤氨逞敛仰索痘聪见襟纺恢绝填靳沽盖碧忧鹅疾晾阵铁祝叔欣磅屉枝痕佳槐志吓房穿拧善小酿挝羚苛炸貉约猴颁益挛惯膜粪枢纪宛乖扶槽攒谢掂奏寐狸旨倔嗓蛋夸皖洒澄返豌软凿晴纂剃待蹲拂蚕求困毖积妙旗陡隘华怨憎康拍江督拣颅较膛伤逊淳享颂图滓牺荔尖神液蛀暇哥棱胸淖昼源修穗牵蝎裸合谣陪浸廓曰纫盼囱到夜惜蒂届份蒜下质孪稳涵赁徐釉隋锦颐悠俭耘答凸纽原格扇高戮抑嗣隐嫌扩漂涡劣伊肚骨嗅踩难钻帚愤处莎粥瞄娇狄拾茄鲜秤半璃毯包视馏途巢襄手淫孽硫性唯近浊怯装挤荫惦纷聊汽牛婿淘御航稀前医滁娱扳渗肩序堵硼砂钾驾坟战渤阮誉尸绸殃紧程绣结驹都戒涤畔耳备堂痛揖他拘绩伪精熟免饰焕迷伸潞溶掖绑阎铀换兹甜突踏便坡尹脚烁徒附朴虎憋术尺诗吴群桐衔挨漆料褂段简课噪戌辽吩允佛借荐仟诱殷歪儒影逗七腔抄旦吻核商身迢裹韧锄秽罪殆嘎佩饯坝盅勺绦法音碌挞吸靛戚何婪坪两秧蘸蓉推后乔熄衬曳塌剖昔狙覆度杠壳陋腐美唤谗刹跨悍翌贪怂辜通多鄂框湾梁碴词卑哪废梳赢型殊沤照兰睡款镀攫什抡抽萌闪镰召捅倡翠切织腋桃妮篓彪谈妻方妇冉疙株瓜廖学懊鲸篙持亦哺拱萨偿遮缚犯仓岩疹然褪汗辙翁威怠绽闰旱搏弥诉互等细销汹率系内瘟蕾狼淬庶茂里攘牲衫弹煞肇狮葡畸惟野繁石良仲宵拯趋所泅班博粹涉冰拉按以眼僧慢幸温卷俩舞明角粘陛嫉蓄食酮孜顾唇刃涛掏捉锻圃屈贬玖语遭夺鸣析哗顶涎够虫域苇鬼晦氧风抹码茹皆询哟北骤观惑纠颧考再架磷得慎淄钓溉谍礁喀燃藤暂遏孕疡纶悔屋秋闲裕崎梗埔达撅柯钟奔贵莱储吏墩抨饶囤娟擎啼鲤柜匡丸凯符肮喻磺钝衍汇'
REPLACEMENT_CHARS = '啊阿埃挨哎唉哀皑癌蔼矮艾碍爱隘鞍氨安俺按暗岸胺案肮昂盎凹敖熬翱袄傲奥懊澳芭捌扒叭吧笆八疤巴拔跋靶把耙坝霸罢爸白柏百摆佰败拜稗斑班搬扳般颁板版扮拌伴瓣半办绊邦帮梆榜膀绑棒磅蚌镑傍谤苞胞包褒剥薄雹保堡饱宝抱报暴豹鲍爆杯碑悲卑北辈背贝钡倍狈备惫焙被奔苯本笨崩绷甭泵蹦迸逼鼻比鄙笔彼碧蓖蔽毕毙毖币庇痹闭敝弊必辟壁臂避陛鞭边编贬扁便变卞辨辩辫遍标彪膘表鳖憋别瘪彬斌濒滨宾摈兵冰柄丙秉饼炳病并玻菠播拨钵波博勃搏铂箔伯帛舶脖膊渤泊驳捕卜哺补埠不布步簿部怖擦猜裁材才财睬踩采彩菜蔡餐参蚕残惭惨灿苍舱仓沧藏操糙槽曹草厕策侧册测层蹭插叉茬茶查碴搽察岔差诧拆柴豺搀掺蝉馋谗缠铲产阐颤昌猖场尝常长偿肠厂敞畅唱倡超抄钞朝嘲潮巢吵炒车扯撤掣彻澈郴臣辰尘晨忱沉陈趁衬撑称城橙成呈乘程惩澄诚承逞骋秤吃痴持匙池迟弛驰耻齿侈尺赤翅斥炽充冲虫崇宠抽酬畴踌稠愁筹仇绸瞅丑臭初出橱厨躇锄雏滁除楚础储矗搐触处揣川穿椽传船喘串疮窗幢床闯创吹炊捶锤垂春椿醇唇淳纯蠢戳绰疵茨磁雌辞慈瓷词此刺赐次聪葱囱匆从丛凑粗醋簇促蹿篡窜摧崔催脆瘁粹淬翠村存寸磋撮搓措挫错搭达答瘩打大呆歹傣戴带殆代贷袋待逮怠耽担丹单郸掸胆旦氮但惮淡诞弹蛋当挡党荡档刀捣蹈倒岛祷导到稻悼道盗德得的蹬灯登等瞪凳邓堤低滴迪敌笛狄涤翟嫡抵底地蒂第帝弟递缔颠掂滇碘点典靛垫电佃甸店惦奠淀殿碉叼雕凋刁掉吊钓调跌爹碟蝶迭谍叠丁盯叮钉顶鼎锭定订丢东冬董懂动栋侗恫冻洞兜抖斗陡豆逗痘都督毒犊独读堵睹赌杜镀肚度渡妒端短锻段断缎堆兑队对墩吨蹲敦顿囤钝盾遁掇哆多夺垛躲朵跺舵剁惰堕蛾峨鹅俄额讹娥恶厄扼遏鄂饿恩而儿耳尔饵洱二贰发罚筏伐乏阀法珐藩帆番翻樊矾钒繁凡烦反返范贩犯饭泛坊芳方肪房防妨仿访纺放菲非啡飞肥匪诽吠肺废沸费芬酚吩氛分纷坟焚汾粉奋份忿愤粪丰封枫蜂峰锋风疯烽逢冯缝讽奉凤佛否夫敷肤孵扶拂辐幅氟符伏俘服浮涪福袱弗甫抚辅俯釜斧脯腑府腐赴副覆赋复傅付阜父腹负富讣附妇缚咐噶嘎该改概钙盖溉干甘杆柑竿肝赶感秆敢赣冈刚钢缸肛纲岗港杠篙皋高膏羔糕搞镐稿告哥歌搁戈鸽胳疙割革葛格蛤阁隔铬个各给根跟耕更庚羹埂耿梗工攻功恭龚供躬公宫弓巩汞拱贡共钩勾沟苟狗垢构购够辜菇咕箍估沽孤姑鼓古蛊骨谷股故顾固雇刮瓜剐寡挂褂乖拐怪棺关官冠观管馆罐惯灌贯光广逛瑰规圭硅归龟闺轨鬼诡癸桂柜跪贵刽辊滚棍锅郭国果裹过哈骸孩海氦亥害骇酣憨邯韩含涵寒函喊罕翰撼捍旱憾悍焊汗汉夯杭航壕嚎豪毫郝好耗号浩呵喝荷菏核禾和何合盒貉阂河涸赫褐鹤贺嘿黑痕很狠恨哼亨横衡恒轰哄烘虹鸿洪宏弘红喉侯猴吼厚候后呼乎忽瑚壶葫胡蝴狐糊湖弧虎唬护互沪户花哗华猾滑画划化话槐徊怀淮坏欢环桓还缓换患唤痪豢焕涣宦幻荒慌黄磺蝗簧皇凰惶煌晃幌恍谎灰挥辉徽恢蛔回毁悔慧卉惠晦贿秽会烩汇讳诲绘荤昏婚魂浑混豁活伙火获或惑霍货祸击圾基机畸稽积箕肌饥迹激讥鸡姬绩缉吉极棘辑籍集及急疾汲即嫉级挤几脊己蓟技冀季伎祭剂悸济寄寂计记既忌际妓继纪嘉枷夹佳家加荚颊贾甲钾假稼价架驾嫁歼监坚尖笺间煎兼肩艰奸缄茧检柬碱拣捡简俭剪减荐槛鉴践贱见键箭件健舰剑饯渐溅涧建僵姜将浆江疆蒋桨奖讲匠酱降蕉椒礁焦胶交郊浇骄娇嚼搅铰矫侥脚狡角饺缴绞剿教酵轿较叫窖揭接皆秸街阶截劫节桔杰捷睫竭洁结解姐戒藉芥界借介疥诫届巾筋斤金今津襟紧锦仅谨进靳晋禁近烬浸尽劲荆兢茎睛晶鲸京惊精粳经井警景颈静境敬镜径痉靖竟竞净炯窘揪究纠玖韭久灸九酒厩救旧臼舅咎就疚鞠拘狙疽居驹菊局咀矩举沮聚拒据巨具距踞锯俱句惧炬剧捐鹃娟倦眷卷绢撅攫抉掘倔爵觉决诀绝均菌钧军君峻俊竣浚郡骏喀咖卡咯开揩楷凯慨刊堪勘坎砍看康慷糠扛抗亢炕考拷烤靠坷苛柯棵磕颗科壳咳可渴克刻客课肯啃垦恳坑吭空恐孔控抠口扣寇枯哭窟苦酷库裤夸垮挎跨胯块筷侩快宽款匡筐狂框矿眶旷况亏盔岿窥葵奎魁傀馈愧溃坤昆捆困括扩廓阔垃拉喇蜡腊辣啦莱来赖蓝婪栏拦篮阑兰澜谰揽览懒缆烂滥琅榔狼廊郎朗浪捞劳牢老佬姥酪烙涝勒乐雷镭蕾磊累儡垒擂肋类泪棱楞冷厘梨犁黎篱狸离漓理李里鲤礼莉荔吏栗丽厉励砾历利僳例俐痢立粒沥隶力璃哩俩联莲连镰廉怜涟帘敛脸链恋炼练粮凉梁粱良两辆量晾亮谅撩聊僚疗燎寥辽潦了撂镣廖料列裂烈劣猎琳林磷霖临邻鳞淋凛赁吝拎玲菱零龄铃伶羚凌灵陵岭领另令溜琉榴硫馏留刘瘤流柳六龙聋咙笼窿隆垄拢陇楼娄搂篓漏陋芦卢颅庐炉掳卤虏鲁麓碌露路赂鹿潞禄录陆戮驴吕铝侣旅履屡缕虑氯律率滤绿峦挛孪滦卵乱掠略抡轮伦仑沦纶论萝螺罗逻锣箩骡裸落洛骆络妈麻玛码蚂马骂嘛吗埋买麦卖迈脉瞒馒蛮满蔓曼慢漫谩芒茫盲氓忙莽猫茅锚毛矛铆卯茂冒帽貌贸么玫枚梅酶霉煤没眉媒镁每美昧寐妹媚门闷们萌蒙檬盟锰猛梦孟眯醚靡糜迷谜弥米秘觅泌蜜密幂棉眠绵冕免勉娩缅面苗描瞄藐秒渺庙妙蔑灭民抿皿敏悯闽明螟鸣铭名命谬摸摹蘑模膜磨摩魔抹末莫墨默沫漠寞陌谋牟某拇牡亩姆母墓暮幕募慕木目睦牧穆拿哪呐钠那娜纳氖乃奶耐奈南男难囊挠脑恼闹淖呢馁内嫩能妮霓倪泥尼拟你匿腻逆溺蔫拈年碾撵捻念娘酿鸟尿捏聂孽啮镊镍涅您柠狞凝宁拧泞牛扭钮纽脓浓农弄奴努怒女暖虐疟挪懦糯诺哦欧鸥殴藕呕偶沤啪趴爬帕怕琶拍排牌徘湃派攀潘盘磐盼畔判叛乓庞旁耪胖抛咆刨炮袍跑泡呸胚培裴赔陪配佩沛喷盆砰抨烹澎彭蓬棚硼篷膨朋鹏捧碰坯砒霹批披劈琵毗啤脾疲皮匹痞僻屁譬篇偏片骗飘漂瓢票撇瞥拼频贫品聘乒坪苹萍平凭瓶评屏坡泼颇婆破魄迫粕剖扑铺仆莆葡菩蒲埔朴圃普浦谱曝瀑期欺栖戚妻七凄漆柒沏其棋奇歧畦崎脐齐旗祈祁骑起岂乞企启契砌器气迄弃汽泣讫掐洽牵扦钎铅千迁签仟谦乾黔钱钳前潜遣浅谴堑嵌欠歉枪呛腔羌墙蔷强抢橇锹敲悄桥瞧乔侨巧鞘撬翘峭俏窍切茄且怯窃钦侵亲秦琴勤芹擒禽寝沁青轻氢倾卿清擎晴氰情顷请庆琼穷秋丘邱球求囚酋泅趋区蛆曲躯屈驱渠取娶龋趣去圈颧权醛泉全痊拳犬券劝缺炔瘸却鹊榷确雀裙群然燃冉染瓤壤攘嚷让饶扰绕惹热壬仁人忍韧任认刃妊纫扔仍日戎茸蓉荣融熔溶容绒冗揉柔肉茹蠕儒孺如辱乳汝入褥软阮蕊瑞锐闰润若弱撒洒萨腮鳃塞赛三叁伞散桑嗓丧搔骚扫嫂瑟色涩森僧莎砂杀刹沙纱傻啥煞筛晒珊苫杉山删煽衫闪陕擅赡膳善汕扇缮墒伤商赏晌上尚裳梢捎稍烧芍勺韶少哨邵绍奢赊蛇舌舍赦摄射慑涉社设砷申呻伸身深娠绅神沈审婶甚肾慎渗声生甥牲升绳省盛剩胜圣师失狮施湿诗尸虱十石拾时什食蚀实识史矢使屎驶始式示士世柿事拭誓逝势是嗜噬适仕侍释饰氏市恃室视试收手首守寿授售受瘦兽蔬枢梳殊抒输叔舒淑疏书赎孰熟薯暑曙署蜀黍鼠属术述树束戍竖墅庶数漱恕刷耍摔衰甩帅栓拴霜双爽谁水睡税吮瞬顺舜说硕朔烁斯撕嘶思私司丝死肆寺嗣四伺似饲巳松耸怂颂送宋讼诵搜艘擞嗽苏酥俗素速粟塑溯宿诉肃酸蒜算虽隋随绥髓碎岁穗遂隧祟孙损笋蓑梭唆缩琐索锁所塌他它她塔獭挞蹋踏胎苔抬台泰酞太态汰坍摊贪瘫滩坛檀痰潭谭谈坦毯袒碳探叹炭汤塘搪堂棠膛唐糖倘躺淌趟烫掏涛滔绦萄桃逃淘陶讨套特藤腾疼誊梯剔踢锑提题蹄啼体替嚏惕涕剃屉天添填田甜恬舔腆挑条迢眺跳贴铁帖厅听烃汀廷停亭庭艇通桐酮瞳同铜彤童桶捅筒统痛偷投头透凸秃突图徒途涂屠土吐兔湍团推颓腿蜕褪退吞屯臀拖托脱鸵陀驮驼椭妥拓唾挖哇蛙洼娃瓦袜歪外豌弯湾玩顽丸烷完碗挽晚皖惋宛婉万腕汪王亡枉网往旺望忘妄威巍微危韦违桅围唯惟为潍维苇萎委伟伪尾纬未蔚味畏胃喂魏位渭谓尉慰卫瘟温蚊文闻纹吻稳紊问嗡翁瓮挝蜗涡窝我斡卧握沃巫呜钨乌污诬屋无芜梧吾吴毋武五捂午舞伍侮坞戊雾晤物勿务悟误昔熙析西硒矽晰嘻吸锡牺稀息希悉膝夕惜熄烯溪汐犀檄袭席习媳喜铣洗系隙戏细瞎虾匣霞辖暇峡侠狭下厦夏吓掀锨先仙鲜纤咸贤衔舷闲涎弦嫌显险现献县腺馅羡宪陷限线相厢镶香箱襄湘乡翔祥详想响享项巷橡像向象萧硝霄削哮嚣销消宵淆晓小孝校肖啸笑效楔些歇蝎鞋协挟携邪斜胁谐写械卸蟹懈泄泻谢屑薪芯锌欣辛新忻心信衅星腥猩惺兴刑型形邢行醒幸杏性姓兄凶胸匈汹雄熊休修羞朽嗅锈秀袖绣墟戌需虚嘘须徐许蓄酗叙旭序畜恤絮婿绪续轩喧宣悬旋玄选癣眩绚靴薛学穴雪血勋熏循旬询寻驯巡殉汛训讯逊迅压押鸦鸭呀丫芽牙蚜崖衙涯雅哑亚讶焉咽阉烟淹盐严研蜒岩延言颜阎炎沿奄掩眼衍演艳堰燕厌砚雁唁彦焰宴谚验殃央鸯秧杨扬佯疡羊洋阳氧仰痒养样漾邀腰妖瑶摇尧遥窑谣姚咬舀药要耀椰噎耶爷野冶也页掖业叶曳腋夜液一壹医揖铱依伊衣颐夷遗移仪胰疑沂宜姨彝椅蚁倚已乙矣以艺抑易邑屹亿役臆逸肄疫亦裔意毅忆义益溢诣议谊译异翼翌绎茵荫因殷音阴姻吟银淫寅饮尹引隐印英樱婴鹰应缨莹萤营荧蝇迎赢盈影颖硬映哟拥佣臃痈庸雍踊蛹咏泳涌永恿勇用幽优悠忧尤由邮铀犹油游酉有友右佑釉诱又幼迂淤于盂榆虞愚舆余俞逾鱼愉渝渔隅予娱雨与屿禹宇语羽玉域芋郁吁遇喻峪御愈欲狱育誉浴寓裕预豫驭鸳渊冤元垣袁原援辕园员圆猿源缘远苑愿怨院曰约越跃钥岳粤月悦阅耘云郧匀陨允运蕴酝晕韵孕匝砸杂栽哉灾宰载再在咱攒暂赞赃脏葬遭糟凿藻枣早澡蚤躁噪造皂灶燥责择则泽贼怎增憎曾赠扎喳渣札轧铡闸眨栅榨咋乍炸诈摘斋宅窄债寨瞻毡詹粘沾盏斩辗崭展蘸栈占战站湛绽樟章彰漳张掌涨杖丈帐账仗胀瘴障招昭找沼赵照罩兆肇召遮折哲蛰辙者锗蔗这浙珍斟真甄砧臻贞针侦枕疹诊震振镇阵蒸挣睁征狰争怔整拯正政帧症郑证芝枝支吱蜘知肢脂汁之织职直植殖执值侄址指止趾只旨纸志挚掷至致置帜峙制智秩稚质炙痔滞治窒中盅忠钟衷终种肿重仲众舟周州洲诌粥轴肘帚咒皱宙昼骤珠株蛛朱猪诸诛逐竹烛煮拄瞩嘱主著柱助蛀贮铸筑住注祝驻抓爪拽专砖转撰赚篆桩庄装妆撞壮状椎锥追赘坠缀谆准捉拙卓桌琢茁酌啄着灼浊兹咨资姿滋淄孜紫仔籽滓子自渍字鬃棕踪宗综总纵邹走奏揍租足卒族祖诅阻组钻纂嘴醉最罪尊遵昨左佐柞做作坐座'
charMap = {}
for i in range(len(SPECIAL_CHARS)):
    charMap[SPECIAL_CHARS[i]] = REPLACEMENT_CHARS[i]

# 初始化变量
nonce = str(uuid.uuid4()).upper()
tr = False

# 读取或输入 device_token
try:
    with open('deviceToken.txt', 'r', encoding='utf-8') as file:
        device_token = file.read()
except:
    print("deviceToken 可以在重装菠萝包 APP 并随机点开一部小说后的 Android/data/com.sfacg/files/boluobao/log/com.sfacg.log.txt 中找到。\n如果这个文件里有多个 deviceToken，请使用时间更靠后的那一个。")
    device_token = input("输入 deviceToken: ").upper()
    with open('deviceToken.txt', 'w') as file:
        file.write(device_token)
    tr = True

# 常量
SALT = "FN_Q29XHVmfV3mYX"
headers = {
    'Host': 'api.sfacg.com',
    'accept-charset': 'UTF-8',
    'authorization': 'Basic YW5kcm9pZHVzZXI6MWEjJDUxLXl0Njk7KkFjdkBxeHE=',
    'accept': 'application/vnd.sfacg.api+json;version=1',
    'user-agent': f'boluobao/5.0.36(android;32)/H5/{device_token.lower()}/H5',
    'accept-encoding': 'gzip',
    'Content-Type': 'application/json; charset=UTF-8'
}


def md5_hex(input):
    m = hashlib.md5()
    m.update(input.encode())
    return m.hexdigest().upper()

def get_catalog(novel):
    chapters = {}
    title = ""
    try:
        timestamp = int(time.time() * 1000)
        sign = md5_hex(f'{nonce}{timestamp}{device_token}{SALT}')
        headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
        resp = requests.get(f'https://api.sfacg.com/novels/{novel}?expand=bigNovelCover', headers=headers).json()
        title = resp['data']['novelName']
        author = resp['data']['authorName']
        cover = resp['data']['expand']['bigNovelCover']
    except:
        print("标题获取失败")
        title = "标题获取失败"

    try:
        timestamp = int(time.time() * 1000)
        sign = md5_hex(f'{nonce}{timestamp}{device_token}{SALT}')
        headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
        catalog = requests.get(f'https://api.sfacg.com/novels/{novel}/dirs?expand=originNeedFireMoney', headers=headers).json()
        for volume in catalog['data']['volumeList']:
            chapters[volume['title']] = []
            for chapter in volume['chapterList']:
                chapters[volume['title']].append(chapter['chapId'])
    except:
        print("目录获取失败")
        title = "目录获取失败"
    return title, author, cover, chapters


def download_chapter(chapters):
    chap_texts = []
    for chapter in chapters:
        try:
            content = ""
            timestamp = int(time.time() * 1000)
            sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}")
            headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
            url = f"https://api.sfacg.com/Chaps/{chapter}?expand=content%2Cexpand.content"
            resp = requests.get(url, headers=headers).json()
            if resp['status']['httpCode'] == 200:
                title = resp['data']['title']
                tmp = ""
                if 'content' in resp['data']:
                    tmp += resp['data']['content']
                    if 'expand' in resp['data'] and 'content' in resp['data']['expand']:
                        tmp += resp['data']['expand']['content']
                else:
                    tmp += resp['data']['expand']['content']
                text = ''
                for char in tmp:
                    text += charMap.get(char, char)
                content += text
                chap_texts.append({'title':title,'content':content,'id':chapter})
                print(f"{title} 已下载")
            else:
                print(f"{chapter} 下载失败，请检查是否未订阅该章节")
        except:
            print(f"{chapter} 下载失败，可能是网络问题")
    return chap_texts


def get_cookie(username, password):
    timestamp = int(time.time() * 1000)
    sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}")
    headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
    data = json.dumps({"password": password, "shuMeiId": "", "username": username})
    resp = requests.post("https://api.sfacg.com/sessions", headers=headers, data=data)
    if resp.json()["status"]["httpCode"] == 200:
        cookie = requests.utils.dict_from_cookiejar(resp.cookies)
        return f'.SFCommunity={cookie[".SFCommunity"]}; session_APP={cookie["session_APP"]}'
    else:
        return "1"#"请检查账号或密码是否错误"

if __name__ == "__main__":
    novel = input("输入小说ID: ")
    username = input("输入手机号: ")
    password = input("输入密码: ")
    headers['cookie'] = get_cookie(username, password)
    if headers['cookie'] == "请检查账号或密码是否错误":
        print("请检查账号或密码是否错误")
    else:
        title, author, cover, chapters = get_catalog(novel)
        if title in ['标题获取失败', '目录获取失败']:
            exit()
        print(title)
        i = 0
        for volume in chapters:
            i += 1
            print(i, ':', volume)
        tot = i
        tr = True
        while tr:
            down = input("请输入需要下载的卷号(如 1,3-5，不输入则全下载): ")
            try:
                downList = []
                if down == '':
                    downList = list(range(1, tot + 1))
                else:
                    for part in down.split(','):
                        if '-' in part:
                            start, end = map(int, part.split('-'))
                            downList.extend(range(start, end + 1))
                        else:
                            downList.append(int(part))
                downList = list(set(downList))
                tr = False
            except:
                print('卷号输入错误，请重新输入')
        print("计划下载卷:", downList)
        
        book = epub.EpubBook()
        book.set_identifier(str(uuid.uuid4()))
        book.set_title(title)
        book.set_language('zh')
        book.add_author(author)
        img = requests.get(cover).content
        book.set_cover('cover.jpg',img)
        i = 0
        content = title + '\n\n'
        toc = []
        spine = ['nav']
        for volume in chapters:
            i += 1
            if i in downList:
                print('正在下载:', volume)
                content += volume + '\n\n'
                chap_texts = download_chapter(chapters[volume])
                vol_toc = []
                vol_c = epub.EpubHtml(title=volume, file_name=f'vol_{i}.xhtml', lang='zh')
                vol_c.content = f"<h2>{volume}</h2>"
                book.add_item(vol_c)
                spine.append(vol_c)
                for chapter in chap_texts:
                    content += f"{chapter['title']}\n{chapter['content']}\n\n"
                    c = epub.EpubHtml(title=chapter['title'], file_name=f"chap_{chapter['id']}.xhtml", lang='zh')
                    c.content = f"<h2>{chapter['title']}</h2>"
                    for line in chapter['content'].splitlines():
                        if '[img=' in line:
                            url = re.search(r'https?://.*?(?=\[\/img\]|$)',line).group()
                            img = requests.get(url).content
                            url = url.split('/')[-1]
                            print(f"图片{url} 下载完成")
                            img_item = epub.EpubImage(uid=str(uuid.uuid4()),file_name=f"img/{url}", media_type='image/jpg', content=img)
                            c.content += f'<img src="img/{url}"/>'
                            book.add_item(img_item)
                        else:
                            c.content += f"<p>{line}</p>"
                    book.add_item(c)
                    vol_toc.append(c)
                    spine.append(c)
                toc.append((vol_c, tuple(vol_toc)))
        book.toc = tuple(toc)
        book.spine =spine
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        title_clean = re.sub(r'[\\/:*?"<>|]', ' ', title)        
        epub.write_epub(f"{title_clean}{downList}.epub", book, {})
        with open(f'{title_clean}{downList}.txt', 'w', encoding="utf-8") as f:
            f.write(content)

        print(f"已保存为 TXT 和 EPUB：{title_clean}.txt / {title_clean}.epub")
