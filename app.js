var express = require('express')
var app = express()

var ips = {
  'test': '127.0.0.1'
}

app.post('/', function(request, response) {
  var details = JSON.parse(request.body)
  ips[details.id] = details.ip_address
  response.send(200)
})

app.get('/', function(request, response)  {
  var ids = Object.keys(ips)
  response.status(200).send(ids.map(function(id){ return `${id}:${ips[id]}` }).join("\n"))
})

app.listen(3567)