Sanitize Input:
        Modify the post.html template to remove the safe filter.
        This change will ensure that user input is escaped, preventing the browser from executing any injected script.

Test the Fix:
        Try injecting the same XSS payload as before:

    <script>alert('XSS Attack!');</script>

This time, the script should not execute. Instead, it will be displayed as plain text, indicating that the vulnerability has been mitigated.
