/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:manager.create_account:AccountCreatePage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');

var GrounpPointsDialog = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},
	
	onChangeStore: function() {
		this.setState(Store.getData());
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		console.log(property, value)
		Action.updateAccount(property, value);
	},

	updateValue: function(index, value, event){
		var property = event.target.getAttribute('name');
		console.log(index,value, property);
		Action.updateRebates(index, property, value);
	},

	deleteSelfShop: function(index){
		Action.deleteSelfShop(index);
	},

	render: function() {
		var SELF_SHOP2TEXT = {
			'weizoom_jia': '微众家',
			'weizoom_mama': '微众妈妈',
			'weizoom_xuesheng': '微众学生',
			'weizoom_baifumei': '微众白富美',
			'weizoom_shop': '微众商城',
			'weizoom_club': '微众俱乐部',
			'weizoom_life': '微众Life',
			'weizoom_yjr': '微众一家人',
			'weizoom_fulilaile': '惠惠来啦'
		}
		var selfUserNames = this.state.self_user_names;
		var _this = this;
		if (selfUserNames.length>0){
			var selfShop = selfUserNames.map(function(selfUser,index){
				var selfUserName = selfUser.self_user_name;
				var userName = SELF_SHOP2TEXT[selfUser.self_user_name];
				return(
						<li key={index} style={{display:'inline-block',position:'relative'}}>
	                        <Reactman.FormInput label={userName} type="text" name={selfUserName+"_value"} onChange={_this.updateValue.bind(_this,index)} value={selfUser[selfUserName+"_value"]}/>
	                    	<span className="rebate-per">%</span>
	                    	<span className="xui-close" onClick={_this.deleteSelfShop.bind(_this,index)} title="删除">x</span>
	                    </li>
					)
			})
			return(
				<div className="self-user-dialog" style={{position:'relative'}}>
					<span style={{position:'absolute',left:'75px'}}>团购扣点</span>
					<ul className="self-user-shop-ul">
						{selfShop}
					</ul>
				</div>
			)
		}else {
			return(
				<div></div>
			)
		}
	}
});
module.exports = GrounpPointsDialog;