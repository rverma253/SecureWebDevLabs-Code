Run the App:

    Start the vulnerable app using the following command:

    bash

    python vulnerable_app.py

    The app will run on http://localhost:5000/.

Login:

    Go to http://localhost:5000/ and log in using the credentials:

    makefile

    Username: admin
    Password: pass

Post a Message:

    After logging in, you can post a message.

Inject XSS:
        Post the following message to trigger an alert:

    <script>alert('XSS Attack!');</script>

    When you post this message, the alert box will pop up in the browser, demonstrating that the input was not sanitized.

Steal Cookies:

    Post the following message to steal the session cookie:


<script>alert(document.cookie);</script>

The session cookie will be displayed in an alert box, demonstrating how XSS can be used to steal sensitive data.
