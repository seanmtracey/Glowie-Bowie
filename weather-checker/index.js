const fetch = require('node-fetch');

const weather_api_host = "api.openweathermap.org";
const weather_api_path = "data/2.5/weather";

function main(params){

    const weather_data_api_request_url = `https://${weather_api_host}/${weather_api_path}?lat=${params.latitude}&lon=${params.longitude}&unit=${ params.unit || "metric" }&APPID=${params.WEATHER_API_KEY}`;

    return fetch(weather_data_api_request_url)
        .then(res => {
            if(res.ok){
                return res.json();
            } else {
                throw res;
            }
        })
        .then(response => {
            console.log(response);
            return { data : response };
        })
        .catch(err => {
            
            console.log(err);

            throw { "err" : err };

        })
    ;

}

exports.main = main;