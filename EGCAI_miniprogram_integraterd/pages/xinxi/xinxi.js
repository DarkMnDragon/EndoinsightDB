// pages/xinxi/xinxi.js
Page({

  /**
   * 页面的初始数据
   */
  
  data: {
    userNameVal:"",
    userSexVal:"",
    userNationVal:"",
    userIdnumberVal:"",
    userBirthdayVal: "",
    userPhonenumberVal:"",
    userFamilymemberPhonenumberVal:"",
    userHomeplaceVal:"",
  },
  loginFormData:function(e){
    
  console.log(e.detail.value);//表单数据
    var formData=e.detail.value;//获取表单数据
    var userNameVal=formData.name;//姓名
    var userSexVal=formData.sex;//性别
    var userNationVal=formData.nation;//民族
    var  userIdnumberVal=formData.id_number;//身份证号
    var   userPhonenumberVal=formData.phone_number;//手机号码
    var   userFamilymemberPhonenumberVal=formData.family_member_phone_number;//联系人手机号码
    var userBirthdayVal=this.data.userBirthdayVal;
    var userHomeplaceVal=formData.homeplace;//家庭住址
    this.setData({
    
        userNationVal:userNationVal,
        userSexVal:userSexVal,
        userNameVal:userNameVal,
        userIdnumberVal: userIdnumberVal,
        userPhonenumberVal: userPhonenumberVal,
        userBirthdayVal: userBirthdayVal,
        userFamilymemberPhonenumberVal:userFamilymemberPhonenumberVal,
        userHomeplaceVal:userHomeplaceVal
        
      })
   
   
    const app = getApp();
  // const user_id = app.globalData.openid;
  const user_id = "hzp";
  const jargon="DeepLeiarning"
  wx.request({
    url: 'https://ecgai.machineilab.org/api/update_basic_info', // 替换为您的服务器 URL
    method: 'POST',
    data: {
      // 这里是您想要发送的 JSON 数据
      "jargon": "DeepLeiarning",
      "user_id": user_id,
      "name":userNameVal,
      "sex": userSexVal,
      "nation":userNationVal,
      "id_number":userIdnumberVal,
      "birthday":userBirthdayVal,
      "phone_number":userPhonenumberVal,
      "family_member_phone_number":userFamilymemberPhonenumberVal,
      //"height":userHeightVal,
      //"weight":userWeightVal,
      "homeplace":userHomeplaceVal
    },
    header: {
      'content-type': 'application/json' // 设置请求的 header
    },
    success: function(res) {
    console.log('更新用户服务器返回数据:', res.data);
      // 这里可以处理服务器返回的数据
      var message=res.data.message
      if(message){
        wx.showToast({
          title: '创建用户成功', // 提示的内容
          icon: 'success', // 图标，支持"success"、"loading"
          duration: 2000, // 提示的延迟时间，单位毫秒，默认：1500
          mask: true // 是否显示透明蒙层，防止触摸穿透，默认：false
        });
      }
    },
    fail: function(error) {
      console.error('请求失败:', error);
      // 这里可以处理请求失败的情况
    }
  })

  },
   goback:function (e) {
    wx.switchTab({
      url: '../yugu/yugu'
    })
   },
  bindDateChange: function(e) {
    console.log('picker发送选择改变，携带值为', e.detail.value)
    this.setData({
      userBirthdayVal: e.detail.value
    })
   
  },
                                                       
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
     // 获取传递过来的数据字符串

  var dataString = options.data;
 
  // 将数据字符串转换为数组
  var dataArray = JSON.parse(decodeURIComponent(dataString));
  console.log('接收到的数组数据：', dataArray);
  if (dataArray && dataArray.length > 0){

  this.setData({
    userNationVal:dataArray[0].nation,
        userSexVal:dataArray[0].sex,
        userNameVal:dataArray[0].name,
        userIdnumberVal:dataArray[0].id_number,
        userPhonenumberVal: dataArray[0].phone_number,
        userBirthdayVal: dataArray[0].birthday,
        userFamilymemberPhonenumberVal: dataArray[0].family_member_phone_number,
        userHomeplaceVal: dataArray[0].homeplace
  })
  // 在这里可以使用传递过来的数组进行相应的操作
} 
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