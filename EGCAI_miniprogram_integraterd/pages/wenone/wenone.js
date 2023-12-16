// pages/wenone/wenone.js
var describe_text="请回答下面问题";
Page({
  
  /**
   * 页面的初始数据
   */
  data: {
    view_tip:1,
    question: '',
    options: [],
    description:describe_text,
    isquestion:true,
    respond_id:'',
    type:'',
    is_first_question: true,
    is_last_question: false,
    type_id:'',
    question_id:0,
    text:'',
    select_options:[],
    selected_options:[],
    post_message:"fail",
    btn_disabled:true,
    isshow:false,
    selectvalue:''
  },

  
  handleRadioChange: function(e) {
     var selected_option = Number(e.detail.value);
     let newArray = [];
    console.log('用户选择的选项索引是：', e.detail.value);
    newArray.push(selected_option);
    this.setData({
      selected_options: newArray
    });
  },

  handleCheckboxChange: function(e) {
    // e.detail.value 是所有选中的复选框的 value 数组
    var selectedIndices = e.detail.value.map(Number);
    console.log('用户选择的选项索引是：', selectedIndices);

    this.setData({
      selected_options: selectedIndices
    });
  },

  // handleButtonClick: function(e) {
  //   const index = e.currentTarget.dataset.index;
  //   let newArray = this.data.selected_options;

  //   if (newArray.includes(index)) {
  //     // 如果数组中已经有这个索引，就移除它（类似于取消选择）
  //     newArray = newArray.filter(i => i !== index);
  //   } else {
  //     // 如果数组中没有这个索引，就添加它（类似于选择）
  //     newArray.push(index);
  //   }

  //   this.setData({
  //     selected_options: newArray
  //   });
  // }




  onLoad: function (options) {
   this.setData({
      question_id:0,
      type_id:4
    })
    let dataTime
  let yy = new Date().getFullYear()
  let mm = new Date().getMonth()+1
  let dd = new Date().getDate()
  let hh = new Date().getHours()
  let mf = new Date().getMinutes()<10?'0'+new Date().getMinutes():
    new Date().getMinutes()
  let ss = new Date().getSeconds()<10?'0'+new Date().getSeconds():
    new Date().getSeconds()
    dataTime = `${yy}-${mm}-${dd} ${hh}:${mf}:${ss}`;
   const app = getApp();
  // const user_id = app.globalData.openid;
  const user_id = "hzp";
  const jargon="DeepLeiarning";
  console.log('目前时间为：',dataTime)
  wx.request({
    url: 'https://ecgai.machineilab.org/api/surveys/1/new_survey_instance', // 替换为您的服务器 URL
    method: 'POST',
    data: {
      "jargon": "DeepLeiarning",
      "user_id":user_id ,
      "time": dataTime
    },
    header: {
      'content-type': 'application/json' // 设置请求的 header
    },
    success: (res) => {
    console.log('创建问卷服务器返回数据:', res.data.message);
    if(res.data.message=="success"){
    var description=res.data.data.description;
    var respond_id =res.data.data.response_id;
    var type =res.data.data.type;
    var type_id=res.data.data.type_id;
    var question_id=res.data.data.question_id;
    var is_last_question=res.data.data.is_last_question;
    var is_first_question=res.data.data.is_first_question;
    this.setData({
      description:description,
      respond_id: respond_id,
      type:type,
      type_id:type_id,
      question_id:question_id,
      is_last_question:is_last_question,
      is_first_question:is_first_question,
      isshow:true
    })
    
    if(type=='Reconnection'){

     //var description=res.data.data.description;
      var question=res.data.data.question_text;
      var options=res.data.data.options_text;
      this.setData({
        isquestion:true,
        description:description,
        question:question,
        options: options
  
      })
    }
   else{
     this.setData({
       isquestion:false
     })
   }
  }
  else{
    wx.showToast({
      title: '请先完成注册', // 提示的内容
      icon: 'error', // 图标，支持"success"、"loading"
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
  
submit:function (e) {
  this.post(this.end_survey);
  
},
end_survey:function (e){
  const app = getApp();
  // const user_id = app.globalData.openid;
  const user_id = "hzp";
  console.log(user_id,this.data.respond_id)
  wx.request({
    url:'https://ecgai.machineilab.org/api/surveys/1/end_survey', // 替换为您的服务器 URL
    method: 'POST',
    data: {
      "user_id":user_id,
      "response_id":this.data.respond_id
    },
   
    header: {
      'content-type': 'application/json' // 设置请求的 header
    },
    success: (res) => {
    console.log('结束服务器返回数据:', res.data);
    wx.showToast({
      title: '填写完成', // 提示的内容
      icon: 'success', // 图标，支持"success"、"loading"
      duration: 2000, // 提示的延迟时间，单位毫秒，默认：1500
      mask: true // 是否显示透明蒙层，防止触摸穿透，默认：false
    }),
    setTimeout(function() {
      // 在定时器结束后执行页面返回
      wx.navigateBack({
        delta: 1, // 返回页面的层数，1表示返回上一级页面
      });
    }, 2000); // 设置延时时间为2000毫秒（2秒）
    },
    fail: function(error) {
      console.error('请求失败:', error);
      // 这里可以处理请求失败的情况
    }
    })

},
  
  /**
   * 生命周期函数--监听页面加载
   */
    //点击协议链接跳转listview
   
    bindAgreeChange:function(e) {
      //  console.log(e.detail.value)
        this.setData({
          isAgree:e.detail.value.length,
        })
        if (e.detail.value.length==1){
         this.setData({
           btn_disabled:false,
         })
       }else{
          //onsole.log(e.detail.value.length)
         this.setData({
           btn_disabled:true,
         })
       }
      },
     
      beginquestion:function(){
       this.setData({
         isquestion:true,
         question_id:0,
         is_first_question: true
       })
       this.nextquestion()
   },
   post :function(callback) {
     console.log('提交号：',this.data.question_id)
     console.log('提交内容：',this.data.text,this.data.selected_options)
    const app = getApp();
    // const user_id = app.globalData.openid;
    const user_id = "hzp";
    var question_id=this.data.question_id;
      wx.request({
      url:'https://ecgai.machineilab.org/api/surveys/1/questions/' + question_id + '/submit', // 替换为您的服务器 URL
      method: 'POST',
      data: {
        question_id:question_id,
        "user_id":user_id,
        "response_id":this.data.respond_id,
        "type_id": this.data.type_id,
        "text": this.data.type_id === 0 ? this.data.text : "select_text",
        "selected_options": this.data.selected_options
      },
      
      header: {
        'content-type': 'application/json' // 设置请求的 header
      },
      success: (res) => {
      console.log('提交成功服务器返回数据:', res.data);
    this.clearInput();
    var message=res.data.message;
    if(message=="fail"&&this.data.view_tip){
      this.setData({
       description:res.data.error.description
      })
      if(this.data.view_tip){
        wx.showToast({
          title: this.data.description,
          icon: 'error', // 图标，可选值：'success', 'loading'，默认无图标
          duration: 2000 // 提示框停留时间，默认为 1500 毫秒
        });
      }
    }
    else{
     
      callback();
     
     
    }
     this.clearInput()
      this.setData({
        post_message:message
      })
    },
    fail: function(error) {
        console.error('请求失败:', error);
        // 这里可以处理请求失败的情况
      }
      })
   },
   inputChange: function(event) {
    const text = event.detail.value; // 获取输入框中的文本内容
    this.setData({
      text: text // 将文本内容存储在 data 中的 inputValue 变量中
    });
  },
  lastquestion:function(){
    
    this.setData({
      view_tip:0
    })
    this.post(this.lastone);
  },
  clearInput() {
    
   this.setData({
     text:'',
    
   })
  },
   nextquestion:function(){
     
    this.setData({
      view_tip:1
    })
    if(this.data.question_id>0){
      this.post(this.nextone);

    }
    else{
      this.nextone();
    }
    this.clearInput();
        },
  
    nextone:function() {
      const app = getApp();
      // const user_id = app.globalData.openid;
      const user_id = "hzp";
      
      wx.request({
        url:'https://ecgai.machineilab.org/api/surveys/1/questions/'+this.data.question_id+'/next_question', // 替换为您的服务器 URL
        method: 'POST',
        data: {
          "user_id":user_id,
          "response_id":this.data.respond_id
        },
       
        header: {
          'content-type': 'application/json' // 设置请求的 header
        },
        success: (res) => {
        console.log('下一题成功服务器返回数据:', res.data);
        var question=res.data.data.question_text;
        var options=res.data.data.options_text;
        var type_id=res.data.data.type_id;
        var question_id=res.data.data.question_id;
        var is_last_question=res.data.data.is_last_question;
        var hist_options=res.data.data.hist_options;
        var hist_text=res.data.data.hist_text;
        this.setData({
          type_id:type_id,
          question_id:question_id,
          question:question,
          is_first_question:false,
          options: options,
          is_last_question:is_last_question,
          selected_options:hist_options,
          select_options:hist_options,
          text:hist_text
        })
       
        },
        fail: function(error) {
          console.error('请求失败:', error);
          // 这里可以处理请求失败的情况
        }
        })
    },
    lastone:function() {
      const app = getApp();
      // const user_id = app.globalData.openid;
      const user_id = "hzp";
      wx.request({
        url:'https://ecgai.machineilab.org/api/surveys/1/questions/'+this.data.question_id+'/previous_question', // 替换为您的服务器 URL
        method: 'POST',
        data: {
          "user_id":user_id,
          "response_id":this.data.respond_id
        },
       
        header: {
          'content-type': 'application/json' // 设置请求的 header
        },
        success: (res) => {
        console.log('上一题成功服务器返回数据:', res.data);
        var question=res.data.data.question_text;
        var options=res.data.data.options_text;
        var type_id=res.data.data.type_id;
        var question_id=res.data.data.question_id;
        var hist_options=res.data.data.hist_options;
        var hist_text=res.data.data.hist_text;
        var is_first_question=res.data.data.is_first_question;
        this.setData({
          type_id:type_id,
          question_id:question_id,
          question:question,
          is_first_question:is_first_question,
          options: options,
          selected_options:hist_options,
          select_options:hist_options,
          text:hist_text
        })
    
        },
        fail: function(error) {
          console.error('请求失败:', error);
          // 这里可以处理请求失败的情况
        }
        })
    },
        /**
         * 生命周期函数--监听页面加载
         */
          //点击协议链接跳转listview
    bindAgreeChange:function(e) {
            //  console.log(e.detail.value)
              this.setData({
                isAgree:e.detail.value.length,
              })
              if (e.detail.value.length==1){
              this.setData({
                btn_disabled:false,
              })
            }else{
                //onsole.log(e.detail.value.length)
              this.setData({
                btn_disabled:true,
              })
            }

            },
      handleButtonClick: function (event) {
       
        var selected_option = parseInt(event.currentTarget.dataset.index, 10);

       var selected_option = event.currentTarget.dataset.index;
       var answertext="Answer_in_Selected_Option";
      var currentArray = this.data.options.slice(); // 先复制数组，确保不直接修改原数组
      currentArray=[];
      currentArray.push(selected_option); // 将新文本添加到数组末尾
       this.setData({
         text:answertext,
         selected_options:currentArray,
         selectedValue: selected_option

       })
       
      },
     
      // handleCheckboxChange: function(e) {
      //   const selectedValues = e.detail.value; // 获取选中的值
      //   var answertext="Answer_in_Selected_Option";
      //   const selectedIndexes = this.data.options.reduce((acc, option, index) => {
      //     if (selectedValues.includes(option)) {
      //       acc.push(index);
      //     }
      //     return acc;
      //   }, []);
        
      //   // 对相对索引进行排序
      //   selectedIndexes.sort((a, b) => a - b);
        
      //   this.setData({
      //     text:answertext,
      //     selected_options:selectedIndexes,
      //     // select_options:selectedIndexes
      //   })
      //   // const { value } = e.detail;
      //   // this.setData({
      //   //   select_options: value
      //   // });
      
      // }  ,
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
   emptyFunction:function(e) {
      // 什么都不做
   },
   
  
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
    this.setData({
      question_id:0
    })
    console.log(this.data.question_id)
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