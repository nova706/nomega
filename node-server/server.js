var http = require('http');

process.title = "nomegaApp";
const PORT=8080;

function handleRequest(request, response){
    response.end(JSON.stringify({response: "Hello from Nomega"}));
}

var server = http.createServer(handleRequest);

server.listen(PORT, function(){
    console.log("Server listening on: http://localhost:%s", PORT);
});

process.on('SIGINT', function() {
    console.log("\nGracefully shutting down from SIGINT\n");
    server.close();
    process.exit();
});