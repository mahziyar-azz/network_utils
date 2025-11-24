Modern IPv4 Subnet Calculator

A modern, dark-themed, responsive web application built with Python (Flask) for calculating IPv4 subnet details.

Features

Instant Calculation: Real-time updates as you type (Debounced input).

Responsive UI: Dark theme, mobile-first design using CSS Grid.

Visuals: Smooth animations and rotating 3D-style network icon.

Calculations: - Subnet Mask, Network ID, Broadcast ID.

First & Last usable IP.

Support for /31 (Point-to-Point) and /32 edge cases.

Legacy Class detection (A, B, C, D, E) and IP Type (Private, Public, Loopback).

Binary representation of addresses.

Tech Stack

Backend: Python 3, Flask.

Frontend: HTML5, CSS3, Vanilla JavaScript (Fetch API).

Deployment: Ready for cPanel (Passenger) or standard WSGI servers.

Installation

Clone the repository:

git clone [https://github.com/mahziyar-azz/subnet-calculator.git](https://github.com/mahziyar-azz/subnet-calculator.git)


Install dependencies:

pip install flask


Run the app:

python app.py
