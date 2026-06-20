### User Story:

As an admin user, I want to log in using my email and password so that I can access the admin dashboard, and automatically receive an OTP for additional security verification.

### Acceptance Criteria:

- Admin can log in using email and password combination
- System validates admin credentials against existing CustomUser model (kindly make necessary additions to the model to support this)
- Upon successful password verification, system automatically generates and sends OTP via email
- Login endpoint returns success response with message indicating OTP sent
- Failed login attempts are properly logged and rate-limited
- Only users with `is_staff=True` can access this endpoint

### Technical Notes:

- Leverage existing `OTPService.generate_and_store_otp()` method for OTP generation
- Use existing `CustomUser` model and authentication backend
- Utilize existing email notification system (`src.notifier.email.EmailDispatcher` and `NotificationDispatcher`)
- Implement rate limiting using existing `EphemeralFlowThrottle` or similar
- Use existing `OTPLog` model for audit trail
- Create new admin-specific Login endpoint: **`POST /api/v1/admin/auth/login`**
- Implement proper validation for admin-only access
- Ensure OTP is sent to admin's registered email address
- Add comprehensive logging for security monitoring

### Dependencies:

- Existing `OTPService` class
- Existing `CustomUser` model and authentication
- Existing email notification infrastructure
- Existing rate limiting mechanisms
- Existing audit logging system

> Note: Admin accounts will be created via the django admin dashboard. Kindly create one or two for your tests.

### API Endpoint Specification:

```text
POST /api/v1/admin/auth/login
Content-Type: application/json

Request Body:
{
    "email": "admin@example.com",
    "password": "adminPassword123!"
}

Response (Success - 200 OK):
{
    "message": "Login successful. OTP has been sent to your email.",
    "data": {
        "user_id": "admin_user_id",
        "email": "admin@example.com",
        "otp_sent_at": "2025-01-27T10:30:00Z"
    }
}
```
