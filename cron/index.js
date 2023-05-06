const cron = require('node-cron');

const cronJob = cron.schedule('*/15 * * * * *', () => {
    console.log('Running every 1 seconds');
})

if(process.argv[2] === 'cron-start'){
    cronJob.start();
}