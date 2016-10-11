/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:postage_config.new_config:SpecialPostagePage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var SpecialPostageStore = require('./SpecialPostageStore');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');
var W = Reactman.W;

var SpecialPostagePage = React.createClass({
	getInitialState: function() {
		SpecialPostageStore.addListener(this.onChangeStore);
		return SpecialPostageStore.getData();
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateSpecialPostages(property, value);
	},

	onChangeStore: function(){
		this.setState(SpecialPostageStore.getData());
	},

	onChangeValue: function(index, value, event){
		var property = event.target.getAttribute('name');
		Action.updateSpecialValues(index, property, value);
	},

	addSpecialPostage: function() {
		Action.addSpecialPostage();
	},

	deleteSpecialPostage: function(index) {
		Action.deleteSpecialPostage(index);
	},

	onSelectArea:function(index, selectedIds, selectedDatas) {
		if(selectedIds==undefined){
			return;
		}
        if(selectedIds.length == 0){
            Reactman.PageAction.showHint('error', '您需要选择地区！');
            return;
        }
        Action.updateSpecialArea(selectedIds, index);
	},

	render:function(){
		var _this = this;
		var specialPostages = this.state.specialPostages;
		var provinceId2name = this.state.provinceId2name;

		var optionsForPostage = [{
			text: '特殊地区运费设置',
			value: '1'
		}];

		var postagesTr = specialPostages.map(function(postages, index){
			var destinationText = []
			var selectedIds = postages.selectedIds;

			for(var i in selectedIds){
				var id = parseInt(selectedIds[i]);
				destinationText.push(provinceId2name[id])
			}
			destinationText = destinationText.join('；');

			return(
				<tr key={index}>
					<td className="xui-destination">
						<span className="mr10" style={{color:'#000'}}>{destinationText}</span>
						<Reactman.ProvinceCitySelect onSelect={_this.onSelectArea.bind(_this, index)} initSelectedIds={postages.selectedIds} resource="postage_config.provinces_cities" >设置区域</Reactman.ProvinceCitySelect>
					</td>
					<td>
						<Reactman.FormInput label="" type="text" name="firstWeight" value={postages.firstWeight} onChange={_this.onChangeValue.bind(_this,index)} />
					</td>
					<td>
						<Reactman.FormInput label="" type="text" name="firstWeightPrice" value={postages.firstWeightPrice} onChange={_this.onChangeValue.bind(_this,index)} />
					</td>
					<td>
						<Reactman.FormInput label="" type="text" name="addedWeight" value={postages.addedWeight} onChange={_this.onChangeValue.bind(_this,index)} />
					</td>
					<td>
						<Reactman.FormInput label="" type="text" name="addedWeightPrice" value={postages.addedWeightPrice} onChange={_this.onChangeValue.bind(_this,index)}/>
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
					<Reactman.FormCheckbox label="" name="hasSpecialPostage" value={this.state.hasSpecialPostage} options={optionsForPostage} onChange={this.onChange} />
				</div>
				<table className="table table-bordered" style={{width:'80%'}}>
					<thead>
						<tr>
							<th>地区</th>
							<th>首重(kg)</th>
							<th>运费(元)</th>
							<th>续重(kg)</th>
							<th>续费(元)</th>
							<th>操作</th>
						</tr>
					</thead>
					<tbody>
						{postagesTr}
					</tbody>
				</table>
				<div className="xui-special-postage">
					<a href="javascript:void(0);" onClick={this.addSpecialPostage}>继续添加</a>
				</div>
			</div>
		)
	}
})

module.exports = SpecialPostagePage;