const express = require('express')
const bodyParser = require('body-parser')
const graphRoutes = require('./routes/graphRoute')
const cors = require('cors');
const sequelize = require('./dbConnection')

var app = express();

sequelize.sync();

app.use(cors());


app.use(bodyParser.json());
app.use('/api', graphRoutes);

app.listen(3000, () => {
    console.log('Server started on port 3000');
});