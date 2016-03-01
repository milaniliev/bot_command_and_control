'use strict'
var THREE = require('three.js')

var Net = require('net')

require('sugar')

class SampleBot {
  constructor(){
    this.position = new THREE.Vector3(0,0,0)
    this.heading  = new THREE.Vector3(0,0,1)
  }
  
  start(){
    this.connection = Net.connect({port: 8888}, function(){
      setInterval(function(){
        var event = Number.random(0, 10)
        
        if(0 <= event && event <= 5){ this.see_wall(event) }
        if(5 === event ){ this.move_forward() }
        if(6 === event ){ this.turn_left() }
      }.bind(this), 1000)
    }.bind(this))
  }
  
  move_forward(){
    this.position = this.position.add(this.heading) 
    this.push_location()
  }
  
  see_wall(distance){
    console.log("SAW WALL")
    this.send({
      command: "update_map",
      obstacles: [this.position.add(this.heading.multiplyScalar(distance))]
    })
  }
  
  turn_left(){
    console.log("GO LEFT")
    this.heading = this.heading.applyEuler(new THREE.Euler(0, 0, 1))
    this.push_location()
  }
  
  push_location(){
    this.send({
      command: "update_map",
      bot_position: this.position,
      bot_heading: this.heading
    }) 
  }
  
  send(command){
    this.connection.write(JSON.stringify(command) + ';')
  }
}

module.exports = SampleBot 
