// app.js
App({
  globalData: {
    upload_url: 'https://ecgai.machineilab.org',
    // upload_url: 'http://172.20.10.2:9999'
    user_id:'0',
  },
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || [];
    logs.unshift(Date.now());
    wx.setStorageSync('logs', logs);

    // 登录
    // 微信小程序登录示例代码
    wx.login({
      success: res => {
        if (res.code) {
          console.log(res.code);
          // 将获取到的code发送到后端服务器
          wx.request({
            url: 'https://ecgai.machineilab.org/api/login', // 替换为你的后端接口地址
            method: 'POST',
            data: {
              code: res.code
            },
            success: function(response) {
              const app = getApp();
              if (app) {
                const globalData = app.globalData;
                globalData.user_id = response.data.data.user_id;
                console.log(globalData);
              } 
              else {
                console.error('未能获取到 App 实例');
              }
            }
          });
        } else {
          console.log('登录失败！' + res.errMsg)
        }
      }
    });
  }
});
