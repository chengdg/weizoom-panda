/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:self_shop.manage:SelfShopManagePage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var Store = require('./Store');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');
var W = Reactman.W;

var PostageConfigManagePage = React.createClass({
	getInitialState: function() {
		Store.addListener(this.onChangeStore);
		return ({});
	},

	onChangeStore: function() {
		this.setState(Store.getData());
		var filterOptions = Store.getData();
		this.refs.table.refresh(filterOptions);
	},

	render:function(){

		return (
			<div className="xui-outlineData-page xui-formPage">
                <form className="form-horizontal mt15">
                    <fieldset>
                        <Reactman.FormInput label="模板名称" name="name" validate="require-string" placeholder="20个以内字符"
                            value={this.state.name} onChange={this.onChange}  />
                        <div className='padd-left'>运送方式：除特殊地区外，其余地区的运费采用“默认运费”</div>
                    </fieldset>
                </form>
            </div>
		)
	}
})
module.exports = PostageConfigManagePage;