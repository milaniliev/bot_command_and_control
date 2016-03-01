'use strict'
var WebSocketServer = require('websocket').server
var HTTP = require('http')
module.exports = {
  boot: function(){
    this.http_server = new HTTP.Server()
    console.log("Booting socket server")
    this.server = new WebSocketServer({httpServer: this.http_server, autoAcceptConnections: true})
    // this.server.on('request', function(request){
    //   console.log("Request received")
    // })
    this.server.on('close', function(a,b,c){
      console.log(a,b,c)
    })
    this.server.on('connect', function(connection){
      console.log("CONSOLE: display connected")
      this.connection = connection
      this.connection.on('message', function(message){
        // console.log(message.utf8Data)
      })
    }.bind(this))
    
    this.http_server.listen(8989)
  },
  
  send: function(message){
    if(this.connection){
      this.connection.sendUTF(JSON.stringify(message))
    } else {
      console.log(`CONSOLE: Discarding ${message}, no display connected`)
    }
  }
}