const sequelize = require('../dbConnection')

const fetchGraphNodesEdges = async (req,res) => {
    try{
        const query = 'select task_name, completion_time, energy_needed, dependencies  from task_table_temp2 ttt;'
        const data = await sequelize.query(query, {
            type: sequelize.Sequelize.QueryTypes.SELECT,
        })

        let node = [];
        const edges = [];
        for(const obj of data){
            const{task_name, dependencies} = obj;
            const process = parseInt(task_name.replace("job",""),10);
            node.push(process);
            if(dependencies){
                const depends = JSON.parse(dependencies);
                depends.map((x) => edges.push({from: x, to: process, arrows: 'to'}));
            }
        }
        node = [...new Set(node)];
        const nodes = [];
        node.map((x) => nodes.push({id:x, label: `Job${x}`}));

        res.status(200).send({
            message: 'Graph fetched successfully',
            nodes,
            edges
        })
    }catch(err) {
        throw err;
    }
    

}

module.exports = {
    fetchGraphNodesEdges
}