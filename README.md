Scan4Good 
Scan4Good is a full-stack health risk assessment platform that leverages Artificial Intelligence to provide personalized health insights. It combines a modern Angular frontend, a robust Spring Boot orchestrator, and a Python based AI microservice powered by Google Gemini and Scikit-learn. System ArchitectureThe application follows a microservices-inspired architecture where the Spring Boot backend acts as an API Gateway and Orchestrator, managing data flow between the user, the database, and the AI inference engine.Code snippetgraph TD
    %% Nodes
    User((User))
    Angular[Frontend: Angular App\n(Port 4200)]
    SpringBoot[Backend: Spring Boot API\n(Port 8080)]
    Flask[AI Service: Flask & Python\n(Port 5000)]
    MySQL[(MySQL Database)]
    Gemini[Google Gemini API]

    %% Styles
    style Angular fill:#dd0031,stroke:#333,stroke-width:2px,color:white
    style SpringBoot fill:#6db33f,stroke:#333,stroke-width:2px,color:white
    style Flask fill:#000000,stroke:#333,stroke-width:2px,color:white
    style MySQL fill:#4479a1,stroke:#333,stroke-width:2px,color:white
    style Gemini fill:#4285f4,stroke:#333,stroke-width:2px,color:white

    %% Edges
    User -- "Interacts" --> Angular
    Angular -- "1. Submit Health Data (JSON)" --> SpringBoot
    SpringBoot -- "2. Predict Risk (HTTP POST)" --> Flask
    Flask -- "3. Generate Advice" --> Gemini
    Gemini -- "4. Return AI Advice" --> Flask
    Flask -- "5. Return Risk + Advice" --> SpringBoot
    SpringBoot -- "6. Fetch Health Tips" --> MySQL
    MySQL -- "7. Return Stored Tips" --> SpringBoot
    SpringBoot -- "8. Full Assessment Response" --> Angular
Key FeaturesAI-Powered Analysis: Uses a Random Forest classifier to predict health risks based on lifestyle data.Generative AI Advice: Integrates Google Gemini to provide compassionate, context aware health recommendations.Full-Stack Modernity: Built with Angular 21 (Standalone Components) and Java 21.Automated CI/CD: A GitHub Actions pipeline ensures code quality by automatically building and testing both frontend and backend on every push.🛠 Tech StackComponentTechnologyDescriptionFrontendAngular + TypeScriptReactive UI with standalone components & Signals.BackendJava 21 + Spring BootREST API, Business Logic, Data Orchestration.AI EnginePython + FlaskScikit-learn (ML) & Google Generative AI (LLM).DatabaseMySQLPersistent storage for health tips and user records.DevOpsGitHub ActionsAutomated CI pipeline for Build & Test.🚀 Getting StartedPrerequisitesJava 21Node.js v20+Python 3.10+MySQL Server1. Database SetupCreate a MySQL database named scan4good and configure your credentials in application.properties.2. Python AI ServiceNavigate to the backend directory and start the Flask service.Bashcd backend
pip install flask pandas scikit-learn google-generativeai
python app.py
# Service runs on http://localhost:5000
3. Spring Boot BackendOpen a new terminal and start the Java application.Bashcd backend
./mvnw spring-boot:run
# Service runs on http://localhost:8080
4. Angular FrontendOpen a third terminal and start the frontend.Bashcd frontend/scan4good-frontend
npm install
ng serve
# App runs on http://localhost:4200
⚙️ CI/CD PipelineThis repository uses GitHub Actions to maintain code quality. The pipeline defined in .github/workflows/ci.yml triggers on every push to main:Backend Job:Sets up JDK 21.Runs mvn package to compile Java code and run JUnit tests.Frontend Job:Sets up Node.js.Installs dependencies (npm ci).Runs Unit Tests (ng test) in Headless mode.Builds the production artifact (ng build).🔮 Future ImprovementsDockerization: Containerize services using Docker Compose for one-command startup.Security: Add JWT authentication for secure user profiles.Cloud Deployment: Deploy to AWS (EC2/ECS) or Azure App Service.Developed by Keenan Dias
