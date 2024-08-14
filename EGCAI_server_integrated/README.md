# EndoinsightDB Server Deployment Instructions

This document provides instructions for deploying the EndoinsightDB server, which is responsible for handling user image uploads and generating potential cancer risk predictions using deep learning models.

## Configuration

Refer to `app.py` for initial setup and configuration details. Make sure to adjust the settings according to your environment and security requirements.

## Directory Structure

- **`./upload`**: This directory is designated for storing images uploaded by users.
- **`./prework`**: Contains the QR model for the survey database and the preprocessing c++ scripts for survey text.
- **`./utils`**: Includes various SQL utility scripts for database interactions and implementation details.
- **`./model_utils.py`**: Implements the CycleGAN model used for generating images that highlight potential cancer risks.
- **`·./nn/params.pt`**: [Download model checkpoint](https://pan.baidu.com/s/1-NLA6iiswOfZ3kSAFpGBJA?pwd=aq72), rename it as params.pt.

## Requirements

Before deployment, ensure that your environment meets the following requirements:

- **Python**: The server is written in Python and requires Python 3. Ensure that you have Python 3 installed on your deployment server.
- **Flask**: This is a micro web framework written in Python, used for serving the application. Install it using pip or another package manager.
- **PyTorch**: The deep learning platform used for running the predictive models. The server requires version 1.7 or newer. Visit the [PyTorch official website](https://pytorch.org/) for installation instructions.

## Installation

To install the necessary libraries and dependencies, run the following commands:

```bash
pip install -r requirements.txt
```

## Running the Server

Once all the requirements are installed, you can start the server by running:

```bash
python app.py
```

Ensure that the server is configured to run on a secure and scalable environment, especially if you are deploying in a production setup.

## Security Notes

- Always keep your Python environment and all dependencies up to date with the latest security patches.
- Secure your upload directory to prevent unauthorized access and potential security vulnerabilities.
- Regularly backup your server, including the SQL databases and uploaded images.

## Support

For any issues or support related to the server deployment, please contact the system administrator 1598744255@qq.com or refer to the application documentation.
