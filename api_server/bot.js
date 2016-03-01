'use strict'

var event = require('events')

class Bot extends event.EventEmitter {
  constructor(options){
    super()
    this.data_buffer = ""
    this.connection = options.connection
    this.connection.on('data', function(data_chunk){
        this.data_buffer = this.data_buffer.concat(data_chunk)
        if(this.data_buffer.has(';')){
          var commands = this.data_buffer.split(';')
          this.data_buffer = commands.pop()
          commands.forEach(function(command){
            this.parse_and_execute(command)
          }.bind(this))
        }
    }.bind(this))
  }

  parse_and_execute(command){
    try {
      var parsed_command = this.parse(command)

    } catch (error) {
      console.log("Malformed command: ", command)
    }
    
    try {
      this.execute(parsed_command)
    } catch (error) {
      console.log("Error executing: ", command)
      throw error
    }
  }

  parse(command){
    return JSON.parse(command)
  }

  execute(command_parameters){
    console.log("EXECUTING", command_parameters)
    if(command_parameters.command === "update_map"){
      this.emit('update_map', command_parameters)
    } else {
      console.log("Unknown command: ", command_parameters.command)
    }
  }
}

module.exports = Bot