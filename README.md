# EndoinsightDB

## Overview
EndoinsightDB is a custom-developed database management system tailored for the Gastrointestinal Endoscopy Center at WestChina Hospital. This project is an integral part of the SCU Database curriculum for the year 2023.

## Purpose
EndoinsightDB's main goal is to efficiently collect and process questionnaires, while enabling effective and real-time machine learning data analysis. It is specifically designed to optimize data processing in clinical settings, enhancing patient care and facilitating medical research. Additionally, the system is equipped to generate educational and warning images, thereby providing a more comprehensive data interpretation experience.

## Deployment

To deploy the application, follow these steps:

1. **Server Setup:**
   - Ensure your Python environment is equipped with `PyTorch` and `Flask`.
   - Navigate to the [Server](./EGCAI_server_integrated/) directory.
   - Modify the port number in the `app.py` file to suit your environment. This step is crucial for customizing the deployment to fit your specific server settings.

2. **Mini Program Configuration:**
   - Access the [Mini Program](./EGCAI_miniprogram_integrated/) folder.
   - Update the server address within this directory to point to your own server environment. This adjustment allows the mini program to interact seamlessly with your deployed server.

## Contribution

前端问卷界面设计、逻辑 @[Liaorl](https://github.com/KINGLRL)，图像生成界面、神经网络实现 @[Liaorl](https://github.com/KINGLRL)；前端问卷界面实现 @[Lisa](https://github.com/lisaaaa0415)、@[Wangyibo](https://github.com/Wangyibo321)；后端问卷逻辑实现 @[Zhangpeng-Hu](https://github.com/LucasQAQ)、@[Liaorl](https://github.com/KINGLRL)；问卷预处理 @[Zhangpeng-Hu](https://github.com/LucasQAQ)；后端服务器部署、维护 @[Liaorl](https://github.com/KINGLRL)；后端逻辑测试 @[Zhangpeng-Hu](https://github.com/LucasQAQ)、@[Liaorl](https://github.com/KINGLRL)、@[Wangyibo](https://github.com/Wangyibo321)；

## Contact

For more details or queries regarding EndoinsightDB, please contact [1598744255@qq.com](mailto:1598744255@qq.com).
