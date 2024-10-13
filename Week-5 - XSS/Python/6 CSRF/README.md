Steps to Perform the CSRF Attack:

Run the Vulnerable App:
        Start the vulnerable app on port 5000:

    python vulnerable_app.py

Login to the Vulnerable App:

    Visit http://127.0.0.1:5000/ and log in using:

        Username: admin
        Password: pass

Simulate the CSRF Attack:
        Open the attacker's form (hosted on a different domain) or save the HTML file (attacker.html) locally and open it in your browser.
        The attacker form will simulate the transfer of $1000 when the victim (logged into the vulnerable app) clicks the button.

Effect of the Attack:
        The malicious form will submit a POST request to http://127.0.0.1:5000/transfer, transferring $1000 without the user’s explicit consent.
        The victim remains unaware that their session was used to perform the unauthorized action.

CSRF Attack Demonstration:

When the victim (logged in to the vulnerable app) clicks the "Click Here to Claim Your Prize!" button, the following steps occur:

    The attacker form submits a POST request to http://127.0.0.1:5000/transfer with a hidden amount of $1000.
    Since the victim is logged in and their session is active, the vulnerable app processes the request as if it was a legitimate request from the user.
    The funds are transferred without the victim's knowledge, demonstrating a successful Cross-Site Request Forgery (CSRF) attack.
