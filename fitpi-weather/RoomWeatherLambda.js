var aws = require('aws-sdk');
var ddb = new aws.DynamoDB({region: 'eu-central-1'})
const documentClient = new aws.DynamoDB.DocumentClient({region: 'eu-central-1'})

exports.handler = async function (event, context) {
    
    const params = {
        TableName: "",
    };

    let scanResults = [];
    let items;
    do{
        items =  await documentClient.scan(params).promise();
        items.Items.forEach((item) => scanResults.push(item));
        params.ExclusiveStartKey  = items.LastEvaluatedKey;
    }while(typeof items.LastEvaluatedKey != "undefined");

    return scanResults;

};