// Dependencies
var express = require('express');
var router  = express.Router();

// Models
var Bears               = require('../models/bears');
var Rafa_CR7            = require('../models/rafa_cr7');
var Sinais_Consistentes = require('../models/sinais_consistentes');
var SlumSignals         = require('../models/slum_signals');
var Testes              = require('../models/testes');

// Routes
Bears.methods(['get', 'put', 'post', 'delete']);
Bears.register(router, '/bears');

Rafa_CR7.methods(['get', 'put', 'post', 'delete']);
Rafa_CR7.register(router, '/rafa_cr7');

Sinais_Consistentes.methods(['get', 'put', 'post', 'delete']);
Sinais_Consistentes.register(router, '/sinais_consistentes');

SlumSignals.methods(['get', 'put', 'post', 'delete']);
SlumSignals.register(router, '/slum_signals');

Testes.methods(['get', 'put', 'post', 'delete']);
Testes.register(router, '/testes');

// Return router
module.exports = router;