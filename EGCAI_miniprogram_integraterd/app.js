// app.js
App({
  globalData: {
    upload_url: 'https://ecgai.machineilab.org',
    // upload_url: 'http://172.20.10.2:9999'
    //appid:'xxx',
    //wxspSecret:'xxx'
    openid:'0',
  },
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 登录
    wx.login({
      success(res) {
        if (res.code) {
          //发起网络请求
    
          wx.request({

          //这里填你自己的appid 和 wxspSecret 
            url: "https://api.weixin.qq.com/sns/jscode2session?appid=wxc33860481c9c5c69" +"&secret=845a44fe14022f6b0d64a3b25ea5687f"+ "&js_code=" + res.code + "&grant_type=authorization_code" ,
            method: "POST",
            success(res){//获取成功要执行的动作
              const app = getApp();
          if (app) {
           
              const globalData = app.globalData;
              console.log(globalData.openid)
              globalData.openid=res.data.openid;
            
                   // 在这里可以使用 globalData
                
                } else {
                console.error('未能获取到 App 实例');
            }
         
              
            },
            fail(data){//失败要执行的动作
             }
          })
        } else {console.log('登录失败！' + res.errMsg)}
      }
   })

  }
   
      
 
})
