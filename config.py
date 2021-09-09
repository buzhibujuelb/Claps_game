import numpy as np

LIMIT = 50

ACT = [
 "聚气","防御","小枪"
,"小弹","竖切","中弹"
,"关","鹰眼","大弹"
,"地裂","飞天"
]

ACTION_COSTS = [
#0聚气 1防御 2小枪
-1, 0, 1,
#3小弹 4竖切 5中弹
1, 2, 2,
#6关 7鹰眼 8大弹
3, 1, 3,
#9地裂 10飞天
4, 1
]

NP_ACTION_COSTS=np.array(ACTION_COSTS)

MAXROUND = 10
