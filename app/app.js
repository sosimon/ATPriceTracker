const express = require('express')
const exphbs = require('express-handlebars')
const app = express()

app.engine('handlebars', exphbs({defaultLayout: 'main'}))
app.set('view engine', 'handlebars')

app.get('/', (req, res) =>
  res.render('index')
)

app.get('/healthz', (req, res) => 
  res.render('healthz')
)

app.listen(3000, () => console.log('Example app listening on port 3000!'))
