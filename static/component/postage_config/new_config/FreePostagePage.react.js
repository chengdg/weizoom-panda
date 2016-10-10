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
		Action.updateFreePostages(property, value);
	},

	onChangePostage: function(index, event) {
		var property = event.target.getAttribute('name');
		var value = event.target.value;
		Action.updateFreeValues(property, value, index);
	},

	onChangeStore: function(){
		this.setState(FreePostageStore.getData());
	},

	onChangeCondition: function(condition, index){
		Action.updateCondition(condition, index);
	},

	addFreePostage: function() {
		Action.addFreePostage();
	},

	deleteFreePostage: function(index) {
		Action.deleteFreePostage(index);
	},

	onSelectArea:function(index, selectedIds, selectedDatas) {
       if(selectedIds==undefined){
			return;
		}
        if(selectedIds.length == 0){
            Reactman.PageAction.showHint('error', '您需要选择地区！');
            return;
        }
        Action.updateFreeArea(selectedIds, index);
	},

	render:function(){
		var _this = this;
		var freePostages = this.state.freePostages;
		var optionsForFreeCondition = [{
			text: '件数',
			value: 'count'
		},{
			text: '金额',
			value: 'money'
		}];

		var postagesTr = freePostages.map(function(postages, index){
			var condition = postages.condition;
			var unit = condition == 'count'? '件': '元';

			return(
				<tr key={index}>
					<td>
						<Reactman.ProvinceCitySelect onSelect={_this.onSelectArea.bind(_this, index)} initSelectedIds={postages.selectedIds} resource="product.provinces_cities" >设置区域</Reactman.ProvinceCitySelect>
					</td>
					<td>
						<Reactman.FormSelect label="" name="condition" value={postages.condition} options={optionsForFreeCondition} onChange={_this.onChangeCondition.bind(_this, condition, index)} />
					</td>
					<td>
						<input type="text" className="form-control" id="conditionValue" name="conditionValue" value={postages.conditionValue} onChange={_this.onChangePostage.bind(_this, index)} style={{width:'80%', display:'inline-block'}}/>
						<span>{unit}</span>
					</td>
					<td>
						<a href="javascript:void(0);" onClick={_this.deleteFreePostage.bind(_this, index)}>删除</a>
					</td>
				</tr>
			)
		});

		var optionsForPostage = [{
			text: '特殊包邮条件',
			value: '1'
		}];

		return (
			<div className="form-horizontal mt15 pt20 pl90">
				<div className="xui-free-postage">
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
				<div className="xui-free-postage">
					<a href="javascript:void(0);" onClick={this.addFreePostage}>继续添加</a>
				</div>
			</div>
		)
	}
})

module.exports = FreePostagePage;