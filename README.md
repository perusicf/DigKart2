# Patient Records System

A web-based application for managing patient records in a clinical setting. The system supports three user roles: doctor, medical staff, and administrator, each with their own interface and permissions.

## Features

- Secure user authentication and role-based access control
- Patient record management
- Medical history tracking
- Diagnosis and treatment records
- User management (admin only)
- Responsive design with modern UI

## Prerequisites

- Node.js (v16 or higher)
- npm (v7 or higher)

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## User Roles

### Doctor
- Search patient records
- Add/edit diagnoses and therapies
- Print medical records

### Medical Staff
- Search and view patient records

### Administrator
- Manage users and patients
- Assign user permissions
- Full system access

## API Integration

The frontend is designed to work with a RESTful API. Update the API endpoints in the components to match your backend implementation.

## Building for Production

To build the application for production:

```bash
npm run build
```

The built files will be in the `dist` directory.

## License

MIT 