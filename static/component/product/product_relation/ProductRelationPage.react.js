/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product.product_relation:ProductRelationPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');
var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var ChooseSyncSelfShopDialog = require('./ChooseSyncSelfShopDialog.react');

var ProductRelationPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return ({});
	},

	onChangeStore: function(event) {
		var _this = this;
		var filterOptions = Store.getFilter();
		var hasProp = false;  
		for (var prop in filterOptions){  
			hasProp = true;  
			break;  
		}
		if (hasProp){  
			this.refs.table.refresh(filterOptions);  
		}else{
			this.setState(Store.getData());
		}	
	},

	cancleChecked: function(product_id, self_name){
		console.log(product_id,self_name,"======");
		Action.cancleChecked(product_id,self_name);
	},

	productRelation: function(self_user_name, product_info) {
		var product_id = product_info['product_id']
		var obj = document.getElementById(product_id);
		obj = obj.getElementsByTagName('input');
		var check_val = [];
		for(var k=0; k<=obj.length-1; k++){
			var has_relation = true;
			if(obj[k]['checked']){
				check_val.push(obj[k].value);
			}
		}

		if (check_val.length==0){
			Reactman.PageAction.showHint('error', '请选择要同步的商城！');
			return;
		}
		var product_data = [{
			'weizoom_self': check_val.join(','),//选择的商城
			'product_id': product_id,//商品id
			'account_id': product_info['account_id'], //所属账号 id
			'product_price': product_info['product_price'],
			'product_name': product_info['product_name'],//商品名称
			'clear_price': product_info['clear_price'],//商品结算价
			'product_weight': product_info['product_weight'],//商品重量
			'product_store': product_info['product_store'],//商品库存(-1:无限)
			'image_path': product_info['image_path'],//轮播图路径
			'promotion_title': product_info['promotion_title'],
			'detail': product_info['remark']//商品详情
		}]
		Action.relationFromWeapp(JSON.stringify(product_data));
	},

	ChooseSyncSelfShop: function(product_id){
		Action.getHasSyncShop(product_id);
		Reactman.PageAction.showDialog({
			title: "选择平台进行同步商品",
			component: ChooseSyncSelfShopDialog,
			data: {
				product_id:product_id
			},
			success: function(inputData, dialogState) {
				console.log("success");
			}
		});
	},

	rowFormatter: function(field, value, data) {
		if (field === 'weapp_name') {
			var id = data['id'];
			var selfUserName = data['self_user_name'].toString();
			var wBChecked = selfUserName.indexOf('weizoom_baifumei')>-1?'checked':null;
			var wCChecked = selfUserName.indexOf('weizoom_club')>-1?'checked':null;
			var wJChecked = selfUserName.indexOf('weizoom_jia')>-1?'checked':null;
			var wMChecked = selfUserName.indexOf('weizoom_mama')>-1?'checked':null;
			var wSChecked = selfUserName.indexOf('weizoom_shop')>-1?'checked':null;
			var wXChecked = selfUserName.indexOf('weizoom_xuesheng')>-1?'checked':null;
			var wLChecked = selfUserName.indexOf('weizoom_life')>-1?'checked':null;
			var wYChecked = selfUserName.indexOf('weizoom_yjr')>-1?'checked':null;
			var wFChecked = selfUserName.indexOf('weizoom_fulilaile')>-1?'checked':null;
			
			return (
				<div id={id}>
					<label className="checkbox-inline" style={{marginRight:'15px',marginLeft:'10px',width:'90px'}}>
						<input type="checkbox" checked={wBChecked} className="checkbox" name={"weizoom_self_"+id} value="weizoom_baifumei" onChange={this.cancleChecked.bind(this,id,'weizoom_baifumei')} />;
						<span>微众白富美</span>
					</label>
					<label className="checkbox-inline" style={{marginRight:'15px',width:'90px'}}>
						<input type="checkbox" checked={wCChecked} className="checkbox" name={"weizoom_self_"+id} value="weizoom_club" onChange={this.cancleChecked.bind(this,id,'weizoom_club')} />
						<span>微众俱乐部</span>
					</label>
					<label className="checkbox-inline" style={{marginRight:'15px',width:'90px'}}>
						<input type="checkbox" checked={wJChecked} className="checkbox" name={"weizoom_self_"+id} value="weizoom_jia" onChange={this.cancleChecked.bind(this,id,'weizoom_jia')} />
						<span>微众家</span>
					</label>
					<label className="checkbox-inline" style={{marginRight:'15px',width:'90px'}}>
						<input type="checkbox" checked={wMChecked} className="checkbox" name={"weizoom_self_"+id} value="weizoom_mama" onChange={this.cancleChecked.bind(this,id,'weizoom_mama')} />
						<span>微众妈妈</span>
					</label>
					<label className="checkbox-inline" style={{marginRight:'15px',width:'90px'}}>
						<input type="checkbox" checked={wSChecked} className="checkbox" name={"weizoom_self_"+id} value="weizoom_shop" onChange={this.cancleChecked.bind(this,id,'weizoom_shop')} />
						<span>微众商城</span>
					</label>
					<label className="checkbox-inline" style={{marginRight:'15px',width:'90px'}}>
						<input type="checkbox" checked={wXChecked} className="checkbox" name={"weizoom_self_"+id} value="weizoom_xuesheng" onChange={this.cancleChecked.bind(this,id,'weizoom_xuesheng')} />
						<span>微众学生</span>
					</label>
					<label className="checkbox-inline" style={{marginRight:'15px',width:'90px'}}>
						<input type="checkbox" checked={wLChecked} className="checkbox" name={"weizoom_self_"+id} value="weizoom_life" onChange={this.cancleChecked.bind(this,id,'weizoom_life')} />
						<span>微众Life</span>
					</label>
					<label className="checkbox-inline" style={{marginRight:'15px',width:'90px'}}>
						<input type="checkbox" checked={wYChecked} className="checkbox" name={"weizoom_self_"+id} value="weizoom_yjr" onChange={this.cancleChecked.bind(this,id,'weizoom_yjr')} />
						<span>微众一家人</span>
					</label>
					<label className="checkbox-inline" style={{marginRight:'15px',width:'90px'}}>
						<input type="checkbox" checked={wFChecked} className="checkbox" name={"weizoom_self_"+id}	 value="weizoom_fulilaile" onChange={this.cancleChecked.bind(this,id,'weizoom_fulilaile')} />
						<span>惠惠来啦</span>
					</label>
					<a className="btn btn-link btn-xs" style={{color:'#1ab394'}} onClick={this.productRelation.bind(this,data['self_user_name'],data['product_info'])}>同步</a>
				</div>
			);
		}else if(field === 'product_name'){
			return(
				<a className="btn btn-link btn-xs" href={'/product/new_product/?id='+data.id}>{value}</a>
			)
		} else if(field === 'action'){
			return(
				<a className="btn btn-link btn-xs" onClick={this.ChooseSyncSelfShop.bind(this,data['id'])}>同步商品</a>
			)
		}else {
			return value;
		}
	},

	onConfirmFilter: function(data){
		Action.filterDates(data);
	},

	render:function(){
		var productsResource = {
			resource: 'product.product_relation',
			data: {
				page: 1,
				first_catalog_id: W.first_catalog_id,
				second_catalog_id: W.second_catalog_id
			}
		};

		return (
			<div className="mt15 xui-product-productListPage">
				<Reactman.FilterPanel onConfirm={this.onConfirmFilter}>
					<Reactman.FilterRow>
						<Reactman.FilterField>
							<Reactman.FormInput label="客户名称:" name="customer_name_query" match='=' />
						</Reactman.FilterField>
						<Reactman.FilterField>
							<Reactman.FormInput label="商品名称:" name="product_name_query" match="=" />
						</Reactman.FilterField>
					</Reactman.FilterRow>
				</Reactman.FilterPanel>
				<Reactman.TablePanel>
					<Reactman.TableActionBar></Reactman.TableActionBar>
					<Reactman.Table resource={productsResource} formatter={this.rowFormatter} pagination={true} expandRow={true} ref="table">
						<Reactman.TableColumn name="商品名称" field="product_name" />
						<Reactman.TableColumn name="客户名称" field="customer_name" />
						<Reactman.TableColumn name="总销量" field="total_sales" />
						<Reactman.TableColumn name="操作" field="action" />
					</Reactman.Table>
				</Reactman.TablePanel>
			</div>
		)
	}
})
module.exports = ProductRelationPage;