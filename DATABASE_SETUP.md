# Database Connection Setup Guide

## Quick Setup Steps

### Step 1: Configure MySQL Password

The error shows that MySQL requires a password. You need to update the password in `config/database.py`.

**Option A: If you know your MySQL password**
1. Open `config/database.py`
2. Find line 16: `'password': '',`
3. Replace the empty string with your password:
   ```python
   'password': 'your_mysql_password',
   ```

**Option B: If you don't know your MySQL password**

#### For XAMPP Users:
- Default password is usually **empty** (already set)
- If that doesn't work, try: `''` (empty string)
- Or check XAMPP Control Panel → MySQL → Config → my.ini

#### For WAMP Users:
- Default password is usually **empty**
- Check WAMP tray icon → MySQL → my.ini

#### For Standalone MySQL:
- You set the password during installation
- If forgotten, you can reset it or check MySQL Workbench

### Step 2: Test Database Connection

Run the test script:
```bash
python test_db_connection.py
```

This will:
- Test MySQL server connection
- Check if database exists
- Initialize database schema if needed

### Step 3: Initialize Database (if needed)

The database will be created automatically when you run:
```bash
python app.py
```

Or manually initialize:
```bash
python test_db_connection.py
# Answer 'y' when asked to initialize
```

## Common Issues & Solutions

### Issue 1: "Access denied for user 'root'@'localhost'"
**Solution**: MySQL requires a password. Update `config/database.py` with your MySQL password.

### Issue 2: "Can't connect to MySQL server"
**Solution**: 
- Make sure MySQL service is running
- For XAMPP: Start MySQL from XAMPP Control Panel
- For WAMP: Start MySQL from WAMP tray icon
- For standalone: Check Windows Services → MySQL

### Issue 3: "Unknown database"
**Solution**: This is normal. The database will be created automatically when you run the app.

## Manual Database Setup (Alternative)

If automatic setup doesn't work, you can manually create the database:

1. Open MySQL command line or phpMyAdmin
2. Create database:
   ```sql
   CREATE DATABASE nozomi.proxy.rlwy.net;
   ```
3. Run the schema:
   ```bash
   mysql -u root -p fake_job_detection < database/schema.sql
   ```

## Testing Connection

After updating the password, test the connection:
```bash
python test_db_connection.py
```

## Next Steps

Once database is connected:
1. Create admin account: `python create_admin.py`
2. Run Flask app: `python app.py`
3. Access at: `http://localhost:5000`
