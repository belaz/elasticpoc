const mysql = require('mysql');
const util = require('util');
const request = require("request-promise");

let mysqlconn = require("../mysqlconn.json");
let esconn = require("../esconn.json");

var con = mysql.createConnection(mysqlconn);

con.connect(function (err) {
    if (err) throw err;
    console.log("Connected!");
    let sql = "select * from node_human limit 1; ";
    con.query(sql, function (err, result) {
        if (err) throw err;
        //  console.log(result[0].node_human_id);
        //  console.log("Result: " + util.inspect(result, false, null));
        console.log(esconn.uri);

        // Add a document to elastic search specify the id
        // sample curl
        // curl -XPUT 'localhost:9200/customer/_doc/1?pretty&pretty' -H 'Content-Type: application/json' -d'{ "name": "John Doe" }'
        request.put({
            uri                    : `${esconn.uri}/node/profile/${result[0].fk_node_id}?pretty`,
            resolveWithFullResponse: true,
            json: true,
            // body: {
            //     "name": "John Doeee"
            // }
            body: result[0]
        }).then((response) => {
            console.log(`elasticsearch response : ${util.inspect(response.body, false, null)}`);
            return true
        });

        // Add a document to elastic search and DONT specify the id
        // sample curl
        // curl -XPOST 'localhost:9200/customer/_doc/1?pretty&pretty' -H 'Content-Type: application/json' -d'{ "name": "John Doe" }'
        request.post({
            uri                    : esconn.uri+'/node/profile?pretty',
            resolveWithFullResponse: true,
            json: true,
            body: {
                 "name": "John Doeee"
            }
        }).then((response) => {
            console.log(`elasticsearch response : ${util.inspect(response.body, false, null)}`);
            return true
        });

    });
});




