OTP VERIFICATION FOR AADHAAR - IMPLEMENTATION GUIDE
======================================================

## System Overview

Complete OTP-based Aadhaar verification system with:
- 6-digit OTP generation and validation
- SMS sending (Mock, Twilio, AWS SNS)
- OTP expiration (10 minutes)
- Attempt limiting (5 attempts max)
- Profile section locking until verified
- Responsive UI with countdown timer

---

## User Flow

```
1. Student enters Aadhaar number (XXXX XXXX XXXX)
   ↓
2. System validates format (12 digits, no leading 0/1)
   ↓
3. OTP Verification section appears
   ↓
4. Student clicks "Request OTP"
   ↓
5. OTP sent to registered mobile (shown as masked: XXXX XXXX 1234)
   ↓
6. Countdown timer starts (10 minutes)
   ↓
7. Student receives SMS with 6-digit OTP
   ↓
8. Student enters OTP in input field
   ↓
9. Clicks "Verify OTP"
   ↓
10. System checks OTP (server-side verification)
    ↓
11. If correct:
    ✅ Aadhaar marked as VERIFIED
    ✅ Input becomes read-only
    ✅ Skills & Portfolio sections UNLOCK
    ✅ Can now fill profile details
    ↓
12. Save Profile - Success!

If incorrect:
❌ Error message shown
❌ Attempts counter decremented
❌ User can retry until 5 attempts exhausted
```

---

## API Endpoints

### 1. REQUEST OTP
**Endpoint:** `POST /student/aadhaar/request-otp`

**Request Body:**
```json
{
  "aadhaar": "234567890123",
  "mobile": "9876543210"  // Optional
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "OTP sent successfully",
  "mobile_masked": "XXXX XXXX 1234",
  "expires_in_seconds": 600
}
```

**Response (Error):**
```json
{
  "success": false,
  "message": "Invalid Aadhaar number"
}
```

### 2. VERIFY OTP
**Endpoint:** `POST /student/aadhaar/verify-otp`

**Request Body:**
```json
{
  "aadhaar": "234567890123",
  "otp": "123456"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Aadhaar verified successfully!",
  "verified": true,
  "verified_at": "2026-03-18T10:30:00"
}
```

**Response (Incorrect OTP):**
```json
{
  "success": false,
  "message": "Invalid OTP. 3 attempts remaining.",
  "attempts_remaining": 3,
  "is_expired": false
}
```

### 3. GET OTP STATUS
**Endpoint:** `GET /student/aadhaar/otp-status?aadhaar=234567890123`

**Response:**
```json
{
  "success": true,
  "status": {
    "has_active_otp": true,
    "is_expired": false,
    "attempts_remaining": 4,
    "time_remaining": 450,
    "mobile_masked": "XXXX XXXX 1234",
    "message": "OTP valid for 7 minutes"
  }
}
```

### 4. RESEND OTP
**Endpoint:** `POST /student/aadhaar/resend-otp`

**Request Body:**
```json
{
  "aadhaar": "234567890123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "OTP resent successfully",
  "expires_in_seconds": 600
}
```

---

## Database Structure

### AadhaarOTP Table
```sql
CREATE TABLE aadhaar_otp (
  id INTEGER PRIMARY KEY,
  student_id INTEGER NOT NULL FOREIGN KEY,
  aadhaar_number VARCHAR(12) NOT NULL,
  mobile_number VARCHAR(20),
  otp_code VARCHAR(6) NOT NULL,
  is_verified BOOLEAN DEFAULT FALSE,
  attempt_count INTEGER DEFAULT 0,
  expires_at DATETIME,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  verified_at DATETIME
);
```

---

## SMS Provider Configuration

### Option 1: Mock Mode (Development)
Set in `.env`:
```
SMS_PROVIDER=mock
```
OTP will be printed to console and logged to `/tmp/aadhaar_otp_log.txt`

### Option 2: Twilio (Production)
Set in `.env`:
```
SMS_PROVIDER=twilio
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1XXXXXXXXXX
```

Install Twilio:
```bash
pip install twilio
```

### Option 3: AWS SNS
Set in `.env`:
```
SMS_PROVIDER=aws
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
```

Install AWS SDK:
```bash
pip install boto3
```

---

## Frontend Components

### OTP Verification Section (HTML)
```html
<div id="otp_verification_section" style="...">
  <!-- Request OTP Button -->
  <button id="request_otp_btn" onclick="requestOTP()">Request OTP</button>

  <!-- OTP Input -->
  <input id="otp_input" type="text" placeholder="Enter 6-digit OTP" maxlength="6" />

  <!-- Verify OTP Button -->
  <button id="verify_otp_btn" onclick="verifyOTP()">Verify OTP</button>

  <!-- Status Messages -->
  <div id="otp_status"></div>

  <!-- Countdown Timer -->
  <div id="otp_timer"></div>

  <!-- Resend Button -->
  <button id="resend_otp_btn" onclick="resendOTP()" style="display:none;">Resend OTP</button>
</div>
```

### JavaScript Functions

**requestOTP()**
- Validates Aadhaar format
- Calls API to generate and send OTP
- Shows mobile number (masked)
- Starts countdown timer
- Hides request button, shows resend

**verifyOTP()**
- Validates OTP format (6 digits)
- Calls API to verify OTP
- On success:
  - Marks Aadhaar as verified
  - Makes input read-only
  - Unlocks Skills & Portfolio sections
  - Updates UI display
- On failure:
  - Shows error message
  - Shows remaining attempts
  - Allows retry

**resendOTP()**
- Requests new OTP
- Rate limited (max 3 requests per minute)
- Resets countdown timer
- Shows updated mobile

**updateLockedSections()**
- Checks if Aadhaar is VERIFIED (not just filled)
- Only unlocks sections if OTP verified
- Shows hover messages for locked sections

**startOTPTimer(seconds)**
- Displays countdown (MM:SS format)
- Updates every second
- Stops after 10 minutes
- Re-enables resend button

---

## Security Features

✅ **OTP Validation**
- 6-digit random generation
- 10-minute expiration
- 5 attempts maximum
- Server-side verification

✅ **Aadhaar Protection**
- 12-digit format validation
- Cannot start with 0 or 1
- Stored securely in database
- Masked display: XXXX XXXX 1234

✅ **Rate Limiting**
- Max 5 verification attempts per OTP
- Max 3 resend requests per minute
- Prevents brute force attacks

✅ **SMS Security**
- OTP never shown in clear in logs
- Mobile number masked: XXXX XXXX 1234
- Uses HTTPS for API calls

---

## Error Handling

### Invalid Aadhaar Format
```
❌ "Invalid Aadhaar number"
→ User must enter exactly 12 digits
```

### OTP Send Failed
```
❌ "OTP generated but SMS sending failed"
→ Check SMS provider credentials
→ Check mobile number format
```

### OTP Expired
```
❌ "OTP has expired. Please request a new one."
→ User can click "Resend OTP"
```

### Maximum Attempts Exceeded
```
❌ "Maximum verification attempts exceeded"
→ User must wait for OTP to expire
→ Or request new OTP
```

### Invalid OTP Format
```
❌ "Enter valid 6-digit OTP"
→ OTP must be exactly 6 digits
→ Only numbers allowed
```

---

## Testing

### Test Case 1: Complete Verification Flow
1. Enter Aadhaar: 234567890123
2. Click "Request OTP"
3. See: "OTP sent to XXXX XXXX 1234"
4. Check console/logs for OTP
5. Enter OTP in input field
6. Click "Verify OTP"
7. Expected: ✅ Verified! Sections unlocked

### Test Case 2: OTP Expiration
1. Request OTP
2. Wait 10+ minutes
3. Try to verify expired OTP
4. Expected: ❌ "OTP has expired"

### Test Case 3: Wrong OTP
1. Request OTP
2. Enter wrong OTP (e.g., 000000)
3. Click Verify
4. Expected: ❌ Shows error + attempts remaining
5. Attempt limit reached: ❌ "Max attempts exceeded"

### Test Case 4: Rate Limiting
1. Request OTP 3 times within 1 minute
2. Try to resend 4th time immediately
3. Expected: ❌ "Too many OTP requests"

### Test Case 5: Profile Unlock
1. Enter Aadhaar without verification
2. Try to click Skills field
3. Expected: Cannot interact (locked, grayed out)
4. After OTP verification
5. Expected: Skills field unlocked and interactive

---

## Production Checklist

- [ ] Choose SMS provider (Twilio/AWS recommended)
- [ ] Get API credentials from SMS provider
- [ ] Add credentials to `.env` file
- [ ] Test OTP delivery with test number
- [ ] Set proper OTP expiration (10 min recommended)
- [ ] Configure attempt limits (5 recommended)
- [ ] Enable HTTPS for all API calls
- [ ] Remove debug endpoint in production:
  ```python
  # Comment out /student/aadhaar/debug-otp route
  ```
- [ ] Set up error logging and monitoring
- [ ] Add SMS cost tracking (for billing)
- [ ] Create admin dashboard for verification stats
- [ ] Document support process for failed verifications

---

## Troubleshooting

### OTP Not Sending?
1. Check SMS provider credentials in `.env`
2. Verify mobile number format (10-12 digits recommended)
3. Check SMS provider account balance
4. Review SMS provider logs for errors
5. Test with mock provider first

### OTP Verification Fails?
1. Check system time (clock sync important)
2. Verify OTP hasn't expired (10 min limit)
3. Check remaining attempts (5 max)
4. Ensure exact 6-digit OTP entered
5. Check database for OTP record

### Sections Not Unlocking?
1. Verify Aadhaar field has green border
2. Check browser console for JavaScript errors
3. Verify `updateLockedSections()` is called
4. Check that OTP is in verified state
5. Reload page and retry

### Mobile Number Masking Issue?
1. Ensure mobile number passed to SMS function
2. Check mask_phone() function
3. Verify mobile format before sending OTP

---

## Files Modified

1. **otp_verification.py** - OTP logic & SMS integration
2. **otp_routes.py** - Flask API endpoints
3. **app.py** - Added AadhaarOTP model & route imports
4. **templates/dashboard_student.html** - OTP UI & JavaScript
5. **Database** - New aadhaar_otp table created

---

## Environment Variables Template

```bash
# SMS Provider Configuration
SMS_PROVIDER=mock  # Options: mock, twilio, aws

# Twilio Configuration (if using Twilio)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1XXXXXXXXXX

# AWS Configuration (if using AWS SNS)
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
```

---

END OF DOCUMENTATION
======================================================