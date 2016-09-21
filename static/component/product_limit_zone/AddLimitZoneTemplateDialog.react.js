/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:product_limit_zone.product_limit_zone:AddLimitZoneTemplateDialog');
//var ProductModel = require('./ProductModel.react');
var React = require('react');
var ReactDOM = require('react-dom');
var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');

var AddLimitZoneTemplateDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);

//        var name = this.props.
        var id = this.props.data.id;
        var name = this.props.data.name;
		return {
            name: name,
            id: id
		}
	},
	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		var newState = {};
		newState[property] = value;
		this.setState(newState);
	},

	onChangeStore: function(){
		this.setState({
		    name: this.state.name,
		    id: this.state.id
		})
	},

    onBeforeCloseDialog: function() {
        var name = this.state.name;
        var id = this.state.id;
        if(id == null || id == ''){
            Reactman.Resource.put({
                resource: 'product_limit_zone.template',
                data: {
                    name: name,
                },
                success: function() {
//                    Reactman.PageAction.showHint('success', '保存成功！');
                    _.delay(function(){
						Reactman.PageAction.showHint('success', '保存成功');
					},500);
                    Action.updateLimitZoneTemplates();
                    this.closeDialog();

                },
                error: function() {
                    Reactman.PageAction.showHint('error', '保存失败！');
                },
                scope: this
            })
        }else{
            Reactman.Resource.post({
                resource: 'product_limit_zone.template',
                data: {
                    name: name,
                    id: id
                },
                success: function() {
                    _.delay(function(){
						Reactman.PageAction.showHint('success', '保存成功');
					},500);
                    Action.updateLimitZoneTemplates();
                    this.closeDialog();

                },
                error: function() {
                    Reactman.PageAction.showHint('error', '保存失败！');
                },
                scope: this
            })
        }
    },
	render:function(){
        var zoneList = [{"provinces":[{"cities":[{"cityId":72,"cityName":"大兴安岭地区"}],"provinceId":8,"provinceName":"黑龙江省"}],"zoneName":"华北-东北"}];

		return (
		<div className="xui-outlineData-page xui-formPage">
		<form className="form-horizontal mt15">
                <fieldset>
                    <Reactman.FormInput label="模板名称:" name="name" validate="require-string" placeholder=""
                        value={this.state.name}
                        onChange={this.onChange} autoFocus={true} />

                </fieldset>
            </form>

		</div>
		)
	}
})
module.exports = AddLimitZoneTemplateDialog;