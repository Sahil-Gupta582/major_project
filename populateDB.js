const fs = require('fs');
const {exec} = require('child_process');
const { Process } = require('./model/process');
const sequelize = require('./dbConnection');

const createTable = async() =>{
    await sequelize.sync();
}

const insertDataInDB = async () => {
    try{
        const res = exec('g++ randomDAG.cpp -o randomDAG && ./randomDAG');
        const contents = fs.readFileSync('dag.txt','utf-8');

        const data = JSON.parse(contents);

        const dependsOn = {};
        let max_process = 0;
        for(const obj of data){
            const {x,y} = obj;
            if(x && y){
                if(!dependsOn[x]){
                    dependsOn[x] = [];
                }
                dependsOn[x].push(y);
                max_process = Math.max(max_process,x,y);
            }
        }
        const insertObject = [];
        for(let i = 1; i <= max_process; i+=1){
            const obj = {
                task_name: i,
                task_priority: Math.random()*max_process,
                task_duration: Math.random()*5,
                task_energy: Math.random()*10,
                task_depends_on: dependsOn[i]?dependsOn[i]:[],
            };
            insertObject.push(obj);
        }
        await Process.bulkCreate(insertObject, {
            updateOnDuplicate: ['updatedAt', 'createdAt']
        });
    }catch(e){
        console.log(e);
    }
}

if(process.argv[2] === 'insertDataInDB'){
    insertDataInDB();
}

if(process.argv[2] === 'createTable'){
    createTable();
}