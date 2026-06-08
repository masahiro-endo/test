import random

class Array2D:
    def __init__(self, width=0, height=0):
        self.create(width, height)
        self.outofrange = -1 # 領域外を指定したときの値
    
    def create(self, width, height):
        # 作成
        self.width  = width  # 幅
        self.height = height # 高さ
        self.vals   = [0] * width * height # 値
    
    def to_idx(self, x, y):
        # 座標をインデックスに変換する
        return x + (y * self.width)
    
    def check(self, x, y):
        # 領域内チェック
        if 0 <= x < self.width:
            if 0 <= y < self.height:
                # 領域内
                return True
        
        return False # 領域外
    
    def check_from_idx(self, idx):
        # 領域内チェック (インデックス指定)
        return 0 <= idx < (self.width * self.height)
    
    def get(self, x, y):
        # 値の取得
        if self.check(x, y) == False:
            return self.outofrange

        return self.get_from_idx(self.to_idx(x, y))
    
    def set(self, x, y, v):
        # 値の設定
        if self.check(x, y) == False:
            return

        return self.set_from_idx(self.to_idx(x, y), v)
    
    def get_from_idx(self, idx):
        # 値の取得 (インデックス指定)
        if self.check_from_idx(idx) == False:
            return self.outofrange
        
        return self.vals[idx]
    
    def set_from_idx(self, idx, v):
        # 値の設定 (インデックス指定)
        if self.check_from_idx(idx) == False:
            return
        
        self.vals[idx] = v

    def count(self, v):
        # 指定の値の存在数をカウントする
        ret = 0
        for j in range(self.height):
            for i in range(self.width):
                if self.get(i, j) == v:
                    ret += 1
        return ret

    def search(self, v):
        # 指定の値を検索する。最初に見つかった値を返す
        for j in range(self.height):
            for i in range(self.width):
                if self.get(i, j) == v:
                    return i, j
        # 存在しない
        return -1, -1

    def choice(self, v):
        # 指定の値の座標をランダムで取得する
        list = []
        for j in range(self.height):
            for i in range(self.width):
                if self.get(i, j) == v:
                    list.append((i, j))
        
        if len(list) == 0:
            # 存在しない
            return -1, -1

        return random.choices(list)        
    
    def fill(self, v):
        # 全てを指定の値で埋める
        self.foreach(lambda x, y, val: self.set(x, y, v))
    
    def foreach(self, func):
        # 繰り返し処理を行う
        for j in range(self.height):
            for i in range(self.width):
                func(i, j, self.get(i, j))
    
    def dump(self):
        # デバッグ出力
        print("[Array2D] (w,h)=(%d,%d)"%(self.width, self.height))
        for j in range(self.height):
            s = ""
            for i in range(self.width):
                s = s + "%d,"%self.get(i, j)
            print(s)
