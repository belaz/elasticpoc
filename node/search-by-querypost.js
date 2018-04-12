const util = require('util');
const request = require("request-promise");

let esconn = require("../esconn.json");

// search by name with querystring
request.post({
    uri                    : esconn.uri + '/node/profile/_search?pretty',
    resolveWithFullResponse: true,
    json                   : true,
    body                   : {
        "query": {
            "term": {
                "username": "hdshsys"
            }
        }
    }
}).then((response) => {
    console.log('search by name with querystring');
    console.log(`elasticsearch response : ${util.inspect(response.body, false, null)}`);
    return true
});





