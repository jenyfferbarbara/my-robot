// Dependencies
var restful = require('node-restful');
var mongoose = restful.mongoose;

// Schema
var summary = new mongoose.Schema({
	user	  : String,
	date	  : String,
	channel	  : String,
	expiration: Number,
	stop_win  : Number,
	stop_loss : Number,
	profit	  : Number,
	recovery  : Number,
	win		  : Number,
	loss	  : Number	
});

module.exports = restful.model('summary', summary);