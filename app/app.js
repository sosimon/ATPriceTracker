const express = require('express')
const exphbs = require('express-handlebars')
const request = require('request')

const app = express()

const getMetadata = (path) => {
  let metaURL = 'http://metadata.google.internal/computeMetadata/v1/'
  let options = {
    url: metaURL + path,
    headers: {'Metadata-Flavor': 'Google'}
  }
  var data = ''
  request.get(options, (err, res, body) => {
    if (!err && res.statusCode == 200) {
      console.log(body)
      data = body
    }
  })
  return data
}

const testData = [
  {'x':20000,'y':25000},
  {'x':40000,'y':20000},
  {'x':60000,'y':17500},
  {'x':80000,'y':15000},
  {'x':100000,'y':12500},
  {'x':120000,'y':10000}
]

app.engine('handlebars', exphbs({defaultLayout: 'main'}))
app.set('view engine', 'handlebars')

app.use('/static', express.static(__dirname + '/static'));

app.get('/', (req, res) =>
  res.render('index')
)

app.get('/healthz', (req, res) => {
  let instance = {
    name: getMetadata('instance/name'),
    hostname: getMetadata('instance/hostname'),
    id: getMetadata('instance/id'),
    zone: getMetadata('instance/zone'),
    internalip: getMetadata('instance/network-interfaces/0/ip'),
    externalip: getMetadata('instance/network-interfaces/0/forwarded-ips'),
    project: getMetadata('project/project-id')
  }
  res.render('healthz', { instance: instance })
})

app.listen(8080, () => console.log('Example app listening on port 8080!'))
