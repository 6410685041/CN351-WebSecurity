# CN351-WebSecurity
## Project Overview
This project demonstrates the simulation of three common web security attack methods: Username Enumeration, SQL Injection, and Cross-Site Scripting (XSS). The objective is to provide a practical understanding of these vulnerabilities and how they can be exploited to compromise web applications.

## Installation
To run this project locally, follow these steps
<ol>
  <li>git clone https://github.com/6410685041/CN351-WebSecurity </li>
  <li>cd CN351-WebSecurity</li>
  <li>pip install -r requirements.txt</li>
  <li>flask run</li>
</ol>

## Usage
Once the application is running, you can access the different sections to simulate the attacks
<ul>
  <li>Username Enumeration: Visit /register input a username that already taken the respone show Username already taken </li>
  
  <li>SQL Injection: Visit /login and input ' or 1=1; -- as the username or password to see the effect of an SQL injection. </li>
  <li>Cross-Site Scripting (XSS): Visit /xss and input <script>alert(1)</script> to see a basic XSS attack in action.</li>
</ul>





## Members
- Natiphon Chanphet 6410615030
- Supapan  Ngorsakun 6410615147
- Chalisa Thummaraj 6410685041
- Thanadon Boontawee 6410685165
