<template lang="html">
  <div class="teachercourseedit-list-item">
    <div class="topictitle-label">
      <p>{{topicTitle}}</p>
      <p style="font-size: 0.6rem;"><span class="span-edit" @click="handleEdit($event)">编辑  </span><span class="span-remove" @click="handleRemove($event)">删除  </span><span class="span-open" @click="handleOpen">展开</span></p>
    </div>
    <div class="section-list" style="display: none;">
      <p v-for="section in sections" :data-sid="section.id">    {{section.sectionTitle}}<span class="span-edit" @click="handleEdit($event)">    编辑  </span><span class="span-remove" @click="handleRemove($event)">删除  </span></p>
      <p><span style="cursor: pointer" @click="handleNewSection($event)"><Icon type="plus" /> 新增小节</span></p>
      <CreateSection :clicked="onCreateSection" @close="handleClose" @save="handleSave" />
    </div>
  </div>
</template>

<script>
import CreateSection from './createsection.vue';
import EditSection from './editsection.vue';
import Hub from '../assets/hub.js';

export default {
  name: 'CourseEditItem',
  data () {
    return {
      id: 0,
      topicTitle: this.course.topicTitle,
      sections: this.course.sections,
      onCreateSection: false,
      onEditSection: false,
      onCreateTopic: false,
      onEditTopic: false
      // sectionTemp: {}
    }
  },
  props: ['course'],
  methods: {
    handleOpen: function (e) {
      var cur = e.path[0].className;
      // console.log(cur);
      if(cur.indexOf('span-open') != -1) {
        // Open
        e.path[3].children[1].style.display = "block";
        e.path[0].className = "span-close";
        e.path[0].innerText = "收起";
      } else if (cur.indexOf('span-close') != -1) {
        // Collapse
        e.path[3].children[1].style.display = "none";
        e.path[0].className = "span-open";
        e.path[0].innerText = "展开";
      }
      // console.log(e.path[3].children[1]);
    },
    handleEdit: function (e) {
      var sectionTemp;
      console.log(e.path[2].className);
      var outerClass = e.path[2].className;
      if (outerClass.indexOf('topic') != -1) {
        // editTopic
        console.log('Edit topic..');
      } else if (outerClass.indexOf('section') != -1) {
        // editSection
        console.log('Edit Section...');
        var sid = e.path[1].dataset.sid;
        for (var i = 0; i < this.sections.length; i++) {
          if (sid === this.sections[i].id) {
            sectionTemp = this.sections[i];
            this.$router.push({name: 'TeacherSectionEdit', params:{id:sid}});
            Hub.$emit('EditSection', sectionTemp);
            // this.onEditSection = true;
            // window.location.assign("localhost:8080/#/teachermain/sectionEdit/123")
            return;
          }
        }
        // this.onModal = true;
      }
      // var outer = e.path[].
    },
    handleRemove: function (e) {
      var outerClass = e.path[2].className;
      if (outerClass.indexOf('topic') != -1) {
        // remove all topic
        this.$emit('removetopic', this.id.toString());
      } else if (outerClass.indexOf('section') != -1) {
        // remove this section
        // console.log(e.path[1].dataset.sid);
        this.$emit('removesection', e.path[1].dataset.sid);
      }
    },
    handleNewSection: function (e) {
      this.onCreateSection = true;
    },
    handleClose: function () {
      this.onCreateSection = false;
      this.onCreateTopic = false;
      this.onEditSection = false;
      this.onEditTopic = false;
    },
    handleSave: function (d) {
      this.sections.push(d);
      console.log(d);
      console.log(this.sections);
    }
  },
  components: {
    'CreateSection': CreateSection,
    'EditSection': EditSection
  }
}
</script>

<style lang="css">
</style>
