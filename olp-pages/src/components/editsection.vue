<template lang="html">
  <div class="editsection-wrap">
    <div class="editsection-content" style="overflow-y: auto;">
      <div style="padding-top: 15px;">
      </div>
      <div class="editsection-title" style="padding-bottom: 10px;">
        <p style="float: left; text-align: left; padding: 7px 10px 7px 0;">小节名</p>
        <Input v-model="sectionTitle" placeholder="小节名" style="width: 300px; float: left;"/>
        <div class="float-clear">
        </div>
      </div>
      <div class="editsection-entity-type" style="padding-bottom: 10px;">
        <p style="float:left; text-align:left; padding-right: 10px;">内容类型</p>
        <RadioGroup v-model="entityType" style="float: left;" @on-change="handleChange">
          <Radio label="video">
            <span>视频</span>
          </Radio>
          <Radio label="doc">
            <span>文档</span>
          </Radio>
        </RadioGroup>
        <div class="float-clear">
        </div>
      </div>
      <div class="editSection-insert-video" style="display: block;" id="editVideo">
        <Upload type="drag" format=".mp4, .flv">
          <div style="padding: 20px 0;">
            <Icon type="ios-cloud-upload" size="52" style="color: #3399ff;" />
            <p>点击选择文件或拖拽文件到此处</p>
          </div>
        </Upload>
      </div>
      <div class="createsection-insert-doc" style="display: none;" id="editDoc">
        <mavon-editor style="height: 500px; width: 805px;" />
      </div>
      <div class="hr-wrap">
        <hr />
      </div>
      <Button type="success" style="margin-bottom: 20px; float:right;">保存此节</Button>
    </div>
  </div>
</template>

<script>
import mavonEditor from 'mavon-editor';
import 'mavon-editor/dist/css/index.css';
import Hub from '../assets/hub.js';

export default {
  name: 'EditSection',
  data () {
    return {
      entityType: 'video',
      id: '',
      sectionTitle: ''
    }
  },
  created () {
    var that = this;
    Hub.$on('EditSection', function(sectionTemp) {
      that.entityType = sectionTemp.entityType;
      that.id = sectionTemp.id;
      that.sectionTitle = sectionTemp.sectionTitle;
    })
  }, 
  components: {
    'mavon-editor': mavonEditor.mavonEditor
  },
  methods: {
    handleChange: function (cur) {
      if (cur === 'video') {
        document.getElementById('editDoc').style.display = "none";
        document.getElementById('editVideo').style.display = "block";
      } else if (cur === 'doc') {
        document.getElementById('editVideo').style.display = "none";
        document.getElementById('editDoc').style.display = "block";
      }
    }
  }
}
</script>

<style lang="css">
.hr-wrap {
  padding: 10px 0;
}
hr {
  height: 1px;
  border: none;
  border-bottom: 1px solid #dddee1;
}
.float-clear {
  clear: both;
}
.editsection-wrap {
  width: 875px;
  height: 100%;
  background-color: #f8f8f9;
  float: right;
  padding: 0 10px;
}
.editsection-content {
  height: 100%;
  background-color: #fff;
  padding: 0 25px;
}
</style>
