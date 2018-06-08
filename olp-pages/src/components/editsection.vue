<template lang="html">
  <div class="editsection-wrap">
    <div class="editsection-content" style="overflow-y: auto;">
      <!-- <div style="padding-top: 15px;">
      </div> -->
      <div class="editsection-label" style="text-align: left; padding: 15px 0;">
        <p style="font-size: 1.5em; font-weight: bold;" v-if="this.type === 'create'">新建小节</p>
        <p style="font-size: 1.5em; font-weight: bold;" v-else-if="this.type === 'edit'">编辑小节</p>
        <!-- <p style="font-size: 1.2em; font-weight: bold; color: #80848f;"></p> -->
      </div>
      <div class="editsection-title" style="padding-bottom: 10px;">
        <p style="float: left; text-align: left; padding: 7px 10px 7px 0;">小节名</p>
        <Input v-model="sectionTitle" placeholder="小节名" style="width: 300px; float: left;"/>
        <div class="float-clear">
        </div>
      </div>
      <div class="editsection-entity-type" style="padding-bottom: 10px;">
        <p style="float:left; text-align:left; padding-right: 10px;">内容类型</p>
        <RadioGroup v-model="entity.entityType" style="float: left;" @on-change="handleChange">
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
        <p v-if="type === 'edit'" style="text-align:left; font-size: 1.1em; font-weight: bold; padding-bottom: 10px; color: #5cadff;">
          <a :href="this.entity.video_url" id="video_link"><span>点击这里查看已上传视频</span></a>
        </p>
        <Upload type="drag" :action="this.actionurl" :on-success="handleSuccess">
          <div style="padding: 20px 0;">
            <Icon type="ios-cloud-upload" size="52" style="color: #3399ff;" />
            <p>点击选择文件或拖拽文件到此处</p>
          </div>
        </Upload>
      </div>
      <div class="createsection-insert-doc" style="display: none; width: 790px;" id="editDoc">
        <!-- <mavon-editor style="height: 500px; width: 805px;" /> -->
        <EditorMd :isView="docshow" :initData="md" style="z-index: 10000;"/>
      </div>
      <div class="hr-wrap">
        <hr />
      </div>
      <Button type="success" style="margin-bottom: 20px; float:right;" @click="handleSave">保存此节</Button>
    </div>
  </div>
</template>

<script>
import mavonEditor from 'mavon-editor';
import 'mavon-editor/dist/css/index.css';
import EditorMd from './mdeditor';
import Hub from '../assets/hub.js';
import axios from 'axios';

export default {
  name: 'TeacherSectionEdit',
  data () {
    return {
      type: '',
      entity: {
        entityType: 'video',
        video_url: '',
        md_url: '',
        content: ''
      },
      sectionid: '',
      topicid: '',
      courseid: '',
      sectionTitle: '',
      docshow: false,
      md: '',
      actionurl: "http://"+this.BASEURL+"/videoUpload"
    }
  },
  components: {
    'mavon-editor': mavonEditor.mavonEditor,
    'EditorMd': EditorMd
  },
  methods: {
    initComp: function () {
      if (this.$route.name.indexOf("TeacherSectionCreate") != -1) {
        // Create Section
        this.type = 'create';
        this.sectionTitle = '';
        this.sectionid = '';
        this.topicid = this.$route.params.topicid;
        this.courseid = this.$route.params.courseid;
      } else if (this.$route.name.indexOf("TeacherSectionEdit") != -1) {
        // Edit Section
        axios.get("http://"+this.BASEURL+"/editSection?sectionId="+this.$route.params.sectionid).then(function(res) {
          console.log(res);
          this.sectionTitle = res.data.sectionTitle;
          // this.entity = res.data.entity;
          this.entity.entityType = res.data.entity.entityType;
          this.type = 'edit';
          this.sectionid = this.$route.params.sectionid;
          this.topicid = this.$route.params.topicid;
          this.courseid = this.$route.params.courseid;

          console.log(this.entity);
          if (this.entity.entityType === 'doc') {
            // console.log(this.entity.url);
            this.entity.md_url = res.data.entity.url;
            this.entity.content = res.data.entity.content;

            axios.get(this.entity.md_url).then(function(res) {
              // console.log(res);
              this.md = res.data;
            }.bind(this));

            document.getElementById('editVideo').style.display = "none";
            document.getElementById('editDoc').style.display = "block";
            this.docshow = true;
          } else if (this.entity.entityType === 'video') {
            this.entity.video_url = res.data.entity.url;

          }
        }.bind(this));
      }
    },
    handleChange: function (cur) {
      if (cur === 'video') {
        document.getElementById('editDoc').style.display = "none";
        document.getElementById('editVideo').style.display = "block";
      } else if (cur === 'doc') {
        document.getElementById('editVideo').style.display = "none";
        document.getElementById('editDoc').style.display = "block";
        this.docshow = true;
      }
    },
    handleSave: function () {
      if (this.type === 'create') {
        if (this.sectionTitle === '') {
          alert("小节名不能为空");
          return;
        } else if (this.entity.entityType === 'video' && this.entity.video_url === '') {
          alert("请上传视频");
          return;
        } else if (this.entity.entityType === 'doc') {
          var md = document.getElementsByName("markdown-editor-markdown-doc")[0].innerText;
          var html = document.getElementsByName("markdown-editor-html-code")[0].innerHTML;
          console.log(md, html);
          this.entity.content = html;
          axios.post("http://"+this.BASEURL+"/createMdFile",{md:md}).then(function(res) {
            console.log(res);
            if (res.data.success) {
              this.entity.md_url = res.data.url;
              var d = {
                courseId: this.courseid,
                topicId: this.topicid,
                title: this.sectionTitle,
                entity: {
                  entityType: 'doc',
                  url: this.entity.md_url,
                  content: this.entity.content
                }
              }
              axios.post("http://"+this.BASEURL+"/createSection", d).then(function(res) {
                if(res.data.state === 'success') {
                  alert("success!");
                  this.$router.push({path: '/teachermain/courseEdit/'+this.courseid});
                }
              }.bind(this));
            }
          }.bind(this));
        }
        if (this.entity.entityType === 'video') {
          var d = {
            courseId: this.courseid,
            topicId: this.topicid,
            title: this.sectionTitle,
            entity: {
              entityType: 'video',
              url: this.entity.video_url
            }
          }
          axios.post("http://"+this.BASEURL+"/createSection", d).then(function(res) {
            if(res.data.state === 'success') {
              alert("success!");
              this.$router.push({path: '/teachermain/courseEdit/'+this.courseid});
            }
          }.bind(this));
        }
      } else if (this.type === 'edit') {
        if (this.sectionTitle === '') {
          alert("小节名不能为空");
          return;
        } else if (this.entity.entityType === 'video' && this.entity.video_url === '') {
          alert("请上传视频");
          return;
        } else if (this.entity.entityType === 'doc') {
          var md = document.getElementsByName("markdown-editor-markdown-doc")[0].innerText;
          var html = document.getElementsByName("markdown-editor-html-code")[0].innerHTML;
          this.entity.content = html;
          axios.post("http://"+this.BASEURL+"/createMdFile", {md:md}).then(function(res) {
            console.log(res);
            if (res.data.success) {
              console.log("here?")
              this.entity.md_url = res.data.url;
              var d = {
                courseId: this.courseid,
                topicId: this.topicid,
                sectionId: this.sectionid,
                sectionTitle: this.sectionTitle,
                entity: {
                  entityType: 'doc',
                  url: this.entity.md_url,
                  content: this.entity.content
                }
              }
              axios.put("http://"+this.BASEURL+"/editSection", d).then(function(res) {
                console.log(res);
                if (res.data.success) {
                  alert("Saved!");
                  this.$router.push({path:'/teachermain/courseEdit/'+this.courseid});
                }
              }.bind(this));
            }
          }.bind(this));
        }
        if (this.entity.entityType === 'video') {
          var d = {
            courseId: this.courseid,
            topicId: this.topicid,
            sectionId: this.sectionid,
            sectionTitle: this.sectionTitle,
            entity: {
              entityType: 'video',
              url: this.entity.video_url
            }
          }
          axios.put("http://"+this.BASEURL+"/editSection", d).then(function(res) {
            console.log(res);
            if (res.data.success) {
              alert("Saved!");
              this.$router.push({path:'/teachermain/courseEdit/'+this.courseid});
            }
          }.bind(this));
        }
      }
      console.log("保存~");
    },
    handleSuccess: function(res) {
      console.log(res);
      if(res.state === "success") {
        // console.log(res.data.url);
        this.entity.video_url = res.url;
      }
    }
  },
  mounted () {
    console.log(this.$route.name);
    this.initComp();
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
