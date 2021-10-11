// Dependencies
var restful = require('node-restful');
var mongoose = restful.mongoose;

// Schema
var users = new mongoose.Schema({
	name	 : String,
	email	 : String,
	password : String,
	wallet   : String,
	value	 : Number,
	stop_win : Number,
	stop_loss: Number
});

// Return model
module.exports = restful.model('users', users);