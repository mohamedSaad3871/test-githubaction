# PowerShell script to test Workout API
# Run: .\test_api.ps1

$baseUrl = "http://localhost:5001/api"

Write-Host "Testing Workout API..." -ForegroundColor Green
Write-Host ""

# 1. Health Check
Write-Host "1. Health Check..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/health" -Method GET
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
    $content = $response.Content | ConvertFrom-Json
    Write-Host "Message: $($content.message)" -ForegroundColor Cyan
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# 2. Add User
Write-Host "2. Adding User..." -ForegroundColor Yellow
$userData = @{
    name = "Ahmed Mohamed"
    age = 30
    weight = 80.0
    height = 180.0
    goal = "muscle_gain"
    level = "intermediate"
    days_per_week = 4
    equipment = "dumbbells, barbell"
    health_issues = ""
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "$baseUrl/users" -Method POST -ContentType "application/json" -Body $userData
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
    $content = $response.Content | ConvertFrom-Json
    Write-Host "User ID: $($content.user_id)" -ForegroundColor Cyan
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# 3. Generate Workout Plan
Write-Host "3. Generating Workout Plan..." -ForegroundColor Yellow
$workoutData = @{
    name = "Sara Ali"
    age = 25
    weight = 60.0
    height = 165.0
    goal = "lose_weight"
    level = "beginner"
    days_per_week = 3
    equipment = "bodyweight"
    health_issues = ""
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "$baseUrl/generate-workout-plan" -Method POST -ContentType "application/json" -Body $workoutData
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
    $content = $response.Content | ConvertFrom-Json
    Write-Host "Goal: $($content.goal)" -ForegroundColor Cyan
    Write-Host "Plan days: $($content.workout_plan.Count)" -ForegroundColor Cyan
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# 4. Get Exercises
Write-Host "4. Getting Exercises..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/exercises" -Method GET
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
    $content = $response.Content | ConvertFrom-Json
    Write-Host "Total exercises: $($content.total)" -ForegroundColor Cyan
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

Write-Host "All tests completed!" -ForegroundColor Green