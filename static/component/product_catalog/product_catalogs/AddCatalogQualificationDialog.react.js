/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product_catalog.product_catalogs:AddCatalogQualificationDialog');

var React = require('react');
var ReactDOM = require('react-dom');
var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var AddCatalogQualificationDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		var catalog_id = this.props.data.catalog_id;
		console.log(this.props.data.qualification_infos);
		var qualification_infos = JSON.parse(this.props.data.qualification_infos);
		console.log(qualification_infos[5]);
		var qualification_name = ''
		if (qualification_infos!=''){
			console.log(qualification_infos[0]);
			if( qualification_infos.length == 1){
				qualification_name = qualification_infos.value
				
			}else{
				// var all_qualification_names = qualification_names.split(',')
				// qualification_name = all_qualification_names[0]
				// for(var i = 1 ; i<all_qualification_names.length; i++){
				// 	var html = '<fieldset><div class="add_model-btn"><div class="form-group ml15"><label class="col-sm-2 control-label xui-mandatory" for="qualification_name">资质名称:</label><div class="col-sm-5"><input type="text" class="form-control" id="qualification_name" name="qualification_name" data-validate="require-notempty" value="'+all_qualification_names[i]+'"><div class="errorHint"></div></div></div><a class="btn btn-default ml20"><span class="glyphicon glyphicon-remove"></span></a></div></fieldset>';
				// 	console.log($('.add_model'));
				// 	$('.add_model').append(html);
				// }
			}
		}
		return {
			catalog_id: catalog_id,
			qualification_name: qualification_name
		}
	},
	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		var newState = {};
		newState[property] = value;
		this.setState(newState);
	},
	onChangeStore: function(){
		var infomations = Store.getData();
		console.log(infomations);
		this.setState({
			// father_catalog: infomations['father_catalog'],
			// catalog_name: infomations['catalog_name']
		})
	},
	onClickAddModel: function(event) {
		var html = '<fieldset><div class="add_model-btn"><div class="form-group ml15"><label class="col-sm-2 control-label xui-mandatory" for="qualification_name">资质名称:</label><div class="col-sm-5"><input type="text" class="form-control" id="qualification_name" name="qualification_name" data-validate="require-notempty" value=""><div class="errorHint"></div></div></div><a class="btn btn-default ml20"><span class="glyphicon glyphicon-remove"></span></a></div></fieldset>';
		$('.add_model').append(html);
		$('.btn-default').click(function(event){
			console.log($(event.target));
			console.log($(event.target).parent().parent().find('.add_model-btn'));
	        $(event.target).parent().parent().parent().find('.add_model-btn').remove();
	    });
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
	onClickDelete: function(event) {
		console.log(event);
		console.log(this);
		if (this.props.onDelete) {
			this.props.onDelete(this.props.index);
		}
	},
	render:function(){
		return (
		<div className="xui-formPage">
			<form className="form-horizontal mt15 add_model">
				<fieldset>
					<div className='add_model-btn'>
						<Reactman.FormInput label="资质名称:" name="qualification_name" validate="require-notempty" value={this.state.qualification_name} onChange={this.onChange} />
						<a className="btn btn-default ml20" onClick={this.onClickDelete}><span className="glyphicon glyphicon-remove"></span></a>
					</div>
				</fieldset>
			</form>
			<a className="ml15" onClick={this.onClickAddModel}>+ 添加资质</a>
		</div>
		)
	}
})
module.exports = AddCatalogQualificationDialog;