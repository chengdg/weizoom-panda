/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.new_product:NewProductPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');
var ProductPreviewDialog = require('./ProductPreviewDialog.react');
var AddProductModelDialog = require('./AddProductModelDialog.react');
var SetValidataTimeDialog = require('./SetValidataTimeDialog.react');
var AddProductCategoryDialog = require('./AddProductCategoryDialog.react');
var NewProductUnPassDialog = require('./NewProductUnPassDialog.react');
var ProductModelInfo = require('./ProductModelInfo.react');
var LimitZoneInfo = require('./LimitZoneInfo.react');
var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');

var NewProductPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		//运营不能编辑
		if(property == 'has_product_model'){
			if(W.role!=3){
				Action.updateProduct(property, value);
			}
		}else if(property == 'limit_zone_type'){
			if(W.role!=3){
				Action.updateProduct(property, value);
			}
		}else if(property == 'images'){
			if(W.role!=3){
				Action.updateProduct(property, value);
			}
		}else if(property == 'has_same_postage'){
			if(W.role!=3){
				Action.updateProduct(property, value);
			}
		}else{
			Action.updateProduct(property, value);
		}
	},

	onChangeStore: function(){
		this.setState(Store.getData());
	},

	productPreview: function(){
		var product = Store.getData();
		var model_values = this.state.model_values;
		var is_true = this.validateProduct();
		var has_product_model = this.state.has_product_model;
		if(product.images.length == 0){
			Reactman.PageAction.showHint('error', '请先上传图片！');
			return;
		}
		if(has_product_model==='0'){
			if(is_true){
				Reactman.PageAction.showHint('error', '请先填写带*的内容！');
				return;
			}
		}else{
			if(has_product_model=='1' && model_values.length==0){
				Reactman.PageAction.showHint('error', '请先添加规格！');
				return;
			}
		}
		Reactman.PageAction.showDialog({
			title: "商品预览",
			component: ProductPreviewDialog,
			data: {
				product: product,
				model_values: model_values
			},
			success: function(inputData, dialogState) {
				console.log("success");
			}
		});
	},

	updateProductCatalog: function(){
		var secondLevelId = 0;
		if(W.second_level_id!=undefined && W.second_level_id!=0){
			//新建商品显示分类
			secondLevelId = this.state.second_id!=0? this.state.second_id: W.second_level_id;
		}else{
			//编辑商品显示分类
			secondLevelId = this.state.second_id!=undefined? this.state.second_id: this.state.old_second_catalog_id;
		}

		Action.ProductCategory(secondLevelId);
		Reactman.PageAction.showDialog({
			title: "请选择商品分类",
			component: AddProductCategoryDialog,
			data: {},
			success: function(inputData, dialogState) {
				console.log("success");
			}
		});
	},
	onClickResubmit: function(event) {
		var title = '确定商品信息已按照驳回原因全部修改完成，再次提交审核？';
		Reactman.PageAction.showConfirm({
			target: event.target, 
			title: title,
			confirm: _.bind(function() {
				this.onSubmit('resubmit');
			}, this)
		});
	},
	onClickUnPass: function(product_id, event) {
		Action.cancleCheckedUnpassReason();
		_.delay(function(){
			Reactman.PageAction.showDialog({
				title: "商品驳回",
				component: NewProductUnPassDialog,
				data: {
					product_id: product_id
				},
				success: function() {
					console.log('success');
				}
			});
		},100)
	},
	validateProduct: function(){
		var is_true = false;
		var product = Store.getData();
		if(!product.hasOwnProperty('product_name') || !product.hasOwnProperty('remark') || !product.hasOwnProperty('product_weight')){
			is_true = true;
		}
		if(product.hasOwnProperty('product_name') && product.product_name.length<=0){
			is_true = true;
		}
		if(product.hasOwnProperty('clear_price') && product.clear_price.length<=0){
			is_true = true;
		}
		if((product.hasOwnProperty('product_weight') && product.product_weight.length<=0) || (product.hasOwnProperty('remark') && product.remark.length<=0)){
			is_true = true;
		}
		return is_true;
	},

	onSubmit: function(resubmit){
		var product = Store.getData();
		if(W.second_level_id!=undefined && W.second_level_id!=0){
			product['second_level_id'] = this.state.second_id!=0? this.state.second_id: W.second_level_id;
		}else{
			product['second_level_id'] = this.state.second_id!=undefined? this.state.second_id: this.state.old_second_catalog_id;
		}

		if(product['second_level_id']==0 || product['second_level_id']==undefined){
			Reactman.PageAction.showHint('error', '请选择商品分类！');
			return;
		}
        if((product['limit_zone_type'] == '1' || product['limit_zone_type'] == '2') && product['limit_zone_id']=='0'){
            Reactman.PageAction.showHint('error', '请选择禁售仅售模板！');
            return
        }
        if(product['limit_zone_type']=='-1'){
            Reactman.PageAction.showHint('error', '请设置商品发货地区设置！');
            return
        }

        if(!this.state.has_postage_config && this.state.has_same_postage=='1'){
        	Reactman.PageAction.showHint('error', '请先前往设置默认运费模板!');
            return;
        }
		var reg =/^\d{0,9}\.{0,1}(\d{1,2})?$/;
		var reg_2 = /^[0-9]+(.[0-9]{1,2})?$/;
		var has_product_model = this.state.has_product_model;

		if(has_product_model===''){
            Reactman.PageAction.showHint('error', '请选择该商品是否多规格!');
            return
        }
		if(has_product_model==='0'){ //不是多规格商品
			if(W.purchase_method==1){
				if(W.role==1){	//固定底价用户默认售价==结算价
					var clear_price = product.clear_price;
					if(clear_price){
						product["product_price"] = clear_price;
					}
				}
			}
			if(product.hasOwnProperty('product_price') && product.product_price.length>0){
				if(!reg_2.test(product.product_price.trim())){
					Reactman.PageAction.showHint('error', '商品售价是数字且保留两位小数,请重新输入!');
					return;
				}
			}
			if(product.hasOwnProperty('product_price') && parseFloat(product.clear_price)>parseFloat(product.product_price)){
				Reactman.PageAction.showHint('error', '结算价不能大于商品售价,请重新输入!');
				return;
			}
		}
		
		if(product.product_name.length > 30 || (product.hasOwnProperty('promotion_title') && product.promotion_title.length > 30)){
			Reactman.PageAction.showHint('error', '商品名称或促销标题最多输入30个字,请重新输入!');
			return;
		}
		if(product.images.length == 0){
			Reactman.PageAction.showHint('error', '请先上传图片！');
			return ;
		}

		if(product.product_store>99999){
			Reactman.PageAction.showHint('error', '库存最多输入99999,请重新输入!');
			return ;
		}

		var model_values = this.state.model_values;
		product['has_product_model'] = this.state.has_product_model;
		if(has_product_model==='1' && model_values.length==0){
			Reactman.PageAction.showHint('error', '请添加商品规格！');
			return ;
		}

		var is_true = false;
		if(has_product_model==='1'){
			_.each(model_values, function(model) {
				if(W.purchase_method==2) {
					var product_price = product['product_price_'+model.modelId];
					if(product_price){
						var points = 1-(W.points/100);
						var product_price = parseFloat(product_price);
						var clear_price= (Math.round((points*product_price*100).toFixed(2))/100).toFixed(2);
					}
				}else if(W.purchase_method==1 && W.role == 3) { //运营修改固定底价用户时候才校验
					// var product_price = product['product_price_'+model.modelId];
					// var clear_price = product['clear_price_'+model.modelId];
					// if(parseFloat(clear_price) > parseFloat(product_price)){
					// 	is_true = true;
					// 	Reactman.PageAction.showHint('error', '结算价不能大于商品售价,请重新输入!');
					// 	return;
					// }
				}

				if(product['product_store_'+model.modelId]>99999) {
					is_true = true;
					Reactman.PageAction.showHint('error', '库存最多输入99999,请重新输入!');
					return;
				}
			})
		}
		if(is_true){
			return false;
		}

		_.each(model_values, function(model) {
			model['product_price_'+model.modelId] = product['product_price_'+model.modelId]
			model['limit_clear_price_'+model.modelId] = product['limit_clear_price_'+model.modelId]
			model['clear_price_'+model.modelId] = product['clear_price_'+model.modelId]
			model['product_weight_'+model.modelId] = product['product_weight_'+model.modelId]
			model['product_store_'+model.modelId] = product['product_store_'+model.modelId]
			if(W.purchase_method==1){
				if(W.role==1){ //固定底价用户默认售价==结算价
					var clear_price = parseFloat(product["clear_price_"+model.modelId]);
					if(clear_price){
						model["product_price_"+model.modelId] = clear_price;
					}
				}
			}
		})

		model_values = model_values.length>0?JSON.stringify(model_values):'';
		//是否是重新提交审核的
		if(typeof(resubmit)=='string'){
			product['resubmit'] = resubmit;
		}else{
			product['resubmit'] = '';
		}
		Action.saveNewProduct(product, model_values);
	},

	render:function(){
		var catalogName = W.catalogName;
		if(this.state.catalog_name.length>0){
			catalogName = this.state.catalog_name;
		}

		var optionsForStore = [{text: '无限', value: '-1'}, {text: '有限', value: '0'}];
		var optionsForModel = [{text: '是', value: '1'}, {text: '否', value: '0'}];
		var optionsForCheckbox = [{text: '', value: '1'}]
		var role = W.role;
		var disabled = role == 3 ? 'disabled' : '';
		var style = (role == 3 && W.purchase_method != 1) ? {margin: '20px 0px 100px 180px'}: {position:'absolute',top:'40px',left:'270px'};
		var reject_style = (role == 3 && W.purchase_method != 1) ? {margin: '20px 0px 100px 0px'}: {position:'absolute',top:'40px',left:'380px'};
		var optionsForKind = [{
            text: '',
            value: '-1'
        },{
            text: '无限制',
            value: '0'
        }, {
            text: '仅发货地区',
            value: '2'
        },{
            text: '不发货地区',
            value: '1'
        }];

        var postageName = this.state.postage_name;
       	var hasPostageConfig = this.state.has_postage_config;
       	var textPostage = hasPostageConfig? '使用默认运费模板：'+ postageName: '使用默认运费模板'

        var optionsForPostage = [{
        	text: '统一运费',
            value: '0'
        },{
        	text: textPostage,
            value: '1'
        }]
        var optionsForLimitInfo = this.state.limit_zone_info;
        //固定底价类型客户-商品结算价提示
        var tipsOfPrice = (role==1 && W.purchase_method==1)? '提示：结算价为商品与微众的结算价格，如无扣点约定，可与售价相同': ''
       	
		return (
			<div className="xui-newProduct-page xui-formPage">
				<form className="form-horizontal mt15">
					<fieldset>
						<div className="preview-btn"><a href='javascript:void(0);' onClick={this.productPreview}>商品预览</a></div>
					</fieldset>
					<fieldset>
						<legend className="pl10 pt10 pb10">基本信息</legend>
						<span className="form-group ml15">
							<label className="col-sm-2 control-label pr0">商品类目:</label>
							<span className="xui-catalog-name">{catalogName}</span>
							<a className="ml10" href="javascript:void(0);" onClick={this.updateProductCatalog}>修改</a>
						</span>
						<Reactman.FormInput label="商品名称:" type="text"  name="product_name" value={this.state.product_name} onChange={this.onChange} validate="require-string" placeholder="最多30个字" />
						<Reactman.FormInput label="促销标题:" type="text" readonly={disabled} name="promotion_title" value={this.state.promotion_title} placeholder="最多30个字" onChange={this.onChange} />
						<Reactman.FormRadio label="多规格商品:" type="text" validate="require-string" name="has_product_model" value={this.state.has_product_model} options={optionsForModel} onChange={this.onChange} />
						<div> <ProductModelInfo Disabled={disabled} onChange={this.onChange} Modeltype={this.state.has_product_model}/> </div>	
                        <Reactman.FormSelect validate="require" label="发货地区设置:"  name="limit_zone_type" value={this.state.limit_zone_type} options={optionsForKind }  onChange={this.onChange}/>
                        <div> <LimitZoneInfo onChange={this.onChange}/></div>
						<Reactman.FormRadio label="运费:" type="text" name="has_same_postage" value={this.state.has_same_postage} options={optionsForPostage} onChange={this.onChange} />
						
						<div> <PostageTemplate onChange={this.onChange} hasSamePostage={this.state.has_same_postage} postageMoney={this.state.postage_money} hasPostageConfig={this.state.has_postage_config} /></div>
						
						
						<Reactman.FormImageUploader label="商品图片:" name="images" value={this.state.images} onChange={this.onChange} validate="require-string"/>
						<div style={{paddingLeft:'180px', color:'rgba(138, 43, 43, 0.82)', marginTop:'-15px'}}>提示：商品轮播图最多6张，200KB以内，建议640-960之间的正方形图片，web格式图片</div>
						
						<div style={{paddingLeft:'180px', color:'rgba(138, 43, 43, 0.82)', marginTop:'20px'}}>提示：商品描述的图片宽度640-960px之间，高度建议小于500px，大小300KB以内，web格式图片</div>
						<Reactman.FormRichTextInput label="商品描述:" name="remark" value={this.state.remark} width="1260" height="600" onChange={this.onChange} validate="require-notempty"/>
					</fieldset>
					<fieldset style={{position:'relative'}}>
						{role == 3 ? '' : <Reactman.FormSubmit onClick={this.onSubmit} />}
						{role == 3 && W.purchase_method ==1 ? <Reactman.FormSubmit onClick={this.onSubmit} /> : ''}
						<a className="btn btn-success mr40 xa-submit xui-fontBold" href="javascript:void(0);" style={style} onClick={this.productPreview}>商品预览</a>
						{role == 1 && W.product_status_value == 3 ? <a className="btn btn-success mr40 xa-submit xui-fontBold" href="javascript:void(0);" style={reject_style} onClick={this.onClickResubmit}>重新提交审核</a> : ''}
						{role == 3 && W.product_status_value == 0 ? <a className="btn btn-success mr40 xa-submit xui-fontBold" href="javascript:void(0);" style={reject_style} onClick={this.onClickUnPass.bind(this,this.state.id)}>驳回修改</a> : ''}
					</fieldset>
				</form>
			</div>
		)
	}
})

var PostageTemplate = React.createClass({
	render: function() {
		var hasSamePostage = this.props.hasSamePostage;
		var hasPostageConfig = this.props.hasPostageConfig;

		if (hasSamePostage == '0'){
			return(
				<div>
					<Reactman.FormInput label="运费金额(元)" type="text" name="postage_money" value={this.props.postageMoney} validate="require-float" onChange={this.props.onChange} />
				</div>
			)
		}else {
			if(hasPostageConfig){
				return(
					<div className="mb10" style={{paddingLeft:'180px'}}>
						<span>提示：需要更换模板，请前往 <a href="/postage_config/postage_list/">运费模板</a> 列表中将需要的模板设置为默认模板即可。</span>
					</div>
				)
			}else{
				return(
					<div className="mb10" style={{paddingLeft:'180px'}}>
						<span>暂未添加任何默认运费模板,请前往<a href="/postage_config/postage_list/">运费模板</a> 列表中添加默认模板。</span>
					</div>
				)
			}
			
		}
	}
});

module.exports = NewProductPage;