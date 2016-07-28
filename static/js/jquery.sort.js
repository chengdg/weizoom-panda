/**
 * jquery.sort.js
 * 商品发布-选择分类
 * author: 锐不可挡
 * date: 2016-07-07
**/
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
var expressP, expressC, expressD, expressArea, areaCont;
var arrow = " <font>&gt;</font> ";

/*初始化一级目录*/
function intProvince() {
	areaCont = "";
	for (var i=0; i<province.length; i++) {
		areaCont += '<li onClick="selectP(' + i + ');"><a href="javascript:void(0)">' + province[i] + '</a></li>';
	}
	$("#sort1").html(areaCont);
}
intProvince();

/*选择一级目录*/
function selectP(p) {
	areaCont = "";
	for (var j=0; j<city[p].length; j++) {
		areaCont += '<li onClick="selectC(' + p + ',' + j + ');"><a href="javascript:void(0)">' + city[p][j] + '</a></li>';
	}
	$("#sort2").html(areaCont).show();
	$("#sort1 li").eq(p).addClass("active").siblings("li").removeClass("active");
	expressP = province[p];
	$("#selectedSort").html(expressP);
}

/*选择二级目录*/
function selectC(p,c) {
	areaCont = "";
	expressC = "";
	// $("#sort2 li").eq(c).addClass("active").siblings("li").removeClass("active");
	if($("#sort2 li").eq(c).hasClass("active")){
		$("#sort2 li").eq(c).removeClass("active");
	}else{
		$("#sort2 li").eq(c).addClass("active");
	}
	expressC = expressP + arrow + city[p][c];
	$("#selectedSort").html(expressC);
}

