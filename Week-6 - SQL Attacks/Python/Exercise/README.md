# SQLi Exercise


This template is designed for students to build their own SQLi exercise. The application should include the following features:

- **User Registration**
- **Login**
- **Profile Management** (View and Update)
- **User Search**

## Instructions

### Clone the Repository

```bash
git clone <YOUR_GITHUB_REPO_URL>
```


### Modify and Run the Application

```
python app.py
```

Complete the placeholders in `app.py` to implement the following:

- **User Registration** with input validation and SQL injection protection.
- **Login Functionality** using parameterized queries.
- **Profile Viewing and Editing** with secure queries.
- **Search Functionality** with read-only database mode.

## Security Considerations

- **Input Validation**: Implement whitelisting to ensure valid input.
- **SQL Injection Prevention**: Use parameterized queries throughout the app.
- **Database Permissions**: The search functionality should operate in read-only mode to limit potential attacks.