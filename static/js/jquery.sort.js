
/*商家入驻、入驻类目/特殊资质提交*/
//一级分类
var first_catalog = [];
var second_catalog = [];
var expressP, expressC, expressArea, areaCont;
var arrow = '_';

$.ajax({
    url:'/business/api/customer_apply/',
    type:'get',
    success:function(resp){
        console.log(resp);
		first_catalog = resp['data']['first_catalog'];
		second_catalog = resp['data']['second_catalog']

		/*初始化一级目录*/
		function initFirstCatalog() {
			areaCont = "";
			expressC = '';
			for (var i=0; i<first_catalog.length; i++) {
				areaCont += '<li onClick="selectA(' + i + ');"><a href="javascript:void(0)">' + first_catalog[i] + '</a></li>';
				for (var j=0; j<second_catalog[i].length; j++) {
					expressC += '<li class="selectB_'+i+' hide selectB_' + i + '_' + j + '" onClick="selectB(' + i + ',' + j + ');"><a href="javascript:void(0)">' + second_catalog[i][j] + '</a></li>';
				}
				$("#sort2").html(expressC)
			}
			$("#sort1").html(areaCont);
		}
		initFirstCatalog();
    },
    error:function(){
        console.log('222222222');
    }
});
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
		$('.selectedSort #'+second_catalog[p][c]+'').remove();
		if(!$('.selectB_' + p +'').hasClass("active")){
			$("#sort1 li").eq(p).removeClass("active");//二级类目全部取消了选择，就把一级类目也取消选择
		}
	}else{
		$('.selectB_' + p + '_' + c + '').addClass("active");
		$("#sort1 li").eq(p).addClass("active");
		$('.selectedSort').append('<span class="selectedSortSpan" id='+second_catalog[p][c]+'>'+second_catalog[p][c]+'</span>');
	}
}