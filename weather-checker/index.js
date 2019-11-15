const fetch = require('node-fetch');
const mqtt = require('mqtt');

const weather_api_host = "api.openweathermap.org";
const weather_api_path = "data/2.5/weather";

function main(params){

    const weather_data_api_request_url = `https://${weather_api_host}/${weather_api_path}?lat=${params.latitude}&lon=${params.longitude}&unit=${ params.unit || "metric" }&APPID=${params.WEATHER_API_KEY}`;

    const MQTT_CLIENT  = mqtt.connect(`mqtt://${params.MQTT_BROKER}`);

    return new Promise( (resolve, reject) => {

            MQTT_CLIENT.on('connect', function () {
                resolve();
            });

            MQTT_CLIENT.on('error', function (err) {
                reject();
            });

        })
        .then(function(){

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

                    return new Promise( (resolve, reject) => {

                        MQTT_CLIENT.publish('brixton-weather-report', JSON.stringify(response), (err) => {
                            if(err){
                                reject(err);
                            } else {

                                MQTT_CLIENT.end();
                                resolve(response);
                                
                            }
                        });  

                    });

                })
                .catch(err => {
                    
                    console.log(err);

                    throw { "err" : err };

                })
            ;

        })
    ;

}

exports.main = main;