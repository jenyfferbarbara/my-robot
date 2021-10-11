// Dependencies
var restful = require('node-restful');
var mongoose = restful.mongoose;

// Schema
var channel = new mongoose.Schema({
	name  : String,
	active: Boolean
});

// Return model
module.exports = restful.model('channel', channel);