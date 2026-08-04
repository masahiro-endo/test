
import pyxel as px


class Maze:
    def getmaze(self,w,h):
        if w<5:
            w=5
        if h<5:
            h=5
        wkw=w-(1-w%2)   #偶数の場合、1引いて奇数にする
        wkh=h-(1-h%2)   #偶数の場合、1引いて奇数にする


        self.cpath=0    #通路
        self.cw=1       #壁
        self.cexw=2     #作成中壁
        lmap=[[self.cpath for i in range(wkw)]for j in range(wkh)]    #迷路マップ初期化
        self.makemaze(lmap,wkw,wkh)        #迷路作成処理


        return lmap


    def extendwall(self,kiten,lmap,w,h): #壁延長処理
        lmap[kiten[0]][kiten[1]]=self.cexw  #起点を作成中壁にする
        #延長可能な方向調査
        lmov=[]
        if lmap[kiten[0]-2][kiten[1]]!=self.cexw:                       #上が作成中壁ではない場合
            lmov.append([[kiten[0]-2,kiten[1]],[kiten[0]-1,kiten[1]]])  #上を延長可能リストに追加
        if lmap[kiten[0]+2][kiten[1]]!=self.cexw:                       #下が作成中壁ではない場合
            lmov.append([[kiten[0]+2,kiten[1]],[kiten[0]+1,kiten[1]]])  #下を延長可能リストに追加
        if lmap[kiten[0]][kiten[1]-2]!=self.cexw:                       #左が作成中壁ではない場合
            lmov.append([[kiten[0],kiten[1]-2],[kiten[0],kiten[1]-1]])  #左を延長可能リストに追加
        if lmap[kiten[0]][kiten[1]+2]!=self.cexw:                       #右が作成中壁ではない場合
            lmov.append([[kiten[0],kiten[1]+2],[kiten[0],kiten[1]+1]])  #右を延長可能リストに追加
        if len(lmov)>0:    #延長可能な場合
            sel=lmov[px.rndi(0,len(lmov)-1)]     #延長可能な方向からランダムに選択
            lmap[sel[1][0]][sel[1][1]]=self.cexw         #選択した方向を作成中壁にする
            if lmap[sel[0][0]][sel[0][1]]==self.cw:    #延長先が壁の場合
                #作成中壁を確定
                for j in range(h):
                    for i in range(w):
                        if lmap[j][i]==self.cexw:
                            lmap[j][i]=self.cw
                return 1    #延長終了
            else:   #延長先が通路の場合
                return self.extendwall(sel[0],lmap,w,h) #壁延長処理(再帰)
        else:   #延長不可能な場合
            #作成中壁を通路に戻す
            for j in range(h):
                for i in range(w):
                    if lmap[j][i]==self.cexw:
                        lmap[j][i]=self.cpath


    def makemaze(self,lmap,w,h): #迷路作成処理
        for i in range(w):
            lmap[0][i],lmap[h-1][i]=self.cw,self.cw   #上下壁作成
        for j in range(1,h-1):
            lmap[j][0],lmap[j][w-1]=self.cw,self.cw   #左右壁作成
        #起点リスト作成
        lkiten=[]
        for j in range(2,h-2,2):
            for i in range(2,w-2,2):
                lkiten.append([j,i])
        #起点シャッフル
        for i in range(len(lkiten)):
            r=px.rndi(0,len(lkiten)-1)
            lkiten[i],lkiten[r]=lkiten[r],lkiten[i]


        for i in lkiten:   #起点リストでforループ
            if lmap[i[0]][i[1]]!=self.cw:  #対象起点が既に壁ならスルー
                endstatus=True  #壁延長再帰処理ステータス初期化
                while endstatus:
                    rslt=self.extendwall(i,lmap,w,h)
                    if rslt==1:     #壁確定
                        endstatus=False #壁延長再帰処理終了

