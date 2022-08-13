import os
import sys

from durable.lang import *


class Figure():
    height: float
    weight: float
    height2: float

    g_hip_167: float
    g_abdomen_161: float 
    g_waist_163: float 
    g_shoulder_104: float
    g_sum_167_104: float # 167 + 104
    g_waist_155: float
    g_neck_140: float
    g_upper_chest_143: float
    g_bust_144: float
    g_lbiceps_125: float
    g_lwrist_123: float
    g_rbiceps_126: float
    g_rwrist_121: float
    g_lmthigh_111: float
    g_rmthigh_112: float
    g_lmcalf_115: float
    g_rmcalf_116: float
    g_lankle_117: float
    g_rankle_118: float

    w_shoulder_210_211: float #肩宽
    w_head_212_213: float  #头宽
    w_busts_205_206: float #乳距

    h_head_202: float #头长
    h_leg_333_334: float
    h_upper_body: float # height - h_leg_333_334
    h_upper_leg: float # 


Params_DICT = {
    34: {
        'symptom_desc': "臀围反映髋部骨骼和肌肉的发育情况。测量时，两腿并拢直立，两臂自然下垂，皮尺水平放在前面的耻骨联合和背后臀大肌最凸处。"
    },
    35: {
        'symptom_desc': "男人的臂围，直接反映了男人的力量。手臂围度是男人的第二张脸，是你的门面，是安全感的象征。"
    },
    36: {
        'symptom_desc': "大腿内外两侧容易堆积脂肪，结实健美的腿，才是人体最美的线条之一。身高(cm)×0.18;小腿的比例约为身高的17%-21%都属正常，重要的是其形状如何。"
    },
    37: {
        'symptom_desc': "腿围作为人体形态指标之一，形象地映射出人体腿部肌肉的发育水平和腿部的发达程度，以及形体美。小腿腿围也成为了当今社会越来越多男性女性关注的重点，每个年龄段和身高都有一个小腿腿围标准哦。"
    },
    31: {
        'symptom_desc': "脖子这个部位是影响人整体身材和气质的关键，其他的部位，可以靠衣服遮掩，但是脖子不可以。你的脖子属于偏粗类型，它正影响着你的整体美观。"
    },
    32: {
        'symptom_desc': "腰粗一寸，病长一分。倘若人的腰围过粗的话，不仅会影响到人的相貌，而且也会影响到身体的身体健康。"
    },
    33: {
        'symptom_desc': "一个身材好与不好，都可以从三围来判定，特别是胸围。不仅是女性会在意自己的身材，男性也会在意自己的身材。而且现在越来越多男性喜欢去健身房了，希望自己也能有一个让人羡慕的身材。"
    },
    21: {
        'symptom_desc': ""
    },
    22: {
        'symptom_desc': ""
    },
    23: {
        'symptom_desc': ""
    },
    24: {
        'symptom_desc': ""
    },
    25: {
        'symptom_desc': ""
    },
    411: {
        'symptom_desc': "拥有完美“头肩比”的你，是每一次合影中最抢眼的那个，一个赤裸裸的合影杀手哦～"
    },
    421: {
        'symptom_desc': ""
    },
    431: {
        'symptom_desc': ""
    },
    441: {
        'symptom_desc': ""
    },
    451: {
        'symptom_desc': ""
    },
    461: {
        'symptom_desc': ""
    },
    412: {
        'symptom_desc': ""
    },
    422: {
        'symptom_desc': ""
    },
    432: {
        'symptom_desc': ""
    },
    442: {
        'symptom_desc': ""
    },
    452: {
        'symptom_desc': ""
    },
    462: {
        'symptom_desc': ""
    },
    611: {
        'symptom_desc': "拜拜肉藏在胳膊底下，一举手晃动着说“拜拜”就摇晃不已，故称为拜拜肉。拜拜肉位于我们手臂肱三头肌部分，除去多余的脂肪原因，因为肱三头肌松弛无力而导致拜拜肉急剧加重，从而形成拜拜肉。"
    },
    612: {
        'symptom_desc': "拜拜肉藏在胳膊底下，一举手晃动着说“拜拜”就摇晃不已，故称为拜拜肉。拜拜肉位于我们手臂肱三头肌部分，除去多余的脂肪原因，因为肱三头肌松弛无力而导致拜拜肉急剧加重，从而形成拜拜肉。"
    },
    # 621: {
    #     'symptom_desc': "乳房下垂是指乳房在合理情形下，尤其是年轻的妇女，乳头的水平位置是在乳房下皱襞之上，若掉在其下即是所谓的乳房下垂。下垂得越严峻，就掉得越低。"
    # },
    # 622: {
    #     'symptom_desc': "乳房下垂是指乳房在合理情形下，尤其是年轻的妇女，乳头的水平位置是在乳房下皱襞之上，若掉在其下即是所谓的乳房下垂。下垂得越严峻，就掉得越低。"
    # },
    621: {
        'symptom_desc': "腹部有游泳圈是长期摄入热量多、消耗少，腹部脂肪长期堆积，缺乏锻炼导致腹部肥胖的表现，此类肥胖属于内脏型肥胖。腹部肥胖对体型的美观影响较大"
    },
    622: {
        'symptom_desc': "腹部有游泳圈是长期摄入热量多、消耗少，腹部脂肪长期堆积，缺乏锻炼导致腹部肥胖的表现，此类肥胖属于内脏型肥胖。腹部肥胖对体型的美观影响较大"
    },


}

BMI_Scores = {
    'thin': {'score': 4, 'desc': '你的体重偏瘦弱，平时要多吃点肉肉哦～'},
    'fat': {'score': 3, 'desc': '你的体重偏肥胖，处于不健康区间，要减肥啦！'},
    'normal': {'score': 6, 'desc': '你的体重非常标准～保持良好的饮食习惯和适当的运动，追求完美身材吧'},
    'perfect': {'score': 8, 'desc': '你的体重堪称完美，请保持哦～'}
}

Body_Scores ={
    121: {
        'score': 20, 
        'desc':'。',
        'suggest': ''
    },
    122: {
        'score': 15, 
        'desc':'。',
        'suggest': ''
        },
    123: {
        'score': 10, 
        'desc':'',
        'suggest': ''
        },
    124: {
        'score': 6, 
        'desc':'。',
        'suggest': ''
        },

}

BMI_Results = ("偏瘦", "完美", "标准", "偏胖")
Body_Results = ("倒三角身材  ",
                "矩形身材",
                "正三角身材",
                "椭圆形身材",)

Part_Scores = {
    211: {
        'score': 6,
        'desc': '拥有完美“头肩比”的你，是每一次合影中最抢眼的那个，一个赤裸裸的合影杀手哦～',
        'symptom_desc': '拥有完美“头肩比”的你，是每一次合影中最抢眼的那个，一个赤裸裸的合影杀手哦～',
        'suggest': '',
        'tip': ''

    },
    212: {
        'score': 4,
        'desc': '标准的头肩比，使得你看起来身姿相对挺拔有气场。',
        'symptom_desc': '通常情况下,男性理想的头肩比在1 : 1.5左右,稍微宽一点会更显高,但不能超过1 : 2,否则就会显得“头太小”。',
        'suggest': '',
        'tip': '选衣服应该圆领不选V领，因为V领的视觉效果是往下延伸的，会把肩膀切割出来。而圆领的视觉效果是左右延伸的，看起来肩膀更平更宽。'
    },
    213: {
        'score': 2,
        'desc': '较窄的肩宽 ，使得在上镜时尤其容易暴露，所以想要让自己的“头肩比”更加和谐，选对发型和造型是关键！',
        'symptom_desc': '通常情况下,女性理想的头肩比在1 : 1.5左右,稍微宽一点会更显高,但不能超过1 : 2,否则就会显得“头太小”。',
        'suggest': '你适合选择泡泡袖、荷叶边或者有小垫肩的衣服，从视觉上增加肩宽，让比例变得更加协调。',
        'tip': '在训练中适当的加入肩部的训练，比如肩上推举，实力举，侧平举等 。'

    },

    221: {
        'score': 2,
        'desc': '你的头身比例犹如古希腊的雕像。世界上只有0.01%的人才拥有这么完美的比例。',
        'symptom_desc': '你的头身比例犹如古希腊的雕像。世界上只有0.01%的人才拥有这么完美的比例。',
        'tip': '',
        'suggest': '我没有办法为你推荐穿搭，因为你怎么穿都很美。'
    },
    222: {
        'score': 1,
        'desc': '你的头部和身体的比例为1:7，是标准的7头身。这样的比例会让人感觉很容易亲近，相处起来舒适。',
        'symptom_desc': '你的头部和身体的比例为1:7，是标准的7头身。这样的比例会让人感觉很容易亲近，相处起来舒适。',
        'suggest': '',
        'tip': ''
    },
    223: {
        'score': 0,
        'desc': '',
        'symptom_desc': '从人体美学来讲，净身长7个头是最接近更多人的比例，净身长7.5头是好看的比例，而净身长8个头是黄金比例，是最完美的。而上下身比例的失衡，造成一种“头重脚轻”的既视感。',
        'suggest': '',
        'tip': '可以通过合适的穿搭改变视觉效果，只要注意选择合适的衣长，以及适当地露出腰线即可。'
    },

    231: {
        'score': 16,
        'desc': '',
        'symptom_desc': '决定腿长的因素有很多，我们日常观察中，看一个人是否腿长，主要注意的要点是腰高和档位。显而易见，腰和档位越高的人，腿看起来（实际上也）就越长。',
        'suggest': '',
        'tip': ''
    },
    232: {
        'score': 12,
        'desc': '',
        'symptom_desc': '决定腿长的因素有很多，我们日常观察中，看一个人是否腿长，主要注意的要点是腰高和档位。显而易见，腰和档位越高的人，腿看起来（实际上也）就越长。',
        'suggest': '',
        'tip': ''
    },
    233: {
        'score': 10,
        'desc': '你的腿部比例是标准的亚洲腿比例。',
        'symptom_desc':'决定腿长的因素有很多，我们日常观察中，看一个人是否腿长，主要注意的要点是腰高和档位。显而易见，腰和档位越高的人，腿看起来（实际上也）就越长。',
        'suggest': '',
        'tip': ''
    },
    234: {
        'score': 6,
        'desc': '你的小腿和大腿的比例低于1。',
        'symptom_desc': '决定腿长的因素有很多，我们日常观察中，看一个人是否腿长，主要注意的要点是腰高和档位。显而易见，腰和档位越高的人，腿看起来（实际上也）就越长。',
        'suggest': '你适合高腰的穿法，在视觉上营造“三七分”的效果，颜色搭配尽可能区分上衣和裤子的颜色，选择这种有反差感的搭配，在视觉上效果会更明显。',
        'tip': '你适合高腰的穿法，在视觉上营造“三七分”的效果，颜色搭配尽可能区分上衣和裤子的颜色，选择这种有反差感的搭配，在视觉上效果会更明显'
    },

    241: {
        'score': 4,
        'desc': '你的大小腿比例太完美了。',
        'symptom_desc': '大腿的正常尺寸是身高乘0.34，小腿的正常比例是身高乘0.21，也就是说大小腿的正常比例一般为3:2。如果大小腿的比例不太符合3:2，就是说腿部比例失衡。',
        'suggest': '',
        'tip': ''
    },
    242: {
        'score': 1,
        'desc': '你的大小腿比例属于标准范围。',
        'symptom_desc': '大腿的正常尺寸是身高乘0.34，小腿的正常比例是身高乘0.21，也就是说大小腿的正常比例一般为3:2。如果大小腿的比例不太符合3:2，就是说腿部比例失衡。',
        'suggest': '',
        'tip': ''
    },

    251: {
        'score': 12,
        'desc': '你的腰臀比堪称完美，超级棒哦～',
        'symptom_desc': '腰臀比是早期研究中预测肥胖的指标。比值越小，说明越健康。这是预测一个人是否肥胖及是否面临患心脏病风险的较佳方法，比目前普遍使用的测量体重指数(体重除以身高的平方)的方法要准确3倍。腰围尺寸大，表明脂肪存在于腹部，是危险较大的信号；而一个人臀围大，表明其下身肌肉发达，对人的健康有益。',
        'suggest': '',
        'tip': ''
    },
    252: {
        'score': 4,
        'desc': '你的腰臀比过高，一定要注意了，这是很危险的肥胖信号。腰臀比过高可能会导致糖尿病、高血压、高血脂等病症。另外，腰部脂肪还会导致肝肥大，使它无法发挥正常功能。',
        'symptom_desc':'腰臀比是早期研究中预测肥胖的指标。比值越小，说明越健康。这是预测一个人是否肥胖及是否面临患心脏病风险的较佳方法，比目前普遍使用的测量体重指数(体重除以身高的平方)的方法要准确3倍。腰围尺寸大，表明脂肪存在于腹部，是危险较大的信号；而一个人臀围大，表明其下身肌肉发达，对人的健康有益。',
        'suggest': '你适合穿着V领、一字领的裙子，这样会让你看起来更瘦哦!',
        'tip': '手持哑铃，腰背应挺直同时收紧核心，单腿向前跨出后，重心下沉，但跨出那条腿的小腿应垂直于地面。然后，注意用臀腿肌群发力，起身。两腿轮流，交替进行。'
    },

    253: {
        'score': 7,
        'desc': '你的腰臀比很标准，超过了58%的女性哦～',
        'symptom_desc':'腰臀比是早期研究中预测肥胖的指标。比值越小，说明越健康。这是预测一个人是否肥胖及是否面临患心脏病风险的较佳方法，比目前普遍使用的测量体重指数(体重除以身高的平方)的方法要准确3倍。腰围尺寸大，表明脂肪存在于腹部，是危险较大的信号；而一个人臀围大，表明其下身肌肉发达，对人的健康有益。',
        'suggest': '',
        'tip': ''
    },
    261: {
        'score': 0,
        'desc': '胸型外扩是指乳房向两边长，形不成乳沟，影响美观。',
        'suggest': '',
        'tip': '建议穿具有调整胸型的内衣，多做胸部运动或者多做健美操让胸部坚挺，需要长时间坚持锻炼。'
    },

    262: {
        'score': 2,
        'desc': '你的胸型非常标准～',
        'suggest': '',
        'tip': '建议穿具有调整胸型的内衣，多做胸部运动或者多做健美操让胸部坚挺，需要长时间坚持锻炼。'
    },
}

Detail_Scores = {
    311: {
        'score': 2,
        'desc': '你的脖型非常修长，请保持哦～',
        'suggest': '你适合穿着简约的高领针织衫，配上修身的西服外套，就是飒酷时尚的模样，整体风格特别显高。',
        'symptom_desc': Params_DICT[31]['symptom_desc'],
        'tip': '你适合穿着简约的高领针织衫，配上修身的西服外套，就是飒酷时尚的绅士，整体风格特别显高。'
    },

    312: {
        'score': 1,
        'desc': '你的脖型非常标准，请保持哦～',
        'suggest': '',
        'symptom_desc': Params_DICT[31]['symptom_desc'],
        'tip': '你适合穿着简约的高领针织衫，配上修身的西服外套，就是飒酷时尚的模样，整体风格特别显高。'
    },

    313: {
        'score': 0,
        'desc': '你的脖型属于相对较粗类型，有很大的提升空间哦',
        'suggest': '我们可以多多动起来，通过挥动天鹅臂来消除斜方肌哦。',
        'symptom_desc':  Params_DICT[31]['symptom_desc'],
        'tip': '胸部扩展：用自己的双手握住毛巾，然后再吸气、挺胸，抬起下巴向斜上方牵引颈椎，同时双臂向斜后方向伸展，扩展胸腔，保持几秒钟。最后呼气，含胸低头，收回下巴贴近锁骨，伸展肩颈肌肉。保持几秒钟，重复5-8次。每天最少要做二十组。'
    },

    321: {
        'score': 6,
        'desc': '你的腰围非常纤细，请保持哦～',
        'suggest': '',
        'symptom_desc':  Params_DICT[32]['symptom_desc'],
        'tip': '你有一个倒三角形身材的底子，锻炼你的肩部和背部肌肉，可以让你看起来更加具有魅力哦'
    },
    322: {
        'score': 4,
        'desc': '你的腰围很标准，请保持哦～',
        'suggest': '',
        'symptom_desc':  Params_DICT[32]['symptom_desc'],
        'tip': ''
    },

    323: {
        'score': 0,
        'desc': '你的腰围属于偏胖类型，快快行动起来吧～',
        'suggest': '你适合穿着上半身深色系的衣服，这样才能起到遮肉显瘦的作用哦。',
        'symptom_desc':  Params_DICT[32]['symptom_desc'],
        'tip': '男性朋友如果想要减掉肚子上的赘肉，一定要避免久坐，改掉久坐不运动的坏习惯，坐一段时间一定要站起来走一走，这样能够帮助加速身体的血液循环和新陈代谢速率，坚持下去你的大肚腩会悄悄溜走。'
    },

    331: {
        'score': 6,
        'desc': '你拥有一对傲人的胸，真让人羡慕～',
        'suggest': '',
        'symptom_desc': Params_DICT[33]['symptom_desc'],
        'tip': ''
    },

    332: {
        'score': 4,
        'desc': '你的胸围很标准，已经超过了74%的女性哦～',
        'suggest': '',
        'symptom_desc': Params_DICT[33]['symptom_desc'],
        'tip': ''
    },

    333: {
        'score': 1,
        'desc': '你的胸围属于平坦型，可以尝试走气质路线',
        'suggest': '你适合挑选设计简单的上衣，对于胸部的平面来说可以展现高级感。',
        'symptom_desc': Params_DICT[33]['symptom_desc'],
        'tip': '胸大肌分为胸肌上束、中束、下束，我们需要全方位锻炼，比如：卧推的时候可以采用上斜卧推、平板卧推、下斜卧推等不同角度来刺激胸肌，还可以采用哑铃夹胸、飞鸟来刺激胸肌中缝。'
    },

    341: {
        'score': 4,
        'desc': '你的臀围堪称完美，请保持哦～',
        'suggest': '',
        'symptom_desc': Params_DICT[34]['symptom_desc'],
        'tip': ''
    },

    342: {
        'score': 2,
        'desc': '你的臀围非常标准，超过了59%的女性哦～',
        'suggest': '',
        'symptom_desc':  Params_DICT[34]['symptom_desc'],
        'tip': ''
    },

    343: {
        'score': 0,
        'desc': '你的臀围属于偏大类型，你距离迷人蜜桃臀仅有一步之遥哦～',
        'suggest': '你适合搭配百褶裙或者是A字裙，这两种裙子的裙型都是在腰部的地方进行收腰，下摆都会向外扩散，这样的话就会很好的掩盖臀围大的缺点。',
        'symptom_desc':  Params_DICT[34]['symptom_desc'],
        'tip': '双腿后踢：男生可以扶住墙面或者栏杆,将一侧下肢最大限度向后踢,双侧下肢交替完成双腿后踢,也可以有效减少臀部脂肪'
    },

    344: {
        'score': 0,
        'desc': '你的臀围偏小，赶快行动修炼蜜桃臀吧～',
        'suggest': '你适合穿着在臀部或胯部两侧有口袋设计的休闲裤，如果口袋有袋盖或是立体口袋，有铆钉、刺绣装饰，效果会更好。',
        'symptom_desc':  Params_DICT[34]['symptom_desc'],
        'tip': '宽距高脚杯深蹲：双脚分开站立，保证之间的距离比肩宽且易于进行动作，身体挺直不要弯曲，胸部挺起，腹部肌肉收紧，双臂弯曲在胸前，双手捧住哑铃。双腿弯曲，臀部向后坐，下蹲一直到大腿大约与地面平行，下蹲过程中身体上半身保证不要弯曲向前稍微倾斜，下蹲结束后起身还原准备的姿势。'
    },

    351: {
        'score': 2,
        'desc': '你的臂围堪称完美，请保持哦～',
        'suggest': '',
        'symptom_desc':  Params_DICT[35]['symptom_desc'],
        'tip': ''
    },

    352: {
        'score': 1,
        'desc': '你的臂围非常标准，超过62%的女性哦～',
        'suggest': '',
        'symptom_desc': Params_DICT[35]['symptom_desc'],
        'tip': ''
    },

    353: {
        'score': 0,
        'desc': '你的手臂有拜拜肉倾向，赶快消除它吧～',
        'suggest': '你适合穿着带蝴蝶袖的上衣。蝴蝶袖的造型随性飘逸，设计感强，流畅的线条对体型有良好的修饰作用，遮盖粗手臂，毫不累赘',
        'symptom_desc':   Params_DICT[35]['symptom_desc'],
        'tip': '负重摇臂运动：首先需要准备一个重量物体，比如哑铃或者是一本书;然后身体站立并且挺直，让双手拿着重物放在胸前;接着晃动手臂，向下摆到大腿位置，注意摆动的时候手臂肘尽量贴近身体的两侧;然后，再向上举到与肩同高的位置，手臂向内弯曲。最后重复上述动作即可。'
    },

    354: {
        'score': 0,
        'desc': '你的手臂偏细小，让他丰满起来更具魅力吧～',
        'suggest': '',
        'symptom_desc':  Params_DICT[35]['symptom_desc'],
        'tip': '单臂哑铃训练：选用合适重量的哑铃辅助训练，训练时靠单手和单腿的力量支撑在一定的训练椅上，上身保持平直状态，单手紧握杠铃，利用大臂的力量带动抬举杠铃，多次重复抬举动作后进行换边训练。'
    },

    361: {
        'score': 2,
        'desc': '你的大腿围堪称完美，请保持哦～',
        'suggest': '',
        'symptom_desc': Params_DICT[36]['symptom_desc'],
        'tip': ''
    },

    362: {
        'score': 1,
        'desc': '你的大腿围非常标准，超过了59%的女性哦～',
        'suggest': '',
        'symptom_desc':Params_DICT[36]['symptom_desc'],
        'tip': ''
    },

    363: {
        'score': 0,
        'desc': '你的大腿围偏粗，赶快行动起来吧！',
        'suggest': '选择下装的时候，一定要注意面料的选择，绝对不能选择软塌塌、没型的版型，那样会更加暴露你腿部的缺点。像是针织裤、雪纺这些垂顺感强的面料也要慎重',
        'symptom_desc': Params_DICT[36]['symptom_desc'],
        'tip': '游泳是对于一些平时缺乏运动的朋友来说，不仅强度适中，而且还能够有效锻炼身体，减少身体堆积的肥肉。在水中运动的时候，我们需要调动身体各个部位的肌肉，所以也能够完整塑造我们美妙的身材。这对于想要减去腿部肥肉的朋友来说，是非常重要的一件事情。'
    },

    364: {
        'score': 0,
        'desc': '你的大腿偏细，快快让它丰满起来吧～',
        'suggest': '',
        'symptom_desc': Params_DICT[36]['symptom_desc'],
        'tip': '蛙跳、下蹲与深蹲跳作为开始是个不错的选择，而作为进阶，硬拉与深蹲则能更好的塑造你的腿部肌肉，从而使腿部的线条更为有力。同时，作为训练后的一环，腿部训练要求更多的休息与放松。'
    },


    371: {
        'score': 4,
        'desc': '你的小腿堪称完美，请保持哦～',
        'suggest': '',
        'symptom_desc': Params_DICT[37]['symptom_desc'],
        'tip': ''
    },

    372: {
        'score': 2,
        'desc': '你的小腿围非常标准，超过了62%的女性哦～',
        'suggest': '',
        'symptom_desc': Params_DICT[37]['symptom_desc'],
        'tip': ''
    },

    373: {
        'score': 0,
        'desc': '你的小腿偏细，让他丰满起来更具魅力吧～',
        'suggest': '',
        'symptom_desc':Params_DICT[37]['symptom_desc'],
        'tip': '平时可以多训练冲刺跑。因为对爆发力要求高，能够全面提升小腿腿围和肌肉。'
    },

    374: {
        'score': 0,
        'desc': '你的小腿偏粗，赶紧行动起来吧～',
        'suggest': '你适合选择裸色的高跟鞋，鞋面会和脚背的肤色融合在一起，在视觉上能拉长小腿。需要注意的是，鞋跟不必太细太高，鞋跟太高会让小腿的肌肉更突出，而且会和小腿形成明显的锥子型，起到反效果。',
        'symptom_desc': Params_DICT[37]['symptom_desc'],
        'tip': ' 平躺在靠近墙的垫子上，脚踩住墙面坐提踵，形象点就是上文提到的判断方法旋转90度，再形象点就是平常的坐姿，只不过变成背着地，脚贴墙，然后做抬脚跟，踮脚尖的动作。'
    },

    381: {
        'score': 2,
        'desc': '你的脚踝堪称完美，请保持哦～',
        'suggest': '',
        'symptom_desc': '',
        'tip': ''
    },

    382: {
        'score': 1,
        'desc': '你的脚踝非常标准，超过了71%的女性哦～',
        'suggest': '',
        'symptom_desc': '',
        'tip': ''
    },

    383: {
        'score': 0,
        'desc': '你的脚踝偏粗，赶紧瘦下来更具魅力吧～',
        'suggest': '你适合穿高跟鞋，穿上高跟鞋后，脚踝变细了不少,整个小腿也变得纤细匀称。',
        'symptom_desc': '',
        'tip': ''
    },

    384: {
        'score': 0,
        'desc': '你的脚踝偏细，让他丰满起来更具魅力吧～',
        'suggest': '',
        'symptom_desc': '',
        'tip': ''
    },

}

Element_Scores = {

    511: {
        'score': 0,
        'desc': '体重偏瘦或许已经危害到你的健康，建议你保持良好睡眠，适当食用含高卡路里食物，保持良好的饮食习惯。',
        'suggest': ''
    },

    512: {
        'score': 0,
        'desc': '你当前的体重处于标准体重范围，状态良好，保持良好的饮食习惯和适当的运动，追求完美身材吧。',
        'suggest': ''
    },

    513: {
        'score': 0,
        'desc': '你当前的体重处于不健康区间！请减少高油高热量食物摄入，加强身体锻炼，努力恢复健康体重和好身材。',
        'suggest': ''
    },

    514: {
        'score': 0,
        'desc': '你当前的体重远高于标准体重，过度肥胖不仅形体臃肿，更是各种慢性疾病的主要导火线，请减少高脂肪、高热量食物的摄入，制定健身计划，加强锻炼，努力恢复健康体重和好身材。',
        'suggest': ''
    },

    521: {
        'score': 0,
        'desc': '你当前的体脂肪水平偏低，处于危险区间。脂肪是维持人体新陈谢和运动的能量物质，过多/过少都不利于健康，建议均衡搭配饮食，适当增加卡路里摄入量。',
        'suggest': ''
    },

    522: {
        'score': 0,
        'desc': '你当前的体脂肪水平标准。保持健康规律作息，注意保持摄入足够水分，增加代谢，有利于保持健康标准体脂率。',
        'suggest': ''
    },

    523: {
        'score': 0,
        'desc': '你当前的体脂肪水平偏高，处于危险区间。脂肪是维持人体新陈谢和运动的能量物质，过多/过少都不利于健康，请注意控制高油高脂食物的摄入，并且多做运动',
        'suggest': ''
    },

    524: {
        'score': 0,
        'desc': '你当前的体脂水平严重偏高，处于危险区间。脂肪是维持人体新陈谢和运动的能量物质，过多/过少都不利于健康，请注意控制高油高脂食物的摄入，并且多做运动',
        'suggest': ''
    },

    525: {
        'score': 0,
        'desc': '你当前的体脂肪水平偏低，处于危险区间。脂肪是维持人体新陈谢和运动的能量物质，过多/过少都不利于健康，建议均衡搭配饮食，适当增加卡路里摄入量。',
        'suggest': ''
    },

    526: {
        'score': 0,
        'desc': '你当前的体脂肪水平标准。保持健康规律作息，注意保持摄入足够水分，增加代谢，有利于保持健康标准体脂率。',
        'suggest': ''
    },

    527: {
        'score': 0,
        'desc': '你当前的体脂肪水平偏高，处于危险区间。脂肪是维持人体新陈谢和运动的能量物质，过多/过少都不利于健康，请注意控制高油高脂食物的摄入，并且多做运动',
        'suggest': ''
    },

    528: {
        'score': 0,
        'desc': '你当前的体脂水平严重偏高，处于危险区间。脂肪是维持人体新陈谢和运动的能量物质，过多/过少都不利于健康，请注意控制高油高脂食物的摄入，并且多做运动',
        'suggest': ''
    },
}

Xiachui_Scores = {
        611: {
        'score': 0,
        'desc': '',
        'suggest': '',
        'symptom_desc': Params_DICT[611]['symptom_desc'],
        'tip': '单臂伸展运动：这个动作可以锻炼到肩部肌肉和肱三头肌，还能顺带锻炼到胸部、腹部、背部、臀部大腿和小腿的肌肉。将手臂按压在放在地板上的枕头上，腿向后伸直使身体呈一条直线。将右侧手臂向右伸展，掠过地板向上抬起。 稍作停顿后，放下手臂回到初 始位置，整个过程中尽量保持身体的直线状态。将手臂向前抬起与地板平行，然后再向上抬起，再回到初始动作。持续30秒后，换手臂再做30秒。然后深呼吸 30秒放松'
    },
        612: {
        'score': 0,
        'desc': '',
        'suggest': '',
        'symptom_desc':  Params_DICT[612]['symptom_desc'],
        'tip': '平时在饮食上，多吃促进血液循环的食物，如番茄、红辣椒等，以及草莓、苹果、菠萝、香蕉、梅子、猕猴桃、柠檬等水果'
    },

        621: {
        'score': 0,
        'desc': '',
        'suggest': '',
        'symptom_desc':  Params_DICT[621]['symptom_desc'],
        'tip': '可以选择多运动一下，比如说多出去跑跑步，游泳或者是跳绳之类的，这样都有利于这部分的赘肉减掉，另外可以做俯卧撑或者是仰卧起坐，还有在饮食方面也要记得适当的节食，千万不要再吃太油腻的食物。'
    },

        622: {
        'score': 0,
        'desc': '',
        'suggest': '',
        'symptom_desc':  Params_DICT[622]['symptom_desc'],
        'tip': '日常一定注意清淡饮食，多摄入全麦类等膳食纤维含量丰富，又容易让人产生饱腹感的食物，保证正常热量的摄入。每日保证合适的体育锻炼，多做转呼啦圈等可以有效促进腹部脂肪燃烧的运动。'
    },
    #     631: {
    #     'score': 0,
    #     'desc': '',
    #     'suggest': '',
    #     'symptom_desc':  Params_DICT[631]['symptom_desc'],
    #     'tip': '可以选择多运动一下，比如说多出去跑跑步，游泳或者是跳绳之类的，这样都有利于这部分的赘肉减掉，另外可以做俯卧撑或者是仰卧起坐，还有在饮食方面也要记得适当的节食，千万不要再吃太油腻的食物。'
    # },
    #     632: {
    #     'score': 0,
    #     'desc': '',
    #     'suggest': '',
    #     'symptom_desc':  Params_DICT[632]['symptom_desc'],
    #     'tip': '日常一定注意清淡饮食，多摄入全麦类等膳食纤维含量丰富，又容易让人产生饱腹感的食物，保证正常热量的摄入。每日保证合适的体育锻炼，多做转呼啦圈等可以有效促进腹部脂肪燃烧的运动.'
    # },
}

BMI_Standards = {
    150: {
        'top_w': 105,
        'down_w': 81,
        'perfect_w': 90,
    },
    151: {
        'top_w': 106,
        'down_w': 82,
        'perfect_w': 91.2,
    },
    152: {
        'top_w': 107,
        'down_w': 83.2,
        'perfect_w': 92.4,
    },
    153: {
        'top_w': 108,
        'down_w': 84.2,
        'perfect_w': 93.6,
    },
    154: {
        'top_w': 109,
        'down_w': 85.4,
        'perfect_w': 94.8,
    },
    155: {
        'top_w': 110,
        'down_w': 86.4,
        'perfect_w': 96.2,
    },
    156: {
        'top_w': 111,
        'down_w': 87.6,
        'perfect_w': 97.4,
    },
    157: {
        'top_w': 112,
        'down_w': 88.8,
        'perfect_w': 98.6,
    },
    158: {
        'top_w': 113,
        'down_w': 89.8,
        'perfect_w': 99.8,
    },
    159: {
        'top_w': 114,
        'down_w': 91,
        'perfect_w': 101.2,
    },
    160: {
        'top_w': 115,
        'down_w': 92.2,
        'perfect_w': 102.4,
    },
    161: {
        'top_w': 116,
        'down_w': 93.4,
        'perfect_w': 103.6,
    },
    162: {
        'top_w': 117,
        'down_w': 94.4,
        'perfect_w': 105,
    },
    163: {
        'top_w': 118,
        'down_w': 95.6,
        'perfect_w': 106.2,
    },
    164: {
        'top_w': 119,
        'down_w': 96.8,
        'perfect_w': 107.6,
    },
    165: {
        'top_w': 120,
        'down_w': 98,
        'perfect_w': 109,
    },
    166: {
        'top_w': 121,
        'down_w': 99.2,
        'perfect_w': 110.2,
    },
    167: {
        'top_w': 122,
        'down_w': 100.4,
        'perfect_w': 111.6,
    },
    168: {
        'top_w': 123,
        'down_w': 101.6,
        'perfect_w': 112.8,
    },
    169: {
        'top_w': 124,
        'down_w': 102.8,
        'perfect_w': 114.2,
    },
    170: {
        'top_w': 125,
        'down_w': 104,
        'perfect_w': 115.6,
    },
    171: {
        'top_w': 126,
        'down_w': 105.2,
        'perfect_w': 117,
    },
    172: {
        'top_w': 127,
        'down_w': 106.6,
        'perfect_w': 118.4,
    },
    173: {
        'top_w': 128,
        'down_w': 107.8,
        'perfect_w': 119.8,
    },
    174: {
        'top_w': 129,
        'down_w': 109,
        'perfect_w': 121.2,
    },
    175: {
        'top_w': 130,
        'down_w': 110.2,
        'perfect_w': 122.6,
    },

}

Body_Standards = {
    'whole': {
        # 1.2
        'delta_Tun_Jian': 2,
        'delta_Jian_Yao': 2,
        'delta_TJ_Yao': 20,
    },
    'part': {
        # 2.1
        'ratio_Jian_Tou': 1.25,
        'range_Jian_Tou_up': 0.4,
        'range_Jian_Tou_down': 0.2,
        # 2.2
        'ratio_Body_Head_top': 8.3,
        'ratio_Body_Head_middle': 7.7,
        'ratio_Body_Head_low': 6.5,
        # 2.3
        'ratio_half_top': 1.0,
        'ratio_half_middle': 0.9,
        'radio_half_down': 0.85,
        # 2.4
        'ratio_half_Leg': 0.48,
        # 2.5
        'ratio_Yao_Tun_top': 0.85,
        'ratio_Yao_Tun_s0': 0.67,
        'ratio_Yao_Tun_s1': 0.7,
        # 2.6
        'ratio_Nip_Shoulder': 0.5,

    },
    'detail': {
        # 3.1
        'girth_Neck_top': 48,
        'girth_Neck_down': 38,
        # 3.2
        'ratio_YaoW_height_top': 0.54,
        'ratio_YaoW_height_down': 0.42,
        # 3.3
        'ratio_XiongW_height_top': 0.48,
        'ratio_XiongW_height_down': 0.32,
        # 3.4
        'radio_TunW_height_top': 0.69,
        'radio_TunW_height_down': 0.59,
        'radio_TunW_height_perfect': 0.64,
        # 3.5
        'radio_ArmW_Wrist_top': 2,
        'radio_ArmW_Wrist_down': 1.4,
        'radio_ArmW_Wrist_perfect': 1.7,
        # 3.6
        'radio_ThighW_height': 0.26,
        'plus_ThighW_height_top': 8.9,
        'plus_ThighW_height_down': 6.5,
        'plus_ThighW_height_perfect': 7.8,
        # 3.7
        'radio_ShankW_height_top': 0.25,
        'radio_ShankW_height_down': 0.12,
        'radio_ShankW_height_perfect': 0.2,
        # 3.8
        'radio_AnkleW_ShankW_top': 0.7,
        'radio_AnkleW_ShankW_down': 0.5,
        'radio_AnkleW_ShankW_perfect': 0.59,

    },
}

FULL_DICT = {
    111: {
		'name': 'BMI',
        'result': '偏瘦',
        'scores': BMI_Scores['thin']
    },
    112: {
		'name': 'BMI',
        'result': '完美',
        'scores': BMI_Scores['perfect']
    },
    113: {
		'name': 'BMI',
        'result': '标准',
        'scores': BMI_Scores['normal']
    },
    114: {
		'name': 'BMI',
        'result': '偏胖',
        'scores': BMI_Scores['fat']
    },
    121: {
		'name': '身型',
        'result': '倒三角形身材',
        'scores': Body_Scores[121]
    },
    122: {
		'name': '身型',
        'result': '矩形身材',
        'scores': Body_Scores[122]
    },
    123: {
		'name': '身型',
        'result': '正三角形身材',
        'scores': Body_Scores[123]
    },
    124: {
		'name': '身型',
        'result': '椭圆形身材',
        'scores': Body_Scores[124]
    },

    211: {
			'name': '头肩比',
			'result': '完美',
          'scores': Part_Scores[211]},
    212: {'name': '头肩比',
			'result': '标准',
          'scores': Part_Scores[212]},
    213: {'name': '头肩比','result': '有待改善',
          'scores': Part_Scores[213]},

    221: {'name': '头身比',
	'result': '八头身',
          'scores': Part_Scores[221]},
    222: {'name': '头身比','result': '标准',
          'scores': Part_Scores[222]},
    223: {'name': '头身比','result': '有待改善',
          'scores': Part_Scores[223]},

    231: {'name': '腿身比', 'result': '超长腿',
          'scores': Part_Scores[231]},
    232: {'name': '腿身比','result': '长腿',
          'scores': Part_Scores[232]},
    233: {'name': '腿身比','result': '标准腿',
          'scores': Part_Scores[233]},
    234: {'name': '腿身比','result': '短腿型',
          'scores': Part_Scores[234]},

    241: {'name': '大小腿长比','result': '黄金比例',
          'scores': Part_Scores[241]},
    242: {'name': '大小腿长比','result': '正常标准',
          'scores': Part_Scores[242]},


    251: {'name': '腰臀比','result': '黄金比例',
          'scores': Part_Scores[251]},
    253: {'name': '腰臀比','result': '标准',
          'scores': Part_Scores[253]},
    252: {'name': '腰臀比','result': '肥胖',
          'scores': Part_Scores[252]},

    262: {'name': '胸型','result': '标准胸型',
          'scores': Part_Scores[262]},
    261: {'name': '胸型','result': '胸外扩',
          'scores': Part_Scores[261]},
    
    311: {'name': '颈围','result': '修长',
          'scores': Detail_Scores[311]},
    312: {'name': '颈围','result': '标准脖',
          'scores': Detail_Scores[312]},
    313: {'name': '颈围','result': '粗脖',
          'scores': Detail_Scores[313]},

    321: {'name': '腰围','result': '纤细',
          'scores': Detail_Scores[321]},
    322: {'name': '腰围','result': '标准',
          'scores': Detail_Scores[322]},
    323: {'name': '腰围','result': '肥胖',
          'scores': Detail_Scores[323]},

    331: {'name': '胸围','result': '完美',
          'scores': Detail_Scores[331]},
    332: {'name': '胸围','result': '标准',
          'scores': Detail_Scores[332]},
    333: {'name': '胸围','result': '偏小',
          'scores': Detail_Scores[333]},

    343: {'name': '臀围','result': '偏大',
          'scores': Detail_Scores[343]},
    341: {'name': '臀围','result': '完美',
          'scores': Detail_Scores[341]},
    342: {'name': '臀围','result': '标准',
          'scores': Detail_Scores[342]},
    344: {'name': '臀围','result': '偏小',
          'scores': Detail_Scores[344]},

    354: {'name': '手臂围','result': '偏细',
          'scores': Detail_Scores[354]},
    351: {'name': '手臂围','result': '完美',
          'scores': Detail_Scores[351]},
    352: {'name': '手臂围','result': '标准',
          'scores': Detail_Scores[352]},
    353: {'name': '手臂围','result': '偏粗',
          'scores': Detail_Scores[353]},


    363: {'name': '大腿围','result': '偏粗',
          'scores': Detail_Scores[363]},
    361: {'name': '大腿围','result': '完美',
          'scores': Detail_Scores[361]},
    362: {'name': '大腿围','result': '标准',
          'scores': Detail_Scores[362]},
    364: {'name': '大腿围','result': '偏细',
          'scores': Detail_Scores[364]},

    373: {'name': '小腿围','result': '偏细',
          'scores': Detail_Scores[373]},
    371: {'name': '小腿围','result': '完美',
          'scores': Detail_Scores[371]},
    372: {'name': '小腿围','result': '标准',
          'scores': Detail_Scores[372]},
    374: {'name': '小腿围','result': '偏粗',
          'scores': Detail_Scores[374]},

    384: {'name': '脚踝','result': '偏细',
          'scores': Detail_Scores[384]},
    381: {'name': '脚踝','result': '完美',
          'scores': Detail_Scores[381]},
    382: {'name': '脚踝','result': '标准',
          'scores': Detail_Scores[382]},
    383: {'name': '脚踝','result': '偏粗',
          'scores': Detail_Scores[383]},


    411: {'result': '正常', 'scores': {}},
    412: {'result': '侧歪', 'scores': {}},

    421: {'result': '正常', 'scores': {}},
    422: {'result': '前引', 'scores': {}},

    432: {'result': '左高', 'scores': {}},
    431: {'result': '正常', 'scores': {}},
    433: {'result': '右高', 'scores': {}},

    442: {'result': '左倾斜', 'scores': {}},
    441: {'result': '正常', 'scores': {}},
    443: {'result': '右倾斜', 'scores': {}},

    452: {'result': 'O型腿', 'scores': {}},
    451: {'result': '正常', 'scores': {}},
    453: {'result': 'X型腿', 'scores': {}},

    511: {'name': '体重','result': '偏瘦',
          'scores': Element_Scores[511]},
    512: {'name': '体重','result': '标准',
          'scores': Element_Scores[512]},
    513: {'name': '体重','result': '偏胖',
          'scores': Element_Scores[513]},
    514: {'name': '体重','result': '肥胖',
          'scores': Element_Scores[514]},
    521: {'name': '体脂率','result': '偏低',
          'scores': Element_Scores[521]},
    522: {'name': '体脂率','result': '标准',
          'scores': Element_Scores[522]},
    523: {'name': '体脂率', 'result': '偏高',
          'scores': Element_Scores[523]},
    524: {'name': '体脂率', 'result': '高',
          'scores': Element_Scores[524]},
    525: {'name': '体脂率', 'result': '偏低',
          'scores': Element_Scores[525]},
    526: {'name': '体脂率', 'result': '标准',
          'scores': Element_Scores[526]},
    527: {'name': '体脂率', 'result': '偏高',
          'scores': Element_Scores[527]},
    528: {'name': '体脂率', 'result': '高',
          'scores': Element_Scores[528]},

    611: {'name': '拜拜肉', 'result': '拜拜肉倾向', 'scores': Xiachui_Scores[611]},
    612: {'name': '拜拜肉', 'result': '正常', 'scores': Xiachui_Scores[612]},
    621: {'name': '游泳圈', 'result': '游泳圈倾向', 'scores': Xiachui_Scores[621]},
    622: {'name': '游泳圈', 'result': '正常', 'scores': Xiachui_Scores[622]},

}

def get_eval_collection(item_id): #item_id 
    res = []
    for _k, _v in FULL_DICT.items():
        if _k // 10 == item_id:
            res.append(_v['result'])

    return res

bmi_thin_rules = []
bmi_perfect_rules = []
bmi_normal_rules = []
bmi_fat_rules = []

for h_k, w_vals in BMI_Standards.items():
    down_w = w_vals['down_w']
    top_w = w_vals['top_w']
    perfect_w = w_vals['perfect_w']

    t_rule = (m.height == h_k) & (m.weight < down_w)
    f_rule = (m.height == h_k) & (m.weight > top_w)
    s_rule = (m.height == h_k) & (m.weight >= down_w) & (m.weight <= top_w)
    p_rule = (m.height == h_k) & (m.weight == perfect_w)

    bmi_thin_rules.append(t_rule)
    bmi_fat_rules.append(f_rule)
    bmi_normal_rules.append(s_rule)
    bmi_perfect_rules.append(p_rule)

BS_W = Body_Standards['whole']
bw_r_1 = (m.g_hip_167 > m.g_shoulder_104 + BS_W['delta_Tun_Jian'])
bw_r_2 = (m.g_shoulder_104 > m.g_waist_155 + BS_W['delta_Jian_Yao'])
bw_r_3 = (m.g_hip_167 <= m.g_shoulder_104 + BS_W['delta_Tun_Jian'])
bw_r_4 = (m.g_shoulder_104 <= m.g_waist_155 + BS_W['delta_Jian_Yao'])
bw_r_5 = (m.g_sum_167_104 <= (m.g_waist_155  + BS_W['delta_TJ_Yao']) * 2 )
bw_r_6 = (m.g_sum_167_104 >  (m.g_waist_155 + BS_W['delta_TJ_Yao']) * 2 )
#- m.g_shoulder_104
rule_123 = bw_r_1 & bw_r_2
rule_124 = bw_r_1 & bw_r_4
rule_122 = bw_r_3 & bw_r_5
rule_121 = bw_r_3 & bw_r_6

BS_P = Body_Standards['part']
r211_a = m.w_shoulder_210_211 <= m.w_head_212_213 * (BS_P['ratio_Jian_Tou'] + BS_P['range_Jian_Tou_down'])
r211_b = m.w_shoulder_210_211 >= m.w_head_212_213 * (BS_P['ratio_Jian_Tou'] - BS_P['range_Jian_Tou_down'])
rule_211 = r211_a & r211_b

r212_a = m.w_shoulder_210_211 >  m.w_head_212_213 * (BS_P['ratio_Jian_Tou'] + BS_P['range_Jian_Tou_down'])
r212_b = m.w_shoulder_210_211 <= m.w_head_212_213 * (BS_P['ratio_Jian_Tou'] + BS_P['range_Jian_Tou_up'])
rule_212 = r212_a & r212_b

r213_a = m.w_shoulder_210_211 > m.w_head_212_213 * (BS_P['ratio_Jian_Tou'] + BS_P['range_Jian_Tou_up'])
r213_b = m.w_shoulder_210_211 <  m.w_head_212_213 * (BS_P['ratio_Jian_Tou'] - BS_P['range_Jian_Tou_down'])
rule_213 = r213_a | r213_b

r221_a = m.height < m.h_head_202 * BS_P['ratio_Body_Head_top'] 
r221_b = m.height >= m.h_head_202 * BS_P['ratio_Body_Head_middle'] 
r222_a = m.height < m.h_head_202 * BS_P['ratio_Body_Head_middle']
r222_b = m.height >= m.h_head_202 *  BS_P['ratio_Body_Head_low']
r223_a = m.height < m.h_head_202 *  BS_P['ratio_Body_Head_low']
r223_b = m.height >= m.h_head_202 * BS_P['ratio_Body_Head_top'] 
rule_221 = r221_a & r221_b
rule_222 = r222_a & r222_b 
rule_223 = r223_a | r223_b


r231_a = m.h_leg_333_334 >= m.h_upper_body * BS_P['ratio_half_top']
r232_a = m.h_leg_333_334 < m.h_upper_body * BS_P['ratio_half_top']
r232_b = m.h_leg_333_334 >= m.h_upper_body * BS_P['ratio_half_middle']
r233_a = m.h_leg_333_334 < m.h_upper_body * BS_P['ratio_half_middle']
r233_b = m.h_leg_333_334 >= m.h_upper_body * BS_P['radio_half_down']
r234_a = m.h_leg_333_334 < m.h_upper_body * BS_P['radio_half_down']
rule_231 = r231_a
rule_232 = r232_a & r232_b
rule_233 = r233_a & r233_b
rule_234 = r234_a

r241_a = m.h_upper_leg < m.h_leg_333_334 * BS_P['ratio_half_Leg']
r242_a = m.h_upper_leg >= m.h_leg_333_334 * BS_P['ratio_half_Leg']
rule_241 = r241_a
rule_242 = r242_a

r251_a = m.g_waist_155 > m.g_hip_167 * BS_P['ratio_Yao_Tun_s0'] 
r251_b = m.g_waist_155 < m.g_hip_167 * BS_P['ratio_Yao_Tun_s1']
r252_a = m.g_waist_155 > m.g_hip_167 * BS_P['ratio_Yao_Tun_top']
r253_a = m.g_waist_155 <= m.g_hip_167 * BS_P['ratio_Yao_Tun_s0']
r253_b = m.g_waist_155 >= m.g_hip_167 * BS_P['ratio_Yao_Tun_s1']
r253_c = m.g_waist_155 <= m.g_hip_167 * BS_P['ratio_Yao_Tun_top']
rule_251 = r251_a & r251_b
rule_252 = r252_a
rule_253 = r253_a | r253_b & r253_c

r261_a = m.w_busts_205_206 > m.w_shoulder_210_211 * BS_P['ratio_Nip_Shoulder']
r262_a =  m.w_busts_205_206 <= m.w_shoulder_210_211 * BS_P['ratio_Nip_Shoulder']
rule_261 = r261_a
rule_262 = r262_a

BS_D = Body_Standards['detail']
rule_311 = m.g_neck_140 <  BS_D['girth_Neck_down']
r312_a = m.g_neck_140 >= BS_D['girth_Neck_down']
r312_b = m.g_neck_140 < BS_D['girth_Neck_top']
rule_312 = r312_a & r312_b
rule_313 = m.g_neck_140 > BS_D['girth_Neck_top']

rule_321 = m.g_waist_155 <= m.height * BS_D['ratio_YaoW_height_down']
r322_a = m.g_waist_155 > m.height * BS_D['ratio_YaoW_height_down']
r322_b = m.g_waist_155 <= m.height * BS_D['ratio_YaoW_height_top']
rule_322 = r322_a & r322_b
rule_323 = m.g_waist_155 > m.height * BS_D['ratio_YaoW_height_top']

rule_331 = m.g_bust_144 >= m.height * BS_D['ratio_XiongW_height_top']
r_332_a = m.g_bust_144 < m.height * BS_D['ratio_XiongW_height_top']
r_332_b = m.g_bust_144 >= m.height * BS_D['ratio_XiongW_height_down']
rule_332 = r_332_a & r_332_b
rule_333 = m.g_bust_144 < m.height * BS_D['ratio_XiongW_height_down']

rule_341 = m.g_hip_167 == m.height * BS_D['radio_TunW_height_perfect']
r342_a = m.g_hip_167 >= m.height * BS_D['radio_TunW_height_down']
r342_b = m.g_hip_167 <= m.height * BS_D['radio_TunW_height_top']
r342_c = m.g_hip_167 != m.height * BS_D['radio_TunW_height_perfect']
rule_342 = r342_a & r342_b & r342_c
rule_343 = m.g_hip_167 > m.height * BS_D['radio_TunW_height_top']
rule_344 = m.g_hip_167 < m.height * BS_D['radio_TunW_height_down']

r351_a = m.g_lbiceps_125 == m.g_lwrist_123 * BS_D['radio_ArmW_Wrist_perfect']
r351_b = m.g_rbiceps_126 == m.g_rwrist_121 * BS_D['radio_ArmW_Wrist_perfect']
rule_351 = r351_a & r351_b
r352_a = m.g_lbiceps_125 >= m.g_lwrist_123 * BS_D['radio_ArmW_Wrist_down']
r352_b = m.g_rbiceps_126 >= m.g_rwrist_121 * BS_D['radio_ArmW_Wrist_down']
r352_c = m.g_lbiceps_125 <= m.g_lwrist_123 * BS_D['radio_ArmW_Wrist_top']
r352_d = m.g_rbiceps_126 <= m.g_rwrist_121 * BS_D['radio_ArmW_Wrist_top']
rule_352 = r352_a & r352_c | r352_b & r352_d
r353_a = m.g_lbiceps_125 > m.g_lwrist_123 * BS_D['radio_ArmW_Wrist_top']
r353_b = m.g_rbiceps_126 > m.g_rwrist_121 * BS_D['radio_ArmW_Wrist_top']
rule_353 = r353_a | r353_b
r354_a = m.g_lbiceps_125 < m.g_lwrist_123 * BS_D['radio_ArmW_Wrist_down']
r354_b = m.g_rbiceps_126 < m.g_rwrist_121 * BS_D['radio_ArmW_Wrist_down']
rule_354 = r354_a | r354_b

r361_a = m.g_lmthigh_111 == m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_perfect']
r361_b = m.g_rmthigh_112 == m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_perfect']
rule_361 = r361_a & r361_b
r362_a = m.g_lmthigh_111 >= m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_down']
r362_b = m.g_rmthigh_112 >= m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_down']
r362_c = m.g_lmthigh_111 <= m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_top']
r362_d = m.g_rmthigh_112 <= m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_top']
rule_362 = r362_a & r362_c | r362_b & r362_d
r363_a = m.g_lmthigh_111 > m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_top']
r363_b = m.g_rmthigh_112 > m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_top']
rule_363 = r363_a | r363_b
r364_a = m.g_lmthigh_111 < m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_down']
r364_b = m.g_rmthigh_112 < m.height * BS_D['radio_ThighW_height'] + BS_D['plus_ThighW_height_down']
rule_364 = r364_a | r364_b

r371_a = m.g_lmcalf_115 == m.height * BS_D['radio_ShankW_height_perfect']
r371_b = m.g_rmcalf_116 == m.height * BS_D['radio_ShankW_height_perfect']
rule_371 = r371_a & r371_b
r372_a = m.g_lmcalf_115 >= m.height * BS_D['radio_ShankW_height_down']
r372_b = m.g_rmcalf_116 >= m.height * BS_D['radio_ShankW_height_down']
r372_c = m.g_lmcalf_115 <= m.height * BS_D['radio_ShankW_height_top']
r372_d = m.g_rmcalf_116 <= m.height * BS_D['radio_ShankW_height_top']
rule_372 = r372_a & r372_c | r372_b & r372_d
r373_a = m.g_lmcalf_115 > m.height * BS_D['radio_ShankW_height_top'] 
r373_b = m.g_rmcalf_116 > m.height * BS_D['radio_ShankW_height_top']
rule_373 = r373_a | r373_b
r374_a = m.g_lmcalf_115 < m.height * BS_D['radio_ShankW_height_down']
r374_b = m.g_rmcalf_116 < m.height * BS_D['radio_ShankW_height_down']
rule_374 = r374_a | r374_b

r381_a = m.g_lankle_117 == m.height * BS_D['radio_AnkleW_ShankW_perfect']
r381_b = m.g_rankle_118 == m.height * BS_D['radio_AnkleW_ShankW_perfect']
rule_381 = r381_a & r381_b
r382_a = m.g_lankle_117 >= m.height * BS_D['radio_AnkleW_ShankW_down']
r382_b = m.g_rankle_118 >= m.height * BS_D['radio_AnkleW_ShankW_down']
r382_c = m.g_lankle_117 <= m.height * BS_D['radio_AnkleW_ShankW_top']
r382_d = m.g_rankle_118 <= m.height * BS_D['radio_AnkleW_ShankW_top']
rule_382 = r382_a & r382_c | r382_b & r382_d
r383_a = m.g_lankle_117 > m.height * BS_D['radio_AnkleW_ShankW_top'] 
r383_b = m.g_rankle_118 > m.height * BS_D['radio_AnkleW_ShankW_top']
rule_383 = r383_a | r383_b
r384_a = m.g_lankle_117 < m.height * BS_D['radio_AnkleW_ShankW_down']
r384_b = m.g_rankle_118 < m.height * BS_D['radio_AnkleW_ShankW_down']
rule_384 = r384_a | r384_b

r511 = m.weight < m.height2 * 0.37
rule_511 = r511
r512_a = m.weight > m.height2 * 0.37
r512_b =  m.weight <= m.height2 * 0.50
rule_512 = r512_a & r512_b
r513_a = m.weight > m.height2  * 0.50
r513_b =  m.weight <= m.height2 * 0.60
rule_513 = r513_a & r513_b
r514 = m.weight > m.height2 * 0.60
rule_514 = r514

r611_a = m.g_lbiceps_125 > m.height * 0.6 +6 
r611_b = m.g_lbiceps_125 > m.g_lmthigh_111 * 0.5
rule_611 = r611_a & r611_b

r612_a = m.g_lbiceps_125 <= m.height * 0.6 +6 
r612_b = m.g_lbiceps_125 <= m.g_lmthigh_111 * 0.5
rule_612 = r612_a | r612_b

# r621 = m.g_upper_chest_143 < m.g_bust_144 * 0.333
# rule_621 = r621
# r622 = m.g_upper_chest_143 >= m.g_bust_144 * 0.333
# rule_622 = r622

r621 = m.g_abdomen_161 > m.g_waist_163 + 5
rule_621 = r621
r622 = m.g_abdomen_161 <= m.g_waist_163 + 5
rule_622 = r622


def get2bmi_rules(bmi_rules):
    _half0 = None
    _half1 = None
    for r in bmi_rules[:13]:
        _half0 = r if not _half0 else (_half0 | r)

    for r in bmi_rules[13:]:
        _half1 = r if not _half1 else (_half1 | r)

    return _half0, _half1


trule_half0, trule_half1 = get2bmi_rules(bmi_thin_rules)
frule_half0, frule_half1 = get2bmi_rules(bmi_fat_rules)
srule_half0, srule_half1 = get2bmi_rules(bmi_normal_rules)
prule_half0, prule_half1 = get2bmi_rules(bmi_perfect_rules)

# global rule_result

def reset_rule_results():
    execute.results = {}

def current_result():
    sum_scores = -1
    sum_descs = []
    sum_suggs = []
    # print(execute.results)
    for _kk, _cls_res in execute.results.items():
        if _kk == "Summary":
            continue
        for _, _res in _cls_res.items():
        # for _res in _cls_res:
            sum_scores += _res['scores']['score']
            sum_descs.append(_res['scores']['desc'])
            if _res['scores'].get('suggest', None):
                sum_suggs.append(_res['scores']['suggest'])
    if execute.results.get('Overall', None) is None:
        execute.results['Overall'] = {}
    overall_res = execute.results['Overall']
    overall_res['total_scores'] = sum_scores
    # overall_res['total_desc'] = " ".join(sum_descs)
    # overall_res['total_suggest'] = " ".join(sum_suggs)
    return execute.results

def execute(facts, rule_str=None):
    # global rule_result
    if rule_str:
        assert_fact(rule_str, facts)
    else:
        post('figure-bmi', facts)
        post('figure-body',facts)

        for i in range(6):
            post(f'figure-part-2{i+1}', facts)

        for i in range(7):
            post(f"figure-detail-3{i+1}", facts)
        
        for i in range(1):
            post(f"body-element-5{i+1}", facts)
        
        for i in range(2):
            post(f"body-xiachui-6{i+1}", facts)
            

    print(f"result is {execute.results}")
    # print(get_facts(rule_str))
    return execute.results

ms_key_dict = {
    11: "BMI",
    12: "Body",
    21: "TouJianBi",
    22: "TouShenBi",
    23: "TuiShenBi",
    24: "DaXiaoTuiBi",
    25: "YaoTunBi",
    26: "XiongXing",
    31: "JingWei",
    32: "YaoWei",
    33: "XiongWei",
    34: "TunWei",
    35: "ShouBiWei",
    36: "DaTuiWei",
    37: "XiaoTuiWei",
    38: "JiaoHuai",
    41: "TouCeWai",
    42: "TouQianYin",
    43: "GaoDiJian",
    44: "ShenTiQingXie",
    45: "YiXingTui",
    51: "TiZhong",
    52: "TiZhiLv",
    53: "ZhiFangLiang",
    54: "QuZhiTiZhong",
    55: "JiRouLv",
    56: "JiRouLiang",
    57: "ShuiFen",
    58: "GuZhong",
    59: "JiChuDaiXieLv",
    510: "DanBaiLv",
    511: "DanBaiLiang",
    512: "NeiZangZhiFangZhiShu",
    513: "PiXiaZhiFang",
    514: "FeiPangDengJi",
    515: "BiaoZhunTiZhong",
    516: "TiZhongKongZhiLiang",
    61: "拜拜肉倾向",
    62: "游泳圈倾向",
    # 63: "游泳圈倾向",
}

classify_dict = {
    'ChengFen': [51, 53],
    'FeiPang' : [11, 52, 25],
    'WeiDu': [31, 32, 33, 34, 35, 36, 37, ],
    'BiLi' : [21, 22, 23, 24, 25, 26],
    'YiTai': [42, 41, 43, 44, 45],
    'XiaChui': [61, 62,],
    'Overall': [12]
}

Summary_dict = {
    "Head": [22, 31, 41, 42],
    "Shoulder": [21, 43],
    "Chest": [26, 33],
    "YaoTun": [25, 32, 34],
    "Leg": [23, 24, 36, 37, 45],
    "XiaChui": [61, 62,],
    "Other": [44, 35]
}


execute.results = {

}

def find_classify_key(item_id):
    res = []
    types = []
    for _k, _v in classify_dict.items():
        if item_id in _v:
            types.append(_v.index(item_id) + 1)
            res.append(_k)
    
    return res, types

def find_summary_key(item_id):
    # res = []
    for _k, _v in Summary_dict.items():
        if item_id in _v:
            return _k
    return None
    # return res

def safe_div(x, y):
    x = float(x)
    y = float(y)
    return x / y if y != 0. else 0.

def eval_g_delta(item_iid, d):
    item_id = item_iid // 10 
    if not 70 > item_id > 10:
        return None

    if item_iid == 211:
        return '非常完美'
    if item_iid == 212:
        return '很标准，请继续保持'
    if item_iid == 213:
        return '美体头肩比1:2.5 有待改善'

    if item_iid == 221:
        return '非常完美'
    if item_iid == 222:
        return '很标准，请继续保持'
    if item_iid == 223:
        return '美体头身比1:8 有待改善'

    if item_iid in (231, 232):
        return '非常完美'
    if item_iid == 233:
        return '很标准，请继续保持'
    if item_iid == 234:
        return '比例失衡，有待改善'

    if item_iid == 241:
        return '非常完美'
    if item_iid == 242:
        return '很标准，请继续保持'

    if item_iid == 251:
        return '非常完美'
    if item_iid == 252:
        return '美体腰臀比0.7，有待改善'
    if item_iid == 253:
        return '很标准，请继续保持'
    
    if item_iid == 261:
        return '胸外扩，有待改善'
    if item_iid == 262:
        return '健康状态，请继续保持哦'

    if item_iid == 311:
        return '非常完美'
    if item_iid == 312:
        return '很标准，请继续保持'
    if item_iid == 313:
        delta_val = round(abs(d.g_neck_140 -35), 0)
        return f'美体围脖35cm  超出{delta_val}cm'
    if item_iid == 321:
        return '非常完美'
    if item_iid == 322:
        return '很标准，请继续保持'
    if item_iid == 323:
        std_val = round(d.height * 0.37, 0)
        delta_val = round(abs(std_val - d.g_waist_155), 0)
        return f'美体腰围{std_val}cm  超出{delta_val}cm'
    if item_iid == 331:
        return '非常完美'
    if item_iid == 332:
        return '很标准，请继续保持'
    if item_iid == 333: 
        std_val = round(d.height * 0.53, 0)
        delta_val = round(abs(std_val - d.g_bust_144), 0)
        return f'美体胸围{std_val}cm  超出{delta_val}cm'
    if item_iid == 341: 
        return '非常完美'
    if item_iid == 342: 
        return '很标准，请继续保持'
    if item_iid in (343, 344): 
        std_val = round(d.height * 0.54, 0)
        delta_val = round(abs(std_val - d.g_hip_167), 0)
        return f'美体臀围{std_val}cm  超出{delta_val}cm'

    if item_iid == 351: 
        return  '非常完美'
    if item_iid == 352: 
        return '很标准，请继续保持'
    if item_iid in (353, 354): 
        std_val = round((d.g_lwrist_123 + d.g_rwrist_121) * 1.7 / 2, 0)
        my_value = (d.g_lbiceps_125 + d.g_rbiceps_126)/2
        delta_val = round(abs(std_val - my_value), 0)
        return f'美体臂围{std_val}cm  超出{delta_val}cm'

    if item_iid == 361: 
        return  '非常完美'
    if item_iid == 362: 
        return '很标准，请继续保持'
    if item_iid in (363, 364): 
        std_val = round((d.height * 0.26 + 7.8), 0)
        my_value = (d.g_lmthigh_111 + d.g_rmthigh_112)/2
        delta_val = round(abs(std_val - my_value), 0)
        return f'美体大腿围{std_val}cm  超出{delta_val}cm'

    if item_iid == 371: 
        return  '非常完美'
    if item_iid == 372: 
        return '很标准，请继续保持'
    if item_iid in (373, 374): 
        std_val = round(d.height * 0.18, 0)
        my_value = (d.g_lmcalf_115 + d.g_rmcalf_116)/2
        delta_val = round(abs(std_val - my_value), 0)
        return f'美体小腿围{std_val}cm  超出{delta_val}cm'

    if item_iid == 611: 
        return  '具有拜拜肉倾向'
    if item_iid == 612: 
        return '健康状态，请继续保持哦'

    if item_iid == 621:
        return  '具有游泳圈倾向'
    if item_iid == 622: 
        return '健康状态，请继续保持哦'

    return ""

def eval_val(item_id, d):
    if item_id == 11:
        return round(safe_div((d.weight * 100 * 100), (d.height * d.height)), 2)
    if item_id == 21:
        return round(safe_div(d.w_head_212_213, d.w_shoulder_210_211 ), 2)
    if item_id == 22:
        return round(safe_div(d.h_head_202, d.height), 2)
    if item_id == 23:
        return round(safe_div(d.h_leg_333_334, d.height), 2)
    if item_id == 24:
        return round(safe_div(d.h_upper_leg, d.h_leg_333_334), 2)
    if item_id == 25:
        return round(safe_div(d.g_waist_155, d.g_hip_167), 2)
    if item_id == 26:
        return round(safe_div(d.w_busts_205_206 * 2, d.w_shoulder_210_211), 2)
    
    if item_id == 31:
        return round(d.g_neck_140, 1)
    if item_id == 32:
        return round(d.g_waist_155, 1)
    if item_id == 33:
        return round(d.g_bust_144 -5, 1)
    if item_id == 34:
        return round(d.g_hip_167, 1)
    if item_id == 35:
        return round((d.g_lbiceps_125 + d.g_rbiceps_126)/2, 1)
    if item_id == 36:
        return round((d.g_lmthigh_111 + d.g_rmthigh_112)/2, 1)
    if item_id == 37:
        return round((d.g_lmcalf_115 + d.g_rmcalf_116)/2, 1)
    if item_id == 38:
        return round((d.g_lankle_117 + d.g_rankle_118)/2, 1)

    if item_id == 61:
        return round(0)
    if item_id == 62:
        return round(0)
    # if item_id == 63:
    #     return round(0)

    return None

GOOD_RESULTS = ('标准', '完美', '八头身', '超长腿', '长腿', '标准腿', '黄金比例', '正常标准', '标准胸型', '修长', '标准脖', '纤细', '正常',)

def rule_result(item_iid, data):
    print(item_iid)
    item_id = item_iid // 10
    value = eval_val(item_id, data)
    tag_str = eval_g_delta(item_iid, data)
    print(item_id)
    cls_keys, cls_types = find_classify_key(item_id)
    print(f"cls keys is:{cls_keys}")
    sm_key = "Summary"
    if execute.results.get(sm_key, None) is None:
        execute.results[sm_key] = {}
    
    sm_dict =  execute.results[sm_key]
  
    in_sm = False
    for cls_key, cls_type in zip(cls_keys, cls_types):
        if execute.results.get(cls_key, None) is None:
            execute.results[cls_key] = {}
        cls_res = execute.results[cls_key]
        py_key = ms_key_dict.get(item_id, "UNKNOWN")
        cls_res[py_key] = FULL_DICT[item_iid]
        # py_res = FULL_DICT[item_iid]
        if value is not None:
            cls_res[py_key]['value'] = value
            # py_res['value'] = value
        if tag_str is not None:
            cls_res[py_key]['tag_str'] = tag_str
        cls_res[py_key]['type'] = cls_type
        cls_res[py_key]['result_collection']  = get_eval_collection(item_id)
        # py_res['result_collection']  = get_eval_collection(item_id)
        # cls_res.append(py_res)

        if not in_sm and 50 > item_id > 20 and FULL_DICT[item_iid]['result'] not in GOOD_RESULTS:
            print("find item_id")
            _sk = find_summary_key(item_id)
            if _sk is not None:
                if sm_dict.get(_sk, None) is None:
                    sm_dict[_sk] = []
                sm_dict[_sk].append(cls_res[py_key].copy())
                in_sm = True
    print(execute.results.keys())
    
def register_rules():

    with ruleset('body-xiachui-61'):
        @when_all(rule_611)
        def r_6(c):
            rule_result(611, c.m)
        
        @when_all(rule_612)
        def r_6(c):
            rule_result(612, c.m)

    with ruleset('body-xiachui-62'):
        @when_all(rule_621)
        def r_6(c):
            rule_result(621, c.m)
        
        @when_all(rule_622)
        def r_6(c):
            rule_result(622, c.m)

    # with ruleset('body-xiachui-63'):
    #     @when_all(rule_631)
    #     def r_6(c):
    #         rule_result(631, c.m)
        
    #     @when_all(rule_632)
    #     def r_6(c):
    #         rule_result(632, c.m)

    with ruleset('body-element-51'):
        @when_all(rule_511)
        def r_5(c):
            rule_result(511, c.m)
        
        @when_all(rule_512)
        def r_5(c):
            rule_result(512, c.m)
        
        @when_all(rule_513)
        def r_5(c):
            rule_result(513, c.m)
        
        @when_all(rule_514)
        def r_5(c):
            rule_result(514, c.m)

    with ruleset('figure-detail-31'):
        @when_all(rule_311)
        def r_3(c):
            rule_result(311, c.m)
            # execute.results['颈围31'] = FULL_DICT[311]

        @when_all(rule_312)
        def r_3(c):
            rule_result(312, c.m)
            # execute.results['颈围31'] = FULL_DICT[312]

        @when_all(rule_313)
        def r_3(c):
            rule_result(313, c.m)
            # execute.results['颈围31'] = FULL_DICT[313]

    with ruleset('figure-detail-32'):
        @when_all(rule_321)
        def r_3(c):
            rule_result(321, c.m)
            # execute.results['腰围32'] = FULL_DICT[321]

        @when_all(rule_322)
        def r_3(c):
            rule_result(322, c.m)
            # execute.results['腰围32'] = FULL_DICT[322]

        @when_all(rule_323)
        def r_3(c):
            rule_result(323, c.m)
            # execute.results['腰围32'] = FULL_DICT[323]

    with ruleset('figure-detail-33'):
        @when_all(rule_331)
        def r_3(c):
            rule_result(331, c.m)
            # execute.results['胸围33'] = FULL_DICT[331]

        @when_all(rule_332)
        def r_3(c):
            rule_result(332, c.m)
            # execute.results['胸围33'] = FULL_DICT[332]

        @when_all(rule_333)
        def r_3(c):
            rule_result(333, c.m)
            # execute.results['胸围33'] = FULL_DICT[333]

    with ruleset('figure-detail-34'):
        @when_all(rule_341)
        def r_3(c):
            rule_result(341, c.m)
            # execute.results['臀围34'] = FULL_DICT[341]

        @when_all(rule_342)
        def r_3(c):
            rule_result(342, c.m)
            # execute.results['臀围34'] = FULL_DICT[342]

        @when_all(rule_343)
        def r_3(c):
            rule_result(343, c.m)
            # execute.results['臀围34'] = FULL_DICT[343]

        @when_all(rule_344)
        def r_3(c):
            rule_result(344, c.m)
            # execute.results['臀围34'] = FULL_DICT[344]

    with ruleset('figure-detail-35'):
        @when_all(rule_351)
        def r_3(c):
            rule_result(351, c.m)
            # execute.results['手臂围35'] = FULL_DICT[351]

        @when_all(rule_352)
        def r_3(c):
            rule_result(352, c.m)
            # execute.results['手臂围35'] = FULL_DICT[352]

        @when_all(rule_353)
        def r_3(c):
            rule_result(353, c.m)
            # execute.results['手臂围35'] = FULL_DICT[353]

        @when_all(rule_354)
        def r_3(c):
            rule_result(354, c.m)
            # execute.results['手臂围35'] = FULL_DICT[354]

    with ruleset('figure-detail-36'):
        @when_all(rule_361)
        def r_3(c):
            rule_result(361, c.m)
            # execute.results['大腿围36'] = FULL_DICT[361]

        @when_all(rule_362)
        def r_3(c):
            rule_result(362, c.m)
            # execute.results['大腿围36'] = FULL_DICT[362]

        @when_all(rule_363)
        def r_3(c):
            rule_result(363, c.m)
            # execute.results['大腿围36'] = FULL_DICT[363]

        @when_all(rule_364)
        def r_3(c):
            rule_result(364, c.m)
            # execute.results['大腿围36'] = FULL_DICT[364]

    with ruleset('figure-detail-37'):
        @when_all(rule_371)
        def r_3(c):
            rule_result(371, c.m)
            # execute.results['小腿围37'] = FULL_DICT[371]

        @when_all(rule_372)
        def r_3(c):
            rule_result(372, c.m)
            # execute.results['小腿围37'] = FULL_DICT[372]

        @when_all(rule_373)
        def r_3(c):
            rule_result(373, c.m)
            # execute.results['小腿围37'] = FULL_DICT[373]

        @when_all(rule_374)
        def r_3(c):
            rule_result(374, c.m)
            # execute.results['小腿围37'] = FULL_DICT[374]

    # with ruleset('figure-detail-38'):
    #     @when_all(rule_381)
    #     def r_3(c):
    #         rule_result(381, c.m)
    #         # execute.results['脚踝38'] = FULL_DICT[381]

    #     @when_all(rule_382)
    #     def r_3(c):
    #         rule_result(382, c.m)
    #         # execute.results['脚踝38'] = FULL_DICT[382]

    #     @when_all(rule_383)
    #     def r_3(c):
    #         rule_result(383, c.m)
    #         # execute.results['脚踝38'] = FULL_DICT[383]

    #     @when_all(rule_384)
    #     def r_3(c):
    #         rule_result(384, c.m)
    #         # execute.results['脚踝38'] = FULL_DICT[384]

    with ruleset('figure-part-21'):
        # part of body
        @when_all(rule_211)
        def r_211(c):
            rule_result(211, c.m)
            # execute.results['头肩比21'] = FULL_DICT[211]

        @when_all(rule_212)
        def r_212(c):
            rule_result(212, c.m)
            # execute.results['头肩比21'] = FULL_DICT[212]

        @when_all(rule_213)
        def r_213(c):
            rule_result(213, c.m)
            # execute.results['头肩比21'] = FULL_DICT[213]

    with ruleset('figure-part-22'):
        @when_all(rule_221)
        def r_221(c):
            rule_result(221, c.m)
            # execute.results['头身比22'] = FULL_DICT[221]

        @when_all(rule_222)
        def r_222(c):
            rule_result(222, c.m)
            # execute.results['头身比22'] = FULL_DICT[222]

        @when_all(rule_223)
        def r_223(c):
            rule_result(223, c.m)
            # execute.results['头身比22'] = FULL_DICT[223]

    with ruleset('figure-part-23'):
        @when_all(rule_231)
        def r_231(c):
            rule_result(231, c.m)
            # execute.results['腿身比23'] = FULL_DICT[231]
        
        @when_all(rule_232)
        def r_232(c):
            rule_result(232, c.m)
            # execute.results['腿身比23'] = FULL_DICT[232]

        @when_all(rule_233)
        def r_233(c):
            rule_result(233, c.m)
            # execute.results['腿身比23'] = FULL_DICT[233]

        @when_all(rule_234)
        def r_234(c):
            rule_result(234, c.m)
            # execute.results['腿身比23'] = FULL_DICT[234]

    with ruleset('figure-part-24'):
        @when_all(rule_241)
        def r_241(c):
            rule_result(241, c.m)
            # execute.results['大小腿长比24'] = FULL_DICT[241]

        @when_all(rule_242)
        def r_242(c):
            rule_result(242, c.m)
            # execute.results['大小腿长比24'] = FULL_DICT[242]

    with ruleset('figure-part-25'):
        @when_all(rule_251)
        def r_251(c):
            rule_result(251, c.m)
            # execute.results['腰臀比25'] = FULL_DICT[251]

        @when_all(rule_252)
        def r_252(c):
            rule_result(252, c.m)
            # execute.results['腰臀比25'] = FULL_DICT[252]

        @when_all(rule_253)
        def r_253(c):
            rule_result(253, c.m)
            # execute.results['腰臀比25'] = FULL_DICT[253]

    with ruleset('figure-part-26'):
        @when_all(rule_261)
        def r_261(c):
            rule_result(261, c.m)
            # execute.results['胸型26'] = FULL_DICT[261]

        @when_all(rule_262)
        def r_262(c):
            rule_result(262, c.m)
            # execute.results['胸型26'] = FULL_DICT[262]

    with ruleset('figure-body'):
        # whole body
        @when_all(rule_121)
        def r_121(c):
            rule_result(121, c.m)
            # execute.results['身型12'] = FULL_DICT[121]
        
        @when_all(rule_122)
        def r_122(c):
            rule_result(122, c.m)
            # execute.results['身型12'] = FULL_DICT[122]

        @when_all(rule_123)
        def r_123(c):
            rule_result(123, c.m)
            # execute.results['身型12'] = FULL_DICT[123]

        @when_all(rule_124)
        def r_124(c):
            rule_result(124, c.m)
            # execute.results['身型12'] = FULL_DICT[124]

    with ruleset('figure-bmi'):
        # thin bmi
        @when_all(trule_half0)
        def thin(c):
            rule_result(111, c.m)
            # execute.results['BMI11'] = FULL_DICT[111]

        @when_all(trule_half1)
        def thin_a(c):
            rule_result(111, c.m)
            # execute.results['BMI11'] = FULL_DICT[111]
        # fat bmi

        @when_all(frule_half0)
        def fat(c):
            rule_result(114, c.m)
            # execute.results['BMI11'] = FULL_DICT[114]

        @when_all(frule_half1)
        def fat_a(c):
            rule_result(114, c.m)
            # execute.results['BMI11'] = FULL_DICT[114]
        # standard bmi

        @when_all(srule_half0)
        def normal(c):
            rule_result(113, c.m)
            # execute.results['BMI11'] = FULL_DICT[113]

        @when_all(srule_half1)
        def normal_a(c):
            rule_result(113, c.m)
            # execute.results['BMI11'] = FULL_DICT[113]
        # perfect bmi

        @when_all(prule_half0)
        def perfect(c):
            rule_result(112, c.m)
            # execute.results['BMI11'] = FULL_DICT[112]

        @when_all(prule_half1)
        def perfect_a(c):
            rule_result(112, c.m)
            # execute.results['BMI11'] = FULL_DICT[112]

register_rules()

if __name__ == '__main__':
    print(get_eval_collection(37))
    print(get_eval_collection(61))
    cls_keys, cls_types = find_classify_key(37)
    print(cls_keys, cls_types)
    item_iid = 372
    item_id = item_iid // 10
    # value = eval_val(item_id, data)
    # tag_str = eval_g_delta(item_iid, data)
    cls_keys, cls_types = find_classify_key(item_id)
    print(f"cls keys is:{cls_keys}")