/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:postage_config.new_config:NewConfigPage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');
var W = Reactman.W;

var NewConfigPage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return ({});
	},

	onChangeStore: function() {
		this.setState(Store.getData());
		var filterOptions = Store.getData();
		this.refs.table.refresh(filterOptions);
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateProduct(property, value);
	},

	addPostageTemplate: function(){
		W.gotoPage('/postage_config/new_config/');
	},

	render:function(){
		return (
			<div>
				<div className="xui-formPage">
					<form className="form-horizontal mt15 pt30">
						<Reactman.FormInput label="模板名称:" type="text" name="product_name" value={this.state.product_name} onChange={this.onChange} placeholder="最多30个字" />
						<div className="pl90">运送方式：除特殊地区外，其余地区的运费采用“默认运费”</div>
					</form>
				</div>
				<div className="mt15 xui-postageConfig-postageListPage">
					<DefaultPostagePage />
					<SpecialPostagePage />
					<FreePostagePage />
				</div>
			</div>
		)
	}
});

var DefaultPostagePage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return ({});
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateProduct(property, value);
	},

	render:function(){
		return (
			<div className="form-horizontal mt15 pt20 pl90">
				<div>默认运费</div>
				<table className="table table-bordered" style={{width:'60%'}}>
					<thead>
						<tr>
							<th>首重(kg)</th>
							<th>运费(元)</th>
							<th>续重(kg)</th>
							<th>续费(kg)</th>
							<th>操作</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>
								<Reactman.FormInput label="" type="text" name="first_weight" value={this.state.first_weight} onChange={this.state.onChange} />
							</td>
							<td>
								<Reactman.FormInput label="" type="text" name="first_weight_price" value={this.state.first_weight_price} onChange={this.state.onChange} />
							</td>
							<td>
								<Reactman.FormInput label="" type="text" name="added_weight" value={this.state.added_weight} onChange={this.state.onChange} />
							</td>
							<td>
								<Reactman.FormInput label="" type="text" name="added_weight_price" value={this.state.added_weight_price} onChange={this.state.onChange}/>
							</td>
							<td>
								<a>删除</a>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
		)
	}
})

var SpecialPostagePage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateProduct(property, value);
	},

	render:function(){
		var optionsForPostage = [{
			text: '特殊地区运费设置',
			value: '1'
		}];
		return (
			<div className="form-horizontal mt15 pt20 pl90">
				<div className="xui-special-postage">
					<Reactman.FormCheckbox label="" name="hasSpecialPostage" value={this.state.hasSpecialPostage} options={optionsForPostage} onChange={this.onChange} />
				</div>
				<table className="table table-bordered" style={{width:'80%'}}>
					<thead>
						<tr>
							<th>地区</th>
							<th>首重(kg)</th>
							<th>运费(元)</th>
							<th>续重(kg)</th>
							<th>续费(kg)</th>
							<th>操作</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>
								设置地区
							</td>
							<td>
								<Reactman.FormInput label="" type="text" name="first_weight" value={this.state.first_weight} onChange={this.state.onChange} />
							</td>
							<td>
								<Reactman.FormInput label="" type="text" name="first_weight_price" value={this.state.first_weight_price} onChange={this.state.onChange} />
							</td>
							<td>
								<Reactman.FormInput label="" type="text" name="added_weight" value={this.state.added_weight} onChange={this.state.onChange} />
							</td>
							<td>
								<Reactman.FormInput label="" type="text" name="added_weight_price" value={this.state.added_weight_price} onChange={this.state.onChange}/>
							</td>
							<td>
								<a>删除</a>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
		)
	}
})

var FreePostagePage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateProduct(property, value);
	},

	render:function(){
		var optionsForPostage = [{
			text: '特殊包邮条件',
			value: '1'
		}];

		return (
			<div className="form-horizontal mt15 pt20 pl90">
				<div className="xui-special-postage">
					<Reactman.FormCheckbox label="" name="hasFreePostage" value={this.state.hasFreePostage} options={optionsForPostage} onChange={this.onChange} />
				</div>
				<table className="table table-bordered" style={{width:'60%'}}>
					<thead>
						<tr>
							<th>地区</th>
							<th>件数/金额</th>
							<th>门槛条件</th>
							<th>操作</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>
								设置地区
							</td>
							<td>
								<Reactman.FormInput label="" type="text" name="first_weight_price" value={this.state.first_weight_price} onChange={this.state.onChange} />
							</td>
							<td>
								<Reactman.FormInput label="" type="text" name="added_weight" value={this.state.added_weight} onChange={this.state.onChange} />
							</td>
							<td>
								<a>删除</a>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
		)
	}
})

module.exports = NewConfigPage;