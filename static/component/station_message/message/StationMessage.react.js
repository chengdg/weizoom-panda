/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";
var React = require('react');
var ReactDOM = require('react-dom');

var Reactman = require('reactman');
var W = Reactman.W;

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');

var AddSelfShopDialog = Reactman.createDialog({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return Store.getData();
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateMessage(property, value);
	},

	onChangeStore: function(){
		this.setState(Store.getData());
	},

    onSubmit: function(){

        Action.addMessage(this.state);
    },
	render:function(){

		return (
			<div className="xui-outlineData-page xui-formPage">
                <form className="form-horizontal mt15">
                    <fieldset>
                        <legend className="pl10 pt10 pb10">站内信</legend>
                        <Reactman.FormInput label="标题:" name="title" validate="require-string" placeholder="" value={this.state.title} onChange={this.onChange}  />
                        <Reactman.FormRichTextInput label="商品详情" name="text" width={800} validate="require-notempty" value={this.state.text} onChange={this.onChange} />
                        <Reactman.FormFileUploader label="附件:" name="attachment" value={this.state.attachment} onChange={this.onChange} max={3} />
                        <Reactman.FormSubmit onClick={this.onSubmit} text="保 存" />
                    </fieldset>
                </form>
            </div>
		)
	}
})
module.exports = AddSelfShopDialog;