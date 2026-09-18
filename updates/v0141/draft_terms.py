"""Exact whole-unit labels only; no inferred replacements inside prose or URLs."""
import draft_qa

draft_qa.FIXES.update({
    'BO':'黑色行动1（BO）','BOI':'黑色行动1（BOI）','BOII':'黑色行动2（BOII）',
    'BOIII':'黑色行动3（BOIII）','BO4':'黑色行动4（BO4）','BOCW':'黑色行动冷战（BOCW）',
    'WaW':'战争世界（WaW）','World at War':'战争世界（World at War）','Black Ops':'黑色行动',
    'Black Ops II':'黑色行动2','Black Ops III':'黑色行动3','Black Ops 4':'黑色行动4',
    'Moon':'月球','Origins':'起源','Buried':'埋葬','Town':'小镇','Farm':'农场','Bus Depot':'公交站',
    'Revelations':'启示录','Revelations (map)':'启示录（地图）','Revelations (mission)':'启示录（战役任务）',
    'Classified':'机密','IX':'IX（九）','Biodome':'生物穹顶（温室）',
    'Primis':'始源小队（Primis）','Ultimis':'终始小队（Ultimis）','Victis':'受害者小队（Victis）',
    'Zwei...':'二……','AHAHAHAHAHAHAHA!':'啊哈哈哈哈哈哈！','KA-BLEWY!':'轰的一声！',
    'Suuuwwweeet!':'太——棒——了！','JUUUIIICE!':'果——汁！','Slain!':'击杀！',
    'The MP40! Wunderbar!':'MP40！太棒了！'
})
if __name__=='__main__':draft_qa.main()
