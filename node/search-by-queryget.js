const util = require('util');
const request = require("request-promise");

let esconn = require("../esconn.json");

// search by name with querystring
request.get({
    uri                    : esconn.uri+'/node/profile/_search?q=step:3&pretty',
    resolveWithFullResponse: true,
    json: true
}).then((response) => {
    console.log('search by name with querystring');
    console.log(`elasticsearch response : ${util.inspect(response.body, false, null)}`);
    return true
});





