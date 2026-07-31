
import pyxel as px
import math as mt
import time as tm


from c103maze import Maze


def sign(x):    #符号関数
    return (x>0)-(x<0)  #符号を返す


class App():
    def __init__(self):
        self.scrh=128
        self.scrw=128
        self.vh=128
        self.vw=128


        px.init(self.scrw,self.scrh,title="迷路内の擬似３Ｄ化"
                ,display_scale=4,capture_sec=20)
        px.load("assets_wall.pyxres")


        #イメージバンク内座標
        self.wallf3=( 0, 0,32, 32)  #正面壁遠
        self.f3left=48              #正面壁遠left
        self.f3top=48               #正面壁遠top
        self.wallf2=(32, 0,48, 48)  #正面壁中
        self.f2left=40              #正面壁中left
        self.f2top=40               #正面壁中top
        self.wallf1=(80, 0,80, 80)  #正面壁近
        self.f1left=24              #正面壁近left
        self.f1top=24               #正面壁近top
        self.f0top=0                #正面壁側top
        self.walll3=(96,80,24, 48)  #左壁中2列目
        self.walll2=( 0,80, 8, 48)  #左壁中
        self.walll1=(16,80,16, 80)  #左壁近
        self.walll0=(48,80,24,128)  #左壁側
        self.f0l=0                  #左壁側left
        self.wallr3=(120,80,24,48)  #右壁中2列目
        self.wallr2=( 8,80, 8, 48)  #右壁中
        self.wallr1=(32,80,16, 80)  #右壁近
        self.wallr0=(72,80,24,128)  #右壁側
        self.f0r=104                #右壁側left
        self.goal2=(160,0,16,32)    #ゴール中
        self.g2t=60                 #ゴール中top
        self.g2l=55                 #ゴール中left
        self.goal1=(176,0,22,44)    #ゴール近
        self.g1t=60                 #ゴール近top
        self.g1l=52                 #ゴール近left
        self.cmps=(0,208,15,15)     #コンパス枠
        self.allow=(16,208,8,8)     #コンパス矢
        self.cmpsleft=112           #コンパスleft
        self.t0=0
        self.distinit=0.1           #割り込み周期初期値
        self.movl=(32,118,0,232,8,8)    #左転回
        self.movr=(88,118,8,232,8,8)    #右転回
        self.movf=(60,118,16,232,10,8)  #移動前
        self.movt=(58,118,32,232,13,8)  #後転回


        self.view=[]        #視界のブロック配置


        #マップデータ
        self.h=21       #迷路縦幅
        self.w=31       #迷路横幅


        self.col=0                          #壁色番号
        self.colcnt=4                       #壁色
        self.colw=8
        self.sttpos=[1,1]                   #スタート座標設定
        self.goalpos=[self.h-2,self.w-2]    #ゴール座標設定
        self.mh=0


        self.mazeinit()


        px.run(self.update,self.draw)


    def mazeinit(self):
        self.mypos=[1,1]    #自分の座標:初期座標(1,1)
        self.compass=1      #自分の向き 0:上,1:右,2:下,3:左
        #マップ作成
        self.lmap=[]        #迷路マップリスト
        wk=Maze()           #迷路自動生成クラスインスタンス
        self.lmap=wk.getmaze(self.w,self.h) #迷路取得
        self.sttflg=0       #開始フラグ初期化


    def vpos(self,angle):
        #視界の座標と描画順を取得
        #ABCDE
        #56789
        #X234X
        #X0P1X
        lwk=[]          #P周囲座標リスト
        lyx=[]          #視界座標リスト
        wagl=angle%360  #アングル再計算
        #P周囲(-90度～90度：45度毎)
        for i in range(-2,3):
            y=int(round(-mt.cos(mt.radians(wagl+i*45))))
            x=int(round(mt.sin(mt.radians(wagl+i*45))))
            lwk.append([y,x])
        v=lwk[4][0]+lwk[4][1]   #中心から右方向のベクトルを計算
        #視界の奥の座標からリストに追加
        #ABCDE
        for i in range(5):
            y=lwk[2][0]*3+(i-2)*lwk[4][0]   #3マス前のy座標を計算
            x=lwk[2][1]*3+(i-2)*lwk[4][1]   #3マス前のx座標を計算
            dist=(y+x-(lwk[2][0]+lwk[2][1])*3)*v    #中心から各座標の距離を計算
            lyx.append([y,x,dist])  #遠距離の座標を登録
        #56789
        for i in range(5):
            y=lwk[2][0]*2+(i-2)*lwk[4][0]   #2マス前のy座標を計算
            x=lwk[2][1]*2+(i-2)*lwk[4][1]   #2マス前のx座標を計算
            dist=(y+x-(lwk[2][0]+lwk[2][1])*2)*v    #中心から各座標の距離を計算
            lyx.append([y,x,dist])  #中距離の座標を登録
        #59687 に並び順変更
        lyx[6],lyx[7],lyx[9]=lyx[9],lyx[6],lyx[7]   #両側から描画される様に登録順を変更
        #234
        for i in range(3):
            y=lwk[2][0]+(i-1)*lwk[4][0]     #1マス前のy座標を計算
            x=lwk[2][1]+(i-1)*lwk[4][1]     #1マス前のx座標を計算
            dist=(y+x-(lwk[2][0]+lwk[2][1]))*v  #中心から各座標の距離を計算
            lyx.append([y,x,dist])  #近距離の座標を登録
        #243 に並び順変更
        lyx[11],lyx[12]=lyx[12],lyx[11]    #両側から描画される様に登録順を変更
        #01
        lwk[0].append(-1)   #Pの左の距離を要素に追加
        lyx.append(lwk[0])  #左側面の座標を追加
        lwk[4].append(1)    #Pの右の距離を要素に追加
        lyx.append(lwk[4])  #右側面の座標を追加


        return lyx


    def getvmap(self):  #視界内のブロック取得
        l=[]
        for i in self.view:
            wy,wx=i[0]+self.mypos[0],i[1]+self.mypos[1]
            if wy<0 or wy>self.h-1 or wx<0 or wx>self.w-1:  #壁の外側は全てブロック
                l.append(1)
            else:
                l.append(self.lmap[wy][wx]) #ブロック配置を登録


        return l


    def update(self):
        self.mh=0
        if px.mouse_wheel:              #マウスホイール操作ありの場合
            self.mh=sign(px.mouse_wheel)     #マウスホイール状態更新


        if (px.btnp(px.KEY_Q)
            or px.btnp(px.MOUSE_BUTTON_LEFT) and px.btnp(px.MOUSE_BUTTON_RIGHT)
            or px.btnp(px.GAMEPAD1_BUTTON_START)):    #迷路リセット
            self.mazeinit()


        if (px.btnp(px.KEY_UP)
            or px.btnp(px.GAMEPAD1_BUTTON_DPAD_UP)
            or self.mh>0):
            if self.vmap[-3]==0:    #前が通路の場合
                self.mypos[0]+=self.view[-3][0] #一歩前に進む
                self.mypos[1]+=self.view[-3][1]
                self.t0=tm.time()   #基準時間取得
                self.lmovv=list(self.movf)
                self.sttflg=0
        if (px.btnp(px.KEY_RIGHT)
            or px.btnp(px.GAMEPAD1_BUTTON_RIGHTSHOULDER)
            or px.btnp(px.MOUSE_BUTTON_RIGHT)):
            self.compass=(self.compass+1)%4     #右を向く
            self.t0=tm.time()   #基準時間取得
            self.lmovv=list(self.movr)
            self.sttflg=0
        if (px.btnp(px.KEY_DOWN)
            or px.btnp(px.GAMEPAD1_BUTTON_DPAD_DOWN)
            or self.mh<0):
            self.compass=(self.compass+2)%4     #後ろを向く
            self.t0=tm.time()   #基準時間取得
            self.lmovv=list(self.movt)
            self.sttflg=0
        if (px.btnp(px.KEY_LEFT)
            or px.btnp(px.GAMEPAD1_BUTTON_LEFTSHOULDER)
            or px.btnp(px.MOUSE_BUTTON_LEFT)):
            self.compass=(self.compass+3)%4     #左を向く
            self.t0=tm.time()   #基準時間取得
            self.lmovv=list(self.movl)
            self.sttflg=0
        if px.btnp(px.KEY_SPACE):
            self.col=(self.col+1)%self.colcnt   #壁色を変更
            self.sttflg=0


        if self.sttflg==0:
            self.view=self.vpos(self.compass*90)    #視界取得
            self.vmap=self.getvmap()    #視界内のブロック所得
            self.sttflg=1


    def walldraw(self,x,y,col,l):   #壁描画
        xw=0
        for k in range(l[3]//self.colw):
            for j in range(l[2]//self.colw):
                xx=x+j*self.colw
                if xx<=self.vw:
                    if xx+self.colw>self.vw:
                        xw=self.vw-xx
                    else:
                        xw=self.colw
                    px.blt(xx,y+k*self.colw,1,col,0,xw,self.colw) #壁色
        if x<=self.vw:
            if x+l[2]>self.vw:
                xw=self.vw-x
            else:
                xw=l[2]
            px.blt(x,y,0,l[0],l[1],xw,l[3],15)    #壁


    def draw(self):
        px.cls(0)


        col=self.col*self.colw  #壁色


        for i in range(len(self.vmap)):
            if i<=4:    #遠距離ブロック描画
                if self.vmap[i]==1:
                    #正面壁
                    l=list(self.wallf3)
                    x=self.f3left+self.view[i][2]*l[2]
                    self.walldraw(x,self.f3top,col,l)


            elif i<=9: #中距離ブロック描画
                if self.vmap[i]==1:
                    #正面壁
                    l=list(self.wallf2)
                    x=self.f2left+self.view[i][2]*l[2]
                    self.walldraw(x,self.f2top,col,l)
                    if sign(self.view[i][2])==-1:
                        #左壁
                        if self.view[i][2]==-2:
                            ll=list(self.walll3)
                        else:
                            ll=list(self.walll2)
                        self.walldraw(x+l[2],self.f2top,col,ll)
                    elif sign(self.view[i][2])==1:
                        #右壁
                        if self.view[i][2]==2:
                            ll=list(self.wallr3)
                        else:
                            ll=list(self.wallr2)
                        self.walldraw(x-ll[2],self.f2top,col,ll)
                if self.goalpos==[self.mypos[0]+self.view[i][0],self.mypos[1]+self.view[i][1]]:
                    #ゴールポール描画
                    l=list(self.goal2)
                    x=self.g2l+self.view[i][2]*l[2]*2.1
                    px.blt(x,self.g2t,0,l[0],l[1],l[2],l[3],15)


            elif i<=12: #近距離ブロック描画
                if self.vmap[i]==1:
                    #正面壁
                    l=list(self.wallf1)
                    x=self.f1left+self.view[i][2]*l[2]
                    self.walldraw(x,self.f1top,col,l)
                    if sign(self.view[i][2])==-1:
                        #左壁
                        ll=list(self.walll1)
                        self.walldraw(x+l[2],self.f1top,col,ll)
                    elif sign(self.view[i][2])==1:
                        #右壁
                        ll=list(self.wallr1)
                        self.walldraw(x-ll[2],self.f1top,col,ll)
                if self.goalpos==[self.mypos[0]+self.view[i][0],self.mypos[1]+self.view[i][1]]:
                    #ゴールポール描画
                    l=list(self.goal1)
                    x=self.g1l+self.view[i][2]*l[2]*2.5
                    px.blt(x,self.g1t,0,l[0],l[1],l[2],l[3],15)


            else:   #側面ブロック描画
                if self.vmap[i]==1:
                    if self.view[i][2]==-1:
                        #左壁
                        ll=list(self.walll0)
                        self.walldraw(self.f0l,self.f0top,col,ll)
                    elif self.view[i][2]==1:
                        #右壁
                        ll=list(self.wallr0)
                        self.walldraw(self.f0r,self.f0top,col,ll)


        #自分の座標と向きを表示
        px.text(0,0,f"[X,Y]=[{self.mypos[1]},{self.mypos[0]}]",7)
        px.text(0,8,f"GOALPOS=[{self.goalpos[1]},{self.goalpos[0]}]",7)    #ゴール座標を表示
        l=list(self.cmps)
        px.blt(self.cmpsleft,0,0,l[0],l[1],l[2],l[3],15)      #コンパス枠描画
        ll=list(self.allow)
        px.blt(self.cmpsleft+4,0+4,0,ll[0]+self.compass*8,ll[1],ll[2],ll[3],15)   #コンパス矢描画


        if tm.time()>self.t0+self.distinit: #描画時間タイマー
           self.t0=0    #タイマー停止


        if self.t0>0:
            l=self.lmovv
            px.blt(l[0],l[1],0,l[2],l[3],l[4],l[5],15)      #移動操作描画


        posmes=""
        if self.mypos==self.sttpos:
            posmes="START!"
        elif self.mypos==self.goalpos:
            posmes="GOAL!"
        px.text(54,16,posmes,2) #スタート座標時にSTART!,ゴール座標時GOAL!を表示


App()



