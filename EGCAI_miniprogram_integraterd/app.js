// app.js
App({
  globalData: {
    upload_url: 'https://ecgai.machineilab.org',
    // upload_url: 'http://172.20.10.2:9999'
    // appid:'wxc33860481c9c5c69',
    // wxspSecret:'845a44fe14022f6b0d64a3b25ea5687f'
    openid:'0',
  },
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || [];
    logs.unshift(Date.now());
    wx.setStorageSync('logs', logs);

    // 登录
    wx.login({
      success(res) {
        if (res.code) {
          // 发起网络请求
          wx.request({
            // 这里填你自己的appid 和 wxspSecret 
            url: "https://api.weixin.qq.com/sns/jscode2session?appid=wx074393c2a541fc34" +
              "&secret=6b1c7d27cdcfa3da0981c2c324c96375" + "&js_code=" + res.code + "&grant_type=authorization_code",
            method: "POST",
            success(res) { // 获取成功要执行的动作
              const app = getApp();
              if (app) {
                const globalData = app.globalData;
                // 输出整个 res.data 对象
                // console.log(res.data);
                globalData.openid = res.data.openid;
                console.log(globalData.openid);
                // 在这里可以使用 globalData
              } else {
                console.error('未能获取到 App 实例');
              }
            },
            fail(data) { // 失败要执行的动作
              console.error(data);
            }
          });
        } else {
          console.log('登录失败！' + res.errMsg);
        }
      }
    });
  }
});
