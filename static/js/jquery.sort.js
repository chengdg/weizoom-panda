
/*定义三级分类数据*/
//一级分类
var province = ["教育", "文艺", "青春", "人文社科", "经管", "科技", "电子书"];
//二级分类
var city = [
	["教材", "外语", "考试"],
	["文学", "传记", "艺术", "摄影"],
	["青春文学", "动漫", "幽默"],
	["历史", "文化", "古籍", "心理学", "哲学宗教"],
	["管理", "投资理财", "经济"],
	["科普读物", "建筑", "医学", "计算机网络", "农业林业", "自然科学", "工业技术"],
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
	
	if($("#sort1 li").eq(p).hasClass("active")){
		if(!$('.selectB_'+p+'').hasClass("active")){ //没有二级分类被选中时，不选择一级分类
			$("#sort1 li").eq(p).removeClass("active");
		}
	}
}

/*选择二级目录*/
function selectB(p,c) {
	if($('.selectB_' + p + '_' + c + '').hasClass("active")){
		$('.selectB_' + p + '_' + c + '').removeClass("active");
		$('.selectedSort #'+city[p][c]+'').remove();
		if(!$('.selectB_' + p +'').hasClass("active")){
			$("#sort1 li").eq(p).removeClass("active");//二级类目全部取消了选择，就把一级类目也取消选择
		}
	}else{
		$('.selectB_' + p + '_' + c + '').addClass("active");
		$("#sort1 li").eq(p).addClass("active");
		$('.selectedSort').append('<span class="selectedSortSpan" id='+city[p][c]+'>'+city[p][c]+'</span>');
	}
}

