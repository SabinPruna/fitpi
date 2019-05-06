console.log('function starts')

const AWS = require('aws-sdk')
const docClient = new AWS.DynamoDB.DocumentClient({region: 'eu-central-1'})

exports.handler = (event, context, callback) => {
    console.log(JSON.stringify(event));
    console.log('event data: ', JSON.stringify(event.state));
    console.log('event data: ', JSON.stringify(event.state.reported));
    console.log('event data: ', JSON.stringify(event.state.reported.temperature));
    console.log('event data: ', JSON.stringify(event.state.reported.humidity));
    console.log('event data: ', JSON.stringify(event.state.reported.date));

let params =  {
        Item: {
            date: event.state.reported.date,
            temperature: event.state.reported.temperature,
            humidity: event.state.reported.humidity
        },
        TableName: ''
    };

    docClient.put(params, function(err,data){
        if(err) {
            callback(err, null)
        }else{
            callback(null, data)
        }
    });
   
  console.log(params); 
      
};
