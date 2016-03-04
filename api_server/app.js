'use strict'
require('sugar')

var Communications = require('./communications.js')
var Console = require('./console.js')

Communications.boot()
Console.boot()

Communications.ready = function(){
  console.log("COMMS READY")
  Communications.current_bot.on('update_map', function(command_parameters){
    console.log('MAP UPDATE:', command_parameters)
    Console.send(command_parameters)
  })
}

