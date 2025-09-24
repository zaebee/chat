import { createRouter, createWebHistory } from "vue-router";
import ChatView from "../views/ChatView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "chat",
      component: ChatView,
    },
    {
      path: "/playground",
      name: "playground",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/PlaygroundView.vue"),
    },
    {
      path: "/journey",
      name: "journey",
      component: () => import("../views/JourneyView.vue"),
    },
    {
      path: "/xp-dashboard",
      name: "xp-dashboard",
      component: () => import("../components/XpDashboard.vue"),
    },
    {
      path: "/bee-test",
      name: "bee-test",
      component: () => import("../components/HiveBeeTest.vue"),
    },
    {
      path: "/topology",
      name: "topology",
      component: () => import("../components/SacredTopologyView.vue"),
    },
    {
      path: "/autoevolution",
      name: "autoevolution",
      component: () => import("../components/AutoEvolutionDashboard.vue"),
    },
    {
      path: "/sacred-echo",
      name: "sacred-echo",
      component: () => import("../components/SacredEchoLetterDashboard.vue"),
    },
  ],
});

export default router;
