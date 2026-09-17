window.ZOMBIE_GAMES={
bo1:{name:"COD7 · 黑色行动",short:"COD7",series:"Black Ops",maps:window.BO1_ORDER||[]},
bo2:{name:"COD9 · 黑色行动 II",short:"COD9",series:"Black Ops II",maps:window.BO2_ORDER||[]},
bo3:{name:"COD12 · 黑色行动 III",short:"COD12",series:"Black Ops III",maps:window.BO3_ORDER||[]},
bo4:{name:"COD15 · 黑色行动 4",short:"COD15",series:"Black Ops 4",maps:window.BO4_ORDER||[]}
};
window.ZOMBIE_GAME_ORDER=["bo1","bo2","bo3","bo4"];
window.ZOMBIE_DATA=Object.assign({},window.BO1_DATA||{},window.BO2_DATA||{},window.BO3_DATA||{},window.BO4_DATA||{});
Object.keys(window.ZOMBIE_GAMES).forEach(g=>window.ZOMBIE_GAMES[g].maps.forEach(k=>{if(window.ZOMBIE_DATA[k])window.ZOMBIE_DATA[k].game=g;}));