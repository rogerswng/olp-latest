import Vue from 'vue';
import Router from 'vue-router';
import HelloWorld from '../components/HelloWorld';

// Pages
import Login from '../pages/login';
import StudentMain from '../pages/studentmain';
import Practice from '../pages/practice';
import Course from '../pages/course';
import Section from '../pages/section';

// Components
import StudentCourseList from '../components/studentcourselist';
import StudentPracticeList from  '../components/studentpracticelist';


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
    }
  ]
})
