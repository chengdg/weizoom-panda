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
		var selfShop = [{
			'name': '微众白富美',
			'value': 'weizoom_baifumei'
		},{
			'name': '微众俱乐部',
			'value': 'weizoom_club'
		},{
			'name': '微众家',
			'value': 'weizoom_jia'
		},{
			'name': '微众妈妈',
			'value': 'weizoom_mama'
		},{
			'name': '微众商城',
			'value': 'weizoom_shop'
		},{
			'name': '微众学生',
			'value': 'weizoom_xuesheng'
		},{
			'name': '微众Life',
			'value': 'weizoom_life'
		},{
			'name': '微众一家人',
			'value': 'weizoom_yjr'
		},{
			'name': '惠惠来啦',
			'value': 'weizoom_fulilaile'
		},{
			'name': '居委汇',
			'value': 'weizoom_juweihui'
		},{
			'name': '微众中海',
			'value': 'weizoom_zhonghai'
		}];
		return {
			select_self_shop: Store.getData()['selectSelfShop'],
			self_shop: selfShop
		}
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.addProductModelValue(property, value);
	},

	onChangeStore: function(){
		this.setState({
			select_self_shop: Store.getData()['selectSelfShop']
			// product_info: Store.getData()['product_info']
		});
	},

	ChooseSelfShop: function(value){
		Action.chooseSelfShop(value);
	},

	cancleChecked: function(product_id){
		var selectSelfShop = this.state.select_self_shop;
		var _this = this;

		if (selectSelfShop.length==0){
			Reactman.PageAction.showHint('error', '请选择要取消同步的商城！');
			return;
		}

		Action.cancleChecked(product_id,selectSelfShop.join(','));
	},

	chooseAllSelfShop: function(){
		Action.chooseAllSelfShop();
	},

	productRelation: function(product_ids,sync_type) {
		var _this = this;
		var selectSelfShop = this.state.select_self_shop;
		// var productInfo = this.state.product_info;
		if (selectSelfShop.length==0){
			Reactman.PageAction.showHint('error', '请选择要同步的商城！');
			return;
		}
		console.log(sync_type,selectSelfShop,"------");
		var product_data = [{
			'weizoom_self': selectSelfShop.join(','),//选择的商城
			'product_ids': product_ids,//商品id
			'sync_type': sync_type
			// 'account_id': productInfo['account_id'] //所属账号 id
		}]
		Action.relationFromWeapp(JSON.stringify(product_data));
	},

	render: function(){
		var _this = this;
		var productId = this.props.data.product_id;
		var syncType = this.props.data.sync_type;
		var selfShop = this.state.self_shop;
		var selectSelfShop = this.state.select_self_shop.toString();
		var checked = this.state.select_self_shop.length==11?'checked':null;

		var selfs = selfShop.map(function(self_shop,index){
			var value = self_shop.value;
			var bgStyle = {};
			bgStyle['style'] = {};
			if(selectSelfShop.indexOf(value) >-1){
				bgStyle['style'] = {background: '#009DD9', color:'#FFF'};
			}
			return(
				<li key={index} style={bgStyle['style']} className="self-shop-li" onClick={_this.ChooseSelfShop.bind(_this,value)}>{self_shop.name}</li>
			)
		})

		return (
			<div className="xui-formPage">
				<ul>
					{selfs}
				</ul>
				<span style={{display:'block',paddingLeft:'50px'}}>
					<input type="checkbox" checked={checked} className="checkbox" name="select" value="0" style={{display:'inline-block'}} onChange={this.chooseAllSelfShop}/>全选
				</span>
				<span className='cancle-relation-tips' style={{display:'none'}}>( 提示：取消平台勾选，商品将从该平台禁售不可见 )</span>	
				<a href="javascript:void(0);" className="btn btn-success" style={{marginLeft:'190px'}} onClick={this.productRelation.bind(this,productId,syncType)}><span>确定同步</span></a>
				<a href="javascript:void(0);" className="btn btn-success" style={{marginLeft:'50px',display:'none'}} onClick={this.cancleChecked.bind(this,productId,syncType)}><span>取消同步</span></a>
			</div>
		)
	}
})
module.exports = ChooseSyncSelfShopDialog;