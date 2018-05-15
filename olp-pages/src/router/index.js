import Vue from 'vue';
import Router from 'vue-router';
import HelloWorld from '../components/HelloWorld';

// Pages
import Login from '../pages/login';
import StudentMain from '../pages/studentmain';
import Practice from '../pages/practice';
import Course from '../pages/course';
import Section from '../pages/section';
import PracticeDetail from '../pages/practicedetail';
import TeacherMain from '../pages/teachermain';

// Components
import StudentCourseList from '../components/studentcourselist';
import StudentPracticeList from  '../components/studentpracticelist';
import TeacherCourseList from '../components/teachercourselist';
import TeacherPracticeList from '../components/teacherpracticelist';
import TeacherCourseCreate from '../components/teachercoursecreate';
import TeacherPracticeCreate from '../components/teacherpracticecreate';
import TeacherCourseEdit from '../components/teachercourseedit';
import EditSection from '../components/editsection';


Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/studentmain',
      name: 'StudentMain',
      component: StudentMain,
      children: [
        {
          path:'',
          name: 'StudentCourse',
          component: StudentCourseList
        },
        {
          path: 'course',
          name: 'StudentCourse',
          component: StudentCourseList
        },
        {
          path: 'practice',
          name: 'StudentPractice',
          component: StudentPracticeList
        }
      ]
    },
    {
      path:'/practice/:id',
      name: 'Practice',
      component: Practice
    },
    {
      path: '/course/:id',
      name: 'Course',
      component: Course
    },
    {
      path: '/section/:id',
      name: 'Section',
      component: Section
    },
    {
      path: '/practice/:id/detail',
      name: 'PracticeDetail',
      component: PracticeDetail
    },
    {
      path: '/teachermain',
      name: 'TeacherMain',
      component: TeacherMain,
      children: [
        {
          path: '',
          name: 'TeacherCourseList',
          component: TeacherCourseList
        },
        {
          path: 'course',
          name: 'TeacherCourseList',
          component: TeacherCourseList
        },
        {
          path: 'courseCreate',
          name: 'TeacherCourseCreate',
          component: TeacherCourseCreate
        },
        {
          path: 'practiceCreate',
          name: 'TeacherPracticeCreate',
          component: TeacherPracticeCreate
        },
        {
          path: 'practice',
          name: 'TeacherPracticeList',
          component: TeacherPracticeList
        },
        {
          path: 'courseEdit/:id',
          name: 'TeacherCourseEdit',
          component: TeacherCourseEdit
        },
        {
          path: 'sectionEdit/:id',
          name: 'TeacherSectionEdit',
          component: EditSection
        }
      ]
    }
  ]
})
