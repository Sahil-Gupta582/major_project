const Sequelize = require('sequelize');
const sequelize = require('./../dbConnection')

const Process = sequelize.define('Process', {
    task_name:{
        type: Sequelize.STRING,
        allowNull: false,
        primaryKey: true
    },
    task_priority:{
        type: Sequelize.INTEGER,
        allowNull: false,
    },
    task_duration:{
        type: Sequelize.FLOAT,
        allowNull: false,
    }, 
    task_energy:{
        type: Sequelize.INTEGER,
        allowNull: false,
    },
    task_depends_on:{
        type: Sequelize.JSON,
        allowNull: true,
    }
});

module.exports = {
    Process,
}