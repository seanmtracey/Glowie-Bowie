require('dotenv').config( {silent : process.env.NODE_ENV === "production" } )

const awsIot = require('aws-iot-device-sdk');
const uuid = require('uuid').v4;

function convertWeatherIdToType(id){

    if(id >= 200 && id <= 232){
        return "thunderstorm";
    } else if(id >= 300 && id <= 321){
        return "drizzle";
    } else if(id >= 500 && id <= 531){
        return "rain";
    } else if(id >= 600 && id <= 622){
        return "snow";
    } else if(id >= 700 && id <= 781){
        return "atmosphere";
    } else if(id === 800){
        return "clear";
    } else if(id >= 801 && id <= 804){
        return "clouds";
    }

}

function convertTemperatureToColor(temperature){
    
    if(temperature < 0){
        return [255,255,255]
    } 
    
    if(temperature >= 0){
        return [150, 255, 255];
    }

    if(temperature > 15){
        return [255, 255, 0];
    }

    if(temperature > 22){
        return [255, 175, 0];
    }

    if(temperature > 30){
        return [255, 0, 0];
    }

}

function setLights(weather, temperature){

    const weatherColors = {
        "thunderstorm" : [255, 255, 0],
        "drizzle" : [150, 255, 255],
        "rain" : [0, 0, 255],
        "snow" : [255, 255, 255],
        "atmosphere" : [255, 175, 0],
        "clear" : [0, 255, 0],
        "clouds" : [190, 255, 200]
    };

    let temperatureColor = convertTemperatureToColor(temperature);

    return {
        leftStrip : {
            color : temperatureColor
        },
        rightStrip : {
            color : weatherColors[weather]
        }
    };

}

exports.handler =  async function(event, context) {

    return new Promise( (resolve, reject) => {
        
        const data = event.responsePayload;
        const clientId = `${process.env.CLIENT_ID}+${uuid()}`;

        const device = awsIot.device({
            keyPath: process.env.PRIVATE_KEY_PATH,
            certPath: process.env.CERTIFICATE_PATH,
                caPath: process.env.CA_PATH,
                clientId: clientId,
                host: process.env.MQTT_HOST
        });
    
        device.on('connect', function() {
            console.log('connect');

            const lightSettings = setLights( convertWeatherIdToType(data.weather.id), data.main.feels_like);

            device.publish('glowie_bowie/lights/update', JSON.stringify({ lightSettings : lightSettings, time : Date.now() / 1000 | 0 }), { qos : 1 }, (err) => {

               if(err){
                    reject(err);
                } else {
                    device.end(false, {}, () => {
                        resolve();
                    })
                }

            });

            

        });
    
        device.on('error', (err) => {
            console.log("err:", err);
        })
    
        device.on('error', function(error) {
            console.log('error', error);
        });

    });

}
