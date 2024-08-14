# EndoinsightDB

## Overview
EndoinsightDB is a custom-developed database management system tailored for the Gastrointestinal Endoscopy Center.

## Purpose
EndoinsightDB's main goal is to efficiently collect and process questionnaires, while enabling effective and real-time machine learning data analysis. It is specifically designed to optimize data processing in clinical settings, enhancing patient care and facilitating medical research. Additionally, the system is equipped to generate educational and warning images, thereby providing a more comprehensive data interpretation experience.

## Deployment

To deploy the application, follow these steps:

1. **Server Setup:**
   - Ensure your Python environment is equipped with `PyTorch` and `Flask`.
   - Navigate to the [Server](./EGCAI_server_integrated/) directory.
   - Modify the port number in the `app.py` file to suit your environment. This step is crucial for customizing the deployment to fit your specific server settings.

2. **Mini Program Configuration:**
   - Access the [Mini Program](./EGCAI_miniprogram_integraterd/) folder.
   - Update the server address within this directory to point to your own server environment. This adjustment allows the mini program to interact seamlessly with your deployed server.
