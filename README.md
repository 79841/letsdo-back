<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/79841/kscia-back">
    <img src="images/readme/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">KSCIA BACKEND</h3>

  <p align="center">
    KSCIA backend server to provide APIs and services
    <br />
    <a href="https://github.com/79841/kscia-back"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/79841/kscia-back">View Demo</a>
    ·
    <a href="https://github.com/79841/kscia-back/issues">Report Bug</a>
    ·
    <a href="https://github.com/79841/kscia-back/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

![Product Screen Shot][product-screenshot]

While there are websites dedicated to individuals with spinal cord injuries, there seemed to be a noticeable absence of mobile applications catering to their specific needs. Recognizing the physical challenges these individuals face, we believed that an easily accessible and user-friendly app was essential. Our goal was to provide on-the-go support and help foster a sense of community. Thus, we embarked on the development of a "Lifestyle App for Individuals with Spinal Cord Injuries". This app was crafted using the cross-platform framework, Flutter, ensuring compatibility with both Android and iOS devices. The backend, which provides the API, was developed using FastAPI.

Features include:

- A direct link to the Spinal Cord Injury Association website.
- A real-time chat system for counseling.
- Health and hygiene programs and checklists.

Through this app, we hope to simplify access to the services provided to individuals with spinal cord injuries, potentially enhancing their quality of life.

The current repository focuses on the backend component.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

This section lists major frameworks/systems used to this project.

- [![FastAPI][FastAPI]][FastAPI-url]
- [![Mysql][Mysql]][Mysql-url]
- [![Redis][Redis]][Redis-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

- bash

  ```sh
  sudo add-apt-repository ppa:deadsnakes/ppa
  sudo apt-get update
  ```

  ```sh
  sudo apt install python3.10
  sudo apt-get install mysql-server
  sudo apt-get install redis-server
  ```

- mysql

  ```mysql
  CREATE DATABASE kscia;
  CREATE USER userid@localhost IDENTIFIED BY 'password';
  GRANT ALL privileges ON kscia.* TO userid@locahost IDENTIFIED BY 'password';
  FLUSH privileges;
  ```

### Installation

_Below is an example of how you can install and set up your app._

1. Clone the repo

   ```sh
   git clone https://github.com/79841/kscia-back.git
   ```

2. Start virtual environment

   ```sh
   python3.10 -m venv .venv
   source .venv/bin/activate
   ```

3. Install PIP packages

   ```sh
   pip intall -r requirements.txt
   ```

4. Enter your API in `.env`

   ```plain
   DATABASE_URL=mysql+pymysql://userid:password@127.0.0.1:3306/kscia?charset=utf8
   ASYNC_DATABASE_URL=mysql+aiomysql://userid:password@127.0.0.1:3306/kscia?charset=utf8
   PROFILE_IMAGE_DIR=images/profile
   ```

5. Start server

   ```sh
   python main.py
   ```

6. Test

   _It is the process of adding the test dataset to the database._

   ```sh
   cd ./test
   python test.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

_Please refer to the [Documentation](https://141.164.51.245:22222/docs)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

`Letmedev` - <79841@naver.com>

Project Link: [https://github.com/79841/kscia-back](https://github.com/79841/kscia-back)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/79841/kscia-back.svg?style=for-the-badge
[contributors-url]: https://github.com/79841/kscia-back/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/79841/kscia-back.svg?style=for-the-badge
[forks-url]: https://github.com/79841/kscia-back/network/members
[stars-shield]: https://img.shields.io/github/stars/79841/kscia-back.svg?style=for-the-badge
[stars-url]: https://github.com/79841/kscia-back/stargazers
[issues-shield]: https://img.shields.io/github/issues/79841/kscia-back.svg?style=for-the-badge
[issues-url]: https://github.com/79841/kscia-back/issues

<!-- [linkedin-url]: https://linkedin.com/in/othneildrew -->

[product-screenshot]: images/readme/product_screenshot.png
[FastAPI]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
[FastAPI-url]: https://fastapi.tiangolo.com/
[Mysql]: https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=MySQL&logoColor=white
[Mysql-url]: https://www.mysql.com/
[Redis]: https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white
[Redis-url]: https://vuejs.org/
