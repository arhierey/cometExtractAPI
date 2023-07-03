QUERY = '''
    mutation authenticate($email: EmailType!, $password: String!, $signupToken: String)
    {\n  authenticate(email: $email, password: $password, signupToken: $signupToken) {\n    ...User\n    }\n}
    \n\nfragment User on User
    {\n  email\n  firstName\n  jobTitle\n  lastName\n
    phoneNumber\n  profilePictureUrl\n
    corporate {\n    role\n    company {\n      id\n      skipTermsValidation\n    }\n    }\n
    freelance {\n   isAvailable\n    ...LinkedInImport\n    }\n
    teamMember {\n    accountManager\n    freelancerAgent\n    }\n  \n}
    \n\nfragment LinkedInImport on Freelance
    {\n  biography\n    experienceInYears\n
    experiences {\n    startDate\n    endDate\n
    companyName\n    description\n    location\n
    skills {\n      name\n    }\n    }\n    \n}\n
    '''

HTML_FORM = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Request form</title>
    </head>
    <body>
        <form id="loginForm" action="/fetch" method="POST">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required><br><br>

            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required><br><br>

            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    '''