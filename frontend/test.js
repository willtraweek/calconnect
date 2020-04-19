//fs = require('fs')
import fs from 'fs'

let raw    = fs.readFileSync('./client_secret.json')
let parsed = JSON.parse(raw)

let client_id = parsed.web.client_id
let client_secret = parsed.web.client_secret

console.log(client_id)
console.log(client_secret)

