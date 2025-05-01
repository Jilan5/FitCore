# FitCore
FitCore is a cross-platform fitness application with workout videos and AI-generated meal plans. 
# Proposed Architecture:
itCore’s backend will leverage Django REST Framework (DRF) for building a scalable, RESTful API with JWT-based authentication and OAuth2.0 for third-party logins. The PostgreSQL database will handle structured relational data, while Redis caches high-frequency queries and session data. AWS S3 stores media assets (workout videos, thumbnails). The AI service layer integrates with OpenAI’s API  via a modular adapter pattern, ensuring flexibility in meal plan generation. Health data from Apple HealthKit and Google Fit will be ingested via secure webhooks, normalized, and stored in PostgreSQL. Payment processing relies on Google Play Billing and Apple App Store Connect APIs, with transaction validation handled server-side. API responses follow JSON:API specifications, and Swagger/OpenAPI docs ensure clear developer integration. 
# Database Diagram
[database relational Diagram.png](https://github.com/Jilan5/FitCore/blob/main/database%20relational%20Diagram.png)
# API Endpoints

**Authentication (10 hours)**

POST /api/auth/register - User registration
POST /api/auth/login - Email/password login
POST /api/auth/social - Social login (Google/Apple)
POST /api/auth/refresh - Refresh JWT token
POST /api/auth/logout - Invalidate token

**User Profile (15 hours)**

GET /api/users/{userid} - Get current user profile
PUT /api/users/{userid} - Update profile
GET /api/users/{userid}/health-data - Get health data
POST /api/users/{userid}/health-data - Submit health data (manual)
GET /api/users/{userid}/health-data/sync - Initiate health data sync

**Workouts (16 hours)**
GET /api/workouts/categories - List all categories
GET /api/workouts - List all workouts (filter by category, intensity)
GET /api/workouts/{id} - Get workout details
GET /api/workouts/recommended - Get recommended workouts based on user profile
POST /api/workouts/{id}/favorite - Favorite a workout
GET /api/workouts/favorites - Get favorite workouts

**Meal Plans (30 hours)**

GET /api/meal-plans/current - Get current meal plan
POST /api/meal-plans/generate - Generate new meal plan
PUT /api/meal-plans/{id}/adjust - Adjust meal plan
GET /api/meal-plans/history - Get meal plan history
GET /api/meal-plans/{id} - Get meal plan details

**Payments (20 hours)**

GET /api/subscriptions/plans - List available subscription plans
POST /api/subscriptions/subscribe - Create subscription
GET /api/subscriptions/status - Get user's subscription status
POST /api/purchases/verify - Verify in-app purchase
GET /api/purchases/history - Get purchase history

**Admin (40 hours)**

POST /admin/workouts - Create workout
PUT /admin/workouts/{id} - Update workout
GET /admin/users - List users
GET /admin/analytics - Get analytics data
POST /admin/meal-templates - Create meal template
GET /admin/subscriptions - List all subscriptions
