/* global THREE */ //for VS Code to stop complaining

'use strict'

var map = {
  element: document.getElementById("map"),
  block_cubes: [],

  shadows: true,

  boot: function(){
    this.scene = new THREE.Scene()
    this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
    this.renderer = new THREE.WebGLRenderer({canvas: this.element, antialias: true})
	  
    if(this.shadows){
      this.renderer.shadowMapEnabled = true;
      this.renderer.shadowMapType = THREE.PCFSoftShadowMap;
    }
     
    this.renderer.setClearColor(0xeeeeee, 1)

    this.renderer.setSize(window.innerWidth, window.innerHeight)
    
    var groundTexture = THREE.ImageUtils.loadTexture('background.png') 
    groundTexture.wrapS = THREE.RepeatWrapping 
    groundTexture.wrapT = THREE.RepeatWrapping 
    groundTexture.repeat.x = 256
    groundTexture.repeat.y = 256
    
    var wallTexture = THREE.ImageUtils.loadTexture('wall.png') 
    wallTexture.wrapS = THREE.RepeatWrapping 
    wallTexture.wrapT = THREE.RepeatWrapping 
    wallTexture.repeat.x = 1
    wallTexture.repeat.y = 1
    
    this.material = new THREE.MeshPhongMaterial({ color: 0xFFFFFF, specular: 0x444444, map: wallTexture, shininess: 30, shading: THREE.SmoothShading, transparent: true })
    
    this.top_light = new THREE.DirectionalLight(0x404040, 1)
    this.top_light.castShadow = true;
    this.top_light.shadowCameraVisible = true;
    this.top_light.shadowDarkness = 1;
    
    this.top_light.shadowMapWidth = 512;
    this.top_light.shadowMapHeight = 512;

    var d = 10;

    this.top_light.shadowCameraLeft = -d;
    this.top_light.shadowCameraRight = d;
    this.top_light.shadowCameraTop = d;
    this.top_light.shadowCameraBottom = -d;

    this.top_light.shadowCameraFar = 25;
    
    this.top_light.position.x = 0
    this.top_light.position.y = 20
    this.top_light.position.z = 0
	  this.scene.add(this.top_light)
    
    var light = new THREE.AmbientLight( 0xA0A0A0 ); // soft white light 
    this.scene.add( light );


    this.ground = new THREE.Mesh(new THREE.PlaneGeometry(400,400), new THREE.MeshPhongMaterial({map: groundTexture, color: 0xFFFFFF}))
    this.ground.receiveShadow = true
    this.ground.position.y = -0.5 //lower it 
    this.ground.rotation.x = -Math.PI/2 //-90 degrees around the xaxis 
    this.ground.doubleSided = true //IMPORTANT, draw on both sides 
    this.scene.add(this.ground)
    
    this.bot = new THREE.Mesh(new THREE.SphereGeometry(0.5, 32, 32), new THREE.MeshPhongMaterial({ color: 0x0089FF, specular: 0x777777, shininess: 10, shading: THREE.SmoothShading }))
    this.bot.castShadow = true
    // this.bot_light = new THREE.PointLight(0x0089FF, 0.3, 2)
    // this.scene.add(this.bot_light)
    this.scene.add(this.bot)
    this.render()
  },
  
  render: function render() { 
    requestAnimationFrame(this.render.bind(this))
    this.renderer.render(this.scene, this.camera)
    
    // simulations
 	  this.moveBotTo({z: this.bot.position.z - 0.02})

  },
  
  placeBlockAt(grid_coordinates){
    this.block_cubes[grid_coordinates.x] = this.block_cubes[grid_coordinates.x] || []
    var cube = this.block_cubes[grid_coordinates.x][grid_coordinates.z] || new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), window.map.material)
    cube.receiveShadow = true
    cube.position.x = grid_coordinates.x
    cube.position.z = grid_coordinates.z
    this.block_cubes[grid_coordinates.x][grid_coordinates.z] = cube 
    
    this.scene.add(this.block_cubes[grid_coordinates.x][grid_coordinates.z])
  },
  
  removeBlockAt(grid_coordinates){
    this.scene.remove(this.block_cubes[grid_coordinates.x][grid_coordinates.z])
  },
  
  moveBotTo(grid_position){
    if(grid_position.x != null && grid_position != undefined){
      this.bot.position.x = grid_position.x
    }
    
    if(grid_position.z != null && grid_position.z != undefined){
      this.bot.position.z = grid_position.z
    }
    
    this.top_light.position.x = this.bot.position.x
    this.top_light.position.z = this.bot.position.z
    this.top_light.position.y = this.bot.position.y + 10
    
    this.camera.position.x = this.bot.position.x
    this.camera.position.z = this.bot.position.z + 5
    this.camera.position.y = this.bot.position.y + 1
  },
  
  load(map_data){
    map_data.forEach(function(block_coordinates){
      this.placeBlockAt(block_coordinates)
    }.bind(this))
  }
}

map.boot()

map.load([
  {x: 1, z: -1},
  {x: 1, z: 0},
  {x: 1, z: 1},
  {x: 1, z: 2},

  
  {x: -1, z: -10},
  {x: -2, z: -10},
  {x: -3, z: -10},
  {x: -4, z: -10},
          
  
  {x: -1, z: -5},
  {x: -2, z: -5},
  {x: -3, z: -5},
  {x: -4, z: -5},
  {x: -4, z: -4},
  {x: -4, z: -3},
  {x: -4, z: -2},
  {x: -4, z: -1},
  {x: -4, z: 0},
  
  {x: 2, z: -3},
  {x: 1, z: -4},
  {x: 2, z: -3},
  {x: 1, z: -5},
  {x: 3, z: -2},
  {x: 1, z: -3}
])

// indicate uncertainty
map.block_cubes[1][0].material = map.block_cubes[1][0].material.clone()
map.block_cubes[1][0].material.opacity = 0.6

window.map = map