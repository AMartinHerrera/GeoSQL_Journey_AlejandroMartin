const express = require('express');

const app = express();
const port = 4000;

app.use('/static', express.static(__dirname + '/client'));

app.get('/', function (req, res) {
    res.sendfile('client/index.html');
})

app.listen(port, () => {
    console.log(`Listening on port ${port}`);

    if (process.send) {
        process.send('online');
    }
});