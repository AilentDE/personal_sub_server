# personal_sub_server

## Project Overview

This project originated from the need to enhance certain functionalities lacking in the backend of a large-scale website project I am currently responsible for. It is developed as a small-scale project to address these specific requirements. The current implemented features include:

1. Email notification to specific users under certain conditions.
2. Implementation of HMAC-SHA1 protection for endpoint requests.
3. Creation of presigned_url for AWS S3 resources.

## Technical Specifications

The project adopts the following technical specifications:

1. Endpoint functionalities are implemented using FastAPI.
2. Docker is used to build the image, which is stored in AWS ECR.
3. AWS Lambda is utilized to create instances.
4. AWS SES is employed to send email notification messages.

## Usage Instructions

### 1. Docker Image

The `.dockerignore` file is already configured, allowing for the direct building of the image. Please take note of configuring the environment variables, which can be found in the `schema/setting.py` file.

### 2. Deployment Method

For detailed deployment instructions, refer to the [HackMD note](https://hackmd.io/@Ailent-DE/Skt76Ntwa), documenting the specific deployment steps. Feel free to check it out if you are interested.

---
For further inquiries, feel free to reach out to the project maintainer. Thank you for your interest and support!