from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say')
    ]
    
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    # Remove these fields from AbstractUser that we won't use
    first_name = None
    last_name = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email

class UserProfile(models.Model):
    FITNESS_GOALS = [
        ('WL', 'Weight Loss'),
        ('MG', 'Muscle Gain'),
        ('MT', 'Maintenance'),
        ('OT', 'Other')
    ]
    
    ACTIVITY_LEVELS = [
        ('S', 'Sedentary'),
        ('L', 'Lightly Active'),
        ('M', 'Moderately Active'),
        ('A', 'Active'),
        ('V', 'Very Active')
    ]
    
    DIETARY_PREFERENCES = [
        ('NO', 'None'),
        ('VG', 'Vegetarian'),
        ('VN', 'Vegan'),
        ('KT', 'Keto'),
        ('GF', 'Gluten Free'),
        ('OT', 'Other')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    height = models.FloatField(help_text="Height in cm", null=True, blank=True)
    weight = models.FloatField(help_text="Weight in kg", null=True, blank=True)
    fitness_goal = models.CharField(max_length=2, choices=FITNESS_GOALS, default='MT')
    activity_level = models.CharField(max_length=1, choices=ACTIVITY_LEVELS, default='M')
    dietary_preferences = models.CharField(max_length=2, choices=DIETARY_PREFERENCES, default='NO')
    allergies = models.TextField(blank=True)
    health_data_consent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile for {self.user.email}"

class HealthData(models.Model):
    SOURCE_CHOICES = [
        ('MN', 'Manual Entry'),
        ('GF', 'Google Fit'),
        ('AH', 'Apple Health')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_data')
    steps = models.IntegerField(null=True, blank=True)
    calories_burned = models.FloatField(null=True, blank=True)
    heart_rate = models.FloatField(null=True, blank=True)
    sleep_hours = models.FloatField(null=True, blank=True)
    recorded_at = models.DateTimeField()
    source = models.CharField(max_length=2, choices=SOURCE_CHOICES, default='MN')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-recorded_at']
    
    def __str__(self):
        return f"Health data for {self.user.email} at {self.recorded_at}"

class WorkoutCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class WorkoutVideo(models.Model):
    INTENSITY_LEVELS = [
        ('B', 'Beginner'),
        ('I', 'Intermediate'),
        ('A', 'Advanced')
    ]
    
    category = models.ForeignKey(WorkoutCategory, on_delete=models.SET_NULL, null=True, related_name='workouts')
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField()
    intensity_level = models.CharField(max_length=1, choices=INTENSITY_LEVELS, default='B')
    video_url = models.URLField()
    thumbnail_url = models.URLField()
    is_premium = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_plans')
    start_date = models.DateField()
    end_date = models.DateField()
    total_calories = models.FloatField()
    protein_grams = models.FloatField()
    carbs_grams = models.FloatField()
    fat_grams = models.FloatField()
    generated_at = models.DateTimeField(auto_now_add=True)
    ai_model_used = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"Meal Plan for {self.user.email} ({self.start_date} to {self.end_date})"

class Meal(models.Model):
    MEAL_TYPES = [
        ('BR', 'Breakfast'),
        ('LU', 'Lunch'),
        ('DI', 'Dinner'),
        ('SN', 'Snack')
    ]
    
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name='meals')
    day_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    meal_type = models.CharField(max_length=2, choices=MEAL_TYPES)
    name = models.CharField(max_length=100)
    description = models.TextField()
    calories = models.FloatField()
    protein_grams = models.FloatField()
    carbs_grams = models.FloatField()
    fat_grams = models.FloatField()
    ingredients = models.TextField()
    instructions = models.TextField()
    
    def __str__(self):
        return f"{self.get_meal_type_display()} on day {self.day_number}: {self.name}"

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} (${self.price})"

class UserSubscription(models.Model):
    PAYMENT_STATUS = [
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('F', 'Failed'),
        ('R', 'Refunded')
    ]
    
    PLATFORM_CHOICES = [
        ('AP', 'Apple'),
        ('GP', 'Google')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS, default='P')
    transaction_id = models.CharField(max_length=100)
    platform = models.CharField(max_length=2, choices=PLATFORM_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email}'s {self.plan.name} subscription"

class Purchase(models.Model):
    CONTENT_TYPES = [
        ('WV', 'Workout Video'),
        ('MP', 'Meal Plan')
    ]
    
    PLATFORM_CHOICES = [
        ('AP', 'Apple'),
        ('GP', 'Google')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    content_type = models.CharField(max_length=2, choices=CONTENT_TYPES)
    content_id = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    purchase_date = models.DateTimeField()
    platform = models.CharField(max_length=2, choices=PLATFORM_CHOICES)
    transaction_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} purchased {self.get_content_type_display()} #{self.content_id}"

class UserFavoriteWorkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_workouts')
    workout = models.ForeignKey(WorkoutVideo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'workout')
    
    def __str__(self):
        return f"{self.user.email} favorites {self.workout.title}"