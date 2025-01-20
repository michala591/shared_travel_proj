# Shared Travel App

The **Shared Travel App** is a platform designed to simplify shared car trips by connecting drivers and passengers. It provides an intuitive interface for managing trips, coordinating travel routes, and dynamically handling seat availability.

---

## Features

### Driver Operations (after login)
- **Trip Management:**
  - Create, view, update, and delete trips (`trip-detail`).
- **Passenger Management:**
  - View the list of passengers for a trip.
- **Car Management:**
  - Add, view, update, and delete cars (`car-detail`).
- **Locations:**
  - Add and search locations.
- **Trip Creation:**
  - Add new trips.

### Passenger Operations
- **Available Trips:**
  - View and search available trips.
- **Reservations:**
  - Join or cancel a trip, dynamically freeing up seats.

### General User Operations
- Register, log in, and log out.
- View active trips and all trips.
- **Invite to Trip:**
  - Requires authentication to join a trip.

---

## Technologies Used

### Backend
- **Framework:** Django Rest Framework
- **Database:** 
  - Development: SQLite
  - Production: PostgreSQL (hosted on Render)
- **Authentication:** JWT-based login and registration
- **Notifications:** Plan to implement email updates for trip changes or cancellations soon.

### Frontend
- **Framework:** React 
- **HTTP Client:** Axios for API communication (async/await)
- **UI Framework:** Bootstrap for responsive and user-friendly interfaces
- **Deployment:** Hosted on Render

---

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js and npm (for frontend development)
- PostgreSQL (for production)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/michala591/shared_travel_proj.git
   cd shared-travel-app
   ```

2. Set up the backend:
   ```bash
   cd backend
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

3. Set up the frontend:
   ```bash
   cd ../frontend
   npm install
   npm start
   ```

4. Update `.env` with environment variables for:
   - Secret key
   - Email service credentials
   - Database connection (for production)

---

## App Flow

### Screens
1. **Login/Register**: For users to sign up and access the system.
2. **Driver Dashboard**: Manage trips, cars, and passengers.
3. **Available Trips**: For passengers to view and search trips.
4. **Logout**: Log out from the system.

---

## Roadmap
- Implement React-based frontend.
- Add dashboards for visualizations (e.g., occupancy rates).
- Include a feature for passengers to favorite routes.
- Extend notifications to SMS.

---

## Contributions
Contributions are welcome! Fork the repository and submit a pull request with your changes.

---

## License
This project is licensed under the MIT License.

---