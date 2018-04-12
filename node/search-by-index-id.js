const util = require('util');
const request = require("request-promise");

let esconn = require("../esconn.json");


// search by index id
request.get({
    uri                    : esconn.uri + '/node/profile/278?pretty',
    resolveWithFullResponse: true,
    json                   : true
}).then((response) => {
    console.log('search by index id');
    console.log(`elasticsearch response : ${util.inspect(response.body, false, null)}`);
    return true
});






