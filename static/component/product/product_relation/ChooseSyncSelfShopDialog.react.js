/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');

var ChooseSyncSelfShopDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return {
			'selectSelfShop': Store.getData()['selectSelfShop'],
			'selfShop': Store.getData()['selfShop']
		}
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.addProductModelValue(property, value);
	},

	onChangeStore: function(){
		console.log(Store.getData());
		this.setState({
			'selectSelfShop': Store.getData()['selectSelfShop'],
			'selfShop': Store.getData()['selfShop'],
			'product_info': Store.getData()['product_info']
		});
	},

	ChooseSelfShop: function(value){
		Action.chooseSelfShop(value);
	},

	cancleChecked: function(product_id){
		var selectSelfShop = this.state.selectSelfShop;
		var _this = this;
		if (selectSelfShop.length==0){
			Reactman.PageAction.showHint('error', '请选择要取消同步的商城！');
			return;
		}
		Action.cancleChecked(product_id,selectSelfShop.join(','));
		_.delay(function(){
			_this.closeDialog();
		},500)
	},

	chooseAllSelfShop: function(){
		Action.chooseAllSelfShop();
	},

	productRelation: function(product_id) {
		var _this = this;
		var selectSelfShop = this.state.selectSelfShop;
		var product_info = this.state.product_info;
		if (selectSelfShop.length==0){
			Reactman.PageAction.showHint('error', '请选择要同步的商城！');
			return;
		}
		console.log(selectSelfShop.join(','),"========");
		var product_data = [{
			'weizoom_self': selectSelfShop.join(','),//选择的商城
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
		_.delay(function(){
			_this.closeDialog();
		},500)
	},

	render: function(){
		var _this = this;
		var product_id = this.props.data.product_id;
		var selfShop = this.state.selfShop;
		console.log(this.state['selfShop'],"======")
		var selectSelfShop = this.state.selectSelfShop.toString();

		var selfs = selfShop.map(function(self_shop,index){
			var value = self_shop.value;
			var bg_style = {};
			bg_style['style'] = {};
			if(selectSelfShop.indexOf(value) >-1){
				bg_style['style'] = {background: '#009DD9', color:'#FFF'};
			}
			return(
				<li key={index} style={bg_style['style']} className="self-shop-li" onClick={_this.ChooseSelfShop.bind(_this,value)}>{self_shop.name}</li>
			)
		})
		var checked = this.state.selectSelfShop.length==9?'checked':null;
		return (
			<div className="xui-formPage">
				<ul>
					{selfs}
				</ul>
				<span style={{display:'block',paddingLeft:'50px'}}>
					<input type="checkbox" checked={checked} className="checkbox" name="select" value="0" style={{display:'inline-block'}} onChange={this.chooseAllSelfShop}/>全选
				</span>
				<span className='cancle-relation-tips' style={{display:'none'}}>( 提示：取消平台勾选，商品将从该平台禁售不可见 )</span>	
				<a href="javascript:void(0);" className="btn btn-success" style={{marginLeft:'190px'}} onClick={this.productRelation.bind(this,product_id)}><span>确定同步</span></a>
				<a href="javascript:void(0);" className="btn btn-success" style={{marginLeft:'50px',display:'none'}} onClick={this.cancleChecked.bind(this,product_id)}><span>取消同步</span></a>
			</div>
		)
	}
})
module.exports = ChooseSyncSelfShopDialog;