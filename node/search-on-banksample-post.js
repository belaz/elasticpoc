const util = require('util');
const request = require("request-promise");

let esconn = require("../esconn.json");

// bool query

// {
//     "query": {
//       "bool": {
//         "must": [
//           { "match": { "address": "mill" } },
//           { "match": { "address": "lane" } }
//         ]
//       }
//     }
//   }

// 40 year and not living in ohio

// {
//     "query": {
//       "bool": {
//         "must": [
//           { "match": { "age": "40" } }
//         ],
//         "must_not": [
//           { "match": { "state": "ID" } }
//         ]
//       }
//     }
//   }

// group accounts by state

// {
//     "size": 0,
//     "aggs": {
//       "group_by_state": {
//         "terms": {
//           "field": "state.keyword"
//         }
//       }
//     }
//   }

// group by state and show average balance 

// {
//     "size": 0,
//     "aggs": {
//       "group_by_state": {
//         "terms": {
//           "field": "state.keyword"
//         },
//         "aggs": {
//           "average_balance": {
//             "avg": {
//               "field": "balance"
//             }
//           }
//         }
//       }
//     }
//   }

// filter by balance range

// {
//     "query": {
//       "bool": {
//         "must": { "match_all": {} },
//         "filter": {
//           "range": {
//             "balance": {
//               "gte": 20000,
//               "lte": 30000
//             }
//           }
//         }
//       }
//     }
//   }

// pagination 

// {
//     "query": { "match_all": {} },
//     "from": 10,
//     "size": 10
//   }

// search all sorted by account number asc
request.post({
    uri                    : esconn.uri + '/bank/_search?pretty',
    resolveWithFullResponse: true,
    json                   : true,
    body: {
            "query": { "match_all": {} },
            "sort": [
              { "account_number": "asc" }
            ]
          }
}).then((response) => {
    console.log('search all sort by account number asc');
    console.log(`elasticsearch response : ${util.inspect(response.body, false, null)}`);
    return true
});





