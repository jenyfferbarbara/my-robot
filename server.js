var config = require('./config.json');

// Dependencies
const express = require('express');
const mongoose = require('mongoose');
const {PythonShell} = require('python-shell');

// mongoDB
const mongoURL = `mongodb://myRobot:6eJ%402chTyxn2%2as@${config.host}:27017/my_robot?authSource=admin`;
mongoose.connect(mongoURL, {useNewUrlParser: true, useUnifiedTopology: true, useFindAndModify: false});

// Express
const app = express();
app.use(express.static('public')); // Server static files
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.disable('etag');

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
		res.send(result)
    });
});

app.get("/run_robot", async(req, res, next) => {
	const user       = req.query.user

    let options = {
        mode: 'text',
        pythonOptions: ['-u'],
        scriptPath: 'iq_option',
        args: [user]
    };
      
    PythonShell.run('main.py', options, function (err, result){
      if (err) throw err;
      res.send(result)
    });
});

// Start server
const port = 8080;
app.listen(port, "0.0.0.0");
console.log(`Server is running on port: ${port}`);
