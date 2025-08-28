# ⚡ Electricity Consumption Analysis Dashboard

[](https://www.python.org/)
[](https://streamlit.io/)
[](https://opensource.org/licenses/MIT)

An interactive web dashboard built with Streamlit and Pandas to analyze and visualize customer electricity billing data from a MySQL database. This project transforms raw billing records into actionable insights on consumption trends, revenue, and customer behavior.


-----

## 📸 Screenshot

<img width="1861" height="407" alt="image" src="https://github.com/user-attachments/assets/1d02aee6-dff0-45fc-ac6c-0a79ad20259a" />
<img width="1758" height="788" alt="image" src="https://github.com/user-attachments/assets/08be59bf-ef63-4b39-8820-02546f1ec984" />
<img width="1774" height="624" alt="image" src="https://github.com/user-attachments/assets/b1ae084f-ca18-4faf-ac0c-3b28ed9d744a" />


-----

## ✨ Key Features

  * **Interactive Dashboard:** A user-friendly web interface built with Streamlit for seamless data exploration.
  * **KPI Metrics:** At-a-glance cards displaying key metrics such as Total Revenue, Average Consumption, and Unpaid Bills.
  * **Trend Analysis:** A line chart visualizing total electricity consumption over time to identify seasonal patterns.
  * **Customer Segmentation:** A bar chart identifying the top consumers based on their total bill amount.
  * **Data Explorer:** An interactive table that allows for viewing and sorting the raw, underlying data.

-----

## 🛠️ Tech Stack

  * **Front-End:** Streamlit
  * **Data Analysis:** Pandas, NumPy
  * **Data Visualization:** Matplotlib, Seaborn
  * **Database:** MySQL
  * **ETL & Data Generation:** Faker
  * **Configuration:** python-dotenv, Streamlit Secrets

-----

## 🚀 Local Setup and Installation

Follow these steps to set up and run the project on your local machine.

### Prerequisites

  * Python 3.9+
  * Git

### 1\. Clone the Repository

```bash
git clone https://github.com/YourUsername/electricity-dashboard.git
cd electricity-dashboard
```

### 2\. Create a Virtual Environment

It's recommended to create a virtual environment to manage dependencies.

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3\. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4\. Set Up Environment Variables

Create a file named `.env` in the root directory and add your local database credentials.

```
# .env file
DB_HOST=localhost
DB_USER=your_local_user
DB_PASSWORD=your_local_password
DB_NAME=electricity
```

### 5\. Set Up and Populate the Database

Run these scripts to create the database schema and populate it with mock data.

```bash
# Create the tables
python database_setup.py

# Generate mock data
python generate_data.py
```

### 6\. Launch the Streamlit App

```bash
streamlit run dashboard.py
```

The application should now be running and accessible in your web browser at `http://localhost:8501`.

-----

## 🗂️ Database Schema

The project uses a simple relational schema with two main tables:

  * **`customer`**: Stores customer information like name, address, and meter number.
      * `cid`, `name`, `address`, `email`, `phone`, `meterno` (Primary Key)
  * **`bill`**: Stores billing records for each customer.
      * `bill_id` (Primary Key), `meterno` (Foreign Key), `billdate`, `consumed`, `amount`, `paid`

-----

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.
