/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:postage_config.new_config:FreePostagePage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var FreePostageStore = require('./FreePostageStore');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');
var W = Reactman.W;

var FreePostagePage = React.createClass({
	getInitialState: function() {
		FreePostageStore.addListener(this.onChangeStore);
		return FreePostageStore.getData();
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateProduct(property, value);
	},

	onChangeStore: function(){
		this.setState(FreePostageStore.getData());
	},

	addSpecialPostage: function() {
		Action.addSpecialPostage();
	},

	deleteSpecialPostage: function(index) {
		Action.deleteSpecialPostage(index);
	},

	onSelectArea:function(selectedIds, selectedDatas, event) {
        if(selectedIds.length == 0){
            Reactman.PageAction.showHint('error', '您需要选择地区！');
            return;
        }

        // Action.updateLimitZoneTemplateInfo(selectedDatas, selectedIds, event);
	},

	render:function(){
		var optionsForPostage = [{
			text: '特殊包邮条件',
			value: '1'
		}];

		var _this = this;
		var freePostages = this.state.freePostages;
		console.log(freePostages,"========");
		var postagesTr = freePostages.map(function(postages, index){
			return(
				<tr key={index}>
					<td>
						<Reactman.ProvinceCitySelect onSelect={_this.onSelectArea} initSelectedIds={[]} resource="product.provinces_cities" >设置区域</Reactman.ProvinceCitySelect>
					</td>
					<td>
						<Reactman.FormInput label="" type="text" name="first_weight_price" value={postages.first_weight_price} onChange={_this.onChange} />
					</td>
					<td>
						<Reactman.FormInput label="" type="text" name="added_weight" value={postages.added_weight} onChange={_this.onChange} />
					</td>
					<td>
						<a href="javascript:void(0);" onClick={_this.deleteSpecialPostage.bind(_this, index)}>删除</a>
					</td>
				</tr>
			)
		});

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
						{postagesTr}
					</tbody>
				</table>
			</div>
		)
	}
})

module.exports = FreePostagePage;