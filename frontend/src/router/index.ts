import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";
import LoginView from "../pages/LoginView.vue";
import HomeView from "../pages/HomeView.vue";
import ScanView from "../pages/ScanView.vue";
import InstructorSessionView from "../pages/InstructorSessionView.vue";
import InstructorOfferingsView from "../pages/InstructorOfferingsView.vue";
import InstructorOfferingView from "../pages/InstructorOfferingView.vue";
import StudentHistoryView from "../pages/StudentHistoryView.vue";

const routes: RouteRecordRaw[] = [
  { path: "/login", name: "login", component: LoginView, meta: { public: true } },
  { path: "/", name: "home", component: HomeView },
  { path: "/scan", name: "scan", component: ScanView },
  { path: "/instructor", name: "instructorOfferings", component: InstructorOfferingsView },
  { path: "/instructor/offerings/:id", name: "instructorOffering", component: InstructorOfferingView },
  { path: "/instructor/sessions/:id", name: "instructorSession", component: InstructorSessionView },
  { path: "/student/history", name: "studentHistory", component: StudentHistoryView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to) => {
  const isPublic = Boolean(to.meta.public);
  const token = localStorage.getItem("access_token");

  if (!isPublic && !token) {
    return { name: "login", query: { next: to.fullPath } };
  }
  return true;
});

export default router;
