const express = require('express');
const bodyParser = require('body-parser');
const app = express();

// Simulating a database with an array
let comments = [];

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Route to render comments and provide a form to add a comment
app.get('/', (req, res) => {
    let commentsHTML = comments.map(comment => `<p>${comment}</p>`).join('');
    res.send(`
        <h1>Comments</h1>
        ${commentsHTML}
        <form method="post" action="/comment">
            <input type="text" name="comment" placeholder="Enter your comment" />
            <button type="submit">Add Comment</button>
        </form>
    `);
});

// Route to handle new comment submissions
app.post('/comment', (req, res) => {
    const comment = req.body.comment;
    comments.push(comment); // Storing the comment (simulating storing in a database)
    res.redirect('/');
});

app.listen(3000, () => {
    console.log('Vulnerable Stored XSS app listening on port 3000!');
});
