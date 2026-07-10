#0103tetris.py テトリス
import pyxel as px
import bmpfont as bmf
import time as tm


def sign(x):    #符号関数
    return (x>0)-(x<0)  #符号を返す


class App():
    def __init__(self):
        self.row=23     #操作エリア行数
        self.clmn=14    #操作エリア幅数
        px.init(320,self.row*16+16,title="テトリス(TETRIS)",display_scale=2)
        px.load("0103tetris.pyxres")
        self.bmf10 = bmf.BDFRenderer("umplus_j10r.bdf") #日本語フォント
        self.distinit=20        #割り込み周期初期値
       
        #ブロック定義
        self.l=[]
        #4マスブロック
        self.l.append([1,4,3,("001","111","000"),("010","010","011"),("000","111","100"),("110","010","010")])
        self.l.append([2,4,3,("100","111","000"),("011","010","010"),("000","111","001"),("010","010","110")])
        self.l.append([3,4,3,("010","111","000"),("010","011","010"),("000","111","010"),("010","110","010")])
        self.l.append([4,2,4,("0000","1111","0000","0000"),("0100","0100","0100","0100")])
        self.l.append([5,2,3,("000","110","011"),("010","110","100")])
        self.l.append([6,2,3,("000","011","110"),("010","011","001")])
        self.l.append([7,1,2,("11","11")])
        #---追加ブロック定義---
        #5マスブロック
        self.l.append([1,4,3,("011","111","000"),("010","011","011"),("000","111","110"),("110","110","010")])
        self.l.append([2,4,3,("110","111","000"),("011","011","010"),("000","111","011"),("010","110","110")])
        self.l.append([3,2,5,("00000","00000","11111","00000","00000",),("00100","00100","00100","00100","00100")])
        self.l.append([4,1,3,("010","111","010")])
        self.l.append([5,4,3,("111","100","100"),("111","001","001"),("001","001","111"),("100","100","111")])
        self.l.append([6,4,4,("0000","0001","1111","0000"),("0100","0100","0100","0110")
                            ,("0000","1111","1000","0000"),("0110","0010","0010","0010")])
        self.l.append([7,4,4,("0000","1000","1111","0000"),("0110","0100","0100","0100")
                            ,("0000","1111","0001","0000"),("0010","0010","0010","0110")])
        self.l.append([1,4,3,("001","011","110"),("100","110","011"),("011","110","100"),("110","011","001")])
        self.l.append([2,4,3,("010","011","110"),("100","111","010"),("011","110","010"),("010","111","001")])
        self.l.append([3,4,3,("001","111","010"),("010","110","011"),("010","111","100"),("110","011","010")])
        self.l.append([4,4,4,("0000","0010","1111","0000"),("0100","0100","0110","0100")
                            ,("0000","1111","0100","0000"),("0010","0110","0010","0010")])
        self.l.append([5,4,4,("0000","0100","1111","0000"),("0100","0110","0100","0100")
                            ,("0000","1111","0010","0000"),("0010","0010","0110","0010")])
        self.l.append([6,4,3,("000","111","101"),("110","010","110"),("101","111","000"),("011","010","011")])
        self.l.append([7,4,3,("111","010","010"),("001","111","001"),("010","010","111"),("100","111","100")])
        self.l.append([1,4,4,("0000","0011","1110","0000"),("0100","0100","0110","0010")
                            ,("0000","0111","1100","0000"),("0100","0110","0010","0010")])
        self.l.append([2,4,4,("0000","1100","0111","0000"),("0010","0110","0100","0100")
                            ,("0000","1110","0011","0000"),("0010","0010","0110","0100")])
        self.l.append([3,2,3,("001","111","100"),("110","010","011")])
        self.l.append([4,2,3,("100","111","001"),("011","010","110")])
        #3マスブロック
        self.l.append([5,2,3,("000","111","000"),("010","010","010")])
        self.l.append([6,4,2,("10","11"),("11","10"),("11","01"),("01","11")])
        #---------------------


        self.tinit=0    #ブロック初期y座標
        self.linit=5    #ブロック初期x座標
        self.gameinit() #変数初期化
       
        px.run(self.update,self.draw)


    def gameinit(self):
        self.dist=self.distinit #割り込み周期(秒*10)
        self.score=0        #点数
        self.linecnt=0      #消しライン数
        self.blkcnt=1       #ブロック発生回数
        self.mh=0           #マウスホイール値初期化
        self.gmovflg=0      #ゲームオーバーフラグ
        self.t0=tm.time()   #基準時間取得
        self.bx=self.linit  #ブロックx座標初期化
        self.by=self.tinit  #ブロックy座標初期化
        self.set=0          #ブロック向きindex
        self.typ=px.rndi(0,6)   #ブロック型index


        #壁作成
        self.lbox=[[0 for i in range(self.clmn)]for j in range(self.row+1)] #配置管理用リスト
        for i in range(self.row):
            self.lbox[i][1]=1               #左壁
            self.lbox[i][self.clmn-2]=1     #右壁
        for i in range(1,self.clmn-1):
            self.lbox[self.row][i]=1        #下端壁


    def blkdrop(self):  #ブロックドロップ処理
        oldby=self.by   #ブロックy座標を保存
        self.by+=1  #下に移動
        if self.chkbox()==False:    #重なりチェック
            self.by=oldby
            self.lockbox()          #ブロック固定化処理


    def lockbox(self):  #ブロック固定化処理
        for j in range(self.l[self.typ][2]):
            for i in range(self.l[self.typ][2]):
                if self.l[self.typ][3+self.set][j][i]=="1":     #ブロックあり
                    self.lbox[self.by+j][self.bx+i]=self.l[self.typ][0] #ブロックの色をセット
        self.chkline()  #行チェック処理


    def chkline(self):  #行チェック処理
        lll=[]          #行内固定化ブロック数リスト
        sc=0            #加点対象行数初期化
        for j in range(self.row):
            cnt=0       #ブロック数カウンタ
            for i in range(2,self.clmn-2):
                cnt+=sign(self.lbox[j][i])  #ブロックがあれば加算
            lll.append(cnt)     #リストに追加
        for j in range(self.row):
            if lll[j]==10:      #行が埋まっている場合
                sc+=1           #加点対象行追加
                self.linecnt+=1 #消しライン数加算
                for i in range(j,0,-1):
                    self.lbox[i]=self.lbox[i-1] #上の行を下に詰める
                self.lbox[0]=[0,1,0,0,0,0,0,0,0,0,0,0,1,0]  #一番上の行に初期値セット
        if sc>0:    #加点対象行ありの場合
            self.score+=10*2**sc    #点数加算
        self.newblk()


    def newblk(self):
        #ブロック型は通常は4マスブロックのみで、11回毎に5マスブロックor3マスブロックが選択される様に調整
        self.typ=px.rndi((1-sign(self.blkcnt%11))*7,6+(1-sign(self.blkcnt%11))*20)  #ブロック型セット
        self.set=0  #ブロック向き初期化
        self.bx,self.by=self.linit,self.tinit   #ブロックxy座標初期化
        self.blkcnt+=1  #ブロック発生回数+1
        if self.chkbox()==False:
            self.gameover()     #ブロック初期位置に既にブロックがあればゲームオーバー処理
        self.dist=self.distinit-self.blkcnt//10 #ブロック落下速度調整
        if self.dist<1: #落下速度の最速値調整
            self.dist=1
       
    def gameover(self): #ゲームオーバー処理
        self.gmovflg=1  #ゲームオーバーフラグに1をセット


    def chkbox(self):   #ブロック重なりチェック
        chkflg=True #重なりチェックフラグ初期化
        for j in range(self.l[self.typ][2]):
            for i in range(self.l[self.typ][2]):
                if self.l[self.typ][3+self.set][j][i]=="1":     #ブロックあり
                    if self.lbox[self.by+j][self.bx+i]>=1:      #ブロックが壁と重なる場合
                        chkflg=False    #変更中止
                        break
            if chkflg==False:
                break
        return chkflg
   
    def update(self):
        if self.gmovflg==0: #ゲーム中
            t1=tm.time()                    #現時間取得
            if t1-self.t0>=self.dist/10:    #割り込み周期以上の場合
                self.blkdrop()              #ブロックドロップ処理
                self.t0=tm.time()           #基準時間更新
            #移動
            self.mh=-sign(px.mouse_wheel)  #マウスホイール状態更新
            if self.mh:
                oldbx=self.bx   #ブロックx座標を保存
                self.bx=self.bx+self.mh     #マウスホイール操作をブロックに反映
                if self.chkbox()==False:    #重なりチェック
                    self.bx=oldbx
            elif px.btnp(px.KEY_LEFT) or px.btnp(px.KEY_RIGHT): #左右矢印キー
                oldbx=self.bx   #ブロックx座標を保存
                if px.btnp(px.KEY_LEFT):    #左矢印キーの場合
                    self.bx-=1  #左に移動
                else:                       #右矢印キーの場合
                    self.bx+=1  #右に移動
                if self.chkbox()==False:    #重なりチェック
                    self.bx=oldbx
            elif px.btn(px.MOUSE_BUTTON_RIGHT) or px.btn(px.KEY_DOWN):   #右クリックor下矢印キー
                self.blkdrop()      #ブロックドロップ処理
                self.t0=tm.time()   #基準時間更新
            #回転
            #左クリックorスペースキーor上矢印キー
            if px.btnp(px.MOUSE_BUTTON_LEFT) or px.btnp(px.KEY_SPACE) or px.btnp(px.KEY_UP):
                oldset=self.set #ブロック向きindexを保存
                self.set=(self.set+1)%self.l[self.typ][1]
                if self.chkbox()==False:    #重なりチェック
                    self.set=oldset
        else:   #ゲームオーバー時
            if px.btnp(px.MOUSE_BUTTON_LEFT) or px.btnp(px.KEY_RETURN) or px.btnp(px.KEY_KP_ENTER):
                self.gameinit() #左クリックorENTERキー押下でゲーム再開


    def draw(self):
        px.cls(0)   #画面クリア


        #外壁描画
        for i in range(self.row):
            px.blt(0,i*16,0,32,0,16,16)     #左端
            px.blt(11*16,i*16,0,32,0,16,16) #右端
        for i in range(1,self.clmn-3):
            px.blt(i*16,self.row*16,0,48,0,16,16)    #下端
        px.blt(0,self.row*16,0,64,0,16,16)           #左下角
        px.blt(11*16,self.row*16,0,80,0,16,16)       #右下角


        #固定化ブロック描画
        for j in range(self.row):
            for i in range(2,self.clmn-2):
                px.blt(i*16-16,j*16,0,16*self.lbox[j][i],16,16,16) #色
                if self.lbox[j][i]>=1:  #固定化ブロックあり
                    px.blt(i*16-16,j*16,0,16,0,16,16,15)    #ブロック描画


        #操作ブロック描画
        for j in range(self.l[self.typ][2]):
            for i in range(self.l[self.typ][2]):
                if self.l[self.typ][3+self.set][j][i]=="1": #ブロックあり
                    px.blt((self.bx+i)*16-16,(self.by+j)*16,0,16*self.l[self.typ][0],16,16,16) #色
                    px.blt(self.bx*16+i*16-16,self.by*16+j*16,0,0,0,16,16,15)  #ブロック描画


        #点数描画
        self.bmf10.draw_text(210, 40, f"SCORE:{self.score: >8}",7,None,0)   #点数描画
        self.bmf10.draw_text(210, 60, f"LINE :{self.linecnt: >8}",7,None,0) #消しライン数描画


        if self.gmovflg==1:
            px.blt(40,153,0,0,35,111,48)        #文字台黒
            for i in range(37):
                px.blt(40+i*3,150,0,0,32,3,3)   #上線
                px.blt(40+i*3,201,0,0,32,3,3)   #下線
            for i in range(18):
                px.blt(37,150+i*3,0,0,32,3,3)   #左線
                px.blt(151,150+i*3,0,0,32,3,3)  #右線
            self.bmf10.draw_text(70, 155, "GAME OVER",7,1,0)                #ゲームオーバー表示
            self.bmf10.draw_text(45, 165, "RETRY -> 左クリック ",7,1,0)
            self.bmf10.draw_text(115, 175, "or",7,1,0)
            self.bmf10.draw_text(100, 185, "ENTERキー",7,1,0)


App()


