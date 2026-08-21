

def calc_intersection(pointA, pointB, pointC, pointD):
    # 線分ABと線分CDの交点を計算
    denominator = (pointB[0] - pointA[0]) * (pointD[1] - pointC[1]) - (pointB[1] - pointA[1]) * (pointD[0] - pointC[0])

    # 平行な場合
    if denominator == 0:
        return None # 交点なし

    # ベクトル計算
    vectorAC = (pointC[0] - pointA[0], pointC[1] - pointA[1])
    r = ((pointD[1] - pointC[1]) * vectorAC[0] - (pointD[0] - pointC[0]) * vectorAC[1]) / denominator
    s = ((pointB[1] - pointA[1]) * vectorAC[0] - (pointB[0] - pointA[0]) * vectorAC[1]) / denominator

    # 線分上に交点が存在しない場合
    if not (0 <= r <= 1 and 0 <= s <= 1):
        return None

    # 交点座標を計算
    intersection_x = pointA[0] + r * (pointB[0] - pointA[0])
    intersection_y = pointA[1] + r * (pointB[1] - pointA[1])

    return (intersection_x, intersection_y)



# 使用例
pointA = (0 ,  0)
pointB = (40, 40)
pointC = (0 , 9)
pointD = (40, 9)

intersection = calc_intersection(pointA, pointB, pointC, pointD)
if intersection:
    print(f"交点: {intersection}")
else:
    print("交点なし")