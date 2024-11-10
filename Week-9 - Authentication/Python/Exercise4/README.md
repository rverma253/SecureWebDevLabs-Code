# Authentication & Login Security

This project builds on the code from Week 6 (SQL Injection), with enhanced security features in the areas of user registration, login, and authentication.

## Overview
In this exercise, we focus on securing the web application’s authentication process. We have added:

- Stronger password policies.
- Login attempt limits with account lockout.
- Secure password hashing and salting using bcrypt.
- These enhancements aim to provide protection against brute-force attacks and improve overall authentication security.

## Features
### 1. Registration with Strong Password Policy
Enforces password complexity requirements:
- Minimum 8 characters
- Must include uppercase, lowercase, number, and special character.
- Uses bcrypt for hashing and salting passwords securely.
### 2. Login with Account Lockout Mechanism
Tracks failed login attempts per user.
- Locks the account for 5 minutes after 3 failed login attempts to prevent brute-force attacks.
- Logs suspicious login activities (e.g., repeated failed attempts, lockouts, and attempts with non-existent usernames) in a security.log file.