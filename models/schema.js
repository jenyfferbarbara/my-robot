// Dependencies
var restful = require('node-restful');
var mongoose = restful.mongoose;

// Schema
var schema = new mongoose.Schema({
	_id: {
		user: String,
		par: String,
		date: String,
		time: String
	},
	action: String,
	expiration: Number,
	profit: Number,
	status: String
}, { _id: false });

module.exports = schema