// Dependencies
const express = require('express');
const mongoose = require('mongoose');
const {PythonShell} = require('python-shell');

// mongoDB
const mongoURL = 'mongodb://myRobot:6eJ%402chTyxn2%2as@vps31601.publiccloud.com.br:27017/my_robot?authSource=admin';
mongoose.connect(mongoURL, {useNewUrlParser: true, useUnifiedTopology: true});

// Express
const app = express();
app.use(express.static('public')); // Server static files
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Routes
app.use('/api', require('./routes/api'));

app.get("/install_requirements", (req, res, next) => {
    let options = {
        mode: 'text',
        pythonOptions: ['-u'],
        scriptPath: 'iq_option'
    };
      
    PythonShell.run('requirements.py', options, function (err, result){
          if (err) throw err;
          res.send(result.toString())
    });
});

app.get("/run_robot", (req, res, next) => {
	const user       = req.query.user
	const wallet     = req.query.wallet
	const stop_win   = req.query.stop_win
	const stop_loss  = req.query.stop_loss
	const expiration = req.query.expiration
	const channel    = req.query.channel

    let options = {
        mode: 'text',
        pythonOptions: ['-u'],
        scriptPath: 'iq_option',
        args: [user, wallet, stop_win, stop_loss, expiration, channel]
    };
      
    PythonShell.run('main.py', options, function (err, result){
          if (err) throw err;
          res.send(result.toString())
    });
});

// Start server
const port = 8080;
app.listen(port, "0.0.0.0");
console.log(`Server is running on port: ${port}`);
