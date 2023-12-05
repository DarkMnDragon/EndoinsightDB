const app = getApp();
const BENIGN = 0;
const UPLOAD_URL = app.globalData.upload_url;
const STRINGS = {
  loading: '计算中...',
  addImageFirst: '请先添加图片!',
  systemError: '系统故障!',
  uploadSkinImage: '请上传胃镜照片',
  userClicked: '用户点击主操作',
};

Page({
  data: {
    image_url: "",
    stained_image_url: "",
  },

  addImage(e) {
    wx.chooseImage({
      count: 1,
      sizeType: ['original', 'compressed'],
      sourceType: ['album', 'camera'],
      success: (res) => {
        this.setData({
          image_url: res.tempFilePaths[0]
        });
      },
      fail: () => {
        wx.showToast({
          title: STRINGS.addImageFirst,
          icon: 'none',
          duration: 1500,
        });
      },
    });
  },

  uploadImage(e) {
    if (this.data.image_url == '') {
      wx.showToast({
        title: STRINGS.addImageFirst,
        icon: 'none',
        duration: 1500,
      });
      return;
    }

    wx.showLoading({
      title: STRINGS.loading
    });

    wx.uploadFile({
      url: UPLOAD_URL + '/upload_image',
      filePath: this.data.image_url,
      name: 'file',
      success: (res) => {
        const jsonObj = JSON.parse(res.data);

        if (jsonObj.msg == 'success') {
          wx.hideLoading();
          this.setData({
            stained_image_url: jsonObj.image_url,
          });
        } else {
          wx.hideLoading();
          wx.showToast({
            title: STRINGS.systemError,
            icon: 'none',
            duration: 3500,
          });
        }
      },
      fail: () => {
        wx.hideLoading();
        wx.showToast({
          title: STRINGS.systemError,
          icon: 'none',
          duration: 3500,
        });
      },
    });
  },

  // Function to preview the original image
  previewOriginalImage: function () {
    wx.previewImage({
      urls: [this.data.image_url],
    });
  },

  // Function to preview the stained image
  previewStainedImage: function () {
    wx.previewImage({
      urls: [this.data.stained_image_url],
    });
  },
  
  deleteImage(e) {
    this.setData({
      image_url: "",
      result_content: "",
      result_type: BENIGN,
    });
  },
});