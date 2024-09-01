## Project Overview
The Digital School Attendance System is a web-based application designed to serve as a digital attendance register for schools. The system is built to enhance student safety by notifying parents if their child is absent, takes early leave, or arrives late. By tracking student attendance and sending real-time notifications, this system aims to reduce the increasing incidents of kidnapping before and after school hours.

## Why This Project Is Useful
This project addresses a critical concern in school environments: student safety. With the rise in kidnapping cases, the need for a reliable and efficient system to monitor student attendance has never been greater. The Digital School Attendance System provides a proactive approach by:
- Ensuring that parents are immediately informed about their child's attendance status.
- Allowing schools to maintain accurate records of student attendance.
- Reducing the response time in case of any suspicious or unexpected absence.

## Getting Started

### Setup and Configuration

To get started with this project, follow the instructions below:

1. **Fork the Repository:**
   - On GitHub, navigate to the repository you want to fork.
   - Click the "Fork" button at the top right of the page.

2. **Clone the Repository:**
   - On GitHub, copy the URL of the repository you just forked.
   - Open your terminal or command prompt and navigate to the folder where you want to clone the repository.
   - Run the following command:
     ```bash
     git clone <URL-of-your-forked-repository>
     ```
   - Navigate into the cloned repository folder:
     ```bash
     cd <repository-name>
     ```

3. **Set Up the Virtual Environment:**
   - Create a virtual environment:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - **Windows:**
       ```bash
       venv\Scripts\activate
       ```
     - **Mac/Linux:**
       ```bash
       source venv/bin/activate
       ```

4. **Install Requirements:**
   - Install the required Python packages:
     ```bash
     pip install -r requirements.txt
     ```

5. **Run the Application:**
   - Start the Django development server:
     ```bash
     python manage.py runserver
     ```

6. **Set Up the React Frontend:**
   - Navigate to the folder where React is installed (e.g., frontend):
     ```bash
     cd frontend
     ```
     
7. **Install the React dependencies:**
     ```bash
     npm install
     ```

8. **Start the React development server:**
     ```bash
     npm start
     ```
### Contributing

To contribute to this project, follow these guidelines:

1. **Create a New Branch:**
   - Always create a new branch for your changes. For example:
     ```bash
     git checkout -b feature/new-feature
     ```

2. **Make Your Changes:**
   - Make the necessary changes in your branch.

3. **Stage and Commit Your Changes:**
   - Stage your changes:
     ```bash
     git add .
     ```
   - Commit your changes with a descriptive message:
     ```bash
     git commit -m "Add detailed description of your changes"
     ```

4. **Push Your Branch:**
   - Push your branch to GitHub:
     ```bash
     git push origin feature/new-feature
     ```

5. **Create a Pull Request:**
   - On GitHub, navigate to the "Pull Requests" tab.
   - Click "New Pull Request" and select your branch.
   - Add a descriptive title and description, then submit the pull request for review.

## Maintainers and Contributors
This project is actively maintained by:

- [M. Yusha Ally](https://github.com/Yusha2849)
- [A. Zishaan Banoo](https://github.com/azb5499)
- [Ilhaam Kader](https://github.com/ilhaamkader)
- [Ashlee Imrith](https://github.com/Ashlee001)
- [M. Shuaib Charfaray](https://github.com/)
- [Singethwe Mzila](https://github.com/)
- [Londiwe Buthelezi](https://github.com/)
- [Ngesihle Mthembu](https://github.com/)

## Components

The project uses Django for the backend, React for the frontend, and PostgreSQL for the database. 

### Folder Structure

- `backend/`: Contains Django application code.
- `frontend/`: Contains React application code.
- `docs/`: Contains project documentation.
- `requirements.txt`: Lists the Python dependencies.
- `.env`: Contains environment variable configurations.

### Git & GitHub

This project uses version control with Git and is hosted on GitHub. 

#### Branch Structure

- **main**: The deployment-ready branch with stable changes.
- **development**: The branch for development changes, including features and fixes.
- **frontend**: The branch for front-end changes and features.
- **backend**: The branch for back-end changes and features.
- **docs**: The branch for documentation-related updates.

#### Branch Management

- **main**: Contains the stable, production-ready code.
- **development**: Contains the latest development changes that are tested and validated.
- **frontend**: Contains all changes related to the front-end. Features and pages are developed here.
- **backend**: Contains all changes related to the back-end. New features and updates are developed here.
- **docs**: For project documentation and planning.

