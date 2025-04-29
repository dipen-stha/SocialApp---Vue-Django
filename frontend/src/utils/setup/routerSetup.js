import router from "@/router";
import { useUserStore } from "@/stores/user/user";

const initRouter = (app) => {
    const userStore = useUserStore();
    router.beforeEach(async (to, from, next) => {
        try{
            await userStore.fetchSelfDetail();
        } catch (error){
            console.log("Error fetching user detail", error)
        }
        if (to.name === 'login'){
            if(userStore.isAuthenticated){
                next({name: 'feed'})
            } else{
                next();
            }
        } else {
            if (to.meta.requiresAuth) {
                if (userStore.isAuthenticated){
                    next();
                } else {
                    next({ name: 'login'});
                }
            } else {
                next({ name: 'login'});
            }
        }
    });
    app.use(router);
}

export default initRouter;