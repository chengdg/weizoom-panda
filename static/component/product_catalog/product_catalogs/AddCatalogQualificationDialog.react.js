/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product_catalog.product_catalogs:AddCatalogQualificationDialog');
var ProductModel = require('./ProductModel.react');
var React = require('react');
var ReactDOM = require('react-dom');
var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var AddCatalogQualificationDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		// var catalog_id = this.props.data.catalog_id;
		var qualification_infos = JSON.parse(this.props.data.qualification_infos);
		// var qualification_name = ''
		// if (qualification_infos!=''){
		// 	console.log(qualification_infos);
		// 	if( qualification_infos.length == 1){//只有一个分类，直接把分类名给Reactman
		// 		qualification_name = qualification_infos[0]['name']
				
		// 	}else{
		// 		qualification_name = qualification_infos[0]['name']
		// 		for(var i = 1 ; i<qualification_infos.length; i++){
		// 			// var html = '<fieldset><div class="add_model-btn"><div class="form-group ml15"><label class="col-sm-2 control-label xui-mandatory" for="qualification_name">资质名称:</label><div class="col-sm-5"><input type="text" class="form-control" id="qualification_name" name="qualification_name" data-validate="require-notempty" value="'+qualification_infos[i]['name']+'"><div class="errorHint"></div></div></div><a class="btn btn-default ml20"><span class="glyphicon glyphicon-remove"></span></a></div></fieldset>';
		// 			// $('.add_model').append(html);
		// 			// qualification_name += ';'+ qualification_infos[i]['name']

		// 			console.log(qualification_infos[i]['name']);
		// 		}
		// 	}
		// }
		// return {
		// 	catalog_id: catalog_id,
		// 	qualification_name: qualification_name,
		// 	qualification_infos: qualification_infos
		// }
		return {
			'models': qualification_infos,
			qualification_infos: qualification_infos,
			name: qualification_infos
		}
	},
	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		var newState = {};
		newState[property] = value;
		this.setState(newState);
	},
	onChangeModel: function(value, event) {
		var model = this.state.models[value.index];
		model.name = value.name;
		// this.callChangeHandler();
	},
	onChangeStore: function(){
		var infomations = Store.getData();
		console.log(infomations['models']);
		this.setState({
			models: infomations['models']
		})
	},
	onClickAddModel: function(event) {
		// var html = '<fieldset><div class="add_model-btn"><div class="form-group ml15"><label class="col-sm-2 control-label xui-mandatory" for="qualification_name">资质名称:</label><div class="col-sm-5"><input type="text" class="form-control" id="qualification_name" name="qualification_name" data-validate="require-notempty" value=""><div class="errorHint"></div></div></div><a class="btn btn-default ml20"><span class="glyphicon glyphicon-remove"></span></a></div></fieldset>';
		// $('.add_model').append(html);
		// $('.btn-default').click(function(event){
		// 	console.log($(event.target));
		// 	console.log($(event.target).parent().parent().find('.add_model-btn'));
	 //        $(event.target).parent().parent().parent().find('.add_model-btn').remove();
	 //    });
		this.state.models.push({
				name: ''
			});

		// this.callChangeHandler();
	},
	onBeforeCloseDialog: function() {
		var qualificationNames = [];
		var len = $('.form-control').length;
		for(var i = 0;i< len;i++){
			var qualification_name = $('.form-control').eq(i).val();
			if(qualification_name.length>48){
				Reactman.PageAction.showHint('error', '资质名称不能超过48个字符');
				return;
			}
			qualificationNames.push(qualification_name);
		}
		if (this.state.catalog_id){
			Reactman.Resource.post({
				resource: 'product_catalog.qualification',
				data: {
					catalog_id: this.state.catalog_id,
					qualification_names: String(qualificationNames)
				},
				success: function() {
					this.closeDialog();
					_.delay(function(){
						Reactman.PageAction.showHint('success', '编辑资质成功');
					},500);
				},
				error: function(data) {
					Reactman.PageAction.showHint('error', data.errMsg);
				},
				scope: this
			})
		}else{
			Reactman.Resource.put({
				resource: 'product_catalog.qualification',
				data: {
					catalog_id: this.state.catalog_id,
					qualification_names: String(qualificationNames)
				},
				success: function() {
					this.closeDialog();
					_.delay(function(){
						Reactman.PageAction.showHint('success', '设置资质成功');
					},500);
				},
				error: function(data) {
					Reactman.PageAction.showHint('error', data.errMsg);
				},
				scope: this
			})
		}
		
	},
	onDeleteModel: function(index) {
		// this.state.models.splice(index, 1);
		// this.setState({
		// 	models: this.state.models.splice(index, 1)
		// })
		Action.deleteCatalogQualification(index,this.state.qualification_infos);
		// this.callChangeHandler();
	},
	render:function(){
		var models = this.state.qualification_infos;
		var cModels = '';
		if (models) {
			var _this = this;
			cModels = models.map(function(model, index) {
				return (
					<ProductModel models={models} model={model} value={name} index={index} key={index} onChange={_this.onChangeModel} onDelete={_this.onDeleteModel} />
				)
			});
		}
		return (
		<div className="xui-formPage">
			{cModels}
			<a className="ml15" onClick={this.onClickAddModel}>+ 添加资质</a>
		</div>
		)
	}
})
module.exports = AddCatalogQualificationDialog;