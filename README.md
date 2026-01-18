# Scan4Good 🏥

## Overview

Scan4Good is a full-stack health risk assessment application built using Angular, Spring Boot, and Python. It allows users to input their lifestyle habits (such as sleep, exercise, and diet) to receive an immediate health risk assessment. The application uses a hybrid approach: a Spring Boot backend orchestrates the data, while a Flask microservice leverages AI (Random Forest & Google Gemini) to generate predictions and personalized advice.

## Features

* **Risk Assessment:** Users can calculate their health risk (Low, Medium, High) based on inputs like BMI, smoking habits, and activity levels.
* **AI-Powered Advice:** The application integrates Google Gemini (GenAI) to provide compassionate, context-aware health recommendations specific to the user's profile.
* **Health Tips:** Users receive curated health tips stored in a MySQL database based on their calculated risk level.
* **Modern UI:** The application features a responsive, user-friendly interface built with Angular 21.
* **CI/CD Pipeline:** The project includes a GitHub Actions pipeline that automatically builds and tests both the frontend and backend on every push.

## System Architecture

The following diagram illustrates how the Angular frontend communicates with the Spring Boot API Gateway, which coordinates with the Python AI service and MySQL database.

```mermaid
graph TD
    User((User))
    Angular[Frontend: Angular App]
    SpringBoot[Backend: Spring Boot API]
    Flask[AI Service: Flask & Python]
    MySQL[(MySQL Database)]
    Gemini[Google Gemini API]

    %% Flow
    User -- "1. Enters Data" --> Angular
    Angular -- "2. Sends JSON" --> SpringBoot
    SpringBoot -- "3. Requests Prediction" --> Flask
    Flask -- "4. Generates Advice" --> Gemini
    Gemini -- "5. Returns AI Text" --> Flask
    Flask -- "6. Returns Risk + Advice" --> SpringBoot
    SpringBoot -- "7. Fetches Tips" --> MySQL
    SpringBoot -- "8. Returns Final Result" --> Angular
