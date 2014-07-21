# -*- coding: utf-8 -*-

import xmlrpc.client
from 臺灣言語工具.翻譯.摩西工具.語句編碼器 import 語句編碼器

class 摩西用戶端():
	網址格式 = "http://{0}:{1}/{2}"
	未知詞記號 = '|UNK|UNK|UNK'
	def __init__(self, 位址, 埠, 路徑='RPC2'):
		網址 = self.網址格式.format(位址, 埠, 路徑)
		self.主機 = xmlrpc.client.ServerProxy(網址)
	def 翻譯(self, 語句, 編碼器=None, 另外參數={}):
		if 編碼器 == None:
			來源 = 語句
		else:
			來源 = 編碼器.編碼(語句)
		參數 = {"text":來源, "align":"true", "report-all-factors":"true",
			'nbest':0}
		參數.update(另外參數)
# 218     si = params.find("sg");
# 220     si = params.find("topt");
# 224     si = params.find("nbest");
# 226     si = params.find("nbest-distinct")
		weights = None
		model_name = None
		if weights:
			if not model_name:
				raise RuntimeError("Error: if you define weights, you need to specify the feature to which the weights are to be applied (e.g. PhraseDictionaryMultiModel0)\n")
			參數['model_name'] = model_name
			參數['lambda'] = weights
		結果 = self.主機.translate(參數)
		if 編碼器 != None:
			結果['text'] = 編碼器.解碼(結果['text'])
			if 'nbest' in 結果:
				for 候選 in 結果['nbest']:
					候選['hyp'] = 編碼器.解碼(候選['hyp'])
		return 結果
	def 更新(self, 來源, 目標, 對齊, 編碼器=None):
		if 編碼器 != None:
			來源 = 編碼器.編碼(來源)
			目標 = 編碼器.編碼(目標)
		
		參數 = {"source":來源, "target":目標, "alignment":對齊}
		print("Updating with %s ..." % 參數)
		
		result = self.主機.updater(參數)
		print(result)

	def 最佳化(self, phrase_pairs, model_name):
		'''
		optimize
			phrase_pairs=[(1,2),(1,2)]
		'''
		params = {}
		params['phrase_pairs'] = phrase_pairs
		params['model_name'] = model_name
		weights = self.主機.optimize(params)
		print('weight vector (set lambda in moses.ini to this value to set as default): ')
		print(','.join(map(str, weights)) + '\n')
		return weights
	def 是未知詞(self, 詞):
		return 詞.endswith(self.未知詞記號)
	def 提掉後壁未知詞記號(self, 詞):
		return 詞[:-len(self.未知詞記號)]

if __name__ == '__main__':
	編碼器 = 語句編碼器()
	用戶端 = 摩西用戶端('localhost', '8301')
	語句 = '台-灣-人｜tai5-uan5-lang5 反-抗｜huan2-khong3 的｜e5 力-量｜lik8-liong7 迫｜pik4 中-華-民-國｜tiong1-hua5-bin5-kok4 佇｜ti7 1996｜1996 年｜ni5 開-放｜khai1-hong3 總-統｜tsong2-thong2 民-選｜bin5-suan2 ，｜, 佇｜ti7 選-舉｜suan2-ki2 期-間｜ki5-kan1 ，｜, 中-國｜tiong1-kok4 為-欲｜ui7-beh4 阻-擋｜tsoo2-tong3 台-灣｜tai5-uan5 行｜hang5 向｜hiang3 獨-立｜tok8-lip8 自｜tsu7 主-的｜tsu2-e5 趨-勢｜tshu1-se3 ，｜, 以｜i2 台-灣｜tai5-uan5 做｜tso3 目-標｜bok8-phiau1 進-行｜tsin3-hing5 飛-彈｜hui1-tuann5 試-射｜tshi3-sia7 演-習｜ian2-sip8 ，｜, 台-灣-島｜tai5-uan5-to2 內-的｜lai7-e5 China｜China 統-治｜thong2-ti7 集-團｜tsip8-thuan5 嘛｜ma7 全-力｜tsuan5-lik8 壓-制｜ap4-tse3 社-會｜sia7-hue7 力-的｜lat8-e5 覺-醒｜kak4-tshenn2 ，｜, 台-灣｜tai5-uan5 社｜sia7 會-有｜hue7-iu2 嚴-重-的｜giam5-tiong7-e5 信-心｜sin3-sim1 危-機｜gui5-ki1 ，｜, 充-滿｜tshiong1-mua2 不-安｜put4-an1 佮｜kap4 投-降-的｜tau5-hang5-e5 氣-氛｜khi3-hun1 。｜. 3｜3 月-初｜gueh8-tshue1 9｜9 ，｜, 促-進-會｜tshiok4-tsin3-hue7 成-員｜sing5-uan5 佇｜ti7 台-北｜tai5-pak4 二-二-八｜ji7-ji7-pat4 公-園｜kong1-hng5 襄｜siang1 陽｜iong5 路｜loo7 大-門-口｜tua7-mng5-khau2 靜-坐｜tsing7-tso7 ，｜, 呼-籲｜hoo1-iok8 社-會｜sia7-hue7 毋｜m7 通-驚｜thang1-kiann1 中-國-的｜tiong1-kok4-e5 威-脅｜ui1-hiap8 ，｜, 愛｜ai3 共｜ka7 台-灣-人-的｜tai5-uan5-lang5-e5 主-體｜tsu2-the2 立-場｜lip8-tiunn5 守｜tsiu2 予｜hoo7 牢｜tiau5 ；｜; 靜-坐｜tsing7-tso7 期-間｜ki5-kan1 有｜u7 遊｜iu5 行-去｜kiann5-khi3 教-育-部｜kau3-iok8-poo7 抗-議｜khong3-gi7 ，｜, 閣｜koh4 燒｜sio1 充-滿｜tshiong1-mua2 中-國｜tiong1-kok4 意｜i3 識-的｜sik4-e5 教-科-書｜kau3-kho1-su1 ，｜, 要｜iau3 求-愛｜kiu5-ai3 隨｜sui5 停-止｜thing5-tsi2 用｜ing7 中-國｜tiong1-kok4 意-識｜i3-sik4 來｜lai5 共｜ka7 台-灣｜tai5-uan5 囡-仔｜gin2-a2 洗-腦｜se2-nau2 。｜. 這-擺｜tsit4-pai2 靜-坐｜tsing7-tso7 行-動｜hing5-tong7 維-持｜i5-tshi5 17｜17 工｜kong1 、｜, 一｜it4 直-到｜tit8-kau3 3｜3 月｜gueh8 25｜25 才｜tsiah4 結-束｜kiat4-sok4 。｜. 發-起｜huat4-khi2 靜｜tsing7 坐-的｜tse7-e5 有｜u7 台-大｜tai5-tai7 ，｜, 政-大｜tsing3-tai7 ，｜, 淡｜tam7 江｜kang1 ，｜, 東-吳｜tong1-ngoo5 ，｜, 師-大｜su1-tai7 ，｜, 成-大｜sing5-tua7 ，｜, 清｜tshing1 大｜tua7 ，｜, 交｜kau1 大｜tua7 等｜ting2 各｜kok4 學-校-的｜hak8-hau7-e5 台-語-文｜tai5-gi2-bun5 社｜sia7 佮｜kap4 台-灣-文-化｜tai5-uan5-bun5-hua3 研-究｜gian2-kiu3 社｜sia7 成-員｜sing5-uan5 。｜. 對｜tui3 這-擺｜tsit4-pai2 靜-坐｜tsing7-tso7 活-動｜huat8-tong7 ，｜, 「｜“ 創｜tshong3 國｜kok4 基-金-會｜ki1-kim1-hue7 」｜” 提-供｜the5-kiong1 真-大-的｜tsin1-tua7-e5 支-援｜tsi1-uan7 。｜. 創｜tshong3 國｜kok4 基-金-會｜ki1-kim1-hue7 是｜si7 過-去｜kue3-khi3 流-亡｜liu5-bong5 日-本｜jit8-pun2 的｜e5 烏-名-單｜oo1-mia5-tuann1' 
	語句 ='郭｜kueh4 榮｜ing5 桔｜kiat4 創｜tshong3 辦-的｜pan7-e5 ，｜, 辦-公-室｜pan7-kong1-sik4 道｜to7 佇｜ti7 台-北-市｜tai5-pak4-tshi7 襄｜siang1 陽｜iong5 路｜loo7 二-二-八｜ji7-ji7-pat4 公-園｜kong1-hng5 對-面｜tui3-bin7 ，｜, 彼-冬-陣｜hit4-tang1-tsun7 促-進-會｜tshiok4-tsin3-hue7 創｜tshong3 會｜e7 成-員｜sing5-uan5 Looⁿg｜Looⁿg 佇-遐｜ti7-hia1 做｜tso3 專-職｜tsuan1-tsit4 ，｜, 促-進-會｜tshiok4-tsin3-hue7 成-員｜sing5-uan5 本-底｜pun2-te2 就｜to7 常-在｜tshiang5-tsai7 佇-遐｜ti7-hia1 行-踏｜kiann5-tah8 。｜. 17｜17 工｜kang1 靜-坐｜tsing7-tso7 行-動｜hing5-tong7 結-束｜kiat4-sok4 了-後｜liau2-au7 ，｜, 為-欲｜ui7-beh4 延-續｜ian5-siok8 靜-坐｜tsing7-tso7 行｜kiann5 動-的｜tang7-e5 力-量｜lik8-liong7 ，｜, 成-立｜sing5-lip8 「｜「 台-灣｜tai5-uan5 學-生｜hak8-sing1 工-作｜kang1-tsok4 隊｜tui7 、｜」 ，｜, 尾-手｜bue2-tshiu2 淡｜tam7 江｜kang1 台-文-社｜tai5-bun5-sia7 的｜e5 張｜tiunn1 志-偉｜tsi3-ui2 閣｜koh4 招｜tsio1 參-與｜tsham1-u2 靜｜tsing7 坐-的｜tse7-e5 台-語-學-生｜tai5-gi2-hak8-sing1 佇｜ti7 創｜tshong3 國｜kok4 基-金-會｜ki1-kim1-hue7 辦-過｜pan7-kue3 3｜3 ~｜~ 4｜4 擺｜pai2 座-談｜tso7-tam5 討-論｜tho2-lun7 ，｜, 邀-請｜iau1-tshiann2 運-動-界｜un7-tong7-kai3 sianpai｜sianpai 佮｜kap4 學-生｜hak8-sing1 對-話｜tui3-ue7 。｜. 1997｜1997 年｜ni5 9｜9 月｜gueh8 開-始｜khai1-si2 ，｜, 參-與｜tsham1-u2 靜｜tsing7 坐-的｜tse7-e5 台-語-學-生｜tai5-gi2-hak8-sing1 逐-禮-拜｜tak8-le2-pai3 6｜6 暗｜am3 相-招｜sio1-tsio1 佇｜ti7 創｜tshong3 國｜kok4 基-金-會｜ki1-kim1-hue7 聚-會｜tsu7-hue7 ，｜, 就｜tsiu7 台-灣｜tai5-uan5 社-會｜sia7-hue7 各｜kok4 方-面-的｜hong1-bin7-e5 問-題｜bun7-te5 來｜lai5 對-話｜tui3-ue7 ，｜, 交-換｜kau1-uann7 觀-點｜kuan1-tiam2 ，｜, 按-算｜an3-sng3 欲｜beh4 累-積｜lui2-tsik4 未-來｜bi7-lai5 鬥-陣｜tau3-tin7 運-作-的｜un7-tsok4-e5 共-識｜kiong7-sik4 。｜. 10｜10 月-初｜gueh8-tshue1 2｜2 開-始｜khai1-si2 ，｜, 逐-个｜tak8-e5 拜｜pai3 6｜6 聚-會｜tsu7-hue7 討-論｜tho2-lun7 煞｜suah4 ，｜, 隨｜sui5 寫-稿｜sia2-ko2 ，｜, 編-輯｜pian1-tsip8 ，｜, 出-刊｜tshut4-khan1 《｜“ 台-獨｜tai5-tok8 虎-難｜hoo2-lan7 報｜po3 》｜》 （｜( a4｜a4 版-面｜pan2-bin7 ，｜, 4｜4 頁｜iah8 ，｜, 攏-總｜long2-tsong2 出｜tshut4 6｜6 期｜ki5 ，｜, 使-用｜su2-iong7 無｜bo5 標-調｜phiau1-tiau7 的｜e5 教-會｜kau3-hue7 羅-馬-字｜lo5-ma2-ji7 、｜) ，｜, 用｜iong7 較｜khah4 詼-諧｜khue1-hai5 ，｜, 較｜khah4 輕-鬆-鞋｜khin1-sang1-e5 方-式｜hong1-sik4 來｜lai5 表-達｜piau2-tat8 無｜bo5 仝-鞋｜kang5-e5 觀-點｜kuan1-tiam2 ，｜, 想-欲｜siunn7-beh4 刺-激｜tshi3-kik4 運-動｜un7-tong7 箍-仔｜khoo1-a2 的｜e5 反-省｜huan2-sing2 ，｜, 像｜tshiunn7 第｜te7 1｜1 期｜ki5 的｜e5 〈｜〈 週｜tsiu1 休｜hiu1 二-日｜ji7-jit8 建-國｜kian3-kok4 論｜lun7 〉｜” 就｜to7 直-接｜tit8-tsiap4 剾-洗｜khau1-se2 運-動｜un7-tong7 箍-仔｜khoo1-a2 紡｜phang2 運-動-的｜un7-tong7-e5 態-度｜thai7-too7 。｜.'
	語句 =' 聚-會｜tsu7-hue7 成-員｜sing5-uan5 嘛｜ma7 佇｜ti7 「｜“ BBS｜BBS 台-灣-文-化｜tai5-uan5-bun5-hua3 資-訊｜tsu1-sin3 站｜tsam7 」｜” 成-立｜sing5-lip8 1｜1 的｜e5 版｜pan2 ，｜, 利-用｜li7-iong7 網-路｜bang7-loo7 來｜lai5 聯-絡｜lian5-lok8 抑-是｜iah4-si7 交-換｜kau1-uann7 ，｜, 討-論｜tho2-lun7 看-法｜khuann3-huat4 。｜. 1998｜1998 年｜ni5 年-初｜ni5-tshue1 郭｜kueh4 榮｜ing5 桔｜kiat4 佇｜ti7 日-本｜jit8-pun2 過-身｜ker3-sin1 ，｜, 創｜tshong3 國｜kok4 基-金-會｜ki1-kim1-hue7 煎-仔｜tsuann1-a2 按-呢｜an2-ne1 來｜lai5 停-辦｜thing5-pan7 ，｜, 2｜2 月｜gueh8 聚-會｜tsu7-hue7 徙｜sua2 到｜kau3 台-語-文｜tai5-gi2-bun5 sianpai｜sianpai 阿-仁｜a1-jin5 佮｜kap4 阿-惠｜a1-hui7 開-的｜khui1-e5 「｜“ 巢-窟｜tsau5-khut4 咖-啡｜ka1-pi1 」｜” (｜（ 佇｜ti7 台-北｜tai5-pak4 公-館｜kong1-kuan2 ）｜” ，｜, 繼-續｜ke3-siok8 逐-禮-拜｜tak8-le2-pai3 1｜1 擺｜pai2 的｜e5 討-論｜tho2-lun7 會-佮｜e7-kap4 讀-冊-會｜thak8-tsheh4-hue7 ，｜, 一-直｜it4-tit8 維-持｜i5-tshi5 到｜kau3 1998｜1998 月｜gueh8 12｜12 月｜gueh8 才｜tsiah4 停｜thing5 起-來｜khi2-0lai5 。｜. 清-華｜tshing1-hua5 大-學-教-授｜tai7-hak8-kau3-siu7 李-家｜li2-ka1 維｜i5 以｜i2 「｜「 Taiwan｜Taiwan ，｜, China｜China 」｜」 的｜e5 身-分｜sin1-hun7 ，｜, 佇｜ti7 國-際｜kok4-tse3 科-學｜kho1-hak8 期-刊｜ki5-khan1 《｜“ Science｜Science 》｜” 發-表｜huat4-piau2 論-文｜lun7-bun5 ��｜. 1998｜1998 年｜ni5 3｜3 月｜gueh8 清｜tshing1 大｜tua7 佮｜kap4 交｜kau1 大｜tua7 台｜tai5 研｜gian2 社｜sia7 四-界｜si3-ke3 走-傱｜tsau2-tsong5 共｜ka7 檢-舉｜kiam2-ki2 ，｜, 路-尾｜loo7-bue2 決-定｜kuat4-tiann7 欲｜beh4 店｜tiam3 學-校｜hak8-hau7 共｜ka7 唱-聲｜tshiang3-siann1 。｜. 4｜4 月｜gueh8 24｜24 透-早｜thau3-tsa2 ，｜, 台-灣｜tai5-uan5 學-生｜hak8-sing1 工-作｜kang1-tsok4 隊｜tui7 （｜( 促-進-會｜tshiok4-tsin3-hue7 、｜) 佮｜kap4 台-灣｜tai5-uan5 青-年｜tshing1-lian5 成-長｜sing5-tiong2 團｜thuan5 佇｜ti7 新-竹｜sin1-tik4 清-華｜tshing1-hua5 大-學｜tai7-hak8 大-門-口｜tua7-mng5-khau2 靜-坐｜tsing7-tso7 抗-議｜khong3-gi7 ，｜, 提-醒｜the5-tshenn2 受｜siu7 台-灣｜tai5-uan5 人-民｜jin5-bin5 供｜kiong1 養-的｜iong2-e5 學-者｜hak8-tsia2 著-愛｜tioh8-ai3 有｜u7 社-會｜sia7-hue7 責-任｜tsik4-jim7 ，｜, 若｜na7 為-著｜ui7-tioh8 個｜e5 人-的｜lang5-e5 利-益｜li7-ik4 去｜khi3 配-合｜phue3-hap8 中-國｜tiong1-kok4 「｜「 學-術｜hak8-sut8 統｜thong2 戰｜tsian3 」｜」 的｜e5 企-圖｜khi3-too5 ，｜, 台-灣｜tai5-uan5 人-愛｜jin5-ai3 共｜ka7 片-相｜phinn3-siunn3 。｜. 續｜siok8 接｜tsih4 ，｜, 中-央｜tiong1-iang1 研-究-院｜gian2-kiu3-inn7 院-長｜inn7-tiunn2 李｜li2 遠｜uan2 哲｜tiat4 佮｜kap4 台-灣｜tai5-uan5 12｜12 間-大｜king1-tua7 學-校-長｜hak8-hau7-tiunn2 欲-去｜beh4-khi3 中-國｜tiong1-kok4 參-加｜tsham1-ka1 北-京｜pak4-kiann1 大-學｜tai7-hak8 100｜100 周-年｜tsiu1-ni5 校-慶｜hau7-khing3 。｜. 4｜4 月｜gueh8 28｜28 社-運｜sia7-un7 團-體｜thuan5-the2 佇｜ti7 台-大｜tai5-tai7 抗-議｜khong3-gi7 ，｜, 佇｜ti7 中-國｜tiong1-kok4 政-府｜tsing3-hu2 不-斷｜put4-tuan7 打-壓｜ta2-ap4 台-灣｜tai5-uan5 的-時｜e5-si5 ，｜, 要-求｜iau1-kiu5 這-寡｜tsit4-kua2 學-術｜hak8-sut8 人｜lang5 享-受｜hiong2-siu7 台-灣｜tai5-uan5 人-民｜lin5-bin5 的｜e5 勞-動｜lo5-tong7 成-果｜sing5-ko2 ，｜, 嘛｜ma7 愛｜ai3 擔｜tam1 負｜hu7 𪜶｜in1 相-對-的｜siong1-tui3-e5 社-會｜sia7-hue7 責-任｜tsik4-jim7 ，｜, 拒-絕｜ku7-tsuat8 中-國-的｜tiong1-kok4-e5 邀-請｜iau1-tshiann2 ，｜, 避-免｜pi7-bian2 變-做｜pinn3-tsue3 中-國｜tiong1-kok4 統｜thong2 戰｜tsian3 的｜e5 工-具｜kong1-ku7 。｜. 4｜4 月｜gueh8 30｜30 台-灣｜tai5-uan5 學-生｜hak8-sing1 工-作｜kang1-tsok4 隊｜tui7 苦-勸｜khoo2-khng3 台-大｜tai5-tai7 校-長｜hau7-tiunn2 陳｜tan5 維｜i5 昭｜tsiau1 無｜bo5 成-功｜sing5-kong1 ，｜, 佮｜kap4 台-灣｜tai5-uan5 青-年｜tshing1-lian5 成-長｜sing5-tiong2 團｜thuan5 佇｜ti7 台-灣｜tai5-uan5 大-學｜tai7-hak8 大-門-口｜tua7-mng5-khau2 「｜“ 禁-食｜kim3-tsiah8 ，｜, 懺-悔｜tsham3-hue2 ，｜, 靜-坐｜tsing7-tso7 」｜” 1｜1 工｜khang1 ，｜. 5｜5 月-初｜gueh8-tshue1 1｜1 ，｜, 閣｜koh4 佮｜kap4 台-灣｜tai5-uan5 青-年｜tshing1-lian5 電-台｜tian7-tai5 ，｜, 建-國｜kian3-kok4 廣-場｜kong2-tiunn5 電-台｜tian7-tai5 到｜kau3 中-央｜tiong1-iang1 研-究-院｜gian2-kiu3-inn7 ，｜, 要-求｜iau1-kiu5 李｜li2 遠｜uan2 哲｜tiat4 莫-去｜mai3-khir3 中-國｜tiong1-kok4 。｜. 另-外｜ling7-gua7 ，｜, 促-進-會｜tshiok4-tsin3-hue7 成-員｜sing5-uan5 嘛｜ma7 一-直｜it4-tit8 有｜u7 共｜ka7 軍-中｜kun1-tiong1 人-權｜jin5-kuan5 促-進｜tshiok4-tsin3 會-的｜e7-e5 『｜『 黃｜ng5 媽-媽｜ma1-ma1 』｜” （｜( 陳｜tan5 碧｜phik4 娥｜ngoo5 ）｜) 鬥-相-仝｜tau3-sann1-kang7 ，｜, 支-援｜tsi1-uan7 受-害-者｜siu7-hai7-tsia2 家-屬｜ka1-siok8 的｜e5 抗-議｜khong3-gi7 行-動｜hing5-tong7 ，｜, 嘛｜ma7 燒｜sio1 連-續｜lian5-siok8 幾-若｜kui2-na7 冬｜tang1 （｜( 1998｜1998 ~｜~ 2003｜2003 ）｜) 參-與｜tsham1-u2 9｜9 月-初｜gueh8-tshue1 3｜3 去｜khi3 台-北｜tai5-pak4 大-直｜tai7-tit8 忠-烈-祠｜tiong1-liat8-su5 的｜e5 抗-議｜khong3-gi7 遊-行｜iu5-hing5 。｜. 2008｜2008 年-中｜ni5-tiong1 ，｜, 北-部｜pak4-poo7 的｜e5 成-員｜sing5-uan5 參-與｜tsham1-u2 淡-水｜tam7-tsui2 竹-圍-仔｜tik4-ui5-a2 在-地｜tsai7-te7 發｜huat4 起-的｜khi2-e5 「｜「 反｜huan2 淡｜tam7 北｜pak4 道-路｜to7-loo7 運-動｜un7-tong7 、｜」 ，｜, 反-對｜huan2-tui3 一-直｜it4-tit8 為-著｜ui7-tioh8 開-發｜khai1-huat4 ，｜, 為-著｜ui7-tioh8 財｜tsai5 團-的｜thuan5-e5 利-益｜li7-ik4 來｜lai5 破-壞｜pho3-huai7 環-境｜khuan5-king2 。｜.'
	結果 = 用戶端.翻譯(語句, 編碼器)
	print(結果['text'])
	