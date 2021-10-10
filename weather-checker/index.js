require('dotenv').config( {silent : process.env.NODE_ENV === "production" } )
const fetch = require('node-fetch');

const weather_data_api_request_url = `https://${process.env.WEATHER_API_HOST}/${process.env.WEATHER_API_PATH}?lat=${process.env.TARGET_LATITUDE}&lon=${process.env.TARGET_LONGITUDE}&units=${ process.env.WEATHER_UNITS || "metric" }&APPID=${process.env.WEATHER_API_KEY}`;

exports.handler =  async function(event, context) {

    return fetch(weather_data_api_request_url)
        .then(res => {
            if(res.ok){
                return res.json();
            } else {
                throw res;
            }
        })
        .catch(err => {
            
            console.log(err);
    
            throw { "err" : err };
    
        })
    ;
    
}
