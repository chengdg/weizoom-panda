/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:postage_config.new_config:DefaultPostagePage');
var React = require('react');
var ReactDOM = require('react-dom');
var _ = require('underscore');

var Reactman = require('reactman');

var DefaultPostageStore = require('./DefaultPostageStore');
var Constant = require('./Constant');
var Action = require('./Action');
require('./style.css');
var W = Reactman.W;

var DefaultPostagePage = React.createClass({
	getInitialState: function() {
		DefaultPostageStore.addListener(this.onChangeStore);
		return DefaultPostageStore.getData();
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateDefaultPostages(property, value);
	},

	render:function(){
		var _this = this;
		var defaultPostages = this.state.defaultPostages;
		var postagesTr = defaultPostages.map(function(postages, index){
			return(
				<tr key={index}>
					<td>
						<Reactman.FormInput label="" type="text" name="first_weight" value={postages.first_weight} onChange={_this.onChange} />
					</td>
					<td>
						<Reactman.FormInput label="" type="text" name="first_weight_price" value={postages.first_weight_price} onChange={_this.onChange} />
					</td>
					<td>
						<Reactman.FormInput label="" type="text" name="added_weight" value={postages.added_weight} onChange={_this.onChange} />
					</td>
					<td>
						<Reactman.FormInput label="" type="text" name="added_weight_price" value={postages.added_weight_price} onChange={_this.onChange}/>
					</td>
				</tr>
			)
		});

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

module.exports = DefaultPostagePage;