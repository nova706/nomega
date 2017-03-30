var ps = require('ps-node');

ps.lookup({
    command: "nomegaApp"
}, function (err, resultList) {
    if (err) {
        throw err;
    }

    resultList.forEach(function (prcs) {
        if (prcs) {
            process.kill(prcs.pid, 'SIGINT');
            console.log('Process Stopped');
            process.exit();
        }
    });
});