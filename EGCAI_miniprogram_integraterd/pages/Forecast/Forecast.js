// pages/yugu/yugu.js
var app = getApp()
Page({
  
  /**
   * 页面的初始数据
   */
  data: {

  },
 
 goto:function(){
    const app = getApp();
    const user_id = app.globalData.user_id;
    const jargon="DeepLeiarning"
    console.log(user_id)
    console.log("SSSSS")
    wx.request({
      url: 'https://ecgai.machineilab.org/api/get_basic_info', // 替换为您的服务器 URL
      method: 'POST',
      data: {
        // 这里是您想要发送的 JSON 数据
        "jargon": "DeepLeiarning",
        "user_id": user_id
     
        
      },
      header: {
        'content-type': 'application/json' // 设置请求的 header
      },
      success: function(res) {
      console.log('新建用户服务器返回数据:', res.data);
      var message=res.data.message
      if(message=="success"){
      
      var dataArray = res.data.data;// 将数组转换为字符串
  var dataString = JSON.stringify(dataArray); // 使用 wx.navigateTo 跳转页面并携带数组数据
  wx.navigateTo({
    url: '/pages/Information/Information?data=' + encodeURIComponent(dataString),
  });
}
else{
  wx.navigateTo({
    url: '/pages/Information/Information',
  });
}
      },

      fail: function(error) {
        console.error('请求失败:', error);
        // 这里可以处理请求失败的情况
      }
    })
  

  },
  
    
  goto1:function(){
    wx.navigateTo({
      url: '/pages/Survey/Survey',
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
   
  
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  }
})