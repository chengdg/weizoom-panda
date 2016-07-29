
/*定义三级分类数据*/
//一级分类
var province = ["教育", "文艺", "青春", "生活", "人文社科", "经管", "科技", "电子书"];
//二级分类
var city = [
	["教材", "外语", "考试"],
	["文学", "传记", "艺术", "摄影"],
	["青春文学", "动漫", "幽默"],
	["休闲/爱好", "孕产/胎教", "烹饪/美食", "时尚/美妆", "旅游/地图", "家庭/家居", "亲子/家教", "两性关系", "育儿/早教", "保健/养生"],
	["历史", "文化", "古籍", "心理学", "哲学/宗教"],
	["管理", "投资理财", "经济"],
	["科普读物", "建筑", "医学", "计算机/网络", "农业/林业", "自然科学", "工业技术"],
	["新华出品", "文艺", "网络文学", "人文社科", "经管励志", "生活", "童书", "科技", "教育", "期刊杂志"]
];
var expressP, expressC, expressArea, areaCont;
var arrow = '_';

/*初始化一级目录*/
function intProvince() {
	areaCont = "";
	expressC = '';
	for (var i=0; i<province.length; i++) {
		areaCont += '<li onClick="selectA(' + i + ');"><a href="javascript:void(0)">' + province[i] + '</a></li>';
		for (var j=0; j<city[i].length; j++) {
			expressC += '<li class="selectB_'+i+' hide selectB_' + i + '_' + j + '" onClick="selectB(' + i + ',' + j + ');"><a href="javascript:void(0)">' + city[i][j] + '</a></li>';
		}
		$("#sort2").html(expressC)
	}
	$("#sort1").html(areaCont);
}
intProvince();

/*选择一级目录*/
function selectA(p) {
	$("#sort2 li").addClass("hide")
	$('.selectB_'+p+'').removeClass("hide");//暴露出二级分类
	// $("#sort1 li").eq(p).addClass("active").siblings("li").removeClass("active");
	if($("#sort1 li").eq(p).hasClass("active")){
		if(!$('.selectB_'+p+'').hasClass("active")){ //没有二级分类被选中时，不选择一级分类
			$("#sort1 li").eq(p).removeClass("active");
		}
	}else{
		$("#sort1 li").eq(p).addClass("active");
	}
	
	// expressP = province[p];
	// console.log('expressP',expressP);
	// $("#selectedSort").html(expressP);
}

/*选择二级目录*/
function selectB(p,c) {
	// $("#sort2 li").eq(c).addClass("active").siblings("li").removeClass("active");
	// console.log($("#sort2 li").eq(c));
	console.log($('.selectB_' + p + '_' + c + ''));
	if($('.selectB_' + p + '_' + c + '').hasClass("active")   ){
		$('.selectB_' + p + '_' + c + '').removeClass("active");
	}else{
		$('.selectB_' + p + '_' + c + '').addClass("active");
	}
	// console.log('city:',city[p][c]);
}

