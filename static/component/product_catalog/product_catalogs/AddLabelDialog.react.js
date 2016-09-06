/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product_catalog.product_catalogs:AddLabelDialog');
var ProductModel = require('./ProductModel.react');
var React = require('react');
var ReactDOM = require('react-dom');
var Reactman = require('reactman');

var Store = require('./AddLabelDialogStore');
var Constant = require('./Constant');
var Action = require('./Action');

var AddLabelDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		var catalogId = this.props.data.catalogId;
		var productId = this.props.data.productId;
		return {
			catalogId: catalogId,
			productId: productId,
			catalogs: Store.getData().catalogs,
			labelFirstId: Store.getData().labelFirstId,
			labelCatalogs: Store.getData().labelCatalogs,//所有的标签分类值
			propertyId2names: Store.getData().propertyId2names,
			labelId2name: Store.getData().labelId2name,
			valueId2name: Store.getData().valueId2name,
			labelValues: [],//所有的标签值
			selectLabels: Store.getData().selectLabels,//选择的标签值(id)
			selectCatalogLabels: Store.getData().selectCatalogLabels//组织 选择的标签,分类
		}
	},

	onChange: function(value, event) {
		var propertyId2names = this.state.propertyId2names;
		var property = event.target.getAttribute('name');
		var newState = {};
		newState[property] = value;
		newState['labelValues'] = propertyId2names[value];
		newState['labelFirstId'] = -1;
		this.setState(newState);
	},

	onChangeStore: function() {
		this.setState({
			selectLabels: Store.getData().selectLabels,
			selectCatalogLabels: Store.getData().selectCatalogLabels
		});
	},

	chooseLabelValue: function(propertyId, valueId) {
		Action.chooseLabelValue(propertyId, valueId);
	},

	onBeforeCloseDialog: function() {
		var selectCatalogLabels = this.state.selectCatalogLabels;
		var catalogId = this.state.catalogId;
		var productId = this.state.productId;

		if(selectCatalogLabels.length == 0) {
			Reactman.PageAction.showHint('error', '请选择标签!');
		}else{
			Reactman.Resource.put({
				resource: 'label.catalog_label',
				data: {
					select_catalog_labels: JSON.stringify(selectCatalogLabels),
					catalog_id: catalogId,
					product_id: productId
				},
				success: function() {
					this.closeDialog();
					_.delay(function(){
						Reactman.PageAction.showHint('success', '配置标签成功');
					},500);
				},
				error: function(data) {
					Reactman.PageAction.showHint('error', '配置标签失败');
				},
				scope: this
			})
		}
	},

	render: function() {
		var _this = this;
		var labelCatalogs = this.state.labelCatalogs.length>0? JSON.parse(this.state.labelCatalogs): [];
		var labelValues = this.state.labelValues;
		var selectLabels = this.state.selectLabels;
		var selectCatalogLabels = this.state.selectCatalogLabels;
		var labelId2name = this.state.labelId2name;
		var valueId2name = this.state.valueId2name;
		var labelValuesList = '';
		var selectCatalogLabelsList = '';

		if(this.state.labelFirstId != -1){
			labelValues = this.state.propertyId2names[this.state.labelFirstId];
		}
		
		if(labelValues.length > 0) {
			labelValuesList = labelValues.map(function(label, index){
				var value = label.value_id;
				var bgStyle = {};
				bgStyle['style'] = {};

				for (var i = 0; i < selectLabels.length; i++) {
					if (selectLabels[i] === value) {
						bgStyle['style'] = {background: '#FF6600', color:'#FFF'};
					}
				}

				return (
					<li key={index} style={bgStyle['style']} className="label-value-li" onClick={_this.chooseLabelValue.bind(_this, label.property_id, label.value_id)} title={label.name}>
						{label.name}
					</li>
				)
			})
		}

		if(selectCatalogLabels.length>0) {
			selectCatalogLabelsList = selectCatalogLabels.map(function(selectCatalogLabel, index) {
				var propertyId = selectCatalogLabel.propertyId;
				var valueIds = selectCatalogLabel.valueIds;
				var labelValueNames = '';

				for(var i in valueIds) {
					if(valueId2name.hasOwnProperty(valueIds[i])) {
						labelValueNames = labelValueNames + valueId2name[valueIds[i]] + '; '
					}
				}

				if(labelId2name[propertyId] != undefined) {
					return (
						<li key={index} style={{marginTop: '5px'}}>
							<span style={{color: '#000'}}>{labelId2name[propertyId]}</span>:<span style={{marginLeft: '10px'}}>{labelValueNames}</span>
						</li>
					)
				}
			})
		}
		
		var title_tips = selectCatalogLabels.length>0 ? <li>已选择:</li>: '';
		return (
			<div className="xui-formPage xui-add-label-dialog">
				<Reactman.FormSelect label="标签分类:" name="catalogs" value={this.state.catalogs} options={labelCatalogs} onChange={this.onChange} />
				<div style={{clear: 'both'}}></div>
				<ul className="xui-label-dialog-ul">
					{labelValuesList}
				</ul>
				<ul className="xui-label-dialog-ul" style={{paddingLeft: '30px'}}>
					{title_tips}
					{selectCatalogLabelsList}
				</ul>
			</div>
		)
	}
})
module.exports = AddLabelDialog;