const util = require('util');
const request = require("request-promise");

let esconn = require("../esconn.json");

// search all sort by account number asc
request.get({
    uri                    : esconn.uri + '/bank/_search?q=*&sort=account_number:desc&pretty',
    resolveWithFullResponse: true,
    json                   : true
}).then((response) => {
    console.log('search all sort by account number asc');
    console.log(`elasticsearch response : ${util.inspect(response.body, false, null)}`);
    return true
});





