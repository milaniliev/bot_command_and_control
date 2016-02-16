module.export = class Bot {
  constructor(options){
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
      this.execute(this.parse(command))
    } catch (error) {
      console.log("Malformed command: ", command)
    }
  }

  parse(command){
    JSON.parse(command)
  }

  execute(command){
    console.log("EXEC:", command)
  }
}