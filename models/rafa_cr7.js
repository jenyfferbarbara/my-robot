// Dependencies
var restful = require('node-restful');
var Schema = require('./schema');

// Return model
module.exports = restful.model('rafa_cr7', Schema);