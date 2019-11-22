
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/jp19-lafa/IoT-Node">
    <img src="https://raw.githubusercontent.com/jp19-lafa/Documentation/master/images/branding/plant_transparent.png" alt="Logo" width="200" height="200">
  </a>

  <h3 align="center">IoT Node</h3>

  <p align="center">
    Code running on a single smart farm.
    <br />
    <a href="https://github.com/jp19-lafa/IoT-Node"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/jp19-lafa/IoT-Node">View Demo</a>
    ·
    <a href="https://github.com/jp19-lafa/IoT-Node/issues">Report Bug</a>
    ·
    <a href="https://github.com/jp19-lafa/IoT-Node/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
  * [Bluetooth](#Bluetooth)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

The IoT Node is a part of FarmLab project. It works together with the rest of the projects to create a full scalable and modern farm.

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Install python 3.X
```sh
sudo apt install python3
```

Install paho-mqtt
```sh
sudo pip install paho-mqtt
```

### Installation
 
1. Clone the IoT-Node
```sh
git clone https:://github.com/jp19-lafa/IoT-Node.git
```
2. Install prerequisites
```sh
sudo apt install python3
sudo pip install paho-mqtt
```



<!-- USAGE EXAMPLES -->
## Usage

Edit the `config.py` file to contain all settings for connecting to the mqtt broker

Simply run the `network.py` file to start the connection. Make sure you build the hardware correctly as described in the wiki

```sh
python3 src/network.py
```

### Bluetooth

When launching `bluetooth/main.py` the server will listen for all incomming bluetooth pairing requests. When such a request comes in the server will automatically accept the request.
After that it waits until a bluetooth connection is made. (Using RFCOMM)

Here is a list of command to send to the bluetooth server to establish a network connection

| Type           | Code  | Value  |
|----------------|-------|--------|
| Wifi standard  | TYPE: | wpa2   |
| SSID name      | SSID: | String |
| Password       | PWD:  | String |
| Try to connect | TRY:  | 1      |

Here is a list of exit/success codes

| Code      | return type | Meaning                                             |
|-----------|-------------|-----------------------------------------------------|
| Error 1   | ERROR:1     | You didn't tell the server the wifi connection type |
| Error 2   | ERROR:2     | The wifi connection type isn't recognized           |
| Error 3   | ERROR:3     | Your network connection credentials are wrong       |
| Success 1 | SUCCESS:1   | Sever connected to the network succesfully          |

In a short example the Android application should listen for ERROR codes an display them correctly to the user.
When a Success message has been send the bluetooth connection can be ended.

_For more examples, please refer to the [Documentation](https://github.com/jp19-lafa/IoT-Node/wiki)_



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/jp19-lafa/IoT-Node/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

tom - tom@odex.be

Project Link: [https://github.com/jp19-lafa/IoT-Node](https://github.com/jp19-lafa/IoT-Node)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [jp19-lafa](https://github.com/jp19-lafa/IoT-Node)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/jp19-lafa/IoT-Node.svg?style=flat-square
[contributors-url]: https://github.com/jp19-lafa/IoT-Node/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/jp19-lafa/IoT-Node.svg?style=flat-square
[forks-url]: https://github.com/jp19-lafa/IoT-Node/network/members
[stars-shield]: https://img.shields.io/github/stars/jp19-lafa/IoT-Node.svg?style=flat-square
[stars-url]: https://github.com/jp19-lafa/IoT-Node/stargazers
[issues-shield]: https://img.shields.io/github/issues/jp19-lafa/IoT-Node.svg?style=flat-square
[issues-url]: https://github.com/jp19-lafa/IoT-Node/issues
[license-shield]: https://img.shields.io/github/license/jp19-lafa/IoT-Node.svg?style=flat-square
[license-url]: https://github.com/jp19-lafa/IoT-Node/blob/master/LICENSE.txt
[product-screenshot]: https://raw.githubusercontent.com/jp19-lafa/Documentation/master/images/branding/plant_transparent.png
