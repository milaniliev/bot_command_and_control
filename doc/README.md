Bots communicate with CnC via a TCP connection from the bot to the CnC host.

The default TCP port is 8888.

Bots can send the following updates to CnC.
All communication is in JSON, and separate messages are separated by `;` (a semicolon).


### Reload Map

The CnC server should discard any existing map data it has and replace it with the following map data.

The command MUST include "bot_position" and "obstacles".

```json
{
  "command": "reload_map",
  "obstacles": [
    {"x": 1, "y": 1, "z": 1, "p": 0.5},
    {"x": 2, "y": 0, "z": 2}    
  ],
  "bot_position": {"x": 0.124123, "y": 1.24312423, "z": 0.2421423}
}
```

### Update Map

The CnC server should keep existing map data and update it as indicated.

```json
{
  "command": "update_map",
  "add_obstacles": [
    {"x": 1, "y": 1, "z": 1}
  ],
  "remove_obstacles": [
    {"x": 1, "y": 1, "z": 2}
  ],
  "update_obstacles": [
    {"x": 1, "y": 1, "z": 1, "p": 0.2}
  ]
  "bot_position": {"x": 0.124123, "y": 1.24312423, "z": 0.2421423}
}