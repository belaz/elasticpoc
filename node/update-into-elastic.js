const util = require('util');
const request = require("request-promise");

let esconn = require("../esconn.json");

// update indexed document
request.post({
    uri                    : esconn.uri + '/node/profile/278/_update?pretty',
    resolveWithFullResponse: true,
    json                   : true,
    body                   : {
        "doc": {
            "userphone": "lol"
        }
    }
}).then((response) => {
    console.log('update indexed document');
    console.log(`elasticsearch response : ${util.inspect(response.body, false, null)}`);
    return true
});





