# Modern IPv4 Subnet Calculator

A modern, dark-themed, responsive web application built with **Python (Flask)** for calculating IPv4 subnet details.

## Features

* **Instant Calculation** – Real-time updates as you type (debounced input)
* **Responsive UI** – Dark theme, mobile-first design using CSS Grid
* **Visuals** – Smooth animations and rotating 3D-style network icon
* **Calculations Included**:

  * Subnet Mask
  * Network ID
  * Broadcast ID
  * First & Last usable IP
* Full support for **/31 (Point-to-Point)** and **/32** edge cases
* Legacy Class detection (**A, B, C, D, E**) and IP type (**Private, Public, Loopback**)
* Binary representation of IP addresses

## Tech Stack

* **Backend:** Python 3, Flask
* **Frontend:** HTML5, CSS3, Vanilla JavaScript (Fetch API)
* **Deployment:** Ready for cPanel (Passenger) or any WSGI server

## Installation

Clone the repository:

```bash
git clone https://github.com/mahziyar-azz/subnet-calculator.git
```

Install dependencies:

```bash
pip install flask
```

Run the app:

```bash
python app.py
```
