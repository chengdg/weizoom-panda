/**
 * Copyright(c) 2012-2016 weizoom
 */
"use strict";

var debug = require('debug')('m:business.detail:Action');
var _ = require('underscore');

var Reactman = require('reactman');
var Dispatcher = Reactman.Dispatcher;
var Resource = Reactman.Resource;

var Constant = require('./Constant');

var Action = {
	updateAccount: function(property, value) {
		Dispatcher.dispatch({
			actionType: Constant.NEW_ACCOUNT_UPDATE_ACCOUNT,
			data: {
				property: property,
				value: value
			}
		});
	},
	selectCatalog: function(){
		Resource.get({
			resource: 'product_catalog.get_all_second_catalog',
			data: {},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.SELECT_CATALOG
			}
		})
	},
	getQualifications: function(id,catalog_ids){
		Resource.get({
			resource: 'business.get_qualifications',
			data: {
				business_id: id,
				catalog_ids: catalog_ids
			},
			dispatch: {
				dispatcher: Dispatcher,
				actionType: Constant.GET_QUALIFICATIONS
			}
		})
	},
	saveAccount: function(data) {
		var business_info = {
			company_type: data['company_type'],
			company_name: data['company_name'],
			company_money: data['company_money'],
			legal_representative: data['legal_representative'],
			contacter: data['contacter'],
			phone: data['phone'],
			e_mail: data['e_mail'],
			we_chat_and_qq: data['we_chat_and_qq'],
			company_location: data['company_location'],
			address: data['address'],
			business_license: JSON.stringify(data['business_license']),
			business_license_time: data['business_license_time'],
			tax_registration_certificate: JSON.stringify(data['tax_registration_certificate']),
			tax_registration_certificate_time: data['tax_registration_certificate_time'],
			organization_code_certificate: JSON.stringify(data['organization_code_certificate']),
			organization_code_certificate_time: data['organization_code_certificate_time'],
			account_opening_license: JSON.stringify(data['account_opening_license']),
			account_opening_license_time: data['account_opening_license_time'],
			apply_catalogs: JSON.stringify(data['apply_catalogs'])
		};
		business_info['uploadBusinessQualifications'] = JSON.stringify(data['uploadBusinessQualifications']);
		business_info['id'] = data.id;
		Resource.post({
			resource: 'business.business_detail',
			data: business_info,
			success: function() {
				Reactman.PageAction.showHint('success', '编辑客户信息成功');
				setTimeout(function(){
					Dispatcher.dispatch({
						actionType: Constant.NEW_ACCOUNT_CREATE,
						data: data
					});
				},1000);
			},
			error: function(data) {
				Reactman.PageAction.showHint('error', data.errMsg);
			}
		});
	},
	updateCatalog: function(property, value, model, id) {
		Dispatcher.dispatch({
			actionType: Constant.UPDATE_CATALOG,
			data: {
				property: property,
				value: value,
				model: model,
				id: id
			}
		});
	}
};

module.exports = Action;