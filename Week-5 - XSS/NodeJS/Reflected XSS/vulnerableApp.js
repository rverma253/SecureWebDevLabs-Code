const express = require('express');
const bodyParser = require('body-parser');
const app = express();

app.use(bodyParser.urlencoded({ extended: true }));

app.get('/search', (req, res) => {
    const query = req.query.query || '';
    res.send(`<h1>Search Results for: ${query}</h1>`);
});

app.listen(3000, () => {
    console.log('Vulnerable app listening on port 3000!');
});
